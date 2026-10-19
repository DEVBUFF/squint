---
name: learn
description: Study new moodboard references. Looks at each image, extracts palette, type, layout, shape, mood and signature moves, then rebuilds the user's taste profile, also counting what they accepted or rejected in audits.
when_to_use: After a moodboard sync or inbox import, when references are pending, or when the user asks it to learn their taste. Examples - "learn from my references", "update my taste profile", "what's my style", "изучи мои референсы", "обучись на мудборде", "какой у меня вкус".
argument-hint: "[--project] [--rebuild]"
allowed-tools:
  - Bash(python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py" *)
  - Read
  - Write
  - Edit
  - Agent
---

# Learn the user's taste

Helper: `python3 "${CLAUDE_SKILL_DIR}/../../scripts/squint.py"` (`sq`). Arguments: `$ARGUMENTS`
(`--project` = the project store; `--rebuild` = rewrite the profile even if nothing is pending).

1. **Import** anything dropped into the inbox: `sq inbox` (and `sq inbox --project` inside a project).
2. **Batch**: `sq pending [--project] --limit 24` lists the files plus the analysis schema
   (`templates/reference-analysis.json`). Read the schema once.
3. **Analyse.**
   - For 12 or fewer items, do it yourself. Read each image, get exact colours with
     `sq palette <file>` when Pillow is installed (otherwise estimate them visually), and fill in the schema.
   - For more, spawn `reference-analyst` agents in parallel, about 12 items each. Give each the item
     list (id + absolute file path + title/tags), the schema path, and its own output path in the
     scratchpad.
   - Use `"skip"` for images with no design signal (memes, blurry photos, duplicates).
   - `like_why` is your best guess at why the user saved the image. `signature_moves` are reusable
     moves ("oversized serif numerals as section markers"), not descriptions ("a nice page").
4. **Save**: `sq annotate --file <batch.json> [--project]`. Repeat steps 2–4 until nothing is pending.
5. **Aggregate**: `sq stats` (use `--with-project` for a project profile that inherits the global one).
6. **Rewrite the profile** using `templates/taste-profile.md`: the global profile is
   `~/.squint/taste/profile.md` and the project one is `.squint/taste.md`.
   - Front matter: `updated: <today>`, `based_on: N references, M feedback events`.
   - "Strong signals" carry their percentages. Contradictions go under "Context splits" (by tag or
     board). Rejected audit items go under "Avoid".
   - End with 5–10 imperative **Rules for the art director**. Audits quote them as their basis, so
     make them concrete ("one accent colour, used only for primary actions").
   - Keep everything the user wrote by hand. If a line isn't explained by the stats, keep it under a
     "Your notes" heading. Never silently delete their edits.
7. **Tell the user** (their language, 5–8 lines) what you learned, what changed since the last
   profile, and the 3 most characteristic references by file path. Ask whether anything is wrong;
   their corrections are the strongest signal.
