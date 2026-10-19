# Privacy policy

_Last updated: 2026-10-19_

Squint is an open-source plugin for Claude Code. It has no server, no account and no analytics, and
its author receives no data from you.

## What stays on your computer
- **Your taste data**: moodboard sources, downloaded reference images, image analyses, your taste
  profile, feedback on recommendations and personal trend research. Stored in `~/.squint/` (or the
  folder you set with `SQUINT_HOME`).
- **Project data**: the product brief, audit reports, concept pages, screenshots and the decisions
  log. Stored in `<your project>/.squint/`. Reference images there are git-ignored by default.
- **Settings**: an optional local monthly schedule (`scripts/schedule.sh`) writes a launchd agent or
  cron entry on your machine and logs to `~/.squint/logs/`.

You can delete all of it at any time by removing those folders.

## What leaves your computer, and to whom
Only what you ask Squint to do, through the services below:

| Where it goes | What is sent | When |
|---|---|---|
| Anthropic (Claude) | Your prompts, the files Claude reads, screenshots and tool results, under **your** Claude account and Anthropic's terms | Every time you use Claude Code; Squint runs inside your own session |
| Exa (exa.ai) remote search MCP | Search queries about design trends and competitors | When research or positioning uses Exa search; no account or key is used |
| Pinterest | A request for the public RSS feed of boards you add, and the pin images in it | When you sync a Pinterest source |
| Websites you name | Normal page and image requests | When you add a URL to a moodboard or ask for a screenshot |
| Optional tools you connect yourself (Figma, Mobbin, Refero, Firecrawl, Are.na, the `squint-devices` companion) | What each tool needs to work, under that tool's own terms | Only after you install or connect them |

Squint does not sell, share or collect personal data, and it contains no tracking or telemetry. The
optional `squint-devices` companion starts its servers with usage statistics and telemetry disabled.

## Shared trend base
The trend files shipped with the plugin (`knowledge/trends/`) are researched by the maintainer and
contain only public, cited information about design trends. Nothing about users is included.

## Contact
Questions or requests: open an issue at https://github.com/DEVBUFF/squint/issues.
