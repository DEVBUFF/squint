# Trend file format

Every monthly research run writes `<YYYY-MM>/{web,ios,android,branding}.md` plus `summary.md`.
The plugin reads these files and compares them month to month, so keep the structure exact.

Rules
- **Trend ids are stable** kebab-case with a prefix: `web-`, `ios-`, `and-`, `brand-`. Reuse last
  month's id when a trend continues; only rename if the trend really changed.
- **Momentum** compares with the previous period: `new`, `↑` (gaining), `→` (steady), `↓` (losing).
  A trend that fades out moves to "Fading" with a one-line reason instead of silently disappearing.
- **Status**: `emerging` (a few leaders) → `rising` (spreading in good products) → `mainstream`
  (expected) → `peaking` (overused, risk of looking generic) → `fading` (starting to look dated).
- Every claim needs a dated source. Prefer primary sources (platform vendors, standards bodies,
  the studio that did the work). Unverifiable signals go to Watchlist marked `unverified`.
- Never invent products, APIs, rebrands or dates.

```markdown
---
platform: ios            # web | ios | android | branding
period: 2026-10
researched_at: 2026-10-18
previous: 2026-09        # null on first run
sources: 24
---

# iOS — UI/UX trends · October 2026

## TL;DR
- 5–7 most actionable shifts, one line each.

## Platform baseline (expected now, not a trend)
- **<thing>** — what + why it matters for a product shipping now. [n]

## Trends

### ios-<trend-id> — <Human name>
- **Status:** emerging | rising | mainstream | peaking | fading
- **Momentum:** new | ↑ | → | ↓
- **What:** 1–3 sentences.
- **Seen in:** 2–5 named real products/brands.
- **Fits:** product types / audiences where it works.
- **Avoid when:** risks, a11y/perf costs, where it hurts.
- **Implement:** concrete — APIs, token values, patterns.
- **Sources:** [n], [m]

## Fading — now looks dated
- **<thing>** — why. [n]

## Watchlist — verify next month
- <signal> (unverified / early)

## Sources
1. [Title](url) — Publisher, YYYY-MM-DD
```

`summary.md` (cross-platform digest, ≤ 120 lines):

```markdown
---
period: 2026-10
researched_at: 2026-10-18
---

# Design trends digest · October 2026

## The month in five lines
## What changed since last month   (new / promoted / demoted / faded, per platform, with ids)
## Cross-platform themes            (trends that show up on 2+ platforms)
## Safe bets vs. risky bets         (mainstream-and-useful vs. peaking-and-generic)
## Positioning & branding signals
```
