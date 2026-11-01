---
platform: web
period: 2026-11
researched_at: 2026-11-01
previous: 2026-10
sources: 63
---

# Web — UI/UX trends · November 2026

## TL;DR
- Scroll-driven animations now ship in all three engines: Firefox 159 enabled them by default on 2026-10-27, after Chrome 115+ and Safari 26. Treat them as a normal enhancement (still wrap in `@supports` and reduced-motion). Cross-document view transitions still lack Firefox. [18][10][19]
- The "AI default" look (indigo gradient, Inter, centred pill-badge hero, three emoji cards) still signals "generated", and the usual fixes (cream plus terracotta, broadsheet hairlines, mono eyebrows) are turning into tells too. Every visible choice should come from the brand. [52][53][54]
- Type with character is back: high-contrast and "mutant heritage" serifs, photo-lettering revivals, oversized kinetic display type, delivered as variable fonts. [40][41]
- Color is warmer and systematic: warm neutrals (Linear, Tailwind, Pantone Cloud Dancer) built as OKLCH tokens with relative color and `contrast-color()` (Baseline April 2026). [39][35][38][5]
- AI UX has moved from chat to oversight (intent previews, autonomy levels, specific status lines, undo windows), and agents are now users of your UI (semantic HTML, WebMCP origin trial in Chrome 149). [29][30][27][21]
- Chrome 150 (2026-06-30) adds declarative `focusgroup` for toolbar-style arrow-key navigation, `background-clip: border-area` for gradient borders and `text-fit`. All are Chrome-only for now, so use them as progressive enhancement. [63]
- Compliance has consequences: a French court ordered Carrefour to make its site and app accessible within six months (June 2026). WCAG 2.2 AA and INP ≤ 200 ms (p75) are table stakes. [25][23][22]

## Platform baseline (expected now, not a trend)
- **Native overlay stack** — `popover` (Baseline Jan 2025), invoker commands `command`/`commandfor` (Baseline Dec 2025), `<dialog>`, and the `:open` pseudo-class (Baseline May 2026) cover menus, modals and toasts without JS libraries. Core anchor positioning (`anchor-name`, `position-anchor`, `position-area`, `@position-try`) is in Chrome 125+, Safari 26+ and Firefox 147+ (enabled 2026-01-13). Web Platform Status still marked the full feature "limited" at last check while Interop 2026 fixes edge cases. [10][1][6][11][17][14]
- **Layout primitives** — container size queries (Widely available since Aug 2025), `:has()` and CSS nesting (both Widely available June 2026), subgrid (Widely available March 2026). Build components to respond to their container, not the viewport. [10][7][4]
- **Newly Baseline in 2026 to use now** — container style queries (May), `field-sizing: content` (June), `contrast-color()` (April), `shape()` (February), `sibling-index()`/`sibling-count()` (August), Navigation API (January). `@scope` is also Baseline newly available. [6][7][5][3][9][2][8][1][10]
- **Scroll-driven animations** — Chrome 115+, Safari 26+, and now Firefox 159 (default-on, released 2026-10-27, so all three engines). Baseline status on webstatus.dev was not re-checked after the release. Use `animation-timeline: scroll()/view()` and keep a non-animated fallback. [18][19][11]
- **Color stack** — OKLCH and `color-mix()` (Widely available Nov 2025), relative color syntax and `light-dark()` (Baseline 2024). Safari 27 adds `alpha()`, `color-mix()` with more than two colors, and `light-dark()` with images. [10][12]
- **Entry/exit animation** — `@starting-style` and `transition-behavior: allow-discrete` (Baseline Aug 2024) animate `display`/popover/dialog in and out without JS. [10][15]
- **Same-document view transitions** — Baseline since 2025-10-14 (Firefox 144), with `view-transition-class`. Low-risk enhancement for SPA state changes. [10]
- **Typography hygiene** — `text-wrap: balance` is Baseline (2024). `text-wrap: pretty` works in Chrome and Safari 26 and degrades safely. Variable fonts are the default delivery format. [10][11][40]
- **Command palette (⌘K / Ctrl+K)** — power users expect one in SaaS. GitHub paused its planned removal after user feedback (July 2025). [55]
- **Accessibility floor** — WCAG 2.2 AA: Focus Not Obscured (2.4.11), Dragging Movements (2.5.7), Target Size ≥ 24×24 CSS px (2.5.8), Consistent Help, Redundant Entry, Accessible Authentication. EN 301 549 (EAA presumption of conformity) still points to WCAG 2.1 AA, with a new version due in 2026. WCAG 3 is still a draft and W3C says to meet 2.2 now. [23][25][24]
- **Performance floor** — INP: good ≤ 200 ms, poor > 500 ms at p75. The LCP and Event Timing APIs became Baseline in Dec 2025 (Safari 26.2), so field responsiveness is measurable in every engine. [22][1][10]

## Trends

