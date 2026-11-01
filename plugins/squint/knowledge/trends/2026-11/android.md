---
platform: android
period: 2026-11
researched_at: 2026-11-01
previous: 2026-10
sources: 74
---

# Android — UI/UX trends · November 2026

## TL;DR
- Android Dev Summit (2026-10-28) put adaptive and agentic UI front and centre. Compose 1.13 (1.13.0-beta02, 2026-10-21) brings Grid and FlexBox to stable, plus Progressive Blur and Formatted Text. [69][72]
- Material3 1.5.0 is still not stable (1.5.0-beta02, 2026-10-21; stable 1.4.0). Design on M3 Expressive, but pin the beta deliberately and keep `MaterialShapes` and `LoadingIndicator` behind opt-ins. [3]
- Navigation 3 1.2.0 is stable (2026-09-23): result API, deep links (KMP) and predictive-back via `NavigationBackHandler`. 1.3.0-alpha03 is out. Use it for new adaptive navigation. [25][69]
- Adaptive is being enforced through Play. Google says Play will scrutinize foldable behavior "next year", with requirements announced later this year. Aim for Adaptive Tier 2 now. [69][26]
- A2UI for Jetpack Compose (alpha) is now announced as a first-party feature: agents answer with UI built from your own Compose components. Agentic UI keeps rising. [69][39]
- Contacts are moving to permissionless intents: apps targeting the next release lose direct `WRITE_CONTACTS` writes. Use `ACTION_INSERT`/`ACTION_EDIT`/the contact picker. [70]
- The target-SDK extension window (to 2026-11-01) closes today. Anything shipping now must target API 36. [50]

## Platform baseline (expected now, not a trend)
- **Target SDK 36 (Android 16)** — Since 2026-08-31, new apps and updates on Google Play must target API 36 (Wear OS and Automotive API 35; TV and XR API 34). The extension, if granted, ended 2026-11-01. The page was updated 2026-10-28 and lists no API 37 deadline yet. [50]
- **Edge-to-edge, no opt-out** — From API 36, `windowOptOutEdgeToEdgeEnforcement` is disabled. Draw behind the system bars, handle insets yourself, and give scrolling content transparent bars. [17]
- **Predictive back on by default** — For targetSdk 36, back-to-home, cross-task and cross-activity animations are on. `onBackPressed` is not called and `KEYCODE_BACK` is not dispatched. Use the AndroidX back APIs: Navigation 3 1.2 stable has `NavigationBackHandler` and `rememberNavigationEventState`; Compose 1.12 has `DeferredAnimatedContent`/`DeferredAnimatedVisibility` for two-stage back previews. [17][25][22]
- **Large-screen resizability** — Android 16 ignores `screenOrientation`, `resizeableActivity=false`, `min/maxAspectRatio` and `setRequestedOrientation()` on sw≥600dp. For API 37 targets the opt-out (`PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY`) is gone; games are exempt. Test with the `UNIVERSAL_RESIZABLE_BY_DEFAULT` compat flag. [17][15][18]
- **Android 17 (API 37) is stable** — Shipped to Pixels 2026-06-16, QPR1 in the September Pixel Drop. Activities are no longer recreated for keyboard, navigation, touchscreen or color-mode config changes (opt back in with `android:recreateOnConfigChanges`). QPR2 is at Beta 4; stable is expected around December per press. [14][49][73]
- **Compose-first stack** — Stable: Compose UI/Foundation 1.12.1, material3 1.4.0, BOM 2026.09.00. Beta: Compose 1.13.0-beta02 and material3 1.5.0-beta02 (both 2026-10-21). Compose 1.12 needs AGP 9.1.1+ and compileSdk 37. Instagram Direct's move to LazyColumn halved its UI codebase. [23][68][3][22][60]
- **Permissionless system pickers** — Use the photo picker, the Android 17 contact picker (`ACTION_PICK_CONTACTS`), the system location button and the EyeDropper (`ACTION_OPEN_EYE_DROPPER`). For writes, use `ACTION_INSERT`, `ACTION_EDIT` and `ACTION_INSERT_OR_EDIT`; a narrowed `WRITE_CONTACTS` and a new `MANAGE_CONTACTS` (Play declaration) are coming with the next release. [14][70]
- **Dynamic color + themed icons** — Since Android 16 QPR2 the launcher auto-tints icons that lack a monochrome layer. Ship a deliberate monochrome adaptive-icon layer and test both dynamic and brand schemes. [45]
- **Play Billing Library 8+** — Required for new apps and updates since 2026-08-31. The latest is 9.1.0 (2026-06-18). [51]
- **Adaptive app quality tiers** — Tier 3 Adaptive ready → Tier 2 Adaptive optimized → Tier 1 Adaptive differentiated. Google recommends at least Tier 2, and Play will look more closely at foldable behavior in 2027. [26][69]
- **Widget and notification memory caps (API 37)** — RemoteViews bitmaps in widgets are capped at 1.5 × screen width × height × 4 bytes; going over is a fatal `IllegalArgumentException`. [15][14]
- **Wear OS 7 (brief)** — Based on Android 17. Tiles evolve into Wear Widgets (Glance + RemoteCompose). Watch apps should use Live Updates instead of Ongoing Activities. Stable rollout date unverified. [62][29]
- **Android XR (brief)** — Jetpack XR core libraries (SceneCore, ARCore for Jetpack XR, XR Runtime) are now stable, as announced at Dev Summit. Jetpack Compose Glimmer is the design system for display glasses. Only build for XR with a spatial use case. [69][64]

