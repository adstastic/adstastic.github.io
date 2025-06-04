# Blog

Personal blog built with Hugo and Tailwind CSS v4.

## Development

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (extended version)
- Node.js 20+
- Python 3.9+ (for Readwise quote fetching)

### Setup

```bash
# Install Node dependencies
npm install

# Install Python dependencies (using uv)
uv pip install -r pyproject.toml
```

### Local Development

```bash
# Start Tailwind CSS in watch mode
npm run dev

# In another terminal, start Hugo server
hugo server -D
```

The site will be available at `http://localhost:1313/`

### Building for Production

```bash
# Build CSS
npm run build

# Build site
hugo
```

## Content Management

### Posts

Create new posts in `content/posts/`:

```bash
hugo new posts/my-new-post.md
```

### Quotes

Quotes are fetched from Readwise using the Python script:

```bash
# Set your Readwise token
export READWISE_ACCESS_TOKEN=your_token_here

# Fetch quotes from a specific date
python fetch_and_generate_quotes.py --start-date 2024-01-01

# Fetch quotes for a date range
python fetch_and_generate_quotes.py --start-date 2024-01-01 --end-date 2024-12-31
```

## Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the `master` or `main` branch.

The deployment process:
1. Builds Tailwind CSS with minification
2. Builds Hugo site with proper baseURL
3. Deploys to GitHub Pages

## Architecture

- **Static Site Generator**: Hugo
- **CSS Framework**: Tailwind CSS v4
- **Theme**: Custom theme based on the original textlog design
- **Color Scheme**: Solarized (light/dark mode)
- **Fonts**: Ubuntu (body), Ubuntu Mono (code/meta)
- **Deployment**: GitHub Pages via GitHub Actions

## License

MIT
