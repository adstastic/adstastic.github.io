from datetime import datetime, timedelta
import httpx
from pathlib import Path
import logging
from typing import List, Optional
import click
from dotenv import load_dotenv
import os
from slugify import slugify
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from jinja2 import Environment, FileSystemLoader
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List
from openai import OpenAI
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Database setup
DATABASE_URL = "sqlite:///readwise.db"
engine = create_engine(DATABASE_URL)

class Document(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: Optional[str] = None
    author: Optional[str] = None
    source_url: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    summary: Optional[str] = None
    parent_id: Optional[str] = None
    content: Optional[str] = None
    updated_at: Optional[datetime] = None

class QuotePost(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    parent_id: str = Field(index=True)
    title: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    updated_at: datetime
    markdown_path: Optional[str] = None
    is_published: bool = Field(default=False)

class Highlight(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    quote_post_id: int = Field(foreign_key="quotepost.id")
    content: str
    order: int

def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)

class ReadwiseAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://readwise.io/api/v3"
        self.headers = {"Authorization": f"Token {token}"}
        logger.debug(f"Readwise API token: {self.headers}")
        self.client = httpx.Client(headers=self.headers)
    
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        before_sleep=lambda retry_state: logger.info(f"Rate limited, waiting {retry_state.outcome.next_action.sleep} seconds...")
    )
    def _make_request(self, params: dict) -> dict:
        """Make a request to the Readwise API with retry logic"""
        response = self.client.get(f"{self.base_url}/list/", params=params)
        
        if response.status_code == 429:
            # If we get a rate limit response, extract retry-after if available
            retry_after = int(response.headers.get('retry-after', 5))
            logger.info(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            response.raise_for_status()
            
        response.raise_for_status()
        return response.json()
    
    def fetch_documents(self, updated_after: Optional[datetime] = None, updated_before: Optional[datetime] = None) -> List[Document]:
        """Fetch all documents from Readwise and optionally filter by date range"""
        documents = []
        next_page_cursor = None
        
        while True:
            params = {}
            if next_page_cursor:
                params["pageCursor"] = next_page_cursor
            if updated_after:
                params["updatedAfter"] = updated_after.replace(tzinfo=None).isoformat()
            
            logger.info(f"Fetching documents with params: {params}")
            try:
                data = self._make_request(params)
                
                # Convert documents and filter by updated_before if specified
                for doc in data["results"]:
                    document = Document(**doc)
                    if updated_before and document.updated_at:
                        doc_date = datetime.fromisoformat(document.updated_at).replace(tzinfo=None)
                        if doc_date > updated_before.replace(tzinfo=None):
                            continue
                    documents.append(document)
                
                next_page_cursor = data.get("nextPageCursor")
                if not next_page_cursor:
                    break
                    
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                raise

        return documents

    def save_documents(self, documents: List[Document]) -> None:
        """Save documents to database"""
        with Session(engine) as session:
            for doc in documents:
                # Convert string date to datetime
                if doc.updated_at:
                    doc.updated_at = datetime.fromisoformat(doc.updated_at)
                
                # Check if document exists
                existing = session.get(Document, doc.id)
                if existing:
                    for key, value in doc.dict(exclude_unset=True).items():
                        setattr(existing, key, value)
                else:
                    session.add(doc)
            
            session.commit()
            logger.info(f"Saved {len(documents)} documents to database")

def generate_title_slug(title: str) -> str:
    """Generate a URL slug from a title using GPT-4"""
    client = OpenAI()
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a URL slug generator. Output only the slug, nothing else."
                },
                {
                    "role": "user",
                    "content": f"Convert this title into a max 4 word descriptive URL slug: {title}"
                }
            ],
            max_tokens=50,
            temperature=0.3
        )
        
        # Get the generated slug and clean it
        generated_slug = response.choices[0].message.content.strip()
        return slugify(generated_slug)
    except Exception as e:
        logger.error(f"Failed to generate slug for title '{title}': {e}")
        # Fallback to basic slugify if GPT fails
        return slugify(title)