## Trends

### and-m3-expressive-components — Material 3 Expressive component set
- **Status:** rising
- **Momentum:** ↑
- **What:** The Expressive set is the default vocabulary for Google's apps: button groups, split buttons, FAB menu, floating and docked toolbars, flexible top app bars, the short navigation bar, the wide navigation rail, toggle buttons with sizes, and loading/wavy progress. Material3 1.5.0 is now at beta02 (2026-10-21); stable has no date yet. Beta01 also touched the carousel (`HorizontalCenteredHeroCarousel` `maxItemWidth` renamed `preferredItemWidth`).
- **Seen in:** Google Drive (search app bar, button group, FAB menu), Pixel Now Playing app (floating toolbar + FAB), Phone by Google (short M3E bottom bar), Google Tasks widget.
- **Fits:** Consumer and productivity apps that want to feel native on Pixel and current Android; any app starting a redesign now.
- **Avoid when:** Your brand system is strongly non-Material (luxury, games). Floating toolbars hurt on small screens; keep them to a handful of actions. Also avoid shipping a beta dependency in a release train you cannot patch quickly.
- **Implement:**
  - Theme: `MaterialExpressiveTheme(colorScheme = expressiveLightColorScheme(), motionScheme = MotionScheme.expressive())`.
  - Components: `ButtonGroup`, `SplitButton`, `FloatingActionButtonMenu` with `ToggleFloatingActionButton`, `HorizontalFloatingToolbar`, `FlexibleBottomAppBar`, `ShortNavigationBar`, `WideNavigationRail`/`ModalWideNavigationRail`.
  - Top bars and toggles: `MediumFlexibleTopAppBar`/`LargeFlexibleTopAppBar`; `ToggleButton` overloads take `ButtonSize`.
  - Carousel: rename `maxItemWidth` to `preferredItemWidth` when moving to 1.5.0-beta01+; `CarouselDefaults.ItemSpacing`/`ContentPadding` are new.
  - Still experimental (verify in the beta02 API surface): `LoadingIndicator`, `MaterialShapes`.
  - Views: MDC-Android 1.14.0 adds Expressive themes for 11 components.
- **Sources:** [2], [3], [46], [47], [48], [37], [12]

### and-spring-motion-physics — Spring-based motion schemes
- **Status:** rising
- **Momentum:** →
- **What:** Material's motion physics replaces easing+duration with springs. One scheme (expressive or standard) is set at theme level; components read spatial and effects tokens in three speeds. Expressive overshoots; standard settles with minimal bounce.
- **Seen in:** Pixel system UI on Android 17 QPR1 (Quick Settings pull-down), Material 3 Compose components (bottom sheets follow `motionScheme` during drag), Wear OS physics-based motion.
- **Fits:** Gesture-heavy UIs, hero transitions, toggles, sheets. Expressive suits consumer apps; standard suits utilitarian and enterprise apps.
- **Avoid when:** Dense data tools where bounce reads as imprecision. Always honor the system "remove animations" setting, and don't overshoot opacity or color (use effects springs).
- **Implement:**
  - Read springs from `MaterialTheme.motionScheme`: `fastSpatialSpec()`, `defaultSpatialSpec()`, `slowSpatialSpec()` and the `*EffectsSpec()` variants. `LocalMotionScheme` was removed in 1.5.0-alpha27.
  - Expressive spatial: fast 0.6/800, default 0.8/380, slow 0.8/200 (damping/stiffness). Effects: damping 1.0 with stiffness 3800/1600/800.
  - Standard spatial: damping 0.9 with stiffness 1400/700/300.
  - Spatial springs drive position, size, rotation and corner radius; effects springs drive color and opacity.
  - Web parity: expressive default spatial ≈ cubic-bezier(0.38, 1.21, 0.22, 1.00) over 500ms.
- **Sources:** [4], [5], [3], [49]

### and-shape-morphing — Shape-led identity and shape morphing
- **Status:** rising
- **Momentum:** →
- **What:** M3E added a 35-shape library, built-in shape morphing and larger corner tokens. Shape carries identity (unique silhouettes, pills, asymmetric containers) and morphs to communicate state or progress. Material warns against abstract shapes without meaning.
- **Seen in:** Google Workspace icons (each app gets its own shape), Google Tasks widget (pill-shaped add button), Google Drive (rounded-top/square-bottom list corners), Gemini (circle-based shape language).
- **Fits:** Selected and pressed states, avatars and media thumbnails, loading moments, empty states, brand moments.
- **Avoid when:** Shapes would carry meaning on their own (accessibility); dense lists; low-end devices animating many morphs at once.
- **Implement:**
  - `MaterialShapes.*` (e.g. `Cookie9Sided`, `Sunny`); morph with `androidx.graphics.shapes.Morph` between `RoundedPolygon`s.
  - Since 1.5.0-beta01 `PolygonShape` uses top-level `CornerRounding` with `dp()`/`fraction()` and `PolygonShape.transform()`/`copy()` (replacing `transformed()`/`scaledToFit()`).
  - Corner tokens: large-increased 20dp, extra-large-increased 32dp, extra-extra-large 48dp, "full" for pills.
  - Animate morph progress with spatial springs.
