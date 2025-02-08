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
        before_sleep=lambda retry_state: logger.info("Rate limited, retrying...")
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
    
    def fetch_documents(self, updated_after: Optional[datetime] = None) -> List[Document]:
        """Fetch all documents from Readwise with optional updated_after filter"""
        documents = []
        next_page_cursor = None
        
        while True:
            params = {}
            if next_page_cursor:
                params["pageCursor"] = next_page_cursor
            if updated_after:
                params["updatedAfter"] = updated_after.isoformat()
            
            logger.info(f"Fetching documents with params: {params}")
            try:
                data = self._make_request(params)
                
                # Convert documents
                for doc in data["results"]:
                    document = Document(**doc)
                    documents.append(document)
                
                next_page_cursor = data.get("nextPageCursor")
                if not next_page_cursor:
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching documents: {e}")
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

def get_latest_update_time() -> Optional[datetime]:
    """Get the most recent updated_at timestamp from the database"""
    with Session(engine) as session:
        statement = select(Document.updated_at).order_by(Document.updated_at.desc()).limit(1)
        result = session.exec(statement).first()
        logger.info(f"Latest document update time in DB: {result}")
        return result

@click.command()
@click.option("--updated-after", type=click.DateTime(formats=["%Y-%m-%d"]), 
              help="Only fetch documents updated after this date. Defaults to most recent update in DB.",
              default=None)
def main(updated_after: Optional[datetime]):
    """Sync Readwise documents to local database"""
    api_token = os.getenv("READWISE_ACCESS_TOKEN")
    if not api_token:
        raise click.ClickException("No Readwise token provided. Set READWISE_ACCESS_TOKEN in .env file")
    
    init_db()
    api = ReadwiseAPI(api_token)
    
    # If no updated_after provided, use the most recent update time from DB
    if updated_after is None:
        updated_after = get_latest_update_time()
        if updated_after:
            logger.info(f"Using last update time from DB: {updated_after}")
    
    try:
        documents = api.fetch_documents(updated_after)
        api.save_documents(documents)
    except Exception as e:
        logger.error(f"Failed to sync documents: {e}")
        raise click.ClickException(str(e))

if __name__ == "__main__":
    main() 
