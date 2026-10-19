# Web — platform guide

Stable principles for web products (SaaS, landing pages, dashboards, e-commerce). For what changed
recently (newly Baseline CSS/HTML features, regulation, visual trends) read the newest
`knowledge/trends/<period>/web.md`.

## Non-negotiables
- **WCAG 2.2 AA**: contrast 4.5:1 text / 3:1 large text, UI parts and focus rings; target size ≥ 24×24
  CSS px (44 recommended for primary actions); visible focus not obscured by sticky UI; keyboard
  operable; no dragging-only interactions; accessible authentication (no puzzles, allow paste).
- Responsive from 320 px; no horizontal scroll; touch-friendly on mobile.
- **Core Web Vitals** (75th percentile): LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1. Design choices
  (huge hero video, web-font swaps, layout-shifting banners) affect them.
- `prefers-reduced-motion`, `prefers-color-scheme`, `forced-colors` respected.
- Semantic HTML first: landmarks, headings in order, buttons are `<button>`, links are `<a>`.

## Typography
- Body 16–18 px, line-height 1.4–1.6, line length 45–75 ch.
- Fluid display sizes with `clamp()`; a modular scale (1.2–1.333) for UI, bigger jumps for marketing.
- ≤ 2 families; variable fonts to cut requests; `font-display: swap` + size-adjusted fallbacks to avoid CLS.
- `text-wrap: balance` for headings, `pretty` for paragraphs.

## Colour & theming
- Tokens as CSS custom properties (or the framework's theme: Tailwind `@theme` / `theme.extend`,
  shadcn/ui variables in `globals.css`). OKLCH makes even, accessible ramps.
- Real dark theme (elevated surfaces lighter, desaturated accents), not inversion.
- `color-scheme` set so form controls and scrollbars match.

## Layout & patterns
- Landing: hero (outcome headline, subhead, primary CTA, proof visual) → social proof → problem /
  solution → benefits (not features) → objections / FAQ → pricing → final CTA.
- App shells: persistent nav, clear page titles, command palette (⌘K) for power users, breadcrumbs for
  deep hierarchies, sensible empty states with a first action.
- Forms: visible labels, `autocomplete` attributes, inline validation on blur, clear error recovery.
- Tables / dashboards: alignment by data type, tabular numbers, density toggle, sticky headers.

## Motion
- Transitions explain change (View Transitions, shared-element feel); 150–300 ms for UI.
- Scroll-driven effects only when they serve the story; always a reduced-motion path.

## Where the design lives in code
`tailwind.config.*` / `@theme` in CSS, `globals.css` / `variables.css`, `theme.ts` / `tokens.*`,
component library folders (`components/ui/`), font loading in layout files (`next/font`, `<link>`).

## Capture & checks
- A **browser MCP** (the `squint-devices` companion's Chrome DevTools server, or Playwright): navigate, resize to 1440×900 / 768×1024 / 390×844, full-page screenshots,
  emulate dark mode, click through flows.
- Fallback: `squint.py capture url --url <url> --out screens/before/home.png [--mobile]`.
- Contrast: compute from token values; Lighthouse / axe when available (`npx lighthouse <url> --only-categories=accessibility,performance`).