### web-expressive-serif-revival — Expressive & high-contrast serif revival
- **Status:** rising
- **Momentum:** →
- **What:** After a decade of uniform neo-grotesk branding, high-contrast and "mutant heritage" serifs (classic forms re-cut with an off-kilter, hand-made edge) are returning for headlines and brand voice. Practitioners frame it as a reaction to AI's uniform polish.
- **Seen in:** Little Bird AI assistant (Meraki serif on cream), Flamingo Estate (Exposure VAR), Post Post Hotel (BR-Post), Olive + Gourmando (HAL Timezone). [40]
- **Fits:** AI assistants that want to feel humane, DTC, hospitality, editorial and publishing, premium B2B brands.
- **Avoid when:** dense data UI or small UI labels (keep a neutral sans for chrome). Thin hairlines fail at small sizes. Cream plus serif plus terracotta is already a known "second-wave AI" combination, so it needs a real brand reason. [54]
- **Implement:** Serif for display (≥ 32 px) paired with a neutral sans for UI and body. Use a variable serif with an optical-size axis (`font-optical-sizing: auto`). Fluid size: `font-size: clamp(2.5rem, 4vw + 1rem, 6rem)`. `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs. Check stroke contrast (WCAG 1.4.3) at the smallest rendered size. Subset and `preload` the display face to protect LCP.
- **Sources:** [40], [41], [54]

### web-kinetic-oversized-type — Oversized, kinetic display type
- **Status:** mainstream
- **Momentum:** →
- **What:** Type becomes the main visual, set huge, cropped and often animated (on-beat, scroll-linked or variable-axis morphing). 60s–70s photo-lettering proportions are being recut digitally. With scroll-driven animations now in all engines, scroll-linked type needs no JS.
- **Seen in:** Spotify Wrapped microsite, Apex Wheels "GO FAST." cropped lettering (Gold Front), Shopify Editions Spring '26 (particle-dispersing type). [40][41][48]
- **Fits:** campaigns, launches, brand and portfolio sites, event pages, product reveals.
- **Avoid when:** the headline must carry meaning in a narrow viewport (cropped words lose legibility). Avoid looping motion with no pause control (WCAG 2.2.2). Never ship text as canvas or image without real DOM text.
- **Implement:** Animate variable axes with a registered property: `@property --wght { syntax: '<number>'; inherits: true; initial-value: 400 }` and `font-variation-settings: 'wght' var(--wght)`. Stagger per-letter spans with `animation-delay: calc(sibling-index() * 30ms)` (Baseline Aug 2026). Wrap motion in `@media (prefers-reduced-motion: no-preference)`. Try `text-box: trim-both cap alphabetic` for optical alignment (Chrome/Safari). Chrome 150 `text-fit` can fit a headline to its box width but is Chrome-only, so keep a `clamp()` fallback. [15][9][10][63]
- **Sources:** [40], [41], [48], [15], [9], [63]

### web-anti-ai-craft-texture — Anti-AI craft: texture, grain and visible human touch
- **Status:** rising
- **Momentum:** →
- **What:** Landor's Graham Sykes calls this "Anti-AI Crafting". Designers push back on slick, generated visuals with analogue surfaces, collage, hand marks, real photography and deliberate friction in type. Homepage audits also list textured backgrounds among 2026 patterns.
- **Seen in:** Burberry Cross-Stitch campaign and Madalena Studio for Crucible (brand-level) [41]; Tidal Magazine's Bashar Murad interview [40]; textured backgrounds across 2026 SaaS homepages [49].
- **Fits:** consumer brands, creative tools, culture and media, AI products trying not to look like competitors.
- **Avoid when:** texture lowers text contrast or adds large raster payloads (LCP). Avoid it in task-heavy app UI.
- **Implement:** Keep texture on decorative layers only (`::before` with `pointer-events: none`). Use small tileable noise (SVG `feTurbulence` or a ≤ 20 KB WebP) with `background-blend-mode`/`mix-blend-mode`. Use real photography and illustration over stock 3D blobs. Serve images with `image-set()` (Widely available March 2026). Re-check contrast over the textured area. [4]
- **Sources:** [41], [40], [49], [4]

### web-warm-neutral-palettes — Warm neutrals & soft off-whites replace cool gray and stark white
- **Status:** rising
- **Momentum:** →
- **What:** Neutral bases are moving warmer and less saturated. Pantone named a white, Cloud Dancer (PANTONE 11-4201), its 2026 Color of the Year. Linear's March 2026 refresh moved both themes to warmer gray. Tailwind added "gray with personality" palettes.
- **Seen in:** Linear [35]; Tailwind CSS `mauve`/`olive`/`mist`/`taupe` palettes [38]; Little Bird (cream background) [40]; Pantone Cloud Dancer [39].
- **Fits:** productivity SaaS, AI assistants, content-heavy sites, wellness and lifestyle.
- **Avoid when:** it is the only idea. Cream plus terracotta (≈ #F4F1EA / #D97757) is flagged as a second-wave AI tell [54]. Linear notes that going too warm turns muddy [35]. Warm off-white plus pale text quickly fails contrast.
- **Implement:** Define neutrals in OKLCH with small chroma and a warm hue, e.g. `--surface: oklch(97% 0.008 85)`, `--surface-2: oklch(94% 0.01 85)`, dark theme `oklch(19% 0.01 85)` rather than pure black. Use `color-scheme: light dark` with `light-dark()` per token. Keep one saturated accent for actions. Pantone publishes no web hex for Cloud Dancer, so any hex is an approximation. [39][10]
- **Sources:** [39], [35], [38], [40], [54]

### web-oklch-token-systems — OKLCH-generated themes, relative color & automatic contrast
- **Status:** mainstream
- **Momentum:** →
- **What:** Teams generate whole themes from a few perceptual inputs instead of hand-picking dozens of hex values. Linear builds themes from base, accent and contrast. Tailwind v4's default palette has been OKLCH since January 2025. `contrast-color()` became Baseline in April 2026 and is an Interop 2026 focus area.
- **Seen in:** Linear theme generator [35]; Tailwind CSS v4 palette [37]; Chrome DevRel "respect user preferences" guidance [15].
- **Fits:** any product with dark mode, user themes, white-labeling or data-viz color scales.
- **Avoid when:** you rely on `contrast-color()` alone for brand-tinted text, since it returns only black or white. OKLCH hue shifts can leave the sRGB/P3 gamut, so clamp and test.
- **Implement:** `--accent: oklch(62% 0.19 255)`, `--accent-hover: oklch(from var(--accent) calc(l - 0.06) c h)`, `--on-accent: contrast-color(var(--accent))`, `--accent-soft: color-mix(in oklch, var(--accent) 14%, var(--surface))`. Drive variants with container style queries, e.g. `@container style(--tone: inverted)`. Generate scales by stepping L at fixed C and H, then verify WCAG contrast pairs in CI. [5][6][37]
- **Sources:** [35], [37], [5], [6], [13], [15]

### web-immersive-3d-webgpu — Cinematic real-time 3D storytelling (WebGL → WebGPU)
- **Status:** rising
- **Momentum:** →
- **What:** Award-level sites are scroll-sequenced 3D "films" built with Three.js, GSAP and Lenis, now used for flagship brand launches. WebGPU renderers with WebGL fallback are starting to ship (WebGPU is in Chrome/Edge and Safari 26 but not yet Baseline). Awwwards Sites of the Month in 2026 (Oryzo AI, GQ × Audemars Piguet, Why Zero) still lean this way, while Aug 2026 and Jun 2026 went to ERA Residence and Son Daven (The First The Last), which I did not review. [43]
- **Seen in:** Oryzo AI by Lusion (SOTM Apr 2026) [43][45]; Cartier Watches & Wonders 2026 by Immersive Garden [48]; GQ × Audemars Piguet "The Extraordinary Lab" (SOTM Mar 2026) [43]; Why Zero (SOTM Sep 2026) [46]; IVRESS (WebGPU with WebGL fallback) [48].
- **Fits:** luxury, automotive, product launches, campaign microsites, agency and portfolio sites.
- **Avoid when:** SaaS conversion pages or anything needing fast INP/LCP on mid-range Android. Awwwards Dev Award accessibility sub-scores (≈ 6.8–7.0) trail animation scores (≈ 8.6) on these sites [44][45]. Don't hide core content in canvas.
- **Implement:** Keep the LCP element as HTML text or an image, and lazy-init 3D on idle or first interaction. Use Three.js `WebGPURenderer` with WebGL fallback, writing shaders once in TSL [48]. Use glTF with Draco/Meshopt. Provide `prefers-reduced-motion` and low-power fallbacks (static poster) plus audio opt-in. Keep a parallel semantic HTML layer.
- **Sources:** [43], [45], [46], [48], [42], [10]

### web-editorial-storytelling — Editorial, magazine-style long-form layouts
- **Status:** mainstream
- **Momentum:** →
- **What:** Reports, launches and brand pages are designed like magazines: strong typographic hierarchy, data-viz chapters, motion-paced sections. Research PDFs become editorial sites.
- **Seen in:** Ai in Design Report 2026 (Awwwards SOTD 2026-08-26) [44]; Shopify Design "The Renaissance Edition" (SOTM Feb 2026) [43]; GQ × Audemars Piguet Extraordinary Lab [47].
- **Fits:** annual reports, product "Editions", thought-leadership, D2C storytelling.
- **Avoid when:** users need to scan or compare (pricing, docs reference). "Broadsheet cosplay" (hairline rules, zero radius, dense columns) on a SaaS brief is a second-wave AI tell. [54]
- **Implement:** CSS grid with named lines and `subgrid` to align captions, figures and pull-quotes. Measure 60–75ch with `text-wrap: pretty`. Chapter navigation with `position: sticky` and `scroll-margin-top`. Reveal data viz with `animation-timeline: view()` (now all engines; keep `@supports`). Keep a real h1–h3 outline for SEO and agents. [4][27][18]
- **Sources:** [44], [43], [47], [54], [4]

### web-bento-feature-grids — Bento feature grids
- **Status:** peaking
- **Momentum:** →
- **What:** Modular, varied-size card grids remain the default for showing 6–9 features on SaaS homepages. Overuse and stock visuals make them generic. They work best when cell size reflects real priority.
- **Seen in:** Linear, Notion, Customer.io, Huly, Payhawk (cataloged by SaaSFrame, 43 implementations). [51]
- **Fits:** feature-dense B2B SaaS, product overview pages, changelog highlights.
- **Avoid when:** content is linear or deep. Avoid when every cell is the same stock card with an icon. Adoption and conversion stats in 2026 bento articles are unsourced. [51]
- **Implement:** Base unit 80/100/120 px with 16–24 px gutters (12 px mobile), a 2×2 hero cell for the #1 feature, 3–4 columns desktop → 2 → 1 reordered by importance. Visual ≈ 60–70% of card height. Hover limited to one or two properties (4–8 px lift, 200–300 ms). `grid-auto-flow: dense` plus container queries inside cards. Real product UI in cells. [51]
- **Sources:** [51], [49]

### web-css-native-motion — Native, declarative motion (view transitions, scroll-driven, entry/exit)
- **Status:** rising
- **Momentum:** ↑
- **What:** Page transitions, scroll-linked reveals and staggered entry/exit are moving from JS libraries to CSS. Firefox 159 (2026-10-27) turned scroll-driven animations on by default, so the feature now works in every engine. Same-document view transitions are Baseline. Cross-document view transitions (Chrome 126+, Safari 18.2+; not Firefox) remain an Interop 2026 focus area. Chrome is also adding element-scoped view transitions (147) and scroll-triggered animations (146).
- **Seen in:** No verified production list gathered. Award sites still mostly run on GSAP/Lenis (Cartier W&W 2026, Why Zero) [48][46]. Recent (godly.website's redirect target) is full of micro-interaction pieces [61].
- **Fits:** MPAs and marketing sites (cross-doc transitions, no SPA needed), content sites, e-commerce listing→detail, dashboards.
- **Avoid when:** motion carries meaning without a reduced-motion alternative. Avoid scroll-jacking. Cross-document transitions are same-origin only and need both pages to opt in. Firefox users get no cross-doc transition, so it must never block navigation. Older Firefox (< 159) and Safari < 26 lack scroll timelines, so provide a static fallback.
- **Implement:** Cross-doc: `@view-transition { navigation: auto; }` on both pages, `view-transition-name` on shared elements, `pagereveal`/`pageswap` for logic, `<link rel="expect" href="#hero" blocking="render">` (Chrome only). Scroll: `animation-timeline: view(); animation-range: entry 0% cover 50%;` inside `@supports (animation-timeline: view())`. Entry/exit: `@starting-style { opacity: 0; translate: 0 8px }` plus `transition-behavior: allow-discrete`. Springs: `linear()` easing. Wrap everything in `prefers-reduced-motion`. [16][15][10][19][18]
- **Sources:** [10], [11], [13], [14], [15], [16], [18], [19]

### web-prompt-first-hero — Prompt box as the landing-page hero
- **Status:** mainstream
- **Momentum:** →
- **What:** For AI builders and creation tools, the hero is the product: a large prompt input with suggestion chips replaces the headline-plus-two-buttons pattern, and visitors start before signing up.
- **Seen in:** Replit ("What will you build?") [58][49]; Bolt ("What will you build today?" with Website/Slides/App/Prototype chips) [57]; Figma Make ("What do you want to make?") [59].
- **Fits:** generative and creation tools, AI agents, search and research products, developer tools.
- **Avoid when:** the product isn't prompt-driven (a fake prompt box reads as trend-chasing), or users can't yet say what they want: NN/g's Qwen study found newcomers needed a categorized entry point. [28]
- **Implement:** Real `<form>` with visible `<label>` and `<textarea>` using `field-sizing: content` plus `max-block-size`. Chips are `<button type="button">` that insert text (never auto-submit). Enter submits, Shift+Enter adds a newline. Offer import shortcuts. Defer auth until the first result. Respect reduced motion for rotating placeholders and never use the placeholder as the only label. [7][28]
- **Sources:** [57], [58], [59], [49], [28], [7]

### web-interactive-product-demos — Interactive demos & "Take a tour" CTAs
- **Status:** rising
- **Momentum:** →
- **What:** Homepages let visitors click through the real product (HTML-captured, no sign-up). In Navattic's data, interactive-demo CTAs appear on 18% of ~5,000 B2B SaaS sites (12% in 2024), and 48% of top-1% demos sit on homepages (8% in 2024).
- **Seen in:** Linear and Stripe (live product widgets) [49]; "Take a tour" is the most common CTA text among top-1% demos [50].
- **Fits:** B2B SaaS, dev tools, complex products, PLG funnels.
- **Avoid when:** the demo is a screenshot slideshow, traps focus or auto-plays sound. Benchmarks come from one vendor's platform data. [50]
- **Implement:** CTA above the fold or in the navbar (80% of top-1% demo CTAs). Open the demo in `<dialog>` via `<button command="show-modal" commandfor="demo">`. HTML captures over screenshots (86% of top demos), 5–8 guided steps and a clear exit. Track engagement, completion and CTR. [50][1]
- **Sources:** [50], [49], [1]

### web-agent-oversight-ui — Agent oversight UI: previews, autonomy levels, status & undo
- **Status:** rising
- **Momentum:** →
- **What:** As products add agents that act, a standard control-and-transparency layer is emerging: plan previews before acting, per-task autonomy levels, specific status messages, action logs with time-boxed undo, escalation to a human. NN/g calls trust "a major design problem" for AI in 2026.
- **Seen in:** Linear ("The product development system for teams and agents") [36][49]; Notion agents [49]; Figma agent (chats visible to teammates by default) [34]; Qwen agent (permissions and cost confirmation before payment, per NN/g) [28].
- **Fits:** SaaS with automations, finance and ops tools, agentic browsers, any feature that writes, sends, buys or deletes.
- **Avoid when:** confirmation fatigue on trivial reversible actions, raw chain-of-thought or logs shown unsanitized, binary "failed" errors. [30]
- **Implement:** (1) Intent Preview card: numbered plan plus "Proceed / Edit plan / Do it myself", mandatory for irreversible, financial or sharing actions. (2) Autonomy dial per task type: Observe & Suggest → Plan & Propose → Act with Confirmation → Act Autonomously. (3) Status = verb + specific object + constraint, announced via `role="status"`/`aria-live="polite"`. (4) Audit log with "Undo available for 15 minutes". (5) Clarifying questions as option cards. Show fees and totals before any commit. [29][30][28]
- **Sources:** [29], [30], [26], [28], [34], [36], [49]

### web-generative-ui-in-assistants — Generative UI & product UIs rendered inside AI assistants
- **Status:** emerging
- **Momentum:** →
- **What:** Assistants render interactive UI instead of text. Google's generative UI composes custom interactive pages per prompt (Gemini dynamic view, AI Mode). MCP Apps (first official MCP extension, launched 2026-01-26) lets a product ship sandboxed HTML UIs that run inside Claude, ChatGPT, VS Code and Goose. Your design has a second surface you don't control.
- **Seen in:** Claude, ChatGPT, VS Code, Goose (MCP Apps hosts) [33]; Gemini dynamic view and Google AI Mode [32].
- **Fits:** SaaS with high-frequency lookups or actions, commerce, maps and data products.
- **Avoid when:** the flow needs heavy navigation or many screens. Users rated expert-designed sites above generative UI in Google's evaluation, and generation can take a minute or more. [32]
- **Implement:** Design compact, self-contained cards (one task, ≤ 1 screen) with your tokens compiled in. MCP Apps declare `_meta.ui.resourceUri` → `ui://` HTML bundle → sandboxed iframe, JSON-RPC over `postMessage`. Expect no parent-window access, host-imposed theming and user approval of UI-initiated tool calls. Prefer a controlled component registry over open-ended generation. [33][32]
- **Sources:** [32], [33], [31]

