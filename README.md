![Biashara Intelligence](assets/logo-banner.svg)

# Msaidizi — Website

**Landing page for Msaidizi/Biashara AI.**

## Live

https://ovalentine964.github.io/msaidizi-website/

## Stack

- Pure HTML/CSS/JS (no build tools)
- GitHub Pages hosting
- Bilingual (English/Swahili)
- Mobile-first responsive design

## Features

- Problem → Solution → Download flow
- Language toggle (EN/SW)
- WhatsApp community link
- GitHub API download counter
- PWA ready (manifest.json + service worker)

## Editing

Just edit `index.html` and push. GitHub Pages auto-deploys.

## Project Structure

```
msaidizi-website/
├── index.html          # Main landing page
├── style.css           # All styles (mobile-first)
├── script.js           # Interactions, language toggle, download counter
├── swahili-content.js  # Swahili translation strings
├── sw.js               # Service worker (offline support)
├── manifest.json       # PWA manifest
├── assets/             # Images, icons
└── .nojekyll           # Bypass Jekyll on GitHub Pages
```

## Local Development

```bash
# Any static server works
python3 -m http.server 8000
# Open http://localhost:8000
```

## License

Proprietary — Biashara Intelligence