- **Sources:** [6], [3], [43], [37], [46], [42]

### and-emphasized-type-flex — Emphasized type scale and variable type
- **Status:** emerging
- **Momentum:** →
- **What:** The M3 type scale has 30 styles, 15 baseline plus 15 emphasized, for heavier hero moments. It pairs with variable fonts; Google Sans Flex is on Google Fonts. Material added automatic line-height adaptation by script height in August 2026.
- **Seen in:** Google Clock 9.0 (large timer and stopwatch digits), Gemini app (large centered greeting).
- **Fits:** Hero numbers (timers, prices, scores), onboarding headlines, empty states, editorial content.
- **Avoid when:** Body copy and long lists; emphasis everywhere kills hierarchy. Check tall scripts (Thai, Arabic, Indic), since `elegantTextHeight` is ignored from API 36.
- **Implement:**
  - `MaterialTheme.typography.*Emphasized` styles (`displayLargeEmphasized` etc.); they need material3 1.5 (still beta).
  - Views: MDC 1.14.0 ships the emphasized scale.
  - Variable fonts: Compose 1.12 downloadable fonts support font variation settings; load Google Sans Flex and tune weight/width per style.
  - Compose 1.13 adds Formatted Text (announced at Dev Summit; API details unverified).
- **Sources:** [7], [2], [33], [40], [22], [17], [67], [69]

### and-segmented-lists-contained-search — Segmented lists, vibrant menus, contained search
- **Status:** rising
- **Momentum:** →
- **What:** Lists come in standard or segmented (grouped, gapped) styles with better selection. Vertical menus get vibrant color, gaps and submenus. Search defaults to a persistent filled "contained" container and a search app bar.
- **Seen in:** Google Drive (search app bar), Pixel Now Playing (history list with top search bar), Gemini (regrouped settings, Sept 2026 rollout).
- **Fits:** Settings, inboxes, file browsers, catalogs, any search-first app.
- **Avoid when:** Very long, uniform data tables; segmented cards waste vertical space. Don't put gaps in scrollable menus.
- **Implement:**
  - Lists: expressive `ListItem`, segmented list items and non-interactive variants.
  - Search: `SearchBar` with `SearchBarState`, `ExpandedFullScreenContainedSearchBar`, `ExpandedDockedSearchBarWithGap`.
  - Menus: `SelectableDropdownMenuItem`, `CheckableDropdownMenuItem`.
  - Search spec: 8dp vertical padding, 8dp gaps, 24dp horizontal margins (12dp when focused).
- **Sources:** [1], [13], [8], [3], [46], [47], [41]

### and-adaptive-multipane-layouts — Adaptive-by-default multi-pane layouts
- **Status:** mainstream
- **Momentum:** ↑
- **What:** Layouts are designed around five window breakpoints: compact <600dp, medium 600–839, expanded 840–1199, large 1200–1599, extra-large ≥1600. API 37 makes this unavoidable. At Dev Summit Google announced Grid and FlexBox reaching stable in Compose 1.13, an updated Compose adaptive agent skill (tabletop layouts, mediaQuery), and Play scrutiny of foldable behavior in 2027.
- **Seen in:** Notability (window size classes plus adaptive scene strategy), Samsung Galaxy Z Fold8 (landscape-first), Google Pixel 11 Pro Fold, Pixel taskbar.
- **Fits:** Every app with content hierarchy (list-detail, feed + supporting pane), commerce, media, productivity.
- **Avoid when:** Never skip it outright. Do avoid stretching phone UI edge to edge on tablets: set max content widths.
- **Implement:**
  - Navigation: `NavigationSuiteScaffold`, and Navigation 3 `NavDisplay` with `rememberListDetailSceneStrategy()`/`rememberSupportingPaneSceneStrategy()` from `material3.adaptive:adaptive-navigation3:1.3.0`; `SceneDecoratorStrategy` for bars and rails.
  - Window info: the V2 replacement for `currentWindowAdaptiveInfo()` supports L/XL classes.
  - Layout: Compose Grid and FlexBox (stable in 1.13, `ExperimentalGridApi`/`ExperimentalFlexBoxApi` until then); `mediaQuery {}` for posture such as `UiMediaScope.Posture.Tabletop`.
  - Spacing: Material tokens on an 8dp scale.
  - Camera and media: tabletop layouts for foldables via `CameraViewfinder`/CameraX; keep state in ViewModel.
- **Sources:** [9], [18], [24], [25], [21], [22], [27], [28], [29], [8], [14], [69]

