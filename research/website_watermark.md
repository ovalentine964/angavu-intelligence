# Website Watermark & Branding System — Angavu Intelligence

**Version:** 1.0  
**Date:** 2026-07-27  
**Status:** Implemented

---

## Overview

This document describes the live watermark and consistent branding system implemented across the Angavu Intelligence website (`angavu-intelligence/`).

### What Was Implemented

| Feature | Status | File(s) |
|---------|--------|---------|
| SVG Logo Component | ✅ | Inline in all HTML pages |
| Live Watermark | ✅ | `script.js` (injected), `angavu-brand.css` |
| Consistent Header/Footer | ✅ | All 10 HTML pages |
| Homepage Brand Banner | ✅ | `index.html` |
| CSS Animations | ✅ | `angavu-brand.css` |
| Particle System | ✅ | `script.js` |
| Documentation | ✅ | This file |

---

## 1. SVG Logo Component

### Design
The Angavu eye/iris logo is defined in `assets/angavu-logo-icon-fullcolor.svg`:

- **Outer arcs:** Deep navy (#1B4965) — upper and lower eye shape
- **Inner ring:** Navy with 40% opacity
- **Iris/core:** Golden gradient (#E8A838 → #E8853D)
- **Iris highlight:** Light gold (#F5D78E) at 60% opacity
- **Network nodes:** Gold circles at left (8,50) and right (92,50) with pulse rings
- **Pulse lines:** Gold connecting lines from nodes to iris
- **Accent dots:** Orange (#E8853D) at 50% opacity

### Usage (Inline SVG)
Every page uses inline SVG (no extra HTTP requests). Unique gradient IDs prevent conflicts:

```html
<!-- In navigation -->
<svg class="angavu-logo-svg" viewBox="0 0 100 100" width="40" height="40" aria-hidden="true">
  <defs>
    <linearGradient id="navIris" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E8A838"/>
      <stop offset="100%" stop-color="#E8853D"/>
    </linearGradient>
  </defs>
  <!-- arcs, rings, iris, nodes, lines, dots -->
</svg>

<!-- In footer (id="ftIris") -->
<!-- In hero banner (id="heroIris" + glow filter) -->
<!-- In watermark (id="wmIris") — injected by JS -->
```

### Animation
The iris has a subtle pulse animation:

```css
@keyframes angavu-iris-pulse {
  0%, 100% { filter: brightness(1) drop-shadow(0 0 0px rgba(232,168,56,0)); }
  50% { filter: brightness(1.15) drop-shadow(0 0 6px rgba(232,168,56,0.3)); }
}
```

---

## 2. Live Watermark

### Behavior
- **Position:** Fixed, bottom-right corner
- **Size:** 80px (desktop), 50px (mobile), 100px (large screens ≥1400px)
- **Opacity:** 16% base, pulses to 22% every 5 seconds
- **z-index:** 5 (below all interactive content)
- **Pointer events:** None (non-interactive)
- **Accessibility:** `aria-hidden="true"`, `role="presentation"`
- **Print:** Hidden via `@media print`

### Implementation
The watermark is injected by JavaScript (`script.js`) to avoid duplicating SVG markup in every HTML file:

```javascript
// In script.js — runs on every page
(function injectWatermark() {
  var wm = document.createElement('div');
  wm.className = 'angavu-watermark';
  wm.setAttribute('aria-hidden', 'true');
  wm.setAttribute('role', 'presentation');
  wm.innerHTML = '<svg viewBox="0 0 100 100" ...>...</svg>';
  document.body.appendChild(wm);
})();
```

### CSS Animation
```css
@keyframes angavu-watermark-pulse {
  0%, 100% { opacity: 0.16; transform: scale(1); }
  50% { opacity: 0.22; transform: scale(1.04); }
}

.angavu-watermark {
  animation: angavu-watermark-pulse 5s ease-in-out infinite;
}
```

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  .angavu-watermark { animation: none; opacity: 0.15; }
}
```

---

## 3. Header & Footer Templates

### Header (Navigation)
All 10 pages use a consistent nav structure:

```html
<nav class="nav">
    <div class="nav-logo angavu-brand-header">
        <svg class="angavu-logo-svg" viewBox="0 0 100 100" width="40" height="40" aria-hidden="true">
            <!-- Full inline SVG with id="navIris" -->
        </svg>
        <a href="index.html">Angavu Intelligence</a>
    </div>
    <button class="mobile-menu-btn" aria-label="Toggle menu" aria-expanded="false">
        <!-- hamburger icon -->
    </button>
    <div class="nav-links">
        <a href="msaidizi.html">Msaidizi CFO</a>
        <a href="for-workers.html">For Workers</a>
        <a href="about.html">About</a>
        <a href="download.html" class="btn-primary btn-sm">Download</a>
    </div>
</nav>
```

### Footer
All pages now have a consistent footer with:
- Angavu SVG logo + company name
- Tagline: "Africa's Economic Nervous System"
- 4-column grid: Product, Company, Connect links
- Copyright notice
- Social links (Twitter/X, GitHub)

```html
<footer class="footer angavu-brand-footer">
    <div class="footer-grid">
        <div class="footer-brand">
            <a href="index.html" class="nav-logo" style="color:var(--white);">
                <!-- SVG with id="ftIris" -->
                <span class="footer-brand-name">Angavu Intelligence</span>
            </a>
            <p class="footer-brand-tagline">Africa's Economic Nervous System...</p>
            <p class="footer-copyright">© 2026 Angavu Intelligence Ltd.</p>
        </div>
        <!-- Product, Company, Connect columns -->
    </div>
    <div class="footer-bottom">
        <span>© 2026 Angavu Intelligence Ltd. All rights reserved.</span>
        <div class="footer-social"><!-- Twitter, GitHub icons --></div>
    </div>
</footer>
```

---

## 4. Homepage Brand Banner

The homepage hero section was enhanced with:

### Animated Background
- **Particle canvas** (`div.hero-bg-canvas`) with data-flow particles
- Particles: 15 (mobile) / 30 (desktop), gold-colored, floating upward
- Network lines: 3 (mobile) / 6 (desktop), sweeping horizontally
- Orbs: Existing gradient orbs preserved

### Prominent Logo
- Large 96px SVG logo centered above the hero text
- Glow filter on the iris
- Outer ring with pulse animation
- `aria-label="Angavu Intelligence logo"` for accessibility

### Particle JS (in `script.js`)
```javascript
(function initHeroParticles() {
  var canvas = document.querySelector('.angavu-hero-banner .hero-bg-canvas');
  if (!canvas) return;
  // Creates floating particles and sweeping network lines
})();
```

---

## 5. Files Modified/Created

### New Files
| File | Purpose |
|------|---------|
| `angavu-brand.css` | All watermark, animation, header/footer, hero banner styles |
| `research/website_watermark.md` | This documentation |

### Modified Files
| File | Changes |
|------|---------|
| `script.js` | Added watermark injection + hero particle system |
| `index.html` | Brand CSS, SVG nav/logo, hero banner with particles, footer |
| `about.html` | Brand CSS, SVG nav/logo, footer |
| `download.html` | Brand CSS, SVG nav/logo, footer |
| `for-workers.html` | Brand CSS, SVG nav/logo, footer |
| `technology.html` | Brand CSS, SVG nav/logo, footer |
| `msaidizi.html` | Brand CSS, SVG nav/logo, footer |
| `testimonials.html` | Brand CSS, SVG nav/logo, footer |
| `vision.html` | Brand CSS, SVG nav/logo, footer (was missing) |
| `privacy-policy.html` | Brand CSS, SVG nav/logo, footer (was missing) |
| `api.html` | Brand CSS, SVG nav/logo, footer (was missing) |

---

## 6. Animation Specifications

| Animation | Element | Duration | Easing | Loop |
|-----------|---------|----------|--------|------|
| `angavu-iris-pulse` | Nav logo iris | 4s | ease-in-out | infinite |
| `angavu-watermark-pulse` | Watermark | 5s | ease-in-out | infinite |
| `angavu-particle-float` | Data particles | 6-14s | linear | infinite |
| `angavu-line-sweep` | Network lines | 6-14s | ease-in-out | infinite |
| `angavu-glow-ring` | Hero outer ring | 3s | ease-in-out | infinite |

### Performance Notes
- All animations use `will-change` for GPU acceleration
- Particles use CSS animations (not JS requestAnimationFrame) for minimal CPU
- `prefers-reduced-motion` disables all animations
- Watermark has `pointer-events: none` — zero interaction overhead

---

## 7. How to Update All Pages

### Adding a New Page
1. Copy the nav block from any existing page (e.g., `about.html`)
2. Add `<link rel="stylesheet" href="angavu-brand.css">` in `<head>`
3. Copy the footer block (with `angavu-brand-footer` class)
4. The watermark auto-injects via `script.js`

### Changing the Watermark
Edit the `injectWatermark()` function in `script.js` to modify SVG, opacity, or position.

### Changing the Logo
Update the inline SVG in each HTML file. Search for `angavu-logo-svg` to find all instances. Each uses a unique gradient ID (`navIris`, `ftIris`, `heroIris`, `wmIris`).

### Bulk Updates
Use the patterns in this document with a find-and-replace tool. The nav and footer blocks are identical across all pages.

---

## 8. Accessibility

- All SVG logos: `aria-hidden="true"` (decorative)
- Hero logo: `aria-label="Angavu Intelligence logo"` (meaningful image)
- Watermark: `aria-hidden="true"`, `role="presentation"`
- Watermark: `pointer-events: none` (doesn't block clicks)
- Watermark: `z-index: 5` (below content layer)
- All animations respect `prefers-reduced-motion`
- Print stylesheet hides watermark

---

## 9. Browser Compatibility

- **SVG inline:** All modern browsers
- **CSS animations:** All modern browsers, IE10+
- **`will-change`:** Chrome 36+, Firefox 36+, Safari 9.1+
- **`backdrop-filter`:** Chrome 76+, Safari 9+, Firefox 103+
- **`prefers-reduced-motion`:** Chrome 74+, Firefox 63+, Safari 10.1+

---

## 10. Brand Colors Reference

| Token | Hex | Usage |
|-------|-----|-------|
| `--navy` | `#1B4965` | Logo arcs, primary brand |
| `--midnight` | `#0F2D42` | Footer background |
| `--gold` | `#E8A838` | Iris gradient start, nodes |
| `--african-orange` | `#E8853D` | Iris gradient end, accent dots |
| `--gold-light` | `#F5D78E` | Iris highlight |

---

*Generated by the Website Watermark Council — 2026-07-27*
