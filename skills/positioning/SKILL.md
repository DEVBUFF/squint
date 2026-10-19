---
name: positioning
description: A product positioning and brand strategy session. Covers competitive alternatives, unique value, target customer, category, messaging hierarchy, headlines, App Store / Google Play listing and tone of voice, grounded in competitor research and the branding trend base. Proposes first and edits copy only after approval.
when_to_use: The user asks about positioning, messaging, offer, landing copy, store listing, naming, tone of voice or whether to rebrand. Examples - "help me position the product", "rewrite our hero", "improve the App Store page", "помоги с позиционированием", "перепиши оффер", "как нас отличить от конкурентов", "нужен ли ребрендинг".
argument-hint: "[statement | landing | store | voice | naming | rebrand]"
allowed-tools:
  - Bash(python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py" *)
  - Read
  - Glob
  - Grep
  - Write
  - WebSearch
  - WebFetch
  - Agent
---

# Positioning and brand strategy

Helper: `python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py"` (`sq`). Focus: `$ARGUMENTS` (empty = full session).

1. **Context.** Read `${CLAUDE_PLUGIN_ROOT}/knowledge/guidelines/positioning.md` and
   `brand-identity.md`. Get the newest branding trends with `sq trends --platform branding`. Read
   `.squint/brief.md`. If it is missing or a draft, fill it from the code and ask only the gaps,
   as in the audit skill. Collect the shipped copy: README, landing hero, onboarding, paywall and store
   metadata (`sq detect` → `positioning_files`, `store_metadata`).
2. **Research.** Spawn the `brand-strategist` agent, or do it yourself. Cover 3–6 competitors and
   alternatives: headline and category claim, pricing model, visual style (screenshots via the browser
   MCP), and review mining (what users praise and complain about). Search competitors on Exa
   (`mcp__plugin_squint_exa__*`) or WebSearch.
3. **Diagnose.** Run the 5-second test on the current hero or store page, write today's implicit
   positioning in one sentence, and list its gaps.
4. **Options.** Work through the positioning sequence and present **2–3 distinct positioning
   options** (different target or category), each with the statement, headline, the proof it needs and
   its risk. Recommend one and explain why.
5. **Deliverable** → `.squint/positioning/<date>.md`, containing:
   - the canvas (alternatives → attributes → value → target → category)
   - the statement
   - the messaging hierarchy
   - 5 headline + subhead pairs
   - CTAs
   - for mobile: store name and subtitle (30/30 iOS) or title and short description (30/80 Play), plus
     captions for the first 3 screenshots
   - voice attributes ("this, not that") with before → after rewrites of the product's real copy
   For the web hero, you can add a before/after section built from `templates/concepts.html`.
6. **Present, then stop.** Give the recommendation and the options briefly, and link the file. Copy
   changes in the product follow the `apply` flow: list them as R-items in the positioning file and
   wait for the user's approval.
