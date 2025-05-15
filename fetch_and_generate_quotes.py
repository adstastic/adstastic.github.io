import httpx
import os
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Union

import click
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from slugify import slugify
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    AwareDatetime,
    ValidationError,
    field_validator,
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

READWISE_API_TOKEN = os.getenv("READWISE_ACCESS_TOKEN")
DEFAULT_OUTPUT_DIR = "_posts/quotes"
TEMPLATE_NAME = "template.md"


# --- Pydantic Models for Readwise API Response ---
class TagItem(BaseModel):
    id: int
    name: str


class HighlightItem(BaseModel):
    id: int
    text: str
    location: Optional[int] = None
    location_type: Optional[str] = None
    note: Optional[str] = None
    color: Optional[str] = None
    highlighted_at: Optional[AwareDatetime] = None
    created_at: Optional[AwareDatetime] = None
    updated_at: Optional[AwareDatetime] = None
    external_id: Optional[str] = None
    end_location: Optional[int] = None
    url: Optional[HttpUrl] = None
    book_id: Optional[int] = None
    tags: List[TagItem] = Field(default_factory=list)
    is_favorite: Optional[bool] = False
    is_discard: Optional[bool] = False
    readwise_url: Optional[HttpUrl] = None


class BookSource(BaseModel):
    user_book_id: int
    title: str
    author: Optional[str] = None
    readable_title: Optional[str] = None
    source: Optional[str] = None
    cover_image_url: Optional[HttpUrl] = None
    unique_url: Optional[str] = None
    book_tags: List[TagItem] = Field(default_factory=list)
    category: str
    document_note: Optional[str] = None
    summary: Optional[str] = None
    readwise_url: Optional[HttpUrl] = None
    source_url: Optional[str] = None
    asin: Optional[str] = None
    highlights: List[HighlightItem] = Field(default_factory=list)
    updated: Optional[AwareDatetime] = None
    last_highlight_at: Optional[AwareDatetime] = None

    class Config:
        populate_by_name = True


class ExportResponse(BaseModel):
    count: int
    nextPageCursor: Optional[Union[str, int]] = None
    results: List[BookSource] = Field(default_factory=list)


# --- End Pydantic Models ---