### web-agent-legible-sites — Agent-legible sites: semantic UI, WebMCP & AI-search answers
- **Status:** emerging
- **Momentum:** →
- **What:** NN/g argues "user" no longer means only human: browser agents read screenshots, the accessibility tree or APIs, so clear labels and predictable patterns serve both. Chrome opened a WebMCP origin trial (Chrome 149, June 2026) so sites can declare tools for agents. Marketing sites add "summarize us in ChatGPT/Claude/Perplexity" entry points. Chrome 150's declarative `focusgroup` also improves keyboard and agent-readable composite widgets (Chrome only). [63]
- **Seen in:** Wispr Flow (AI-summary buttons) [49]; Chrome WebMCP early preview → origin trial [20][21]. Per Webflow's 2026 report summary, 52% of marketing leaders plan to prioritize AI-search optimization. [56]
- **Fits:** e-commerce, booking, SaaS settings and forms, documentation.
- **Avoid when:** the visit itself is the product, or flows are regulated or competitively sensitive. WebMCP is not on the W3C standards track and its API will change. [27][21]
- **Implement:** Semantic landmarks and headings, no icon-only buttons without accessible names, no "click here", standard form patterns with `autocomplete` tokens. Expose structured actions via APIs/MCP. Pilot WebMCP's declarative and imperative tool APIs behind the origin trial. Test with the accessibility tree. [27][20][21]
- **Sources:** [27], [20], [21], [49], [56], [63]