def aggregate_highlights_from_db() -> None:
    """Aggregate highlights from database into QuotePost records"""
    with Session(engine) as session:
        # Get all articles that don't have QuotePosts yet
        articles = session.exec(
            select(Document).where(
                Document.category == "article",
                ~Document.id.in_(select(QuotePost.parent_id))
            )
        ).all()

        for article in articles:
            # Get all highlights for this article
            highlights = session.exec(
                select(Document)
                .where(
                    Document.category == "highlight",
                    Document.parent_id == article.id
                )
                .order_by(Document.updated_at)
            ).all()

            if not highlights:
                continue

            # Create QuotePost
            quote_post = QuotePost(
                parent_id=article.id,
                title=article.title,
                author=article.author,
                url=article.source_url,
                updated_at=article.updated_at or datetime.now(),
            )
            session.add(quote_post)
            session.flush()  # Get the ID

            # Add highlights
            for i, highlight in enumerate(highlights):
                if highlight.content:
                    h = Highlight(
                        quote_post_id=quote_post.id,
                        content=highlight.content.replace("\n", "<br>"),
                        order=i
                    )
                    session.add(h)

            session.commit()
            logger.info(f"Created QuotePost for article: {article.title}")

def create_markdown_posts(output_dir: Path, force: bool = False) -> None:
    """Convert QuotePosts to markdown files. If force=True, regenerate all posts."""
    with Session(engine) as session:
        # Get posts query - either all posts or just unpublished ones
        query = select(QuotePost)
        if not force:
            query = query.where(QuotePost.is_published == False)
        posts = session.exec(query).all()

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template("template.md")

        for post in posts:
            highlights = session.exec(
                select(Highlight)
                .where(Highlight.quote_post_id == post.id)
                .order_by(Highlight.order)
            ).all()

            if not highlights:
                continue

            # Generate slug using GPT-4
            title_slug = generate_title_slug(post.title) if post.title else slugify(post.author)
            filename = f"{post.updated_at.strftime('%Y-%m-%d')}-{title_slug}.md"
            
            content = template.render(
                quote=post,
                highlights=[h.content for h in highlights]
            )
            
            output_file = output_dir / filename
            output_file.write_text(content)
            
            # Update post record
            post.markdown_path = str(output_file)
            post.is_published = True
            session.add(post)
            
            logger.info(f"{'Regenerated' if force else 'Created'} post: {output_file}")
        
        session.commit()

@click.command()
@click.option("--output-dir", type=click.Path(exists=True), default=".", help="Output directory for posts")
@click.option("--updated-after", type=click.DateTime(formats=["%Y-%m-%d"]), help="Only fetch documents updated after this ISO date")
@click.option(
    "--updated-before", 
    type=click.DateTime(formats=["%Y-%m-%d"]), 
    default=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
    help="Only fetch documents updated before this ISO date (defaults to tomorrow)"
)
@click.option(
    "--force",
    is_flag=True,
    help="Force regeneration of all markdown files, even for already published posts"
)
def main(output_dir: str, updated_after: Optional[datetime], updated_before: datetime, force: bool):
    """Convert Readwise documents to Jekyll markdown posts"""
    api_token = os.getenv("READWISE_ACCESS_TOKEN")
    if not api_token:
        raise click.ClickException("No Readwise token provided. Set READWISE_TOKEN in .env file")
    
    init_db()
    api = ReadwiseAPI(api_token)
    
    try:
        # Fetch and save documents
        documents = api.fetch_documents(updated_after, updated_before)
        api.save_documents(documents)
        
        # Aggregate highlights into posts
        aggregate_highlights_from_db()
        
        # Create markdown files
        create_markdown_posts(Path(output_dir), force=force)
    
    except Exception as e:
        logger.error(f"Failed to process documents: {e}")
        raise click.ClickException(str(e))

if __name__ == "__main__":
    main() 
