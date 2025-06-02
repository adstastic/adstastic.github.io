# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Jekyll Development
```bash
# Install dependencies
bundle install

# Serve site locally with live reload
bundle exec jekyll serve

# Build site
bundle exec jekyll build

# Run CI build (includes HTMLProofer)
./script/cibuild.sh
```

### Python Scripts
```bash
# Install Python dependencies (using uv)
uv pip install -r pyproject.toml

# Fetch and generate quote posts from Readwise
python fetch_and_generate_quotes.py --start-date YYYY-MM-DD [--end-date YYYY-MM-DD]
```

## Architecture

### Jekyll Structure
This is a Jekyll blog using the textlog theme with custom modifications:

- **Posts**: Located in `_posts/` with two subcategories:
  - `_posts/posts/` - Regular blog posts (permalink: `/p/:slug/`)
  - `_posts/quotes/` - Quote posts from Readwise (permalink: `/q/:slug/`)
- **Layouts**: `post.html` for blog posts, `quote.html` for quotes
- **Plugins**: jekyll-sitemap, jemoji, tagging, jekyll-tagging-related_posts

### Readwise Integration
The `fetch_and_generate_quotes.py` script:
- Fetches highlights from Readwise API using the v2 export endpoint
- Generates Jekyll markdown posts in `_posts/quotes/` using the `template.md` Jinja2 template
- Requires `READWISE_ACCESS_TOKEN` environment variable
- Uses Pydantic models for API response validation
- Implements retry logic with exponential backoff for API requests
- Determines post date from the latest highlight date (highlighted_at, updated_at, or created_at)

### GitHub Pages Deployment
- Site is deployed via GitHub Pages using the `github-pages` gem
- Custom domain configured via CNAME file
- CI builds run via GitHub Actions (see `script/cibuild.sh`)

## Important Notes from .cursorrules

- Use type annotations in all Python code
- Use `ag` instead of `rg` for code searching (rg is not installed)
- Log using Python's `logging` module, not print statements
- Minimize cognitive load - write readable, self-documenting code