### web-calm-dense-saas-ui — Calm density in SaaS (Linear-style), keyboard-first
- **Status:** mainstream
- **Momentum:** →
- **What:** Pro tools keep high density while removing visual noise: dimmed navigation chrome, fewer and softer dividers, smaller icons, warmer neutral surfaces, and a ⌘K palette as the universal entry point.
- **Seen in:** Linear's March 2026 refresh (dimmed sidebar, compact tabs, softer separators, themes from 3 inputs) [35]; GitHub command palette, kept after pushback [55].
- **Fits:** productivity, dev tools, PM, CRM, analytics, admin consoles.
- **Avoid when:** novice or occasional users need visible affordances. Low-contrast separators must still meet 1.4.11 where they convey meaning. Targets stay ≥ 24×24 px (2.5.8). [23]
- **Implement:** Spacing and surface steps (OKLCH L ±2–4%) instead of 1 px borders everywhere. Nav at reduced emphasis. Icon-only tabs need `aria-label` plus tooltips. ⌘K as `<dialog>` with an APG combobox/listbox, mirrored in visible menus. Toolbars can use Chrome 150 `focusgroup` where available, else roving tabindex. Ship changes behind feature flags. [35][55][63]
- **Sources:** [35], [55], [23], [36], [63]

## Fading — now looks dated
- **The first-wave "AI default" landing page** — indigo-to-violet gradient blob, Inter for everything, centred hero with pill badge and two buttons, three identical emoji cards, the same fade-up on every section. Adam Wathan apologized in August 2025 for making Tailwind UI buttons indigo, often cited as a root of the purple default. [52][53][54]
- **Copy-paste bento grids** — stock cards in a varied grid with no hierarchy. The critique now targets execution. [51]
- **Decade-long neo-grotesk "blanding"** — uniform sans identities are giving way to character type. [40]
- **Cool blue-gray neutrals and glaring pure white** — leaders are moving warmer. [35][39][38]
- **Purposeless glassmorphism and glow** — blurred panels with no function appear on lists of AI-generated tells. [54]
- **Generic "Loading…" spinners and binary "failed" errors in AI features** — users expect specific status and partial-success messaging. [30]
- **Chat as the only AI interface inside products** — task-oriented controls beat a lone message box. Builder landing pages are the exception. [31][28]
- **JS scroll-listener animations and positioning libraries for simple overlays** — scroll-driven animations (now all engines) and popover/anchor positioning replace them. [18][14][10][17]
- **Legacy `grid-template-rows: masonry` syntax** — Firefox 159 removed it (it was Nightly-only) in favor of `display: grid-lanes`. [18]

