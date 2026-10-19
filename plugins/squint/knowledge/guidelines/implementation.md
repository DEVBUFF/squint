# Applying approved changes

The art director edits the product only after the user approved specific items (R-ids or a direction).

## Before the first edit
- Git: if the tree is clean, create `squint/<date>-<short-slug>`; if it is dirty, ask whether to
  continue on the current branch. Never commit unless the user asks.
- Re-read the approved items in the latest `report.md`; list the files each one touches.
- No new dependencies, fonts with commercial licences, or build-config changes without asking.

## Order of work
1. **Tokens** — colours, type scale, spacing, radii, shadows, motion durations. One change, everywhere.
2. **Components** — buttons, inputs, cards, navigation, list rows, sheets. Extend the existing system;
   don't fork it.
3. **Screens** — highest traffic / impact first.
4. **Copy & positioning** — headlines, CTAs, empty states, store metadata.

## Stack notes
- **Web**: CSS variables / Tailwind `@theme` or `theme.extend` / shadcn variables in `globals.css`;
  fonts via the framework loader (`next/font`) with fallbacks; check dark mode and focus styles.
- **SwiftUI**: colour assets with Any/Dark (+ High Contrast) appearances; `Font.custom(_:size:relativeTo:)`
  to keep Dynamic Type; shared `ButtonStyle`s / `ViewModifier`s instead of per-view styling; register
  fonts in `Info.plist` (`UIAppFonts`).
- **Compose**: `ColorScheme` / `Typography` / `Shapes` in `ui/theme`; keep dynamic colour as an
  option with a branded fallback; fonts in `res/font`.
- **Views (Android)**: `themes.xml`, `colors.xml`, `values-night/`.
- **React Native / Expo**: the theme module; `Platform.select` where platforms diverge.
- **Flutter**: `ThemeData` / `ColorScheme.fromSeed`, `CupertinoThemeData`.

## Hard limits
- Don't change business logic, data flow, analytics event names, API calls or tests' intent.
- Don't remove accessibility labels/traits; only improve them.
- Keep changes reviewable: one batch per approved group, summarised with file list.

## After each batch
1. Build / type-check / lint with the project's own commands.
2. Capture **after** screenshots with the same devices, viewports and states as **before**
   (`screens/after/`), and compare side by side.
3. Re-check contrast and target sizes of everything touched.
4. Update `report.md` status, append to `.squint/decisions.md`
   (`date · R# · decision · why · files`), and log taste feedback:
   `squint.py feedback --verdict accepted|rejected|modified --item "R#: …" --tags … --reason "…"`.
