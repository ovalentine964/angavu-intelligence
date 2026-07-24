# Contributing to Angavu Intelligence Website

Thank you for your interest in contributing to the Angavu Intelligence website and documentation.

## 🚀 Getting Started

### Prerequisites

- A modern web browser
- A text editor (VS Code, Sublime Text, etc.)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/ovalentine964/angavu-intelligence.git
cd angavu-intelligence

# Open in your browser (no build step needed — it's static HTML)
open index.html
# or
python3 -m http.server 8080
```

## 📋 How to Contribute

### Content Updates

1. Fork the repository
2. Create a branch: `git checkout -b docs/update-description`
3. Edit the relevant HTML file
4. Test locally in a browser
5. Submit a Pull Request

### Design Improvements

1. Check `design-tokens.css` for the design system
2. Follow existing patterns in `style.css`
3. Ensure mobile responsiveness
4. Test on multiple screen sizes

### Translations

We welcome translations to African languages! To add a new language:

1. Create a new HTML file (e.g., `index.sw.html` for Kiswahili)
2. Translate all content
3. Add language switcher links
4. Submit a Pull Request

## 📐 Style Guidelines

### HTML

- Semantic HTML5 elements
- Accessibility attributes (`aria-label`, `alt`, `role`)
- UTF-8 encoding
- No inline styles (use CSS classes)

### CSS

- Follow the design tokens in `design-tokens.css`
- Use CSS custom properties (variables)
- Mobile-first responsive design
- No `!important` declarations

### JavaScript

- Vanilla JS only (no frameworks)
- ES6+ syntax
- Progressive enhancement
- No external dependencies

## 🐛 Reporting Issues

Use the [Issue Tracker](../../issues/new) with:

1. **Page** — Which page is affected?
2. **Description** — What's wrong?
3. **Browser** — Chrome, Firefox, Safari, etc.
4. **Screenshot** — If applicable

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## 🙏 Thank You

Every contribution helps tell the story of Angavu Intelligence and our mission to empower Africa's informal economy.