## Watchlist — verify next month
- Scroll-driven animations: Firefox 159 ships them by default (confirmed in MDN release notes). Confirm webstatus.dev shows Baseline newly available. [18][10]
- Grid lanes (masonry): Firefox 159 notes name `display: grid-lanes` / `inline-grid-lanes` as the replacement for the legacy syntax, and Safari 27 Web Inspector shows Grid-Lanes badges. No engine confirmed shipping `grid-lanes` by default (unverified). [18][12][10]
- Firefox appears to have moved to a ~2-week release cadence (per release calendar). Faster Baseline movement is plausible (unverified: no announcement seen). [62]
- Customizable `<select>` (`appearance: base-select`, `::picker(select)`) is in Chrome 135+ and Safari 27, and behind a flag in Firefox 149. Watch for Firefox shipping. [12][11]
- Cross-document view transitions in Firefox (Interop 2026 focus area; not implemented). [13][16]
- Chrome 150 `focusgroup`, `background-clip: border-area`, `text-fit`: Chrome-only; watch other engines (early). [63]
- `popover="hint"`, interest invokers (`interestfor`, Chrome only), dialog `closedby`: hover cards and light-dismiss going native (early). [10][14]
- `corner-shape` (Chrome 139), `@function`/`if()` (Chrome only), CSS gap decorations (Chrome 149) (early). [11][15]
- Safari 27 ships the `<model>` element (3D embeds), which could change e-commerce 3D viewers (early). [12]
- WebMCP general availability timing: third-party claim of mid-to-late 2026 (unverified). [21]
- A claim that Google lowered the INP "good" threshold to 150 ms in 2026 (unverified; web.dev says 200 ms). [22]
- "Second-wave AI tells" (cream plus terracotta, near-black with acid green, broadsheet hairlines, mono microcopy) may become the next dated look (single source). [54]
- Liquid/fluid glass on the web after Apple's Liquid Glass: Awwwards "Fluid Glass" case study (2026-05-06); scope unclear (unverified as a trend). [47]
- A claim that immersive 3D was 61% of Awwwards SOTD winners in Q1 2026 (unverified third-party stat; not cited above).
- The Sep 2026 Baseline digest URL (web.dev/blog/baseline-digest-sep-2026) returned 404 at time of research; check again for the September edition.
- Land-book, Lapa Ninja and SiteInspire returned 403 or bot walls to automated fetches earlier. Galleries not reviewed (gap).
- Monotype's 2026 Type Trends report was not located (unverified for 2026).
- EN 301 549 revision (due 2026), Dutch ACM formal EAA enforcement (expected H2 2026), Carrefour's six-month deadline (~Dec 2026). [25]
- Interop 2027: proposals closed 2026-09-23. Final focus areas are expected around early February 2027 and none were announced as of 2026-11-01. [60]