class ReadwiseV2Exporter:
    BASE_URL = "https://readwise.io/api/v2/export/"

    def __init__(self, token: str):
        if not token:
            raise ValueError("Readwise API token is required.")
        self.headers = {"Authorization": f"Token {token}"}

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        retry=retry_if_exception_type(httpx.RequestError),
    )
    def _make_request(self, params: Optional[dict] = None) -> Optional[ExportResponse]:
        # The calling function (fetch_sources_in_date_range) already logs the initial params.
        logger.debug(
            f"Preparing to make API request to base URL: {self.BASE_URL} with effective params: {params}"
        )
        try:
            with httpx.Client(headers=self.headers, timeout=30.0) as client:
                response = client.get(self.BASE_URL, params=params)
                # Log the full URL that was actually hit, including query parameters
                logger.info(
                    f"API response status: {response.status_code} for URL: {response.url}"
                )

                # Check for HTTP errors before attempting to parse JSON
                response.raise_for_status()  # Raises HTTPStatusError for 4xx/5xx errors

                json_data = (
                    response.json()
                )  # Could raise JSONDecodeError if content is not valid JSON
                logger.debug(f"Raw API JSON response: {json_data}")

                try:
                    validated_response = ExportResponse.model_validate(json_data)
                    logger.info("API response successfully parsed and validated.")
                    return validated_response
                except ValidationError as ve:
                    logger.error(
                        f"Pydantic ValidationError after successful HTTP request: {ve}"
                    )
                    json_data_str = str(json_data)  # Convert dict to string for slicing
                    logger.error(
                        f"Problematic JSON data snippet (first 500 chars): {json_data_str[:500]}"
                    )
                    return None  # Explicitly return None on validation error after successful fetch

        except httpx.HTTPStatusError as e:
            # This block is hit if response.raise_for_status() triggers.
            # response.text contains the error body from the server.
            error_text_snippet = (
                e.response.text[:500]
                if hasattr(e.response, "text")
                else "No response text available."
            )
            logger.error(
                f"HTTP Error {e.response.status_code}: {error_text_snippet} (URL: {e.request.url})"
            )
            if e.response.status_code == 401:
                logger.error(
                    "Authorization failed (401). Please check your Readwise API token."
                )
            elif e.response.status_code == 429:
                logger.warning(
                    "Rate limit hit (429). The retry mechanism might handle this if it's a RequestError, or consider adjusting request frequency."
                )
            # Re-raise to stop processing or allow higher-level retry if configured for HTTPStatusError.
            # The current @retry decorator is for RequestError, so this will likely halt execution.
            raise
        except httpx.RequestError as e:
            # Network-level errors (DNS, connection timeout, etc.)
            logger.error(
                f"Network request failed: {e} (URL: {e.request.url if hasattr(e, 'request') and hasattr(e.request, 'url') else 'N/A'})"
            )
            raise  # Re-raise for @retry to handle
        except Exception as e:  # Catch-all for other unexpected errors (e.g., response.json() if content not JSON)
            logger.error(
                f"Unexpected error during API request processing: {e}", exc_info=True
            )
            # Depending on the error, this might be caught by retry if it's a subclass of what @retry handles, or it will halt.
            raise

    def fetch_sources_in_date_range(
        self, start_date_dt: datetime, end_date_dt: Optional[datetime] = None
    ) -> List[BookSource]:
        all_sources: List[BookSource] = []
        next_page_cursor = None
        updated_after_str = start_date_dt.isoformat()

        while True:
            params = {"updatedAfter": updated_after_str}
            if next_page_cursor:
                params["pageCursor"] = next_page_cursor

            logger.info(f"Fetching data from Readwise API with params: {params}")
            parsed_response = self._make_request(params)

            if not parsed_response or not parsed_response.results:
                if parsed_response and parsed_response.count == 0:
                    logger.info("API returned 0 results for this page/query.")
                elif not parsed_response:
                    logger.warning(
                        "Failed to parse API response or no response. Stopping pagination for this query."
                    )
                else:
                    logger.info(
                        "No results on this page, but API indicates more might exist or an issue occurred."
                    )
                break

            current_sources = parsed_response.results

            if end_date_dt:
                aware_end_date = (
                    end_date_dt.replace(tzinfo=timezone.utc)
                    if end_date_dt.tzinfo is None
                    else end_date_dt
                )

                filtered_sources_for_page: List[BookSource] = []
                for source in current_sources:
                    source_date_to_check = source.updated or source.last_highlight_at

                    if source_date_to_check:
                        if source_date_to_check <= aware_end_date:
                            filtered_sources_for_page.append(source)
                        else:
                            logger.debug(
                                f"Source '{source.title}' (date {source_date_to_check}) is after end_date {aware_end_date}, filtering out."
                            )
                    else:
                        filtered_sources_for_page.append(source)
                all_sources.extend(filtered_sources_for_page)
            else:
                all_sources.extend(current_sources)

            next_page_cursor = parsed_response.nextPageCursor
            if not next_page_cursor:
                logger.info("No more pages to fetch.")
                break

        logger.info(f"Total sources fetched considering date range: {len(all_sources)}")
        return all_sources


def generate_markdown_from_source(
    source: BookSource, template_env: Environment, output_dir_path: Path
) -> None:
    latest_highlight_date: Optional[AwareDatetime] = None
    date_source_field = "none"

    if not source.highlights:
        logger.warning(
            f"Source '{source.title}' (ID: {source.user_book_id}) has no highlights. Skipping."
        )
        return

    for highlight in source.highlights:
        current_highlight_dt: Optional[AwareDatetime] = highlight.highlighted_at
        current_field_name = "highlighted_at"

        if not current_highlight_dt:
            current_highlight_dt = highlight.updated_at
            current_field_name = "highlight.updated_at"
        if not current_highlight_dt:
            current_highlight_dt = highlight.created_at
            current_field_name = "highlight.created_at"

        if current_highlight_dt:
            if (
                latest_highlight_date is None
                or current_highlight_dt > latest_highlight_date
            ):
                latest_highlight_date = current_highlight_dt
                date_source_field = current_field_name

    if latest_highlight_date is None:
        logger.warning(
            f"Could not determine a valid date from any highlights for source '{source.title}' (ID: {source.user_book_id}). Skipping."
        )
        return

    post_date = latest_highlight_date
    logger.info(
        f"Using date {post_date.isoformat()} from highlight's '{date_source_field}' field for source '{source.title}' (ID: {source.user_book_id})."
    )

    if not source.title:
        logger.warning(
            f"Skipping source_id '{source.user_book_id}' due to missing title (should not happen with Pydantic)."
        )
        return

    logger.info(
        f"Book tags for '{source.title}' (ID: {source.user_book_id}): {source.book_tags}"
    )
    template_data = {
        "quote": {
            "title": source.title,
            "author": source.author or "N/A",
            "source_url": source.source_url,  # Remains available if template changes
            "url": str(source.readwise_url)
            if source.readwise_url
            else None,  # For {{ quote.url }}
            "user_book_id": source.user_book_id,  # For potential use in ref
            "date": post_date.strftime("%Y-%m-%d"),
            "category": source.category,
            "highlights": [
                h.text for h in source.highlights if h.text
            ],  # Simplified to list of strings
            "tags": [tag.name for tag in source.book_tags if tag.name]
            if source.book_tags
            else [],
            # readwise_url is now mapped to url, so no separate readwise_url key needed here
        }
    }
    logger.debug(f"Template data for '{source.title}': {template_data}")

    date_prefix = post_date.strftime("%Y-%m-%d")
    slug = slugify(source.title)
    if not slug:
        slug = f"untitled-{source.user_book_id}"
        logger.warning(
            f"Title for source ID '{source.user_book_id}' resulted in empty slug. Using fallback: '{slug}'"
        )

    filename = f"{date_prefix}-{slug}.md"
    output_file_path = output_dir_path / filename

    output_dir_path.mkdir(parents=True, exist_ok=True)

    template = template_env.get_template(TEMPLATE_NAME)
    output_content = template.render(template_data)

    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(output_content)
    logger.info(f"Successfully generated: {output_file_path}")


