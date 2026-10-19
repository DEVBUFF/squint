---
name: research
description: Monthly design-trend research for UI/UX (web, iOS, Android) and branding/positioning. Runs parallel trend-scout agents with web search, compares the findings with last month (momentum, new, fading), and writes the dated trend base that audits use.
when_to_use: Monthly refresh, when the trend base is stale (older than 35 days), or when the user asks about current trends. Examples - "/squint:research", "update the design trends", "what's trending in UI right now", "обнови тренды", "собери актуальные тренды", "что сейчас в тренде в дизайне".
argument-hint: "[web,ios,android,branding] [--repo] [--period YYYY-MM] [--force]"
allowed-tools:
  - Bash(python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py" *)
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - WebSearch
  - WebFetch
  - Agent
---

# Monthly trend research

Helper: `python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py"` (`sq`). Arguments: `$ARGUMENTS`.

1. **Target.** Run `sq research` (add `--repo` only when `$ARGUMENTS` contains `--repo`; maintainers
   and CI use it to update the shipped base; pass `--period` if given). It prints the target dir, the
   previous file for each platform, the format spec and the sources list. Read
   `knowledge/trends/FORMAT.md` and `knowledge/sources.md`.
   If this period's files already exist and are under 7 days old, ask whether to redo them or only
   refresh what changed. In non-interactive runs, refresh what changed. With `--force` in the
   arguments, always run the scouts and refresh every requested platform in place, whatever its age.
2. **Scout in parallel.** Platforms are exactly the comma list in `$ARGUMENTS` (for example `branding`
   means only branding). Only when no platform is named, use `web, ios, android, branding`. Ignore
   `update_in_place` when choosing platforms; it only tells you which files to refresh.
   Spawn one `trend-scout` agent per platform, all in one message, **in the foreground**
   (`run_in_background: false`). Wait for every scout before going on: in non-interactive runs (`claude
   -p`, CI) the session ends with your turn, which kills background agents. Give each:
   platform, period, today's date, output path, previous file path (or none), and the absolute paths
   of FORMAT.md and sources.md. For platforms listed in `update_in_place`, say explicitly that this is a
   same-period refresh of the existing file. If agents are unavailable, do the platforms one by one
   yourself with the same instructions.
3. **Check.** Run `sq check-trends <the written files>`. It verifies the front matter, sections,
   prefixed ids, status/momentum/sources fields and the source count. Also skim for invented products
   and undated sources. Make small fixes yourself. Send a scout back if its file is thin (fewer than 8 trends or fewer than 12 sources).
4. **Digest.** Write `summary.md` in the same folder, per FORMAT.md. Cover the month in five lines,
   what changed since last month (by id), cross-platform themes, safe versus risky bets, and
   positioning signals.
5. **Record.** Run `sq research --done` (with the same `--repo` / `--period` flags).
6. **Tell the user** (their language, ≤ 12 lines): the digest, the biggest changes, and, if the
   current project has a `.squint/brief.md`, the 2–3 trends most relevant to it and the ones to
   avoid. If monthly scheduling isn't set up yet (`sq status` shows no `last_research`, or this is a
   manual run), mention `/squint:setup` once.
