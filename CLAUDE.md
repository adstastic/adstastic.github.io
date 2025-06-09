# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Hugo Development
```bash
# Serve site locally with live reload
hugo server -D

# Build site
hugo

# Build with drafts
hugo -D
```

### Python Scripts
```bash
# Install Python dependencies (using uv)
uv pip install -r pyproject.toml

# Run all Python commands using uv
uv run all python commands

# Fetch and generate quote posts from Readwise
python fetch_and_generate_quotes.py --start-date YYYY-MM-DD [--end-date YYYY-MM-DD]
```

## Architecture

### Hugo Structure (Ported from Jekyll)
This is a Hugo blog that was previously a Jekyll site using the textlog theme. The site has been migrated to Hugo with custom layouts:

- **Posts**: Located in `content/` with two subcategories:
  - `content/posts/` - Regular blog posts (permalink: `/p/:slug/`)
  - `content/quotes/` - Quote posts from Readwise (permalink: `/q/:slug/`)
- **Layouts**: `posts/single.html` for blog posts, `quotes/single.html` for quotes
- **Theme**: Custom layouts based on the original textlog theme

### CSS Migration Project
**Current Status**: The site uses custom CSS from the Jekyll version. The project is to port this custom CSS to Tailwind CSS v4 for better maintainability and modern styling capabilities.

**Migration Requirements**:
- Preserve the exact visual appearance shown in the screenshots
- Maintain Solarized color scheme (light and dark modes)
- Keep responsive breakpoints at 768px, 600px, and 400px
- Preserve Ubuntu font family for body text and Ubuntu Mono for code/meta elements

### Tailwind CSS v4 Migration Guidelines

#### Core Concepts
1. **Utility-First Approach**: Replace custom CSS with composable utility classes directly in HTML
2. **Mobile-First**: Start with mobile styles, add responsive variants (`sm:`, `md:`, `lg:`) for larger screens
3. **State Variants**: Use `hover:`, `focus:`, `dark:` prefixes for interactive and conditional styles
4. **Custom Values**: Use arbitrary values in square brackets when needed (e.g., `top-[117px]`)

#### Installation
```bash
# Install Tailwind CSS v4
npm install tailwindcss @tailwindcss/cli

# Create input CSS file with Tailwind import
echo '@import "tailwindcss";' > styles/input.css

# Run Tailwind CLI in watch mode
npx @tailwindcss/cli -i ./styles/input.css -o ./static/css/main.css --watch
```

#### Theme Configuration
Use the `@theme` directive in your CSS to define custom design tokens:
```css
@theme {
  /* Solarized colors */
  --color-base03: #002b36;
  --color-base02: #073642;
  --color-base01: #586e75;
  --color-base00: #657b83;
  --color-base0: #839496;
  --color-base1: #93a1a1;
  --color-base2: #eee8d5;
  --color-base3: #fdf6e3;
  
  /* Accent colors */
  --color-yellow: #b58900;
  --color-orange: #cb4b16;
  --color-red: #dc322f;
  --color-magenta: #d33682;
  --color-violet: #6c71c4;
  --color-blue: #268bd2;
  --color-cyan: #2aa198;
  --color-green: #859900;
  
  /* Custom fonts */
  --font-display: "Ubuntu", sans-serif;
  --font-mono: "Ubuntu Mono", monospace;
  
  /* Custom breakpoints matching current design */
  --breakpoint-sm: 600px;
  --breakpoint-md: 768px;
}
```

#### Dark Mode Implementation
- Use CSS custom properties for theme-aware colors
- Apply dark mode styles with `dark:` variant
- Toggle dark mode by adding/removing `dark` class on HTML element
- Store preference in localStorage for persistence

#### Migration Strategy
1. Start with layout structure (flex containers, max-widths, padding)
2. Add typography utilities (font sizes, weights, line heights)
3. Apply color utilities using custom theme colors
4. Add interactive states (hover, focus)
5. Implement responsive variants
6. Add custom utilities only when Tailwind defaults don't suffice

#### Key Utility Mappings
- `margin: 0 auto` → `mx-auto`
- `display: flex` → `flex`
- `max-width: 48rem` → `max-w-3xl` (or use arbitrary value `max-w-[48rem]`)
- `padding: 2rem 1.5rem` → `py-8 px-6`
- `border-bottom: 1px solid` → `border-b`
- `transition: all 0.3s ease` → `transition-all duration-300 ease-in-out`

### Readwise Integration
The `fetch_and_generate_quotes.py` script:
- Fetches highlights from Readwise API using the v2 export endpoint
- Generates Hugo markdown posts in `content/quotes/` using the `template.md` Jinja2 template
- Requires `READWISE_ACCESS_TOKEN` environment variable
- Uses Pydantic models for API response validation
- Implements retry logic with exponential backoff for API requests
- Determines post date from the latest highlight date (highlighted_at, updated_at, or created_at)

### GitHub Pages Deployment
- Site is deployed via GitHub Pages
- Custom domain configured via CNAME file
- Hugo builds the static site to the `public/` directory

## Important Notes from .cursorrules

- Use type annotations in all Python code
- Use `ag` instead of `rg` for code searching (rg is not installed)
- Log using Python's `logging` module, not print statements
- Minimize cognitive load - write readable, self-documenting code
```