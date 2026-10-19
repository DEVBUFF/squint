# Cross-platform apps (React Native / Expo, Flutter, Compose Multiplatform, KMP)

## The rule
**Brand-consistent core, platform-native shell.**
- Native per platform: navigation model, back behaviour, system controls (pickers, switches, sheets,
  menus), typography defaults, haptics, permission flows, icon conventions, store listing.
- Shared brand: colour, illustration, photography, content, voice, motion *personality*, key moments
  (onboarding, empty states, success).
- When the team deliberately ships one identical UI on both platforms, still fix the platform
  violations users feel immediately: Android back, iOS swipe-back, safe areas/insets, target sizes,
  text scaling, date/time pickers, share sheets.

Audit both platforms separately (iOS and Android trend files + platform guides) and report where they
should diverge.

## React Native / Expo
- Theme in a `theme.ts` / design-system package, NativeWind/Tailwind config, Tamagui, Restyle,
  react-native-paper (Material) or similar — find it with `squint.py detect` (token files).
- `Platform.select` / `.ios.tsx` / `.android.tsx` files for divergence.
- Prefer native-backed navigation (native stack, native tabs) so platform chrome follows the OS
  design language automatically; check the iOS/Android trend files for the current native-tabs and
  material/glass support in Expo / React Navigation.
- Capture: Expo dev build on Simulator / emulator → `squint.py capture ios|android` or the mobile MCP.

## Flutter
- `ThemeData` (Material 3 `ColorScheme.fromSeed`), `CupertinoThemeData`, `theme.dart`, `app_theme.dart`.
- Adaptive widgets (`Switch.adaptive`, platform-aware page transitions) for native feel.
- Flutter draws its own pixels: new native design languages arrive late or need packages — check the
  trends files and say explicitly what is and isn't achievable.

## Compose Multiplatform / KMP
- Shared `MaterialTheme` by default; consider native iOS UI for the shell (SwiftUI) when iOS fit matters.

## Web + mobile in one product
Keep one token source (colours, type scale, radii, spacing) that compiles to CSS variables,
iOS colour assets and Android themes. Recommend it when the audit finds drift between platforms.
