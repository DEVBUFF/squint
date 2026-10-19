# Audit rubric

How the art director judges a product. Every score needs evidence; every recommendation needs a basis.

## Priority of signals (when they conflict, higher wins)
1. **The brief** — product goal, audience, constraints (`.squint/brief.md`).
2. **Accessibility & platform guidelines** — non-negotiable floor (see `platform-*.md`).
3. **Project moodboard** — references the user collected for *this* product.
4. **Global taste profile** — the user's general taste (`~/.squint/taste/profile.md`).
5. **Current trends** — used selectively; a trend is a tool, never a goal.

## Score anchors (1–5)
| Score | Meaning |
|---|---|
| 1 | Broken or missing — blocks users, violates guidelines |
| 2 | Works but generic or inconsistent; several clear problems |
| 3 | Solid and conventional; a few real issues |
| 4 | Polished and consistent; only minor issues |
| 5 | Distinctive and best-in-class for its category |

Half points are fine. Never give 5 without naming what makes it distinctive.

## Areas and what to check

### UX — flows, friction, states
- Key flows end to end: first run / onboarding, the core job, paywall / checkout / signup, settings, recovery.
- Friction: count steps, fields, decisions and waits per flow. Name each removable one.
- Nielsen's 10 heuristics — especially visibility of status, match with the real world, user control
  (undo, back, cancel), consistency, error prevention, recognition over recall.
- States for every data view: empty, loading (skeletons over spinners for content), error, offline,
  partial, success. Missing states are findings.
- Permission and notification prompts are primed (explain value before the system dialog).
- Information architecture: can a new user tell where they are and what to do next in 5 seconds?
- Forms: labels (not placeholder-only), correct input types / keyboards / autocomplete, inline validation.
- Perceived performance: optimistic UI, instant feedback < 100 ms, transitions that explain change.

### UI — visual craft
- Hierarchy: one primary action per screen; scan path is obvious; size/weight/colour used deliberately.
- Typography: a real scale (consistent ratio), ≤ 2 families, readable line length (45–75 ch on web),
  body ≥ 16 px web / platform text styles on mobile, sensible weights and tracking.
- Colour: roles (background, surface, text, accent, semantic), accent discipline (accent = action),
  dark mode quality (not just inverted), no colour-only meaning.
- Spacing: one base unit (4 or 8), consistent rhythm, generous where the brand wants calm.
- Consistency: count distinct button styles, radii, shadows, font sizes and hard-coded colours
  (`squint.py scan` gives the numbers). More variants than roles = design-system debt.
- Iconography: one family, consistent stroke/fill and optical size.
- Imagery: quality, consistent treatment, meaningful (not decorative stock).
- Motion: purposeful (explains change, gives feedback), 150–300 ms for UI, respects Reduce Motion.
- Craft details: alignment, optical centring, truncation, widows, pixel-snapping, icon/text baseline.

### Accessibility
- Contrast: text 4.5:1 (large text 3:1), UI components and focus indicators 3:1.
- Targets: iOS 44×44 pt, Android 48×48 dp, web ≥ 24×24 CSS px (WCAG 2.2) — 44 recommended.
- Text scaling: Dynamic Type / font scale / browser zoom 200% without loss.
- Screen readers: labels, roles, order, grouped elements; images have alt or are decorative.
- Keyboard & focus on web: visible focus, logical order, no traps, skip link.
- Reduce Motion, Reduce Transparency, Increase Contrast respected.

### Platform fit
Use `platform-ios.md`, `platform-android.md`, `platform-web.md`, `platform-cross.md` and the
**Platform baseline** section of the newest trend file for the platform. Native conventions for
navigation, back behaviour, system controls, typography and haptics; brand lives in colour, content,
illustration and motion personality.

### Brand — distinctiveness & coherence
Use `brand-identity.md`. Would someone recognise the product with the logo covered? Is it the same
brand on every screen, the store listing, the site, the icon?

### Positioning & messaging
Use `positioning.md`. Can a stranger say what it is, who it is for and why it beats the alternative
after 5 seconds on the hero / store page?

## Severity
- **P0** — blocks users, breaks a platform requirement or accessibility floor.
- **P1** — clear loss of conversion, trust, retention or perceived quality.
- **P2** — noticeable polish or consistency problem.
- **P3** — nice to have.

## Evidence rules
- Every finding cites at least one of: `file:line`, a screenshot in `screens/before/`, a measured
  number (contrast ratio, count of variants, steps in a flow).
- Every recommendation cites at least one basis: **guideline**, **trend** (id + status + period),
  **taste** (a rule or signal from the profile / project moodboard), **heuristic / data**.
- Trend-based recommendations must pass the **fit test**:
  1. Does it serve the brief's goal?
  2. Does it suit this audience and category?
  3. Status `peaking` or `fading`? Then it risks looking generic or dated — say so or drop it.
  4. Cost: performance, accessibility, engineering effort, maintenance.
- Always include a "Deliberately not recommended" list — saying no to fashionable things is part of the job.

## Recommendation tiers
- **Quick wins** — ≤ 1 day, low risk, mostly tokens, copy, states, spacing, contrast.
- **Core** — component or flow changes, days, measurable impact.
- **Bold** — direction-level (identity, navigation model, positioning). Present as options, never apply
  without an explicit choice.
