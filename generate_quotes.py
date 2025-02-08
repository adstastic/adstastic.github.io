from datetime import datetime
import logging
from typing import Optional
import click
from pathlib import Path
from slugify import slugify
from sqlmodel import Field, Session, SQLModel, create_engine, select
from jinja2 import Environment, FileSystemLoader
from sync_readwise import Document, engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuotePost(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    parent_id: str = Field(index=True)
    title: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    slug: Optional[str] = None
    updated_at: datetime
    is_published: bool = Field(default=False)

class Highlight(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    quote_post_id: int = Field(foreign_key="quotepost.id")
    content: str
    order: int

def process_articles(start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
    """Process articles to create quote posts within a date range, using article titles as slugs"""
    with Session(engine) as session:
        # Build base query
        query = select(Document).where(
            Document.category == "article",
            ~Document.id.in_(
                select(QuotePost.parent_id).where(QuotePost.slug.isnot(None))
            )
        )
        
        # Add date filters if provided
        if start_date:
            query = query.where(Document.updated_at >= start_date)
        if end_date:
            query = query.where(Document.updated_at <= end_date)

        articles = session.exec(query).all()

        for article in articles:
            # Get all highlights
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

            # Generate slug from title
            if article.title:
                # Take first 4 words
                title_words = article.title.split()[:4]
                slug = slugify(" ".join(title_words))
                
                logger.info(f"Processing article: {article.title}")
                logger.info(f"Generated slug: {slug}")

                # Create or update QuotePost
                existing_post = session.exec(
                    select(QuotePost).where(QuotePost.parent_id == article.id)
                ).first()

                if not existing_post:
                    quote_post = QuotePost(
                        parent_id=article.id,
                        title=article.title,
                        author=article.author,
                        url=article.source_url,
                        slug=slug,
                        updated_at=article.updated_at or datetime.now(),
                    )
                    session.add(quote_post)
                    session.flush()

                    # Add highlights
                    for i, highlight in enumerate(highlights):
                        if highlight.content:
                            h = Highlight(
                                quote_post_id=quote_post.id,
                                content=highlight.content.replace("\n", "<br>"),
                                order=i
                            )
                            session.add(h)
                else:
                    existing_post.slug = slug
                    session.add(existing_post)

                session.commit()
                logger.info(f"Saved post with slug: {slug}")

def create_markdown_posts(output_dir: Path, force: bool = False, 
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> None:
    """Generate markdown files from QuotePosts within a date range"""
    with Session(engine) as session:
        query = select(QuotePost).where(QuotePost.slug != None)
        if not force:
            query = query.where(QuotePost.is_published == False)
        
        # Add date filters if provided
        if start_date:
            query = query.where(QuotePost.updated_at >= start_date)
        if end_date:
            query = query.where(QuotePost.updated_at <= end_date)
            
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

            filename = f"{post.updated_at.strftime('%Y-%m-%d')}-{post.slug}.md"
            
            content = template.render(
                quote=post,
                highlights=[h.content for h in highlights]
            )
            
            output_file = output_dir / filename
            output_file.write_text(content)
            
            post.is_published = True
            session.add(post)
            
            logger.info(f"{'Regenerated' if force else 'Created'} post: {output_file}")
        
        session.commit()

@click.command()
@click.option("--output-dir", type=click.Path(exists=True), default=".", help="Output directory for posts")
@click.option("--force", is_flag=True, help="Force regeneration of all markdown files")
@click.option("--start-date", type=click.DateTime(), help="Start date for processing (YYYY-MM-DD)")
@click.option("--end-date", type=click.DateTime(), help="End date for processing (YYYY-MM-DD)")
def main(output_dir: str, force: bool, start_date: Optional[datetime], end_date: Optional[datetime]):
    """Process articles and generate markdown posts within a date range"""
    init_db()
    process_articles(start_date, end_date)
    create_markdown_posts(Path(output_dir), force=force, start_date=start_date, end_date=end_date)

if __name__ == "__main__":
    main() 