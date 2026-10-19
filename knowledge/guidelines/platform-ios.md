# iOS / iPadOS — platform guide

Stable principles from Apple's Human Interface Guidelines. For what changed recently (current OS
design language, SDK deadlines, new APIs) read the **Platform baseline** section of the newest
`knowledge/trends/<period>/ios.md` — it overrides anything here that is out of date.

## Non-negotiables
- Hit targets ≥ 44×44 pt. Spacing between targets so they can't be mis-tapped.
- Support **Dynamic Type**: use text styles (`.font(.body)`, `.title`, …) or
  `.font(.custom(name, size:, relativeTo:))`; layouts must survive the accessibility sizes.
- Semantic colours (`Color.primary`, `.secondary`, `Color(.systemBackground)`, …) or colour assets with
  Any/Dark (and High Contrast) appearances. Test light, dark, Increase Contrast, Reduce Transparency.
- Respect safe areas, the Dynamic Island / notch and the home indicator.
- Respect Reduce Motion (`@Environment(\.accessibilityReduceMotion)`) and VoiceOver labels/traits.

## Typography
- San Francisco (SF Pro / SF Pro Rounded / New York / SF Mono) is the native voice. A brand typeface
  is fine for display/headlines; keep body text readable and scalable.
- Default text styles (large-size defaults): Large Title 34, Title 1 28, Title 2 22, Title 3 20,
  Headline 17 semibold, Body 17, Callout 16, Subheadline 15, Footnote 13, Caption 1 12, Caption 2 11.

## Navigation & structure
- **Tab bar** for top-level sections (typically 3–5). Don't hide primary navigation in a hamburger.
- **Navigation stack** for hierarchy; large titles on top-level screens; swipe-back must keep working.
- **Sheets** (with detents) for focused sub-tasks; full-screen covers only for immersive flows.
- **Toolbars** for actions on the current screen; context menus and swipe actions for shortcuts.
- Search: system search field / `.searchable`.
- iPad: sidebars / split views, pointer and keyboard support, multitasking sizes.

## Components to prefer over custom
Lists/Forms, toggles, pickers, date pickers, menus, segmented controls, share sheet, PhotosPicker,
Sign in with Apple, Apple Pay, system alerts/confirmation dialogs. Custom controls must match their
accessibility and feel (haptics, states, VoiceOver).

## Feel
- Haptics via `.sensoryFeedback(...)` (SwiftUI) / `UIFeedbackGenerator` — on meaningful events only.
- Motion: springs, interruptible, origin-aware (zoom transitions from the tapped element).
- SF Symbols for icons; match symbol weight to adjacent text weight.

## App icon & system surfaces
- One simple, recognisable silhouette that reads at small sizes; no text, no photos.
- Check every icon appearance the current iOS supports (see trends baseline).
- Widgets, Live Activities, Controls, App Shortcuts / App Intents and notifications are part of the
  product surface — audit them when present.

## Where the design lives in code
- SwiftUI: `Assets.xcassets/*.colorset`, `extension Color` / `ShapeStyle`, `Theme.swift`,
  `Font+*.swift`, custom `ViewModifier`s and `ButtonStyle`s, `Info.plist` (`UIAppFonts`).
- UIKit: `UIColor(named:)`, appearance proxies, storyboards/xibs.

## Capture & checks (Simulator)
```bash
xcrun simctl list devices booted
xcrun simctl status_bar booted override --time 9:41 --batteryState charged --batteryLevel 100 --cellularBars 4
xcrun simctl ui booted appearance dark            # or light
xcrun simctl ui booted content_size accessibility-extra-large   # Dynamic Type check; reset: large
xcrun simctl io booted screenshot screens/before/home.png
```
Build & run: `xcodebuild -scheme <Scheme> -destination 'platform=iOS Simulator,name=<device>' build`,
then `xcrun simctl install booted <App.app>` and `xcrun simctl launch booted <bundle id>`.
The bundled **mobile MCP** can tap, swipe and screenshot through flows.
