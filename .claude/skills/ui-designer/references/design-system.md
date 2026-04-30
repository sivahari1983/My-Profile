# My Profile — Design System Reference

> Source of truth for the `ux-design-planner` and `playwright-ui-tester` agents. Reflects the live state of `static/css/style.css` and `templates/index.html`.

---

## 1. Color Tokens (CSS Custom Properties)

All colors are defined in the `:root` block at the top of `static/css/style.css`. Always reference these variables — never hardcode hex or rgba values in new styles.

| Token | Value | Usage |
|---|---|---|
| `--bg` | `#eef7f0` | Page background |
| `--bg2` | `#e2f0e5` | Subtle background variant |
| `--bg3` | `#d5e8d9` | Section alternate background |
| `--fg` | `#0f1a10` | Primary text, headings |
| `--fg2` | `#3d5440` | Secondary text, labels |
| `--green` | `#16a34a` | Primary accent — links, active states, headings |
| `--green2` | `#15803d` | Hover variant of green |
| `--teal` | `#0d9488` | Gradient partner to green |
| `--glow` | `rgba(22,163,74,0.2)` | Green glow shadow |
| `--r` | `0.75rem` | Small border radius (inputs, small chips) |
| `--r2` | `1.25rem` | Standard card border radius |
| `--t` | `all 0.35s cubic-bezier(0.4,0,0.2,1)` | Standard transition |
| `--font` | `'Inter', system-ui, sans-serif` | Body font |
| `--font2` | `'Space Grotesk', system-ui, sans-serif` | Display font (headings, numbers) |

---

## 2. Typography

| Element | Font | Size | Weight | Notes |
|---|---|---|---|---|
| Hero title (`.hero-title`) | `--font2` | `clamp(1.6rem, 5.5vw, 5.5rem)` | 800 | Gradient text, `white-space: nowrap` |
| Section heading (`.section-header h2`) | `--font2` | `clamp(1.8rem, 4vw, 2.8rem)` | 800 | Gradient text, letter-spacing `-0.04em` |
| Nav logo (`.nav-logo`) | `--font2` | `1.4rem` | 700 | Gradient text |
| Stat numbers (`.stat-number`) | `--font2` | `2.2rem` (hero), `3rem` (speaking) | 800 | Color `--green` |
| Body text | `--font` | `1rem` | 400 | Color `--fg2`, line-height 1.6 |
| Card headings (`h3`) | inherit | `1rem–1.1rem` | 600–700 | Color `--green` |
| Labels / meta | inherit | `0.75rem–0.9rem` | 500–600 | Often uppercase, letter-spacing `0.08–0.2em` |

**Gradient text pattern** (used on hero title, section headings, nav logo):
```css
background: linear-gradient(135deg, var(--fg) 30%, var(--green) 80%);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

---

## 3. Spacing & Layout

- **Container**: `max-width: 1200px`, `margin: 0 auto`, `padding: 0 1.5rem`
- **Sections**: `padding: 6rem 0` (desktop), `4rem 0` (≤ 480px)
- **Alternate section tint**: `section:nth-child(even)` gets `background: rgba(210,235,215,0.65)`
- **Section header margin**: `margin-bottom: 4rem`
- **Navbar height**: `68px` (fixed, `z-index: 1000`)

---

## 4. Card Pattern

All cards follow this shared pattern. New cards should match it exactly.

```css
background: rgba(255,255,255,0.65);
border: 1px solid rgba(22,163,74,0.14);   /* or rgba(34,197,94,0.14) — same intent */
border-radius: var(--r2);
box-shadow: 0 2px 12px rgba(0,0,0,0.04);
backdrop-filter: blur(8px);               /* where glassy effect needed */
transition: var(--t);
```

**Hover state** (apply `transform: translateY(-4px)` to all cards):
```css
border-color: rgba(22,163,74,0.35);
transform: translateY(-4px);
box-shadow: 0 8px 24px rgba(22,163,74,0.12);
background: rgba(255,255,255,0.9);        /* or .95 for stronger lift */
```

> `transform: translateY(-4px)` is the canonical hover lift. `translateY(-5px)` and `-6px` are used on taller cards (expertise, projects). Use `-3px` for small pill/link elements.

---

## 5. Scroll Reveal Animation

Add `.reveal-item` to any new card or content block. The IntersectionObserver in `main.js` adds `.revealed` when the element scrolls into view.

```css
/* Starting state */
.reveal-item {
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.6s ease, transform 0.6s cubic-bezier(0.16,1,0.3,1);
}
/* Triggered state */
.reveal-item.revealed {
    opacity: 1;
    transform: translateY(0);
}
```

Section headers use the same pattern with a separate `.revealed` class applied to `h2` and `p` children.

---

## 6. Buttons

| Variant | Class | Usage |
|---|---|---|
| Primary | `.btn.btn-primary` | Green gradient, white text — main CTAs |
| Secondary | `.btn.btn-secondary` | Frosted glass, green text + border |

**Button anatomy:**
```html
<a href="#section" class="btn btn-primary"><span class="btn-inner">Label</span></a>
```
The `.btn-inner` span enables the magnetic warp JS effect. Always wrap button text in it.

**Primary:**
```css
background: linear-gradient(135deg, var(--green), var(--teal));
color: #fff;
box-shadow: 0 4px 20px rgba(22,163,74,0.3);
border-radius: 100px;
padding: 0.85rem 2rem;
```

**Secondary:**
```css
background: rgba(255,255,255,0.6);
color: var(--green);
border: 1.5px solid rgba(22,163,74,0.35);
```

---

## 7. Pill / Tag / Badge Components

| Component | Class | Border Radius | Usage |
|---|---|---|---|
| Skill tag | `.skill-tag` | `100px` | Inside expertise cards |
| Tech badge | `.tech-badge` | `100px` | Inside project cards |
| Skill badge | `.skill-badge` | `100px` | Skills section floating tags |
| Event badge | `.event-badge` | `var(--r2)` | Speaking events list |
| Project status | `.project-status` | `100px` | LIVE / Building labels |
| Eyebrow label | `.hero-eyebrow` / `.section-label` | `100px` / inline | Section identifiers |

**Status badge variants:**
- `.status-live` — green tint, pulsing box-shadow animation
- `.status-building` — amber tint, static

---

## 8. Page Sections

| Section ID | Class | Template Variable | Grid / Layout |
|---|---|---|---|
| `#home` | `.hero` | — | Centered flex, full-viewport |
| `#about` | `.about` | `portfolio.about` | Single column with sub-grid |
| `#expertise` | `.expertise` | `portfolio.expertise` | `auto-fit minmax(300px,1fr)` |
| `#experience` | `.experience` | `portfolio.experience` | Alternating timeline |
| `#projects` | `.projects` | `portfolio.projects` | `auto-fit minmax(340px,1fr)` |
| `#services` | `.services` | `portfolio.services` | `auto-fit minmax(260px,1fr)` |
| `#certifications` | `.certifications` | `portfolio.certifications` | `auto-fit minmax(280px,1fr)` |
| `#speaking` | `.speaking` | `portfolio.speaking` | Stats row + events flex |
| `#skills` | `.skills` | `portfolio.skills` | Centered flex-wrap |
| `#contact` | `.contact` | `portfolio.contact` | 2-col grid (1-col on mobile) |