## Sources
1. [December 2025 Baseline monthly digest](https://web.dev/blog/baseline-digest-dec-2025) — web.dev, 2026-01-26
2. [January 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-jan-2026) — web.dev, 2026-03-02
3. [February 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-feb-2026) — web.dev, 2026-03-30
4. [March 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-mar-2026) — web.dev, 2026-04-14
5. [April 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-apr-2026) — web.dev, 2026-05-27
6. [May 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-may-2026) — web.dev, 2026-06-03
7. [June 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-jun-2026) — web.dev (Jeremy Wagner), 2026-07-17
8. [July 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-jul-2026) — web.dev, 2026-08-10
9. [August 2026 Baseline monthly digest](https://web.dev/blog/baseline-digest-aug-2026) — web.dev, 2026-09-28
10. [Web Platform Status (anchor-positioning, view-transitions, scroll-driven-animations, customizable-select, field-sizing, contrast-color, etc.)](https://webstatus.dev/) — Google / WebDX CG, 2026-10-18 (accessed; not re-checked after Firefox 159)
11. [MDN browser-compat-data](https://github.com/mdn/browser-compat-data) — MDN / Open Web Docs, 2026-10-18 (accessed)
12. [WebKit Features for Safari 27.0](https://webkit.org/blog/18325/webkit-features-for-safari-27-0/) — WebKit, 2026-09-17
13. [Announcing Interop 2026](https://webkit.org/blog/17818/announcing-interop-2026/) — WebKit (Yulun Wu, Jen Simmons), 2026-02-12
14. [Launching Interop 2026](https://hacks.mozilla.org/2026/02/launching-interop-2026/) — Mozilla Hacks (Jake Archibald), 2026-02-12
15. [What's new in web UI (Google I/O 2026)](https://developer.chrome.com/blog/new-in-web-ui-io26) — Chrome for Developers (Bramus, Una Kravets), 2026-07-01
16. [Cross-document view transitions for multi-page applications](https://developer.chrome.com/docs/web-platform/view-transitions/cross-document) — Chrome for Developers, 2024-04-14 (last updated)
17. [Firefox 147 release notes for developers](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/147) — MDN, 2026-01-13
18. [Firefox 159 release notes for developers](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/159) — MDN, 2026-10-27
19. [WebKit Features in Safari 26.0](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/) — WebKit, 2025-09-15
20. [WebMCP is available for early preview](https://developer.chrome.com/blog/webmcp-epp) — Chrome for Developers, 2026-02-10
21. [WebMCP origin trial (Chrome 149)](https://developer.chrome.com/blog/ai-webmcp-origin-trial) — Chrome for Developers, 2026-06-09
22. [Interaction to Next Paint (INP)](https://web.dev/articles/inp) — web.dev, 2025-09-02 (last updated)
23. [What's New in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/) — W3C WAI, 2023-10-05
24. [WCAG 3 Introduction](https://www.w3.org/WAI/standards-guidelines/wcag/wcag3-intro/) — W3C WAI, 2026-09-25 (updated)
25. [EAA compliance in 2026: how enforcement has evolved and what to expect next](https://www.levelaccess.com/blog/eaa-compliance-in-2026-how-enforcement-has-evolved-and-what-to-expect-next/) — Level Access (Carolina Souza), 2026-06-19
26. [State of UX 2026: Design Deeper to Differentiate](https://www.nngroup.com/articles/state-of-ux-2026/) — Nielsen Norman Group, 2026-01-16
27. [AI Agents as Users](https://www.nngroup.com/articles/ai-agents-as-users/) — Nielsen Norman Group (Sarah Gibbons, Kate Moran), 2026-04-10
28. [Designing AI Agents: 4 Lessons from China's Qwen Agent](https://www.nngroup.com/articles/designing-ai-agents/) — Nielsen Norman Group (Feifei Liu, Maria Rosala), 2026-05-08
29. [Designing For Agentic AI: Practical UX Patterns For Control, Consent, And Accountability](https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/) — Smashing Magazine (Victor Yocco), 2026-02-11
30. [Practical Interface Patterns For AI Transparency (Part 2)](https://www.smashingmagazine.com/2026/05/practical-interface-patterns-ai-transparency/) — Smashing Magazine (Victor Yocco), 2026-05-13
31. [Design Patterns For AI Interfaces](https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/) — Smashing Magazine (Vitaly Friedman), 2025-07-14
32. [Generative UI: A rich, custom, visual interactive user experience for any prompt](https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/) — Google Research, 2025-11-18
33. [MCP Apps are here: Rendering interactive UIs in AI clients](https://workos.com/blog/2026-01-27-mcp-apps) — WorkOS (Maria Paktiti), 2026-01-27
34. [Config 2026 recap](https://www.figma.com/blog/config-2026-recap/) — Figma, 2026-06-24
35. [Behind the latest design refresh](https://linear.app/now/behind-the-latest-design-refresh) — Linear (Charlie Aufmann, Maxime Heckel), 2026-03-12
36. [Linear homepage](https://linear.app/) — Linear, 2026-10-18 (accessed)
37. [Tailwind CSS v4.0](https://tailwindcss.com/blog/tailwindcss-v4) — Tailwind Labs, 2025-01-22
38. [Tailwind CSS v4.3: Scrollbars, new colors, and more](https://tailwindcss.com/blog/tailwindcss-v4-3) — Tailwind Labs, 2026-05-08
39. [Pantone names its 2026 Color of the Year: Cloud Dancer](https://www.nbcnews.com/pop-culture/pop-culture-news/pantone-names-2026-color-year-rcna247366) — NBC News, 2025-12-04
40. [Breaking rules and bringing joy: top typography trends for 2026](https://www.creativebloq.com/design/fonts-typography/breaking-rules-and-bringing-joy-top-typography-trends-for-2026) — Creative Bloq (Tom May), 2025-12-28
41. [Texture, warmth and tactile rebellion: the big graphic design trends for 2026](https://www.creativebloq.com/design/graphic-design/texture-warmth-and-tactile-rebellion-the-big-graphic-design-trends-for-2026) — Creative Bloq (Tom May), 2025-12-23
42. [Annual Awards — Winners (2025)](https://www.awwwards.com/annual-awards/winners) — Awwwards, 2026-10-18 (accessed)
43. [Sites of the Month](https://www.awwwards.com/websites/sites_of_the_month/) — Awwwards, 2026-11-01 (accessed)
44. [Ai in Design Report 2026 — Site of the Day](https://www.awwwards.com/sites/ai-in-design-report-2026) — Awwwards, 2026-08-26
45. [Oryzo AI — Site of the Day](https://www.awwwards.com/sites/oryzo-ai) — Awwwards, 2026-04-13
46. [Why Zero — Site of the Day](https://www.awwwards.com/sites/why-zero) — Awwwards, 2026-09-07
47. [Awwwards Blog (Fluid Glass case study 2026-05-06; GQ & Audemars Piguet 2026-06-03)](https://www.awwwards.com/blog/) — Awwwards, 2026-10-18 (accessed)
48. [8 Best Three.js Websites of 2026, Technique by Technique](https://www.utsubo.com/blog/best-threejs-websites-2026) — Utsubo (Jocelyn Lecamus), 2026-09-24 (updated)
49. [Deep: Homepage UX Explored](https://departmentofproduct.substack.com/p/deep-homepage-ux-explored) — Department of Product (Rich Holmes), 2026-03-09
50. [State of the Interactive Product Demo 2026](https://www.navattic.com/report/state-of-the-interactive-product-demo-2026) — Navattic, 2026-10-18 (accessed)
51. [Designing Bento Grids That Actually Work: A 2026 Practical Guide](https://www.saasframe.io/blog/designing-bento-grids-that-actually-work-a-2026-practical-guide) — SaaSFrame, 2026-10-18 (accessed)
52. [How to fix a generic AI landing page](https://superdesign.dev/blog/fix-generic-ai-landing-page) — SuperDesign (Jason Zhou), 2026-07-13
53. [Why Your AI Keeps Building the Same Purple Gradient Website](https://prg.sh/ramblings/Why-Your-AI-Keeps-Building-the-Same-Purple-Gradient-Website) — prg.sh, 2025-10-26
54. [How to Fix AI Slop in Web Design, Tell by Tell](https://capitalandcompute.net/blog/fix-ai-slop-design/) — Capital & Compute, 2026-09-25
55. [Pausing the deprecation of GitHub Command Palette (changelog)](https://github.blog/changelog/2025-07-16-upcoming-deprecation-of-github-command-palette-feature-preview) — GitHub, 2025-07-16
56. [The 2026 State of the Website](https://webflow.com/resources/reports/2026-state-of-the-website) — Webflow / Vanson Bourne, 2026-10-18 (accessed)
57. [Bolt homepage](https://bolt.new/) — StackBlitz, 2026-10-18 (accessed)
58. [Replit homepage](https://replit.com/) — Replit, 2026-10-18 (accessed)
59. [Figma Make](https://www.figma.com/make/) — Figma, 2026-10-18 (accessed)
60. [Submit your ideas for Interop 2027](https://webkit.org/blog/18283/submit-your-ideas-for-interop-2027/) — WebKit (Yulun Wu), 2026-09-03
61. [Recent — Design Inspiration (godly.website 301 target)](https://recent.design/) — Recent, 2026-10-18 (accessed)
62. [Firefox release calendar](https://whattrainisitnow.com/) — Mozilla Release Management, 2026-10-18 (accessed)
63. [New in Chrome 150](https://developer.chrome.com/blog/new-in-chrome-150) — Chrome for Developers, 2026-06-30