### and-desktop-class-windowing — Desktop-class Android (Googlebook, windowing, pointer UX)
- **Status:** emerging
- **Momentum:** ↑
- **What:** Android is now a laptop OS too. Googlebook laptops run Android with trackpads and keyboards; phones get desktop windowing and connected displays. Dev Summit stressed scaling phone apps to laptops with no separate codebase and added agent tooling to audit keyboard shortcuts, cursors, hover and tooltips.
- **Seen in:** Googlebook (OEM lineup), Notability (adaptive canvas plus Continue On), Pixel desktop windowing.
- **Fits:** Productivity, creative, communication, education and finance apps; anything used at a desk.
- **Avoid when:** One-thumb, glance-only utilities. Even there, Tier 3 (no letterboxing, basic keyboard and mouse) is the floor.
- **Implement:**
  - Pointer: hover states, contextual cursors (`PointerIcon`), tooltips, right-click context menus. Trackpad reports as `PointerType.Mouse`.
  - Keyboard: discoverable shortcuts via the Keyboard Shortcuts Helper.
  - Windows: multi-instance, drag and drop between windows, customized caption bar.
  - Handoff: `setHandoffEnabled(true, null)` plus `onHandoffActivityDataRequested()` for Continue On.
  - Test on the Desktop emulator and Googlebook 160ppi / 1600×900dp sizes.
- **Sources:** [27], [18], [14], [49], [21], [3], [26], [66], [69]

### and-live-updates-status-chips — Live Updates and status-bar chips
- **Status:** rising
- **Momentum:** →
- **What:** Promoted ongoing notifications that pin to the top of the shade, lock screen and AOD, with a status-bar chip, for user-initiated, time-bound journeys (rides, delivery, navigation, timers). Android 17 adds MetricStyle (up to 3 metrics); Wear OS 7 shows them on the watch.
- **Seen in:** Google Clock 9.0 (timer and stopwatch chip), Wear OS 7 / Pixel Watch 5.
- **Fits:** Rideshare, food delivery, navigation, fitness sessions, timers, travel, calls.
- **Avoid when:** Ads, promos, chat, package tracking or shortcuts; Google disallows these. Never repost after dismissal.
- **Implement:**
  - Declare `POST_PROMOTED_NOTIFICATIONS`; `NotificationCompat.Builder.setRequestPromotedOngoing(true)`, `setOngoing(true)`, set a content title.
  - Not allowed: custom `RemoteViews`, `setColorized(true)`, group summaries.
  - `setShortCriticalText` (under 7 characters fits fully; chip max width 96dp).
  - `Notification.ProgressStyle` (segments, points, tracker icon); `MetricStyle` (3 metrics, 3 actions).
  - Check `canPostPromotedNotifications()`; add an "Unpin" action for background-started updates.
- **Sources:** [30], [31], [32], [33], [62], [29], [16]

### and-glanceable-widgets-everywhere — Widgets as a retention surface
- **Status:** rising
- **Momentum:** →
- **What:** Widgets are a growth lever with one Compose-based model across phone, Wear and car. Generated previews, dynamic-color backgrounds and interactive content replace static tiles. Google now ships a Glance widget-layout agent skill in the Android CLI.
- **Seen in:** Gratitude (25% higher retention for widget users), Google Tasks (M3E widget), Pixel VIP widget.
- **Fits:** Habit, wellness, productivity, finance-at-a-glance, weather, media, travel.
- **Avoid when:** You can't keep data fresh, or bitmaps would break the API 37 RemoteViews memory cap.
- **Implement:**
  - Glance 1.2.0 stable (2026-08-26); RemoteCompose for animated widgets.
  - `SizeMode.Exact`; generated previews via `GlanceAppWidget.providePreview` + `GlanceAppWidgetManager.setWidgetPreview`.
  - `requestPinGlanceAppWidget(previewSize = …)` from a contextual moment.
  - `GlanceTheme` for dynamic color; keep receiver class name and package when migrating from XML.
- **Sources:** [35], [36], [37], [34], [20], [49], [15], [69]

### and-ai-gradient-glow — Gradient and glow as the AI signifier
- **Status:** mainstream
- **Momentum:** →
- **What:** Google's AI language is soft, directional gradients: a sharp leading edge fading at the tail, pulsing during processing, plus circles and a pill prompt box. In 2026 it spread from Gemini to the Workspace icons.
- **Seen in:** Gemini app (May 2026 redesign), Gmail, Drive and Calendar icons, Google Design's Gemini illustration system.
- **Fits:** AI entry points, assistant and voice states, "thinking" indicators.
- **Avoid when:** Non-AI features (dilutes the signal) and long-running loops on low-end devices. Offer a static fallback; keep text contrast WCAG-safe. It is close to cliché, so use your own palette.
- **Implement:**
  - `Brush.linearGradient`/`radialGradient`/`sweepGradient`, animated via `rememberInfiniteTransition`; state changes on effects springs.
  - Reserve gradient for AI states: idle (static), listening (radial ripple), thinking (directional sweep).
  - Pair with a pill text field and one "+" tools sheet.
- **Sources:** [40], [42], [43], [44], [41]

