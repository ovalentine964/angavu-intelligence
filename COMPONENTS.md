# Shared Components Guide

## Problem

The navigation (`<nav>`) and footer (`<footer>`) are copy-pasted across all 10+ HTML pages. This means any change to nav links, footer content, or SVG logos requires updating every file manually.

## Current State

The following components are duplicated across all HTML files:

| Component | Description | Files |
|-----------|-------------|-------|
| `<nav class="nav">` | Main navigation bar with logo, links, CTA | All `.html` files |
| `<footer class="footer">` | Footer with brand, links, social icons | All `.html` files |
| Angavu logo SVG | The iris/eye logo SVG (40x40 nav, 36x36 footer) | All `.html` files |

## How to Update

### Option A: Manual Find-and-Replace (Current)

1. Make your change to one file (e.g., `index.html`)
2. Copy the changed `<nav>` or `<footer>` block
3. Paste into all other HTML files, replacing the old version
4. Adjust `nav-active` class on the current page's link

### Option B: Build-Time Include (Recommended Future)

Use a static site generator or build script to inject shared components:

```bash
# Example with a simple shell script
for file in *.html; do
  sed -i '/<!-- NAV_START -->/,/<!-- NAV_END -->/{r nav.html
d}' "$file"
done
```

### Option C: JavaScript Include (No Build Step)

Extract nav/footer into separate `.js` files and load them dynamically:

```html
<div id="nav-placeholder"></div>
<script>fetch('nav.html').then(r=>r.text()).then(t=>document.getElementById('nav-placeholder').innerHTML=t);</script>
```

**Trade-off:** This breaks for users with JavaScript disabled and adds a render delay.

## Nav Link Inventory

Current nav structure (B2C pages: index, download, for-workers, msaidizi, about, testimonials, 404):

```
Nyumbani (index.html) | Kwa Wafanyabiashara (for-workers.html) | Sifa (msaidizi.html) | Kuhusu (about.html) | 📲 Pakua (download.html)
```

Current nav structure (Company pages: technology, vision, api, privacy-policy):

```
Msaidizi CFO (msaidizi.html) | For Workers (for-workers.html) | Technology (technology.html) | About (about.html) | Download (download.html)
```

## Footer Link Inventory

Footer has 4 columns:

1. **Brand** — Logo, tagline, copyright
2. **Product/Links** — Download, Features, Workers, Testimonials
3. **Company** — About, Privacy Policy
4. **Connect** — Twitter, GitHub, Email

## Checklist When Updating

- [ ] Update all 10+ HTML files (or use a script)
- [ ] Ensure `nav-active` class is on the correct link per page
- [ ] Update the SVG logo IDs if they conflict (each page uses unique gradient IDs)
- [ ] Test mobile menu on each page
- [ ] Verify footer links work on all pages
