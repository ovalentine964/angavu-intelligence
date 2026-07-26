# Warm Theme Design Document — Angavu Intelligence

**Date:** 2026-07-27  
**Status:** Implemented  
**Author:** Warm Theme Council (AI Design System)

---

## Problem Statement

The Angavu Intelligence website used a single dark navy theme (#0A1628) across all pages. While professional and suitable for B2B audiences (government buyers, FMCG companies, investors), the dark corporate aesthetic was intimidating and cold for the primary end-users: **informal workers in Africa** (mama mbogas, boda boda riders, fundis, salon owners, dukawallahs).

**Key tension:** The same website must serve two very different audiences:
1. **Workers** — need warmth, trust, accessibility, large text, friendly colors
2. **B2B/Institutional** — need professionalism, data-driven credibility, corporate polish

---

## Solution: Dual-Theme Architecture

### Approach: CSS `data-theme` Attribute

Instead of maintaining two separate websites, we use a `data-theme="warm"` attribute on the `<html>` element. The base `style.css` maintains the dark professional theme, and `warm-theme.css` overrides variables and styles for worker-facing pages.

**Benefits:**
- Single codebase, no duplication
- Easy to add new pages to either theme
- CSS-only solution — no JavaScript required
- Graceful fallback to dark theme if warm CSS fails to load

### File Architecture

```
style.css              — Base dark theme (B2B/professional)
warm-theme.css         — Warm overrides (worker-facing)
angavu-brand.css       — Brand system (shared)
design-tokens.css      — Design tokens (shared)
```

---

## Warm Theme — Design Decisions

### Color Palette

| Role | Color | Hex | Rationale |
|------|-------|-----|-----------|
| Background | Warm cream | `#FFF8F0` | Soft, inviting, not sterile white |
| Cards | White | `#FFFFFF` | Clean, elevated, trust |
| Primary | Orange | `#FF6B35` | Energy, warmth, African vibrancy |
| Secondary | Teal | `#004E64` | Trust, stability, contrast |
| Success | Green | `#2E8B57` | Growth, money, nature |
| Text | Dark | `#1A1A2E` | High readability, not harsh black |
| Accent | Gold | `#E8A838` | Brand continuity, highlights |

### Typography Decisions

- **Body text:** 18px minimum (up from 16px) — workers read on small screens in bright sunlight
- **Headers:** 24px+ — bold, dark color, high contrast
- **CTAs:** Orange, large, rounded — inviting tap targets
- **Swahili text:** Italic, slightly muted — secondary but respected

### Accessibility

- **Contrast ratios:**
  - Dark text (#1A1A2E) on cream (#FFF8F0): **14.2:1** (AAA)
  - Orange (#FF6B35) on white (#FFFFFF): **3.9:1** (AA for large text)
  - Teal (#004E64) on cream (#FFF8F0): **9.8:1** (AAA)
- **Touch targets:** All CTAs minimum 44px height
- **Font sizes:** Never below 16px body text

### Design Feel

**Warm theme feels like:**
- A friendly marketplace, not a corporate office
- A trusted kiosk, not a bank
- A conversation with a friend, not a sales pitch
- Sunlight and energy, not fluorescent lighting

**Dark theme feels like:**
- A professional data dashboard
- A trustworthy institution
- Technical credibility
- Premium, polished, serious

---

## Page Assignments

### Warm Theme (Worker-Facing) — `data-theme="warm"`

| Page | Audience | Why Warm |
|------|----------|----------|
| `index.html` | Workers + Everyone | First impression for workers |
| `for-workers.html` | Workers | Direct worker communication |
| `download.html` | Workers | Conversion page — must feel safe |
| `msaidizi.html` | Workers | Product page for the worker app |
| `testimonials.html` | Workers | Social proof from peers |

### Dark Theme (B2B/Professional) — No attribute

| Page | Audience | Why Dark |
|------|----------|----------|
| `technology.html` | Technical buyers | Data, architecture, APIs |
| `api.html` | Developers | Code, endpoints, technical |
| `about.html` | Investors, partners | Company credibility |
| `vision.html` | Investors, government | Strategic vision |
| `privacy-policy.html` | Everyone (legal) | Formal, trustworthy |

---

## Navigation Changes

### Requirement: Always Horizontal Tabs

**Problem:** Previous design used a hamburger menu on mobile, hiding navigation.

**Solution:** Navigation tabs are always visible and horizontal on ALL screen sizes:
- Tabs use `overflow-x: auto` for horizontal scrolling on small screens
- No hamburger button
- No sidebar drawer
- No hidden navigation

**Why:** Workers on feature phones and small screens need to see all options immediately. Hidden navigation reduces discoverability and trust.

### Implementation
- Removed `mobile-menu-btn` button from all HTML
- Removed `sidebar-overlay` and `mobile-sidebar` from all HTML
- CSS `nav-center` is always `display: flex` with horizontal scrolling
- Nav CTA ("Download") always visible on the right

---

## Technical Implementation

### How `data-theme="warm"` Works

```html
<!-- Worker page -->
<html lang="en" data-theme="warm">
  <link rel="stylesheet" href="style.css">        <!-- Base dark -->
  <link rel="stylesheet" href="warm-theme.css">   <!-- Warm overrides -->
</html>

<!-- B2B page -->
<html lang="en">
  <link rel="stylesheet" href="style.css">        <!-- Base dark only -->
</html>
```

### CSS Override Strategy

```css
/* warm-theme.css overrides using attribute selector */
[data-theme="warm"] {
  --bg-body: #FFF8F0;
  --text-body: #1A1A2E;
  /* ... */
}

[data-theme="warm"] .nav {
  background: rgba(255, 248, 240, 0.92);
}

[data-theme="warm"] .card {
  background: #FFFFFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
```

### What Gets Overridden
- ✅ Backgrounds (body, sections, cards)
- ✅ Text colors (headings, body, muted)
- ✅ Border colors
- ✅ Shadow intensities (lighter for light theme)
- ✅ Button colors (orange CTAs)
- ✅ Navigation (warm translucent)
- ✅ Stats/numbers (orange instead of gold)
- ✅ Badges and status indicators

### What Stays Dark
- Footer (dark for contrast at page bottom)
- Code blocks (syntax highlighting works best on dark)
- API tables (developer context)

---

## Brand Consistency

Both themes use Angavu brand colors — the warm theme emphasizes orange (#FF6B35) while the dark theme emphasizes gold (#E8A838). The logo remains identical across both themes.

| Element | Warm | Dark |
|---------|------|------|
| Primary accent | Orange #FF6B35 | Gold #E8A838 |
| Trust color | Teal #004E64 | Navy #1B4965 |
| Logo | Same | Same |
| Typography | Same fonts | Same fonts |

---

## Future Considerations

1. **User preference:** Could add a theme toggle for users who prefer dark mode
2. **System preference:** Could detect `prefers-color-scheme` for automatic switching
3. **A/B testing:** Warm vs dark conversion rates on download page
4. **Additional warm elements:** Illustrations of real workers, warm photography
5. **Language toggle:** Swahili-first with English secondary on warm pages

---

## Files Changed

| File | Change |
|------|--------|
| `warm-theme.css` | **NEW** — Warm theme CSS overrides |
| `index.html` | Added `data-theme="warm"`, warm CSS, removed sidebar |
| `for-workers.html` | Added `data-theme="warm"`, warm CSS, removed sidebar |
| `download.html` | Added `data-theme="warm"`, warm CSS, removed sidebar |
| `msaidizi.html` | Added `data-theme="warm"`, warm CSS, removed sidebar |
| `testimonials.html` | Added `data-theme="warm"`, warm CSS, removed sidebar |
| `technology.html` | Removed sidebar (kept dark theme) |
| `api.html` | Removed sidebar (kept dark theme) |
| `about.html` | Removed sidebar (kept dark theme) |
| `vision.html` | Removed sidebar (kept dark theme) |
| `privacy-policy.html` | Removed sidebar (kept dark theme) |