### and-agentic-generative-ui — Agent-driven and generative UI
- **Status:** emerging
- **Momentum:** ↑
- **What:** Apps expose actions to agents (AppFunctions); in-app agents stream results (AG-UI) and render server-described native UI (A2UI) with Material components. At Dev Summit (2026-10-28) Google announced A2UI for Jetpack Compose (alpha) with a native renderer, so agents answer with UI built from your own components. Sensitive steps need explicit confirmation.
- **Seen in:** Gemini (task automation, Sept 2026 side panel with skills and connectors), DoorDash (Google's Wear OS 7 example), Jetpacker (Google's reference sample).
- **Fits:** Booking, commerce, travel, support, productivity: multi-step tasks.
- **Avoid when:** Regulated or irreversible actions without confirmation, and flows where users need to learn the UI. Generative layouts break consistency and accessibility if the catalog isn't constrained.
- **Implement:**
  - `@AppFunction(isDescribedByKDoc = true)` (Jetpack alpha; Gemini integration in private preview).
  - `androidx.a2ui:*` plus `androidx.compose.material3:material3-a2ui` (1.0.0-alpha01), `A2uiSurface`, `materialA2uiBasicCatalogV1(...)`. Restrict to a versioned component catalog.
  - Stream via the AG-UI Kotlin `HttpAgent`; gate actions with ADK `FunctionTool(..., require_confirmation=True)` and a visible "Confirm …" button.
  - On-device: Gemini Nano 4 via the ML Kit GenAI Prompt API.
- **Sources:** [38], [39], [14], [62], [41], [3], [69]

### and-system-blur-translucency — Blur and translucency layers
- **Status:** emerging
- **Momentum:** ↑
- **What:** Android 17 QPR1 puts translucent background blur across Pixel system UI (volume panel, power menu, folders, widget picker). Compose 1.13 adds Progressive Blur (announced at Dev Summit), so gradient-masked blur on bars and sheets gets a first-party path. It is subtler than iOS-style glass and sits on top of M3E.
- **Seen in:** Pixel system UI (Android 17 QPR1), Haze (community Compose blur library).
- **Fits:** Media and photo apps, overlays and sheets over imagery, floating toolbars over content.
- **Avoid when:** Text-heavy surfaces (contrast), low-end GPUs, battery-sensitive screens. Always provide an opaque fallback.
- **Implement:**
  - `Modifier.blur()` / `RenderEffect.createBlurEffect` (API 31+); Progressive Blur in Compose 1.13 (exact API name unverified; check 1.13.0-beta02 notes).
  - Window-level: `Window.setBackgroundBlurRadius` or `FLAG_BLUR_BEHIND` with `blurBehindRadius`; check `WindowManager.isCrossWindowBlurEnabled()` and fall back to a tonal scrim.
  - Keep blurred-surface text at 4.5:1 contrast.
- **Sources:** [49], [61], [69]

### and-frictionless-credential-onboarding — Passwordless, zero-tap onboarding
- **Status:** rising
- **Momentum:** →
- **What:** Sign-up and sign-in collapse into system bottom sheets. Passkeys via Credential Manager replace passwords, Verified Email replaces OTP, and Restore Credentials signs users in on a new device. Google Play will require Zero-Tap Sign-In by April 2027.
- **Seen in:** WhatsApp (passkeys for 1B+ users), Google Password Manager, Google (Verified Email credential).
- **Fits:** Any app with accounts: commerce, fintech, social, subscriptions.
- **Avoid when:** Workspace or supervised accounts, which Verified Email doesn't support. Keep an OTP path for custom domains.
- **Implement:**
  - Credential Manager `getCredential()` covers passkeys, passwords and Sign in with Google.
  - Verified Email via the Digital Credential API, triggered on email-field focus or "Sign up".
  - Create a passkey right after sign-up; Restore Credentials API for new devices.
  - SMS OTP is delayed about 3 hours for API 37 targets; use SMS Retriever or User Consent.
- **Sources:** [57], [58], [59], [15]

### and-play-native-subscription-flows — Day-0 paywalls plus Play-native retention
- **Status:** rising
- **Momentum:** →
- **What:** Median D35 download-to-paid is 0.9% on Android vs 2.6% on iOS, while trial-to-paid is about the same (32.5%). Winning patterns: Day-0 paywall after one value moment, a surfaced trial, your own trial-end reminders. Play owns more of the flow: retention offers at cancellation, winback offers, in-app messaging and billing choice. The 2026-10-13 Play post adds discovery and engagement tools.
- **Seen in:** Google Play Store (cancellation-flow retention, winback offers), RevenueCat benchmarks (115K+ apps).
- **Fits:** Subscription apps: productivity, health, education, creative.
- **Avoid when:** Network-effect or long-discovery products, where freemium converts later. Hard paywalls before any value are hostile.
- **Implement:**
  - Confirm the Play offer has a free phase before redesigning anything.
  - Paywall in the first session, after one value moment; build trial-end reminders yourself.
  - PBL 9.0.0 price-increase in-app messages show at most once every 7 days.
  - `getBillingChoiceInfoAsync()` (PBL 9.1.0); custom choice screens allowed in the US, UK and EEA under Google's UX guidelines.
- **Sources:** [56], [52], [53], [51], [54], [55]

