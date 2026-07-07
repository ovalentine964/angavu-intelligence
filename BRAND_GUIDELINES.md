# Angavu Intelligence — Brand Guidelines

> **Version:** 1.0 | **Date:** 2026-07-07 | **Author:** Implementation Swarm 11

---

## 1. Brand Architecture

```
Angavu Intelligence (Company)
  └── Msaidizi (Product — Android App)
```

- **Angavu Intelligence** is the company brand. It represents vision, clarity, and intelligence for Africa's invisible economy.
- **Msaidizi** is the consumer-facing product name (Swahili for "helper"). It's what workers see and call the app.
- **The Eye of Africa** is the shared visual symbol that connects both brands.

### Symbol Strategy

The eye/Africa symbol is the **company's visual anchor**. It appears on:
- The company website, decks, and marketing
- The Msaidizi app icon (as the primary recognizable element)
- Future Angavu products

At icon sizes (48dp), text is unreadable. The eye symbol alone carries brand recognition. Workers will come to know it as "the Msaidizi eye" — the app's face on their home screen.

---

## 2. Logo & Icon

### Company Logo (Angavu Intelligence)
- **File:** `angavu-intelligence/assets/angavu-icon.svg`
- **Usage:** Website, presentations, business cards, marketing materials
- **Contains:** Eye symbol + Africa silhouette + "ANGAVU INTELLIGENCE" text + tagline
- **Minimum size:** 120px wide (text becomes illegible below this)

### App Icon (Msaidizi)
- **Files:** `msaidizi-app/app/src/main/res/drawable/ic_launcher_foreground.svg` (foreground) and `ic_launcher_background.svg` (background)
- **Usage:** Android launcher, Play Store, app stores
- **Contains:** Eye symbol + Africa silhouette + "MSAIDIZI" text
- **Minimum effective size:** 48dp (eye symbol alone is recognizable; text is a bonus at larger sizes)

### Favicon
- **File:** `angavu-intelligence/assets/favicon.svg`
- **Usage:** Browser tabs, bookmarks
- **Contains:** Simplified eye symbol + "A" letter

### Icon Sizing Reference

| Context | Size | Notes |
|---------|------|-------|
| Android launcher (mdpi) | 48×48 dp | Eye symbol only, text too small |
| Android launcher (xxxhdpi) | 192×192 dp | Full detail visible |
| Play Store listing | 512×512 px | Full composite with text |
| Adaptive icon canvas | 108×108 dp | Foreground layer with safe zone |
| Favicon | 32×32 px | Simplified eye only |

---

## 3. Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Navy Blue** | `#1B4965` | 27, 73, 101 | Primary backgrounds, headers, app icon bg |
| **Midnight** | `#0F2D42` | 15, 45, 66 | Dark gradient endpoint |
| **Gold** | `#E8A838` | 232, 168, 56 | Accent, eye symbol, highlights |
| **Bright Gold** | `#F5C842` | 245, 200, 66 | Gradient highlight (iris glow) |
| **Deep Gold** | `#D09030` | 208, 144, 48 | Shadow/depth accents |

### Secondary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **African Orange** | `#E8853D` | 232, 133, 61 | Secondary accent, CTAs |
| **Warm White** | `#FFFFFF` | 255, 255, 255 | Text on dark, highlights |
| **Light Navy** | `#2A4070` | 42, 64, 112 | Hover states, secondary bg |

### Semantic Colors

| Name | Hex | Usage |
|------|-----|-------|
| Success | `#4CAF50` | Positive profit, confirmations |
| Error | `#F44336` | Losses, errors |
| Warning | `#FF9800` | Pending states, alerts |
| WhatsApp Green | `#25D366` | WhatsApp integration UI only |

### Color Rules
- **Navy + Gold** is the core pairing. Never substitute.
- Gold is an **accent**, not a primary fill. Use sparingly for maximum impact.
- On dark backgrounds, use white text. On gold backgrounds, use navy text.
- The eye symbol is **always gold on navy**. Never invert.

---

## 4. Typography

### App Typography (Android)
- **Primary:** System default (Roboto on Android)
- **Headers:** Bold (700), tracking +2–5
- **Body:** Regular (400)
- **Monetary values:** Medium (500), tabular figures

### Brand Typography (Marketing)
- **Headlines:** `'Segoe UI'`, `'Helvetica Neue'`, Arial, sans-serif — Bold 700
- **Subheads:** Same family — Light 300, wider letter-spacing (5–7px)
- **Body:** Same family — Regular 400