**Section template pattern:**
```html
<section id="[id]" class="[class]">
    <div class="container">
        <div class="section-header">
            <h2>Section Title</h2>
            <p>Section subtitle</p>
        </div>
        <div class="[section]-grid">
            <!-- cards with class="reveal-item" -->
        </div>
    </div>
</section>
```
Always wrap with `{% if portfolio.[key] %}...{% endif %}` so sections are omitted when data is absent.

---

## 9. Navigation

- Fixed top bar, `z-index: 1000`, `height: 68px`
- Scrolled state: `.navbar.scrolled` adds a stronger background and box-shadow (toggled by JS at 50px scroll)
- Nav links: `.nav-link` — underline grows from `width: 0` to `100%` on hover/active via `::after` pseudo-element
- Active link: `.nav-link.active` — color `--green`, underline visible (toggled by IntersectionObserver in JS)
- Mobile (`≤ 768px`): nav-menu hidden, `.nav-toggle` hamburger shown; `.nav-menu.open` expands full-width dropdown

**Nav links (current set):**
```
Home · About · Expertise · Experience · Projects · Services · Certifications · Contact
```

---

## 10. Hero Section

```
[Hero Canvas — animated dot grid background]
    [hero-content, centered]
        h1.hero-title          — name, gradient text, nowrap
        p.hero-subtitle        — typewriter effect via JS
        p.hero-views           — live view counter
        div.hero-stats         — 3 anchor stat boxes → #experience, #certifications, #speaking
        div.hero-cta           — "Get In Touch" (primary) + "Explore Profile" (secondary)
```

**Stat box** (`.stat`) is an `<a>` anchor. Renders as frosted glass card with green border. Hover lifts `translateY(-4px)`.

---

## 11. Animations & Effects

| Effect | Trigger | Mechanism |
|---|---|---|
| Hero content fade-in | Page load | CSS `@keyframes fadeUp` with staggered `animation-delay` |
| Section header reveal | Scroll into view | IntersectionObserver adds `.revealed` class |
| Card reveal | Scroll into view | `.reveal-item` + `.revealed` via IntersectionObserver |
| Timeline progress fill | Scroll | JS reads `scrollY`, sets `#timeline-fill` height as `%` |
| Timeline dot pulse | Dot enters viewport | JS adds `.pulse` class → `@keyframes pulse-ring` |
| Typewriter | Page load | JS cycles through `portfolio.roles` array |
| Custom cursor | Mouse move | JS animates `#cursor-dot` (snappy) and `#cursor-ring` (lagged) |
| Dot grid background | Continuous | Canvas `requestAnimationFrame` loop, reacts to mouse position |
| Skill badge float | Continuous | CSS `@keyframes float-badge` with varied `animation-duration` per badge |

---

## 12. Responsive Breakpoints

| Breakpoint | Rules |
|---|---|
| `≤ 1024px` | Timeline collapses to single column, track moves to left `24px` |
| `≤ 768px` | Nav hamburger shown, contact grid → 1 col, hero stats stack vertically, cursor hidden |
| `≤ 480px` | Section padding `4rem`, single-column grids for expertise / projects / services |

---

## 13. Adding a New Section — Checklist

1. **Template** (`templates/index.html`): add `<section id="[id]" class="[class]">` with `.container`, `.section-header`, and grid div; wrap in `{% if portfolio.[key] %}`
2. **Data** (`app.py`): add key to `DEFAULT_PORTFOLIO`
3. **CSS** (`static/css/style.css`): add grid + card styles at the end under a comment block; use card pattern from §4; add `.reveal-item` to cards
4. **Nav** (`templates/index.html`): add `<a href="#[id]" class="nav-link">[Label]</a>` to `.nav-menu`
5. **Regenerate**: run `python generate_static.py` → confirm `Static site generated successfully!`
6. **Verify**: use `playwright-ui-tester` agent to confirm section renders, nav link scrolls to it, mobile layout intact