@click.command()
@click.option(
    "--start-date",
    required=True,
    type=str,
    help="Start date for fetching highlights (YYYY-MM-DD).",
)
@click.option(
    "--end-date",
    required=False,
    type=str,
    help="Optional end date for fetching highlights (YYYY-MM-DD).",
)
@click.option(
    "--output-dir",
    default=DEFAULT_OUTPUT_DIR,
    type=click.Path(),
    help="Directory to save markdown files.",
)
@click.option(
    "--template-file",
    default=str(Path(__file__).parent / TEMPLATE_NAME),
    type=click.Path(exists=True),
    help="Path to the Jinja2 template file.",
)
def main(start_date: str, end_date: Optional[str], output_dir: str, template_file: str):
    """Fetches Readwise highlights and generates markdown quote posts."""
    if not READWISE_API_TOKEN:
        logger.error("READWISE_ACCESS_TOKEN environment variable not set.")
        raise click.ClickException(
            "Readwise API token not found. Please set it in your environment or a .env file."
        )

    try:
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        logger.error("Invalid start_date format. Please use YYYY-MM-DD.")
        raise click.ClickException("Invalid start_date format.")

    end_date_dt: Optional[datetime] = None
    if end_date:
        try:
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(
                tzinfo=timezone.utc
            )
            # Adjust end_date_dt to be end of the day to include all highlights on that day
            end_date_dt = end_date_dt.replace(
                hour=23, minute=59, second=59, microsecond=999999
            )
        except ValueError:
            logger.error("Invalid end_date format. Please use YYYY-MM-DD.")
            raise click.ClickException("Invalid end_date format.")

    if end_date_dt and end_date_dt < start_date_dt:
        logger.error("End date cannot be before start date.")
        raise click.ClickException("End date cannot be before start date.")

    output_dir_path = Path(output_dir)
    template_file_path = Path(template_file)

    if not template_file_path.exists():
        logger.error(f"Template file not found at specified path: {template_file_path}")
        logger.error(
            f"Please ensure '{template_file_path.name}' exists at that location or provide the correct path."
        )
        raise click.ClickException(
            f"Template file '{template_file_path.name}' not found."
        )

    try:
        # Template loader should look in the directory of the template file.
        template_env = Environment(
            loader=FileSystemLoader(searchpath=template_file_path.parent),
            autoescape=True,
        )
        template_env.get_template(
            template_file_path.name
        )  # Pre-check template existence and loadability
    except Exception as e:
        logger.error(
            f"Failed to load Jinja2 template '{template_file_path.name}' from '{template_file_path.parent}': {e}",
            exc_info=True,
        )
        raise click.ClickException("Jinja2 template could not be loaded.")

    api_client = ReadwiseV2Exporter(token=READWISE_API_TOKEN)

    # The Pydantic models expect AwareDatetime, which start_date_dt and end_date_dt now are.
    # The fetch_sources_in_date_range function itself takes datetime (which can be naive or aware)
    # but our prepared dt objects are already UTC aware.
    sources: List[BookSource] = api_client.fetch_sources_in_date_range(
        start_date_dt, end_date_dt
    )

    if end_date_dt:
        logger.info(
            f"Fetching Readwise sources updated from {start_date_dt.isoformat()} to {end_date_dt.isoformat()}."
        )
    else:
        logger.info(
            f"Fetching Readwise sources updated since: {start_date_dt.isoformat()}."
        )

    if not sources:
        logger.info("No new or updated sources with highlights found from Readwise.")
        return

    processed_count = 0
    for source_data in sources:
        generate_markdown_from_source(source_data, template_env, output_dir_path)
        processed_count += 1

    logger.info(
        f"Finished processing. Attempted to generate posts for {processed_count} fetched sources."
    )


if __name__ == "__main__":
    # Configure basic logging to show INFO level messages for console output
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    main()
