#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path
import frontmatter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_posts():
    """Migrate Jekyll posts to Hugo format"""
    jekyll_posts_dir = Path("_posts/posts")
    jekyll_quotes_dir = Path("_posts/quotes") 
    hugo_posts_dir = Path("content/posts")
    hugo_quotes_dir = Path("content/quotes")
    
    # Ensure Hugo directories exist
    hugo_posts_dir.mkdir(parents=True, exist_ok=True)
    hugo_quotes_dir.mkdir(parents=True, exist_ok=True)
    
    # Migrate regular posts
    if jekyll_posts_dir.exists():
        for post_file in jekyll_posts_dir.glob("*.md"):
            logger.info(f"Migrating post: {post_file}")
            migrate_single_post(post_file, hugo_posts_dir, "posts")
    
    # Migrate quotes
    if jekyll_quotes_dir.exists():
        for quote_file in jekyll_quotes_dir.glob("*.md"):
            logger.info(f"Migrating quote: {quote_file}")
            migrate_single_post(quote_file, hugo_quotes_dir, "quotes")

def migrate_single_post(jekyll_file, hugo_dir, section):
    """Migrate a single Jekyll post to Hugo format"""
    # Read the Jekyll post
    with open(jekyll_file, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    # Extract date from filename
    filename = jekyll_file.name
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md', filename)
    if date_match:
        date_str = date_match.group(1)
        slug = date_match.group(2)
    else:
        logger.warning(f"Could not extract date from filename: {filename}")
        date_str = "2025-01-01"
        slug = filename.replace('.md', '')
    
    # Update frontmatter for Hugo
    hugo_frontmatter = {
        'title': post.metadata.get('title', slug.replace('-', ' ').title()),
        'date': date_str,
        'slug': slug,
    }
    
    # Handle tags - could be string or list
    tags = post.metadata.get('tags', [])
    if isinstance(tags, str):
        # Split space-separated tags
        hugo_frontmatter['tags'] = tags.split()
    else:
        hugo_frontmatter['tags'] = tags
    
    # Handle layout
    if post.metadata.get('layout') == 'quote':
        hugo_frontmatter['layout'] = 'quote'
        if 'ref' in post.metadata:
            hugo_frontmatter['ref'] = post.metadata['ref']
    
    # Create new Hugo post
    hugo_content = f"""---
title: "{hugo_frontmatter['title']}"
date: {hugo_frontmatter['date']}
slug: "{hugo_frontmatter['slug']}"
"""
    
    if hugo_frontmatter.get('tags'):
        hugo_content += "tags:\n"
        for tag in hugo_frontmatter['tags']:
            hugo_content += f"  - {tag}\n"
    
    if hugo_frontmatter.get('ref'):
        hugo_content += f"ref: {hugo_frontmatter['ref']}\n"
    
    hugo_content += "---\n\n"
    hugo_content += post.content
    
    # Write to Hugo directory  
    hugo_file = hugo_dir / filename
    with open(hugo_file, 'w', encoding='utf-8') as f:
        f.write(hugo_content)
    
    logger.info(f"Created Hugo post: {hugo_file}")

def copy_static_files():
    """Copy static files from Jekyll to Hugo"""
    # Copy images and other assets
    assets_to_copy = [
        ("assets", "static/assets"),
        ("feed.xml", "static/feed.xml"),
        ("CNAME", "static/CNAME")
    ]
    
    for src, dst in assets_to_copy:
        src_path = Path(src)
        dst_path = Path(dst)
        
        if src_path.exists():
            if src_path.is_dir():
                if dst_path.exists():
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
                logger.info(f"Copied directory: {src} -> {dst}")
            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_path, dst_path)
                logger.info(f"Copied file: {src} -> {dst}")

def create_static_pages():
    """Create static pages for Hugo"""
    # About page
    about_content = """---
title: "About"
---

This is a Hugo-powered blog using the Solarized Light theme.
"""
    
    about_dir = Path("content/about")
    about_dir.mkdir(parents=True, exist_ok=True)
    with open(about_dir / "_index.md", 'w') as f:
        f.write(about_content)
    
    # Credits page
    credits_content = """---
title: "Credits"
---

Built with [Hugo](https://gohugo.io) and the Solarized Light color scheme.
"""
    
    credits_dir = Path("content/credits")
    credits_dir.mkdir(parents=True, exist_ok=True)
    with open(credits_dir / "_index.md", 'w') as f:
        f.write(credits_content)

if __name__ == "__main__":
    logger.info("Starting Jekyll to Hugo migration...")
    migrate_posts()
    copy_static_files()
    create_static_pages()
    logger.info("Migration complete!")