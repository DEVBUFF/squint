---
name: moodboard
description: Add inspiration the art director learns your taste from. Accepts Pinterest boards and profiles, Dribbble/Behance/website URLs, image URLs, screenshots and folders, either globally (your taste across all projects) or per project. Syncs new pins and imports the inbox folder.
when_to_use: The user shares a Pinterest, Dribbble, Behance or site link or screenshots of designs they like, or asks to add or sync a moodboard. Examples - "add my Pinterest board", "here's what I like", "sync my boards", "добавь мудборд", "вот что мне нравится", "закинул скрины", "синхронизируй доски".
argument-hint: "add <url|path> [--project] [--tags a,b] | sync | inbox | list | remove <id>"
allowed-tools:
  - Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/squint.py *)
  - Read
---

# Moodboard: collect references

Helper: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/squint.py` (`sq`). Request: `$ARGUMENTS`.

**Scope.** References are **global** by default: they teach the user's taste everywhere. Use
`--project` when the user says the references are for this product only ("for this app", "для этого
проекта"). Ask only when it is unclear and it matters.

| The user gives you | Do |
|---|---|
| Pinterest board or profile URL (any domain, pin.it short links too) | `sq source add <url> [--project] [--tags …]`, then `sq sync [--project] --source <id>` |
| Pinterest board with more than 25 pins | RSS returns only the newest 25 pins. With the user's OK, open the board in a browser MCP (e.g. the `squint-devices` companion), scroll a few times, run `[...document.images].map(i => i.src).filter(s => s.includes('i.pinimg.com'))`, then `sq add <urls…>`. Without a browser MCP, ask the user to save the pins they care about into the inbox. |
| Are.na channel | Are.na does not allow automated access, so it isn't synced. Offer its official MCP with the user's own login, or saving images into the inbox (`sq add` prints the details). |
| Image URL, Dribbble/Behance shot, website | `sq add <url> [--project] [--tags …]` (pages are saved as og:image plus a viewport screenshot) |
| Local files or folders, paths pasted in chat | `sq add <paths…> [--project] [--tags …] [--note "…"]` |
| "I'll drop screenshots somewhere" | `sq inbox --open [--project]`, which opens the folder (subfolders become tags), then `sq inbox` |
| Images pasted straight into the chat | You can see them but have no file. Describe what you notice, then ask the user to save them into the inbox so they persist (`sq inbox --open`). |
| sync | `sq sync [--project]` for every registered source |
| list / remove | `sq source list` / `sq source remove <id>` |

After adding, report the counts (found / new / pending) in one or two lines. Then continue straight
into the **learn** flow for the new items: run `/squint:learn`, or, for 12 or fewer items,
follow its steps inline. With more than 60 pending, ask before analysing them all.

Respect each site's terms. Collect for personal reference only and never redistribute downloaded
images. Reference files are git-ignored in project stores by default.
