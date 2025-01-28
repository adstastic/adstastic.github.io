import frontmatter

import os
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def update_post_frontmatter(filepath: Path) -> None:
    """Update frontmatter of a post file to add category='post'."""
    try:
        post = frontmatter.load(str(filepath))
        post.metadata['tags'] = ' '.join(post.metadata['tags'])
        # Convert the content to string before writing
        content = frontmatter.dumps(post, default_flow_style=False)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Error processing {filepath}: {e}")

def main() -> None:
    posts_dir = Path('_quotes')
    if not posts_dir.exists():
        logger.error(f"Posts directory not found: {posts_dir}")
        return

    for file in posts_dir.glob('*.md'):
        update_post_frontmatter(file)
        logger.info(f"Processed {file}")

if __name__ == '__main__':
    main()