## Fading — now looks dated
- **Hamburger navigation drawer** — Not recommended in M3E; use the expanded navigation rail. [10]
- **Tall baseline navigation bar** — Replaced by the short/flexible navigation bar. [11]
- **Bottom app bar** — Superseded by the docked and floating toolbars. [12]
- **Fixed easing+duration tweens** — Material treats them as legacy; springs handle interruption better. [4]
- **Portrait-locked, letterboxed phone UI on tablets and foldables** — Ignored on sw≥600dp, no opt-out at API 37; Play scrutiny follows in 2027. [15][18][69]
- **Opaque or colored system bars and `windowOptOutEdgeToEdgeEnforcement`** — Disabled from API 36. [17]
- **Back handling via `onBackPressed` with no preview** — Not called for targetSdk 36. [17]
- **New XML/View screens, Fragments, RecyclerView for new features** — Maintenance mode. [19][2]
- **Custom RemoteViews and colorized "fake live" notifications** — Ineligible for Live Updates, memory-capped at API 37. [30][15]
- **XML RemoteViews widgets with static previews** — Glance with generated previews is the norm. [35][36]
- **Email OTP steps and re-login after switching phones** — Replaced by Verified Email and Restore Credentials. [57][59]
- **`READ_CONTACTS`/`WRITE_CONTACTS`/location permission walls for simple picks and edits** — Use pickers and contact intents. [14][70]
- **Four-color, page-container Google icon style** — Google moved to single-hue gradients with distinct shapes. [43][44]
- **Nested-Row/Column hacks and hand-rolled breakpoints for responsive layout** — Grid, FlexBox and `mediaQuery` replace them. [69]

## Watchlist — verify next month
- Compose Material3 **1.5.0 stable** and Compose **1.13.0 stable**: both in beta02 (2026-10-21), no RC listed yet. Check whether `MaterialShapes`, `LoadingIndicator` and emphasized type graduate. (early)
- **Compose Progressive Blur and Formatted Text** exact API names (Dev Summit mention only). (unverified)
- **Android 17 QPR2** (Beta 4; stable ~December per press): `MANAGE_CONTACTS`, People Directory (`PeopleContract`) are confirmed in the contacts post; lock-screen blur, App Lock and customizable Quick Settings remain press-only. (partly unverified)
- **Play foldable requirements** for 2027: Google says they will be announced "later this year". (early)
- **Play API 37 target deadline**: none published as of 2026-10-28. (early)
- **AppState (alpha)** in Compose-first state architecture: check adoption and API shape. (early)
- **Samsung One UI 9 / 9.5 "glass" UI**: leaks only. (unverified)
- **Google apps on iOS** adopting Liquid Glass; Gemini "Neural Expressive" design-language name. (unverified)
- **Google Play "Optimized for large screens" badge** (announced 2026-05-19): display and ranking criteria. (unverified)
- **Googlebook** ship date and **Wear OS 7** stable rollout. (unverified)
- **Play in-app subscription management API** and full retention/winback rollout. (early)
- **Gemini Intelligence** system UI on Pixel 11 (HiLight indicator, cross-app tasks). Press only. (unverified)
- **Gemini 4 "Argon"** model and Android Studio agent tooling (posts of 2026-10-13 and 2026-10-28) have no direct UI impact yet. (early)

