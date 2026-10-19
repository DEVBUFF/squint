---
name: apply
description: Implement design changes the user approved from a Squint audit (R-ids, "quick wins" or a chosen direction). Works tokens first, then components, screens and copy, and verifies every batch with after-screenshots.
when_to_use: After an audit, when the user approves items. Examples - "apply R1 R3", "go with direction B", "do the quick wins", "делай 1, 3 и 5", "внедряй", "давай квик вины", "применяй направление B". Also when they ask to implement a specific recommendation from .squint/audits.
argument-hint: "R1 R3 | quick wins | direction B"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(python3 *)
  - Bash(git status*)
  - Bash(git switch*)
  - Bash(git checkout -b*)
  - Bash(git diff*)
  - Bash(xcrun simctl *)
  - Bash(adb *)
---

# Apply approved design changes

Helper: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/squint.py"` (`sq`). Approved scope: `$ARGUMENTS`.

1. **Resolve the scope.** `sq latest-audit` gives you the report path. Read `report.md`. Map the
   request to exact R-ids ("quick wins" means every R in that section, "direction B" means the B row
   plus the R-items tied to it). If the mapping isn't obvious, confirm it in one line before you edit.
   When the user rejects or reshapes an item, log it now:
   `sq feedback --verdict rejected|modified --item "R#: …" --tags … --reason "…"`.
2. **Prepare.** Read `${CLAUDE_PLUGIN_ROOT}/knowledge/guidelines/implementation.md` and follow its git
   and dependency rules (branch on a clean tree, ask on a dirty one, never commit unless asked, no new
   dependencies or commercial fonts without asking). Note the "before" screenshots that belong to
   each R.
3. **Implement in batches**: tokens → components → screens → copy. Keep the task list current. Extend
   the existing design system rather than forking it. Never change business logic, analytics,
   API calls or the intent of tests.
4. **Verify each batch.**
   - Run the project's own build, type-check and lint.
   - Take "after" screenshots with the same device, viewport, theme and state as "before", saved
     under the same names in `screens/after/`. Use the browser MCP / `sq capture url` for web, and
     `sq capture ios|android` plus the mobile MCP for apps.
   - Look at each before/after pair. Fix regressions before you move on.
   - Re-check contrast and target sizes for everything you touched.
5. **Record.**
   - In `report.md`, mark each R as `✅ applied`, `⚠ partial — <why>` or `⏭ skipped — <why>`, and update
     `status:` in the front matter.
   - Append to `.squint/decisions.md`: `YYYY-MM-DD · R# · applied/modified · why · files`.
   - For every applied item, run `sq feedback --verdict accepted --item "R#: <title>" --tags <tags>`.
     Tags name the design move (e.g. `serif-headlines,accent-discipline,bento,glass,dense-layout`),
     because `learn` aggregates them into the taste profile.
6. **Report** in the user's language: what changed per R (with files), the before → after screenshot
   pairs, anything not done and why, how to revert (branch / `git diff`), and the 2–3 best next items.