### Text Hierarchy
1. **ANGAVU** / **MSAIDIZI** — Bold 700, white, letter-spacing 4–5
2. **INTELLIGENCE** / taglines — Light 300, gold (#E8A838), letter-spacing 7
3. **Body text** — Regular 400, white or dark depending on background

---

## 5. The Eye Symbol — Construction & Usage

### Anatomy
The eye consists of:
1. **Concentric arcs** (top) — 3–5 nested elliptical arcs, increasing opacity inward
2. **Lower arcs** (subtle reflection) — Same arcs mirrored below, very low opacity
3. **Iris ring** — Bold circular stroke
4. **Pupil** — Solid gold fill with radial gradient
5. **Highlights** — Two white circles (primary + secondary reflection)

### Construction Grid
- Built on a 512×512 canvas
- Eye centered vertically, slightly above center (~47% from top)
- Outer arc: 160px radius (horizontal), 120px radius (vertical)
- Each inner arc: ~78% of the previous
- Pupil radius: ~20px
- Africa silhouette behind at 15–18% opacity

### Safe Zone
- Adaptive icon: Keep all content within 66dp of the 108dp canvas (61% safe zone)
- This means ~156px margin on each side of the 512px canvas
- The eye + text fits comfortably within this zone

### Do's ✅
- Use the eye on navy blue background
- Keep the gold-on-navy color scheme
- Maintain the arc hierarchy (thicker = more opaque)
- Include Africa silhouette as a subtle background element
- Use the SVG sources; never rasterize and re-scale

### Don'ts ❌
- Don't change the eye colors
- Don't remove the Africa silhouette
- Don't add extra elements inside the eye
- Don't rotate or skew the symbol
- Don't place the eye on busy/patterned backgrounds
- Don't use the eye without the navy background (except on white with navy eye)
- Don't recreate from memory — always use the source SVG

---

## 6. App Icon Specifications

### Adaptive Icon (Android v26+)
- **Background layer:** Solid navy gradient (`#1B4965` → `#0F2D42`)
- **Foreground layer:** Eye symbol + Africa silhouette + "MSAIDIZI" text
- **Shape:** Determined by device/OEM (circle, squircle, rounded square)
- **Safe zone:** 66dp inner circle of the 108dp canvas

### Legacy Icon (Pre-v26)
- Full composite: background + foreground merged
- Rounded square with subtle gold border

### Round Icon
- Same as legacy; Android applies circular mask

### Density Matrix

| Density | Scale | Launcher | Foreground | Background |
|---------|-------|----------|------------|------------|
| mdpi | 1× | 48×48 | 108×108 | 108×108 |
| hdpi | 1.5× | 72×72 | 162×162 | 162×162 |
| xhdpi | 2× | 96×96 | 216×216 | 216×216 |
| xxhdpi | 3× | 144×144 | 324×324 | 324×324 |
| xxxhdpi | 4× | 192×192 | 432×432 | 432×432 |

### Regeneration
Run `python3 msaidizi-app/generate_icons.py` from the workspace root to regenerate all PNGs from SVG sources.

---

## 7. Cultural Considerations

### East African Context
- **Gold/amber** evokes warmth, prosperity, and sunrise — universally positive in East Africa
- **Navy blue** conveys trust, professionalism, and technology
- **The eye** symbolizes clarity, vision, and watchfulness — positive associations across cultures
- **Africa silhouette** creates continental pride and belonging
- Avoid red as a primary color (can signal danger/debt in financial contexts)
- The "Msaidizi" name is Swahili — the lingua franca of East Africa — ensuring immediate recognition

### Accessibility
- Gold (#E8A838) on Navy (#1B4965) = contrast ratio ~4.8:1 (passes WCAG AA for large text)
- White on Navy = contrast ratio ~8.5:1 (passes WCAG AAA)
- Icon is recognizable without color (works in grayscale due to shape contrast)

---

## 8. File Reference

```
angavu-intelligence/
  assets/
    angavu-icon.svg          # Full company logo (512×512, rounded rect)
    logo-icon.svg            # Detailed logo icon variant
    favicon.svg              # Web favicon (32×32)
    angavu-banner.svg        # Company banner
  BRAND_GUIDELINES.md        # This file

msaidizi-app/
  app/src/main/res/
    drawable/
      ic_launcher_foreground.svg    # App icon foreground (eye + text)
      ic_launcher_background.svg    # App icon background (navy gradient)
    mipmap-anydpi-v26/
      ic_launcher.xml               # Adaptive icon config
      ic_launcher_round.xml         # Round adaptive icon config
    mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/
      ic_launcher.png               # Legacy launcher icon
      ic_launcher_foreground.png    # Adaptive foreground layer
      ic_launcher_background.png    # Adaptive background layer
      ic_launcher_round.png         # Round variant
  generate_icons.py                 # SVG → PNG conversion script
```

---

*These guidelines ensure brand consistency across all Angavu Intelligence products while giving Msaidizi its own recognizable identity on workers' home screens.*
