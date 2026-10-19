# Contributing

Thanks for helping the art director keep good taste.

## Most useful contributions
- **Trend corrections.** If something in `plugins/squint/knowledge/trends/<period>/` is wrong, outdated or unsourced,
  open a PR that fixes the entry and cites a dated primary source.
- **Better sources.** Add feeds and coverage-checklist items to `plugins/squint/knowledge/sources.md`.
- **Platform guides.** Improvements to the stable principles in `plugins/squint/knowledge/guidelines/`.
- **Stack detection.** New frameworks in `plugins/squint/scripts/squint.py detect` / `scan` (with a test project if you can).

## Rules for trend content
- Follow [`knowledge/trends/FORMAT.md`](plugins/squint/knowledge/trends/FORMAT.md). Keep ids stable across months.
- Every claim needs a dated source, preferably primary (the vendor, the standards body, the studio).
- Never invent products, APIs, rebrands or dates. Uncertain signals go to the Watchlist marked
  `unverified`.
- Run `python3 plugins/squint/scripts/squint.py check-trends` before you push.

## Development
```bash
claude --plugin-dir plugins/squint           # load the plugin from your checkout
claude plugin validate . --strict           # marketplace
claude plugin validate plugins/squint --strict   # plugin
python3 plugins/squint/scripts/squint.py -h     # helper CLI (stdlib only)
SQUINT_HOME=/tmp/sqtest python3 plugins/squint/scripts/squint.py status   # isolated data dir for testing
```

The monthly research workflow runs on the maintainer's Claude subscription: `claude setup-token`, then
save the token as the `CLAUDE_CODE_OAUTH_TOKEN` repository secret. Forks can use their own token or
swap the input for `anthropic_api_key`. Merging its PR bumps the plugin version, which ships the update.
