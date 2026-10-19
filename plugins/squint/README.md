# Squint

A UI/UX and branding art director for Claude Code. It keeps up with design trends every month,
learns your taste from Pinterest boards and screenshots, and audits web, iOS and Android products.
It shows a plan with before/after concepts first and changes your product only after you approve.

| Command | What happens |
|---|---|
| `/squint:setup` | Tool check, optional connections, monthly schedule, first moodboard |
| `/squint:moodboard add <url\|path>` | Add Pinterest boards, links, screenshots or folders |
| `/squint:learn` | Study new references and rebuild your taste profile |
| `/squint:audit` | Full audit → `report.md` + `concepts.html` (does not edit the product) |
| `/squint:apply R1 R3` | Implement approved items, verified with after-screenshots |
| `/squint:positioning` | Positioning options, messaging, headlines, store listing, voice |
| `/squint:research` | Monthly design-trend research (web, iOS, Android, branding) |

Natural language works too: "analyse my project and suggest improvements", "проанализируй мой проект и дай улучшения".

Optional device tools (browser, iOS Simulator, Android emulator): `claude plugin install squint-devices@squint`.

Everything runs in your own Claude Code session. Your data stays in `~/.squint/` and
`<project>/.squint/`.

- Full documentation: https://github.com/DEVBUFF/squint
- Privacy policy: https://github.com/DEVBUFF/squint/blob/main/PRIVACY.md
- License: MIT
