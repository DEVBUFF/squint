---
name: setup
description: First-run setup and health check for the art director. Creates folders, checks capture tools (Chrome, Xcode Simulator, adb, Pillow, MCP servers), offers the squint-devices companion and optional design and research tools (Figma, Mobbin, Refero, Firecrawl), adds the first moodboard and schedules the monthly trend research.
when_to_use: First use of the plugin, or when the user asks to set it up, check status, connect tools or schedule research. Examples - "/squint:setup", "set up the art director", "schedule monthly trends", "настрой арт-директора", "подключи инструменты", "что у тебя подключено".
allowed-tools:
  - Bash(python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py" *)
  - Read
---

# Setup and health check

Helper: `python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py"` (`sq`).

1. **Folders and state.** Run `sq init`, then `sq status` and `sq capture devices`.
2. **Tools.** Show a compact table of what works and what doesn't:
   | Capability | Tool | Check |
   |---|---|---|
   | Web screenshots, device emulation, Lighthouse accessibility | `browser` MCP from the `squint-devices` companion | its tools are present; needs Google Chrome |
   | iOS Simulator + Android emulator | `mobile` MCP from the `squint-devices` companion | its tools are present; iOS needs Xcode, Android needs `adb` + an emulator |
   | Trend and competitor search | built-in WebSearch/WebFetch + the plugin's `exa` MCP (no key) | tools present |
   | Exact colour extraction | Pillow | `python3 -c "import PIL"` |
   | Fallback screenshots | Chrome binary | `sq capture devices` → `chrome` |
   If the device tools are missing, offer the companion (the user runs it; Node.js 20+ needed):
   `claude plugin install squint-devices@squint`, then restart Claude Code. Its first start downloads
   the packages via `npx` and can take a minute. Without it, `sq capture` (headless Chrome, `xcrun simctl`,
   `adb`) still covers screenshots.
3. **Optional connections.** Offer only the ones relevant to the user's stack, and print the command
   for the user to run. Never ask them to paste keys into the chat.
   - Figma (design files, variables, pushing UI into Figma):
     `claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp`, then `/mcp` →
     Authenticate. Skip this if a Figma plugin or server is already connected.
   - Mobbin (real app screens and flows, paid):
     `claude mcp add --scope user --transport http mobbin https://api.mobbin.com/mcp`
   - Refero (web and iOS references, paid):
     `claude mcp add --scope user --transport http refero https://api.refero.design/mcp`
   - Firecrawl (scrapes competitor sites, including their brand colours, fonts and logo; keyless tier):
     `claude mcp add --scope user --transport http firecrawl https://mcp.firecrawl.dev/v2/mcp`
   - Are.na (the user's own channels via their login):
     `claude mcp add --scope user --transport http arena https://mcp.are.na/mcp`
   - iOS builds from Claude: `claude mcp add mobilebuild -- npx -y mobilebuildmcp@latest mcp`
4. **Monthly research schedule.** Explain the three layers, then ask which one to set up:
   - **Shipped base.** The plugin's GitHub Action researches on the 1st of every month and publishes
     an update. Users get it with `claude plugin update squint@squint`, or with
     auto-update enabled in `/plugin` → Marketplaces.
   - **Personal base, local (recommended).** Runs on the 1st at 10:00 via launchd on macOS or cron on
     Linux, as `claude -p "/squint:research"`, with research tools pre-approved and nothing
     else. Show what `bash "${CLAUDE_PLUGIN_ROOT}/scripts/schedule.sh" install` will do, then run it
     only after a yes. Use `status` / `remove` / `run-now` for the other actions.
   - **Reminder only.** The session-start hook already offers a refresh when the base is over 35 days old.
5. **First moodboard.** Ask for Pinterest board URLs and/or a folder of screenshots. Then follow the
   `moodboard` skill, and open the inbox with `sq inbox --open`.
6. **Summary**: what is ready and what is optional. Then: "Try: *проанализируй мой проект и дай улучшения*".
