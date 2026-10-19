# Android — platform guide

Stable principles from Material Design 3 and Android's app quality guidelines. For what changed
recently (current Material version, target-SDK deadlines, enforced behaviours) read the **Platform
baseline** section of the newest `knowledge/trends/<period>/android.md` — it overrides this file.

## Non-negotiables
- Touch targets ≥ 48×48 dp.
- Text in `sp`; layouts survive font scale up to 200%.
- Edge-to-edge drawing with correct insets (status bar, navigation bar, display cutouts, IME).
- System back and predictive back work everywhere; no custom back that fights the gesture.
- Light and dark themes; contrast 4.5:1 for text; TalkBack content descriptions and focus order.

## Material 3 foundations
- **Colour roles**: primary / onPrimary / primaryContainer / onPrimaryContainer, secondary, tertiary,
  error, surface + surface container levels, outline. Brand colours map onto roles — don't hard-code.
- **Dynamic colour** (wallpaper-based) where the brand allows; keep a branded fallback scheme.
- **Type scale**: Display L/M/S 57/45/36, Headline L/M/S 32/28/24, Title L/M/S 22/16/14,
  Body L/M/S 16/14/12, Label L/M/S 14/12/11 (sp).
- **Shape scale**: extra-small → extra-large corner families; use shape to signal hierarchy.
- **Spacing**: 4 dp base, 8 dp rhythm; 16 dp standard margins on compact screens.
- **Motion**: Material motion tokens / spring-based physics; respect "Remove animations".

## Navigation & structure
- Navigation bar for 3–5 top-level destinations on compact width; navigation rail on medium;
  rail or permanent drawer on expanded. Window size classes: compact < 600 dp, medium 600–840 dp,
  expanded > 840 dp (plus large / extra-large on desktop-class windows).
- Top app bar (small / medium / large, collapse on scroll); FAB for the single primary action.
- Bottom sheets for secondary content; dialogs only for interruptions that need a decision.
- Large screens / foldables: list-detail and supporting-pane layouts, no stretched phone UI.

## Components to prefer over custom
Material 3 Compose components (buttons and button groups, cards, chips, lists, search bar, date/time
pickers, snackbars, carousels, progress indicators), Photo Picker, Credential Manager, system share.

## System surfaces
Themed (monochrome) app icon layer, adaptive icons, widgets (Glance), notifications (with progress /
live-update styles where available), quick settings tiles, App Shortcuts.

## Where the design lives in code
- Compose: `ui/theme/Theme.kt`, `Color.kt`, `Type.kt`, `Shape.kt`; `MaterialTheme(colorScheme, typography, shapes)`;
  `res/font/`.
- Views: `res/values/colors.xml`, `themes.xml`, `styles.xml`, `res/values-night/`, `dimens.xml`.

## Capture & checks (emulator / device)
```bash
adb devices
adb shell settings put global sysui_demo_allowed 1
adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0941
adb shell cmd uimode night yes                     # dark theme; "no" to revert
adb shell settings put system font_scale 1.5       # font scale check; 1.0 to revert
adb exec-out screencap -p > screens/before/home.png
```
Build & run: `./gradlew installDebug` then `adb shell monkey -p <applicationId> 1`.
A mobile MCP (e.g. the `squint-devices` companion) can tap, swipe and screenshot through flows.
