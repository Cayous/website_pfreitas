# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static website for Pacheco Freitas Advocacia, a law firm specializing in Medical and Healthcare Law (Direito Médico e da Saúde) based in Brasília. The site features a single-page design with a blog system for legal articles.

## Architecture

### File Structure
- `index.html` - Main single-page website with all sections
- `blog.html` - Blog listing page that displays all articles
- `post.html` - Template for individual blog post pages
- `css/` - Stylesheets (reset.css, styles.css)
- `js/` - JavaScript functionality
- `data/posts.json` - Blog content data in JSON format
- `images/` - Static assets and media files

### Key Components

**Main Website (`index.html`)**
- Header with navigation and logo
- Hero section
- About section (`#sobre`)
- Services section (`#servicos`) - Three service areas
- Blog section (`#blog`) - Recent articles preview
- FAQ section (`#faq`)
- Contact section (`#contato`)
- Floating WhatsApp button

**Blog System**
- Dynamic blog powered by `data/posts.json`
- `blog.js` handles blog listing functionality
- `post.js` manages individual post display
- Uses URL parameters for post navigation (`?id=X`)

**JavaScript Functionality (`js/script.js`)**
- Smooth scrolling for anchor links
- Header scroll effects (adds 'scrolled' class)
- Intersection Observer for fade-in animations
- FAQ accordion functionality

### Content Management

Blog posts are managed through `data/posts.json` with structure:
- `id` - Unique post identifier
- `title` - Post title
- `date` - Publication date (YYYY-MM-DD)
- `summary` - Brief description
- `image` - Featured image path
- `content` - Full HTML content

## Common Development Tasks

Since this is a static website, there are no build tools or package managers. Development is straightforward:

### Testing Changes
Open `index.html` directly in a web browser or use a local web server:
```bash
python -m http.server 8000
# or
npx serve .
```

### Adding New Blog Posts
1. Add new post object to `data/posts.json`
2. Include required fields: id, title, date, summary, image, content
3. Ensure unique ID and proper HTML in content field

### Updating Content
- Main site content: Edit `index.html` directly
- Styling: Modify `css/styles.css`
- JavaScript functionality: Update relevant files in `js/`

## SEO and Meta Configuration

The site includes comprehensive SEO optimization:
- Meta descriptions and keywords
- Open Graph tags for social media
- Twitter card metadata
- Canonical URLs
- Structured data for search engines

## Hosting

The site is configured for GitHub Pages deployment:
- `CNAME` file contains domain configuration
- `robots.txt` and `sitemap.xml` are included
- All assets use relative paths for portability