## Sources
1. [What's new at Google I/O 2026](https://m3.material.io/blog/whats-new-at-io26) — Material Design, 2026-05-19
2. [Material Android is Compose-first](https://m3.material.io/blog/material-is-compose-first) — Material Design, 2026-05-19
3. [Compose Material 3 release notes](https://developer.android.com/jetpack/androidx/releases/compose-material3) — Android Developers, 2026-10-21
4. [Motion physics system: Specs](https://m3.material.io/styles/motion/overview/specs) — Material Design, 2026-10-18 (accessed; living doc)
5. [ExpressiveMotionTokens.kt / StandardMotionTokens.kt](https://github.com/androidx/androidx/blob/androidx-main/compose/material3/material3/src/commonMain/kotlin/androidx/compose/material3/tokens/ExpressiveMotionTokens.kt) — AndroidX (source), 2026-10-18 (accessed)
6. [Shape: Overview & principles](https://m3.material.io/styles/shape/overview-principles) — Material Design, 2026-10-18 (accessed; living doc)
7. [Typography overview](https://m3.material.io/styles/typography/overview) — Material Design, 2026-10-18 (accessed; Aug 2026 update)
8. [Spacing overview](https://m3.material.io/styles/spacing/overview) — Material Design, 2026-10-18 (accessed; living doc)
9. [Breakpoints overview](https://m3.material.io/foundations/layout/breakpoints/overview) — Material Design, 2026-10-18 (accessed; living doc)
10. [Navigation drawer overview](https://m3.material.io/components/navigation-drawer/overview) — Material Design, 2026-10-18 (accessed; living doc)
11. [Navigation bar overview](https://m3.material.io/components/navigation-bar/overview) — Material Design, 2026-10-18 (accessed; living doc)
12. [Toolbars overview](https://m3.material.io/components/toolbars/overview) — Material Design, 2026-10-18 (accessed; living doc)
13. [Lists overview](https://m3.material.io/components/lists/overview) — Material Design, 2026-10-18 (accessed; Dec 2025 update)
14. [Android 17 is here](https://android-developers.googleblog.com/2026/06/Android-17.html) — Android Developers Blog, 2026-06-16
15. [Behavior changes: Apps targeting Android 17](https://developer.android.com/about/versions/17/behavior-changes-17) — Android Developers, 2026-10-18 (accessed)
16. [Android 17 features and changes list](https://developer.android.com/about/versions/17/summary) — Android Developers, 2026-10-18 (accessed)
17. [Behavior changes: Apps targeting Android 16](https://developer.android.com/about/versions/16/behavior-changes-16) — Android Developers, 2026-10-18 (accessed)
18. [Adaptive development for the expanding Android ecosystem](https://android-developers.googleblog.com/2026/05/android-adaptive-development-ecosystem.html) — Android Developers Blog, 2026-05-19
19. [Android UI Development is Compose First](https://android-developers.googleblog.com/2026/05/android-ui-development-is-compose-first.html) — Android Developers Blog, 2026-05-19
20. [17 Things to know for Android developers at Google I/O](https://android-developers.googleblog.com/2026/05/17-things-android-developers-google-io.html) — Android Developers Blog, 2026-05-19
21. [What's new in the Jetpack Compose April '26 release](https://android-developers.googleblog.com/2026/04/jetpack-compose-april-2026-updates.html) — Android Developers Blog, 2026-04-22
22. [What's new in the Jetpack Compose August '26 release](https://android-developers.googleblog.com/2026/08/jetpack-compose-august-2026-release.html) — Android Developers Blog, 2026-08-12
23. [Compose BOM to library version mapping](https://developer.android.com/develop/ui/compose/bom/bom-mapping) — Android Developers, 2026-10-18 (accessed)
24. [Compose Material 3 Adaptive release notes](https://developer.android.com/jetpack/androidx/releases/compose-material3-adaptive) — Android Developers, 2026-10-07
25. [Navigation 3 release notes](https://developer.android.com/jetpack/androidx/releases/navigation3) — Android Developers, 2026-10-21
26. [Adaptive app quality guidelines](https://developer.android.com/docs/quality-guidelines/adaptive-app-quality) — Android Developers, 2026-10-03
27. [Land your apps on Googlebook with adaptive development](https://android-developers.googleblog.com/2026/09/adaptive-development-scale-app-googlebook.html) — Android Developers Blog, 2026-09-22
28. [Optimize your apps for the next generation of Samsung Galaxy devices](https://android-developers.googleblog.com/2026/07/optimize-galaxy-screen-sizes.html) — Android Developers Blog, 2026-07-22
29. [Enhance your app for the new Pixel lineup: Unveiled at Made by Google](https://android-developers.googleblog.com/2026/08/pixel-app-experience-made-by-google.html) — Android Developers Blog, 2026-08-12
30. [Create Live Update notifications](https://developer.android.com/develop/ui/views/notifications/live-update) — Android Developers, 2026-10-16
31. [Progress-centric notifications](https://developer.android.com/about/versions/16/features/progress-centric-notifications) — Android Developers, 2026-03-03
32. [Create a metric style notification](https://developer.android.com/develop/ui/views/notifications/metric-style) — Android Developers, 2026-03-18
33. [Google Clock 9.0 adds stopwatch, timer Live Updates on Pixel](https://9to5google.com/2026/08/03/google-clock-9-0-live-updates/) — 9to5Google, 2026-08-03
34. [Building Premium Android Experiences at Google I/O '26](https://android-developers.googleblog.com/2026/06/building-premium-android-experiences-google-io-26.html) — Android Developers Blog, 2026-06-02
35. [Gratitude saw 25% higher retention for widget users](https://android-developers.googleblog.com/2026/05/how-gratitude-widgets-boosted-user-retention-25-percent.html) — Android Developers Blog, 2026-05-08
36. [Glance release notes](https://developer.android.com/jetpack/androidx/releases/glance) — Android Developers, 2026-08-26
37. [Google Tasks rolls out Material 3 Expressive widget redesign](https://9to5google.com/2026/06/04/google-tasks-expressive-widget/) — 9to5Google, 2026-06-04
38. [Top AI on Android updates for building intelligent experiences from Google I/O '26](https://android-developers.googleblog.com/2026/05/android-ai-intelligence-system.html) — Android Developers Blog, 2026-05-26
39. [Build intelligent Android apps: In-app agentic workflows](https://android-developers.googleblog.com/2026/09/android-agentic-workflows.html) — Android Developers Blog, 2026-09-28
40. [Gemini app getting full redesign that overhauls every part of the UI](https://9to5google.com/2026/05/03/gemini-full-redesign/) — 9to5Google, 2026-05-03
41. [Gemini app starts rolling out big side panel simplification, settings redesign](https://9to5google.com/2026/09/28/gemini-side-panel-settings-redesign/) — 9to5Google, 2026-09-28
42. [Illustrating the Gemini App](https://design.google/library/gemini-ai-visual-design) — Google Design, 2026-10-18 (accessed; featured in Material I/O 2026 post)
43. [Google Workspace icons finish rolling out on Android](https://9to5google.com/2026/06/04/google-workspace-android-icons/) — 9to5Google, 2026-06-04
44. [Gmail and Google Workspace gradient icon redesign](https://9to5google.com/2026/04/26/gmail-google-gradient-redesign/) — 9to5Google, 2026-04-26
45. [Android 16 auto-themed icons: apps can't opt out](https://9to5google.com/2025/09/16/android-16-auto-themed-icons-apps-cant-opt-out/) — 9to5Google, 2025-09-16
46. [Google Drive regains full Material 3 Expressive redesign](https://9to5google.com/2026/01/06/google-drive-m3-expressive-redesign-complete/) — 9to5Google, 2026-01-06
47. [Google Pixel Now Playing redesign with M3 Expressive rolling out](https://9to5google.com/2026/03/02/pixel-now-playing-redesign-2/) — 9to5Google, 2026-03-02
48. [Google Phone app gets short Material 3 Expressive bottom bar](https://9to5google.com/2026/01/19/google-phone-m3-expressive-bottom-bar/) — 9to5Google, 2026-01-19
49. [Android 17 QPR1 / September Pixel Drop rollout](https://www.androidheadlines.com/2026/09/android-17-qpr1-september-pixel-drop-rollout.html) — Android Headlines, 2026-09-16
50. [Meet Google Play's target API level requirement](https://developer.android.com/google/play/requirements/target-sdk) — Android Developers, 2026-10-28
51. [Google Play Billing Library release notes](https://developer.android.com/google/play/billing/release-notes) — Android Developers, 2026-06-18
52. [Driving growth on Google Play: The next era of subscriptions](https://android-developers.googleblog.com/2026/09/unlocking-Google-play-subscription-growth.html) — Android Developers Blog, 2026-09-29
53. [I/O 2026: What's new in Google Play](https://android-developers.googleblog.com/2026/05/io-2026-whats-new-in-google-play.html) — Android Developers Blog, 2026-05-19
54. [Expanded billing choice and lower fees on Google Play](https://android-developers.googleblog.com/2026/06/play-expanded-billing.html) — Android Developers Blog, 2026-06-24
55. [New ways to drive smarter discovery, deeper engagement, and business growth on Google Play](https://developer.android.com/blog/posts/google-play-discovery-engagement-growth) — Android Developers Blog, 2026-10-13
56. [The Android paywall conversion gap](https://www.revenuecat.com/blog/engineering/android-paywall-gap/) — RevenueCat, 2026-03-25
57. [Streamline User Journeys with Verified Email via Credential Manager](https://android-developers.googleblog.com/2026/04/streamline-auth-credential-manager-verified-email.html) — Android Developers Blog, 2026-04-22
58. [How WhatsApp Upgraded to Secure, Seamless Sign-In for 1 Billion Users with Passkeys](https://android-developers.googleblog.com/2026/08/whatsapp-passkeys-secure-sign-in.html) — Android Developers Blog, 2026-08-27
59. [Elevating app quality: Reducing memory usage and improving device migration](https://android-developers.googleblog.com/2026/08/app-quality-memory-optimization-secure-onboarding.html) — Android Developers Blog, 2026-08-26
60. [How Instagram Direct engineers built AI-native UI architecture with Jetpack Compose](https://android-developers.googleblog.com/2026/09/jetpack-compose-ai-native-ui-instagram-direct.html) — Android Developers Blog, 2026-09-30
61. [Celebrating 5 years of Jetpack Compose](https://android-developers.googleblog.com/2026/07/five-years-of-jetpack-compose.html) — Android Developers Blog, 2026-07-28
62. [What's New in Wear OS 7](https://android-developers.googleblog.com/2026/05/whats-new-wear-os-7.html) — Android Developers Blog, 2026-05-19
63. [Jetpack XR SDK core libraries reach beta](https://android-developers.googleblog.com/2026/08/jetpack-xr-sdk-core-libraries-beta.html) — Android Developers Blog, 2026-08-18
64. [How to Design for Transparent Screens (Jetpack Compose Glimmer)](https://design.google/library/transparent-screens) — Google Design, 2026-10-18 (accessed; featured in Material I/O 2026 post)
65. [Android Developers Blog is moving](https://android-developers.googleblog.com/2026/10/android-developers-blog-is-moving.html) — Android Developers Blog, 2026-10-15
66. [Get inspired and take your apps to desktop](https://android-developers.googleblog.com/2026/03/Get-inspired-and-take-your-apps-to-desktop.html) — Android Developers Blog, 2026-03-16
67. [Google Sans Flex (Google Fonts CSS API)](https://fonts.googleapis.com/css2?family=Google+Sans+Flex) — Google Fonts, 2026-10-18 (accessed)
68. [Compose release notes (versions table)](https://developer.android.com/jetpack/androidx/releases/compose) — Android Developers, 2026-10-21
69. [Agentic and Flexible: A next era of Android development](https://developer.android.com/blog/posts/build-it-your-way-a-next-era-of-android-development) — Android Developers Blog, 2026-10-28
70. [A more reliable way to add and edit contacts on Android](https://developer.android.com/blog/posts/reliable-way-to-add-and-edit-contacts-android) — Android Developers Blog, 2026-10-21
71. [Android Developers Blog (index, new home)](https://developer.android.com/blog) — Android Developers, 2026-10-28 (accessed)
72. [What's new in Android developer tools and performance at Android Dev Summit](https://developer.android.com/blog/posts/android-dev-summit-26-developer-tools-performance) — Android Developers Blog, 2026-10-28 (index listing only)
73. [Android 17 QPR2 Beta](https://developer.android.com/about/versions/17/qpr2) — Android Developers, 2026-10-31 (accessed; Beta 4 current)
74. [Your favorite agents are now integrated in Android Studio](https://developer.android.com/blog/posts/ai-agents-android-studio-integration) — Android Developers Blog, 2026-10-28 (index listing only)
