---
platform: android
period: 2026-10
researched_at: 2026-10-18
previous: null
sources: 68
---

# Android — UI/UX trends · October 2026

## TL;DR
- Material 3 Expressive is no longer a preview. Google's own apps run it, and Compose Material3 1.5.0 (beta01 on 2026-10-07) is promoting the Expressive APIs to stable. Design on M3E, not baseline M3. [2][3]
- Android UI is officially "Compose First" (I/O 2026). Views, Fragments and RecyclerView are in maintenance mode, and Material Views 1.14.0 is the last feature release. [19][2]
- Adaptive is mandatory. Apps targeting API 37 can no longer lock orientation, aspect ratio or resizability on screens ≥600dp. App Bubbles, desktop windowing, Googlebook and landscape-first foldables are where that shows up. [14][15][27][28]
- Motion now runs on springs, not easing curves. Use `MaterialTheme.motionScheme` tokens; expressive default spatial is damping 0.8 / stiffness 380. [4][5]
- Live Updates are the status-bar surface for ongoing, user-started tasks. Android 16 brought ProgressStyle and Android 17 added MetricStyle; Google Clock adopted them, and Wear OS 7 bridges them to the watch. [30][32][33][62]
- Gradients and glow now signal AI across Google. The Gemini app was redesigned, and Workspace icons moved to gradients with distinct shapes. Generative/agentic UI (A2UI rendered with Material components) is the emerging frontier. [40][43][39]
- Onboarding is going passwordless and zero-tap: passkeys, Verified Email without OTP, and Restore Credentials. Google Play will require Zero-Tap Sign-In by April 2027. [57][58][59]

## Platform baseline (expected now, not a trend)
- **Target SDK 36 (Android 16)** — Since 2026-08-31, new apps and updates on Google Play must target API 36. An extension to 2026-11-01 can be requested. Wear OS and Automotive need API 35; TV and XR need API 34. [50]
- **Edge-to-edge, no opt-out** — From API 36, `windowOptOutEdgeToEdgeEnforcement` is disabled. Draw behind the system bars, handle insets yourself, and give scrolling content transparent bars. [17]
- **Predictive back on by default** — For targetSdk 36, back-to-home, cross-task and cross-activity animations are on. `onBackPressed` is not called and `KEYCODE_BACK` is not dispatched. Use the OnBackInvoked/AndroidX back APIs: Navigation 3 1.2 adds `NavigationBackHandler`, and Compose 1.12 adds `DeferredAnimatedContent`/`DeferredAnimatedVisibility` for two-stage back previews. [17][25][22]
- **Large-screen resizability** — Android 16 began ignoring `screenOrientation`, `resizeableActivity=false`, `min/maxAspectRatio` and `setRequestedOrientation()` on sw≥600dp. For API 37 targets the opt-out (`PROPERTY_COMPAT_ALLOW_RESTRICTED_RESIZABILITY`) is gone; games are exempt. Previously letterboxed apps get stretched to landscape. Test with the `UNIVERSAL_RESIZABLE_BY_DEFAULT` compat flag. [17][15][18]
- **Android 17 (API 37) is stable** — Shipped to Pixels 2026-06-16, with QPR1 in the September Pixel Drop. It changes UI-related defaults: activities are no longer recreated for keyboard, navigation, touchscreen or color-mode config changes (opt back in with `android:recreateOnConfigChanges`). Device-RAM-based memory limits also apply. [14][49]
- **Compose-first stack** — Stable versions: Compose 1.12.1 (BOM 2026.09.00 → material3 1.4.0, material3-adaptive 1.3.0); Compose 1.13.0-beta01 and material3 1.5.0-beta01 are in beta. Compose 1.12 needs AGP 9.1.1+ and compileSdk 37. Over 68% of the top 1,000 apps use Compose in production; Instagram Direct's move to LazyColumn halved its UI codebase. [23][68][3][22][61][60]
- **Permissionless system pickers** — Use the photo picker (portrait thumbnails via `PhotoPickerUiCustomizationParams`), the Android 17 contact picker (`ACTION_PICK_CONTACTS`), the system location button and the EyeDropper (`ACTION_OPEN_EYE_DROPPER`). Don't build permission walls for these. [14]
- **Dynamic color + themed icons** — Since Android 16 QPR2 the launcher auto-tints icons that lack a monochrome layer. Play's Developer Distribution Agreement now requires letting users modify app colors and themes. Ship a deliberate monochrome adaptive-icon layer and test both dynamic and brand schemes. [45]
- **Play Billing Library 8+** — Required for new apps and updates since 2026-08-31. The latest is 9.1.0 (2026-06-18). [51]
- **Adaptive app quality tiers** — Tier 3 Adaptive ready → Tier 2 Adaptive optimized → Tier 1 Adaptive differentiated (guidelines updated 2026-10-03). Google recommends at least Tier 2. [26]
- **Widget and notification memory caps (API 37)** — RemoteViews bitmaps in widgets are capped at 1.5 × screen width × height × 4 bytes; going over is a fatal `IllegalArgumentException`. Custom notification views get stricter limits. [15][14]
- **Wear OS 7 (brief)** — Based on Android 17. Tiles evolve into Wear Widgets (Glance + RemoteCompose, small and large cards matching 2x1/2x2 phone widgets). Watch apps should use Live Updates instead of the Ongoing Activities API. Compose for Wear OS 1.6 brings Navigation 3, and the 1.7 beta adds one-handed gestures (double-pinch, wrist turn). [62][29]
- **Android XR (brief)** — The Jetpack XR core libraries (SceneCore, ARCore for Jetpack XR, XR Runtime) are at 1.0.0-beta02; Compose for XR is at alpha17. Material now has XR guidance (spatial panels, depth-based elevation), and Jetpack Compose Glimmer is the design system for display AI glasses. Only build for XR if you have a spatial use case. [63][1][64]

## Trends

### and-m3-expressive-components — Material 3 Expressive component set
- **Status:** rising
- **Momentum:** new
- **What:** The Expressive set is the default vocabulary for Google's apps: button groups, split buttons, FAB menu, floating and docked toolbars, flexible top app bars, the short navigation bar, the wide navigation rail, toggle buttons with sizes, and loading/wavy progress. It also adds "standard vs vibrant" color styles. Through 2026 these APIs graduated to stable in material3 1.5.0 alphas, and 1.5.0 stable is promised for later in 2026.
- **Seen in:** Google Drive (search app bar, button group, FAB menu, short bottom bar), Pixel Now Playing app (floating toolbar + FAB), Phone by Google (short M3E bottom bar), Google Tasks widget.
- **Fits:** Consumer and productivity apps that want to feel native on Pixel and current Android; any app starting a redesign now.
- **Avoid when:** Your brand system is strongly non-Material (luxury, games). Heavy toolbars also hurt on small screens; keep floating toolbars to a handful of actions and keep content readable beneath them.
- **Implement:**
  - Theme: wrap in `MaterialExpressiveTheme(colorScheme = expressiveLightColorScheme(), motionScheme = MotionScheme.expressive())` (promoted in 1.5.0-alpha18).
  - Components: `ButtonGroup` (stable since alpha22) and `SplitButton` (`SplitButtonLayout` deprecated in alpha25). For the FAB menu use `FloatingActionButtonMenu` with `ToggleFloatingActionButton`. Navigation uses `HorizontalFloatingToolbar`/`FlexibleBottomAppBar`, `ShortNavigationBar` and `WideNavigationRail`/`ModalWideNavigationRail`.
  - Top bars and toggles: `MediumFlexibleTopAppBar`/`LargeFlexibleTopAppBar` (non-experimental since alpha23); `ToggleButton` overloads take `ButtonSize` (alpha27).
  - Still experimental: `LoadingIndicator` and `MaterialShapes` (their promotion was reverted in alpha19).
  - Views: MDC-Android 1.14.0 adds Expressive themes and styles for 11 components.
- **Sources:** [2], [3], [46], [47], [48], [37], [12]

### and-spring-motion-physics — Spring-based motion schemes
- **Status:** rising
- **Momentum:** new
- **What:** Material's motion physics system replaces easing+duration with springs. One scheme (expressive or standard) is set at theme level; components read spatial and effects tokens in three speeds. Expressive overshoots and bounces; standard settles with minimal bounce.
- **Seen in:** Pixel system UI on Android 17 QPR1 (springier Quick Settings pull-down that matches the shade), Material 3 Compose components (bottom sheets follow `motionScheme` during drag), Wear OS (Material's physics-based watch motion guidance).
- **Fits:** Gesture-heavy UIs, hero transitions, toggles, sheets. Expressive suits consumer apps; standard suits utilitarian and enterprise apps.
- **Avoid when:** Dense data tools where bounce reads as imprecision. Always honor the system "remove animations" setting, and don't overshoot opacity or color (use effects springs).
- **Implement:**
  - Read springs from `MaterialTheme.motionScheme`: `fastSpatialSpec()`, `defaultSpatialSpec()`, `slowSpatialSpec()` and the matching `*EffectsSpec()`. `LocalMotionScheme` was removed in 1.5.0-alpha27.
  - Expressive spatial: fast 0.6/800, default 0.8/380, slow 0.8/200 (damping/stiffness). Effects: damping 1.0 with stiffness 3800/1600/800.
  - Standard spatial: damping 0.9 with stiffness 1400/700/300.
  - Spatial springs drive position, size, rotation and corner radius; effects springs drive color and opacity.
  - Web parity: expressive default spatial ≈ cubic-bezier(0.38, 1.21, 0.22, 1.00) over 500ms.
- **Sources:** [4], [5], [3], [49], [1]

### and-shape-morphing — Shape-led identity and shape morphing
- **Status:** rising
- **Momentum:** new
- **What:** M3E added a 35-shape library, built-in shape morphing and larger corner tokens. Shape is used for identity (unique silhouettes, pill containers, asymmetric containers) and morphs to communicate state or progress. Material encourages "tension" by mixing round and sharp shapes, but warns against abstract shapes without meaning.
- **Seen in:** Google Workspace icons (page containers dropped; each app gets its own shape), Google Tasks widget (pill-shaped themed add button), Google Drive (file list with rounded top and square bottom corners), Gemini (circle-based shape language).
- **Fits:** Selected and pressed states, avatars and media thumbnails, loading moments, empty states, brand moments.
- **Avoid when:** Shapes would carry meaning on their own (accessibility); dense lists; low-end devices animating many morphs at once.
- **Implement:**
  - Shapes: `MaterialShapes.*` (e.g. `Cookie9Sided`, `Sunny`); morph with `androidx.graphics.shapes.Morph` between `RoundedPolygon`s.
  - 1.5.0-beta01 reworked `PolygonShape`: top-level `CornerRounding` with `dp()`/`fraction()` factories, plus `PolygonShape.transform()` and `copy()`.
  - Corner tokens: large-increased 20dp, extra-large-increased 32dp, extra-extra-large 48dp, and "full" for pills.
  - Animate morph progress with spatial springs.
- **Sources:** [6], [3], [43], [37], [46], [42]

### and-emphasized-type-flex — Emphasized type scale and variable type
- **Status:** emerging
- **Momentum:** new
- **What:** The M3 type scale now has 30 styles, 15 baseline plus 15 emphasized, for heavier, larger hero moments. It pairs with variable fonts; Google Sans Flex is now on Google Fonts. In August 2026 Material added automatic line-height adaptation by language script height.
- **Seen in:** Google Clock 9.0 (much larger timer and stopwatch count, bigger buttons), Gemini app (large centered greeting).
- **Fits:** Hero numbers (timers, prices, scores), onboarding headlines, empty states, editorial content.
- **Avoid when:** Body copy and long lists; emphasized weight everywhere kills hierarchy. Check tall scripts (Thai, Arabic, Indic), since `elegantTextHeight` is ignored from API 36.
- **Implement:**
  - Use the `MaterialTheme.typography.*Emphasized` styles (`displayLargeEmphasized` and so on). They were internal in 1.4.0, so they need 1.5.
  - Views: MDC 1.14.0 ships the emphasized type scale.
  - Variable fonts: Compose 1.12 downloadable fonts support font variation settings. Load Google Sans Flex or another variable family and tune weight/width per style.
- **Sources:** [7], [2], [33], [40], [22], [17], [67]

### and-segmented-lists-contained-search — Segmented lists, vibrant menus, contained search
- **Status:** rising
- **Momentum:** new
- **What:** "Expressive lists and menus" were the Material headline at I/O 2026. Lists come in standard or segmented (grouped, gapped) styles with better selection. Vertical menus get vibrant color, gaps and submenus. Search defaults to a persistent filled "contained" container and a search app bar.
- **Seen in:** Google Drive (search app bar over a shared surface layer), Pixel Now Playing (history list with top search bar), Gemini (regrouped settings, Sept 2026 rollout).
- **Fits:** Settings, inboxes, file browsers, catalogs, any search-first app.
- **Avoid when:** Very long, uniform data tables; segmented cards waste vertical space there. Don't put gaps in scrollable menus.
- **Implement:**
  - Lists: expressive `ListItem`, segmented list items and non-interactive variants (non-experimental since 1.5.0-alpha23).
  - Search: `SearchBar` with `SearchBarState` (stable in alpha23), `ExpandedFullScreenContainedSearchBar` and `ExpandedDockedSearchBarWithGap`.
  - Menus: `SelectableDropdownMenuItem` and `CheckableDropdownMenuItem` (alpha27).
  - Search spec: 8dp vertical padding, 8dp gaps, 24dp horizontal margins (12dp when focused).
- **Sources:** [1], [13], [8], [3], [46], [47], [41]

### and-adaptive-multipane-layouts — Adaptive-by-default multi-pane layouts
- **Status:** mainstream
- **Momentum:** new
- **What:** Layouts are designed around five window breakpoints, not devices: compact <600dp, medium 600–839, expanded 840–1199, large 1200–1599 and extra-large ≥1600. Screens move from one pane to two or three as the window grows. API 37 makes this unavoidable, and App Bubbles, foldables and split-screen produce arbitrary window sizes. Google cites 580M+ large-screen devices.
- **Seen in:** Notability (window size classes plus adaptive scene strategy; canvas and toolbars reflow while resizing), Samsung Galaxy Z Fold8 (ultra-wide, "landscape-first" natural orientation), Google Pixel 11 Pro Fold, Pixel taskbar.
- **Fits:** Every app with content hierarchy (list-detail, feed + supporting pane), commerce, media and productivity.
- **Avoid when:** Never skip it outright. Do avoid stretching phone UI edge to edge on tablets: set max content widths and don't let text lines run endlessly.
- **Implement:**
  - Navigation: `NavigationSuiteScaffold`, and Navigation 3 `NavDisplay` with a list of scene strategies (`rememberListDetailSceneStrategy()`, `rememberSupportingPaneSceneStrategy()`) from `material3.adaptive:adaptive-navigation3:1.3.0`. Use `SceneDecoratorStrategy` for bars and rails.
  - Window info: use the V2 replacement for `currentWindowAdaptiveInfo()`, which supports the L/XL classes.
  - Layout: Compose Grid (`ExperimentalGridApi`, named areas in 1.12) and FlexBox (`ExperimentalFlexBoxApi`). `mediaQuery {}` (`ExperimentalMediaQueryApi`) handles posture such as `UiMediaScope.Posture.Tabletop`.
  - Spacing: Material tokens on an 8dp scale (space100 = 8dp).
  - Camera and state: CameraX or `CameraViewfinder` previews; keep state in ViewModel.
- **Sources:** [9], [18], [24], [25], [21], [22], [27], [28], [29], [8], [14]

### and-desktop-class-windowing — Desktop-class Android (Googlebook, windowing, pointer UX)
- **Status:** emerging
- **Momentum:** new
- **What:** Android is now a laptop OS as well. Googlebook laptops from HP, Dell, Lenovo, Acer and Asus run Android with trackpads and keyboards. Phones get desktop windowing, connected displays (stable since Android 16 QPR3) and interactive PiP. Apps live in freely resizable windows with caption bars, hover, right-click and keyboard shortcuts.
- **Seen in:** Googlebook (OEM lineup above), Notability (adaptive canvas plus Continue On handoff to laptop), Pixel desktop windowing (QPR1 maximize-button layouts, free-moving PiP).
- **Fits:** Productivity, creative, communication, education and finance apps; anything people use at a desk.
- **Avoid when:** One-thumb, glance-only utilities. Even there, Tier 3 (no letterboxing, basic keyboard and mouse) is the floor.
- **Implement:**
  - Pointer: hover states, contextual cursors and right-click context menus. Trackpad input reports as `PointerType.Mouse`, with two-finger gestures from API 34 (Compose 1.11). For focus rings, use the inset style from `RippleThemeConfiguration` (stable in 1.5.0-alpha18).
  - Keyboard: make shortcuts discoverable through the Keyboard Shortcuts Helper.
  - Windows: support multi-instance and drag and drop between windows; customize the caption header bar.
  - Handoff: `setHandoffEnabled(true, null)` plus `onHandoffActivityDataRequested()` / `HandoffActivityData` for Continue On.
  - Test on the Desktop emulator (Android Studio Canary) and the guideline sizes: Googlebook at 160ppi and a 1600×900dp Chromebook.
- **Sources:** [27], [18], [14], [49], [21], [3], [26], [66]

### and-live-updates-status-chips — Live Updates and status-bar chips
- **Status:** rising
- **Momentum:** new
- **What:** Android's answer to live activities: promoted ongoing notifications that pin to the top of the shade, lock screen and AOD, with a status-bar chip. They are for user-initiated, time-bound journeys such as rides, delivery, navigation, calls and timers. Android 17 adds MetricStyle (up to 3 metrics); Wear OS 7 shows Live Updates on the watch and bridges phone ones on supporting OEMs.
- **Seen in:** Google Clock 9.0 (timer and stopwatch pill in the status bar, Aug 2026), Wear OS 7 / Pixel Watch 5 (Live Updates on the wrist and in At-a-Glance).
- **Fits:** Rideshare, food delivery, navigation, fitness sessions, timers, travel and boarding, calls.
- **Avoid when:** Ads, promos, chat, package tracking or "quick access" shortcuts; Google explicitly disallows these. Never repost after the user dismisses one.
- **Implement:**
  - Promotion: declare `POST_PROMOTED_NOTIFICATIONS`, call `NotificationCompat.Builder.setRequestPromotedOngoing(true)` and `setOngoing(true)`, and set a content title.
  - Not allowed: custom `RemoteViews`, `setColorized(true)`, group summaries.
  - Chip text: `setShortCriticalText` (under 7 characters fits fully; chip max width 96dp).
  - Templates: `Notification.ProgressStyle` with segments (states), points (milestones) and a tracker icon. `MetricStyle` takes up to 3 metrics and 3 actions.
  - Checks and controls: `canPostPromotedNotifications()`; add an "Unpin" action for background-started updates.
- **Sources:** [30], [31], [32], [33], [62], [29], [16]

### and-glanceable-widgets-everywhere — Widgets as a retention surface
- **Status:** rising
- **Momentum:** new
- **What:** Widgets are back as a growth lever, with one Compose-based model across phone, Wear (Wear Widgets) and car. Generated, personalized previews, dynamic-color backgrounds and interactive content (journaling prompts, add buttons) replace static info tiles.
- **Seen in:** Gratitude (25% higher retention for widget users; 10% of DAU use widgets), Google Tasks (M3E widget with dynamic-color background and pill add button), Pixel VIP widget (refreshed in QPR1).
- **Fits:** Habit, wellness, productivity, finance-at-a-glance, weather, media, travel.
- **Avoid when:** You can't keep data fresh, or bitmaps would break the API 37 RemoteViews memory cap.
- **Implement:**
  - Library: Glance 1.2.0 stable (2026-08-26); RemoteCompose for richer, animated widgets.
  - Sizing: `SizeMode.Exact` for resizing.
  - Previews: generated previews via `GlanceAppWidget.providePreview` plus `GlanceAppWidgetManager.setWidgetPreview`.
  - Pinning: offer `requestPinGlanceAppWidget(previewSize = …)` from a bottom sheet at a relevant moment.
  - Theming: `GlanceTheme` for dynamic color.
  - Migration: keep the receiver class name and package when moving from XML so installed widgets aren't lost.
- **Sources:** [35], [36], [37], [34], [20], [49], [15]

### and-ai-gradient-glow — Gradient and glow as the AI signifier
- **Status:** mainstream
- **Momentum:** new
- **What:** Google's AI language is soft, directional gradients: a sharp leading edge fading at the tail, pulsing during processing, plus circles and a pill-shaped prompt box. In 2026 it spread from Gemini to the brand itself, with Workspace icons moving to gradients.
- **Seen in:** Gemini app (May 2026 redesign: pill prompt, "+" bottom sheet, pulsating gradient homepage), Gmail, Drive and Calendar (gradient icon redesign, Android rollout complete 2026-06-04), Google Design's Gemini illustration system.
- **Fits:** AI entry points, assistant and voice states, "thinking" indicators, premium AI tiers.
- **Avoid when:** Non-AI features (it dilutes the signal) and long-running loops on low-end devices. Offer a static fallback when animations are off, and keep text contrast WCAG-safe over gradients. The look is close to cliché; differentiate with your own palette.
- **Implement:**
  - Draw with Compose `Brush.linearGradient`/`radialGradient`/`sweepGradient`, animated via `rememberInfiniteTransition`, and drive state changes with effects springs.
  - Reserve gradient for AI states: idle (static), listening (radial ripple) and thinking (directional sweep).
  - Pair with a pill text field and a single "+" tools sheet, as in Gemini.
- **Sources:** [40], [42], [43], [44], [41]

### and-agentic-generative-ui — Agent-driven and generative UI
- **Status:** emerging
- **Momentum:** new
- **What:** Google calls Android an "intelligence system". Apps expose actions to agents (AppFunctions); in-app agents stream results (AG-UI) and render server-described native UI (A2UI) with Material components. Sensitive steps go through explicit confirmation gates.
- **Seen in:** Gemini (task automation across apps; Sept 2026 side panel adds skills and connectors), DoorDash (Google's example of Wear OS 7 task automation), Jetpacker (Google's reference booking-assistant sample).
- **Fits:** Booking, commerce, travel, support and productivity: multi-step tasks where an agent can do the legwork.
- **Avoid when:** Regulated or irreversible actions without confirmation, and flows where users need to learn the UI. Generative layouts can break consistency and accessibility if the catalog isn't constrained.
- **Implement:**
  - Expose actions: `@AppFunction(isDescribedByKDoc = true)` (Jetpack alpha; Gemini integration in private preview).
  - Render agent UI: `androidx.a2ui:*` plus `androidx.compose.material3:material3-a2ui` (1.0.0-alpha01), with `A2uiSurface` and `materialA2uiBasicCatalogV1(...)`. Restrict to a versioned component catalog.
  - Streaming and confirmation: stream via the AG-UI Kotlin `HttpAgent`; gate actions with ADK `FunctionTool(..., require_confirmation=True)` and a visible "Confirm …" button.
  - On-device models: Gemini Nano 4 via the ML Kit GenAI Prompt API.
- **Sources:** [38], [39], [14], [62], [41], [3]

### and-system-blur-translucency — Blur and translucency layers
- **Status:** emerging
- **Momentum:** new
- **What:** Android 17 QPR1 puts translucent background blur across Pixel system UI: volume panel, power menu, folders, context menus and widget picker. Apps are starting to echo it with frosted bars and sheets. It is subtler than iOS-style glass and sits on top of M3E, not in place of it.
- **Seen in:** Pixel system UI (Android 17 QPR1), Haze (the community Compose background-blur library Google highlighted).
- **Fits:** Media and photo apps, overlays and sheets over imagery, floating toolbars over content.
- **Avoid when:** Text-heavy surfaces (contrast), low-end GPUs, battery-sensitive screens. Always provide an opaque fallback.
- **Implement:**
  - Compose `Modifier.blur()` / `RenderEffect.createBlurEffect` (API 31+).
  - Window-level: `Window.setBackgroundBlurRadius` or `FLAG_BLUR_BEHIND` with `blurBehindRadius`. Check `WindowManager.isCrossWindowBlurEnabled()` and fall back to a tonal scrim.
  - Keep blurred-surface text at a 4.5:1 contrast ratio.
- **Sources:** [49], [61]

### and-frictionless-credential-onboarding — Passwordless, zero-tap onboarding
- **Status:** rising
- **Momentum:** new
- **What:** Sign-up and sign-in collapse into system bottom sheets. Passkeys via Credential Manager replace passwords, Verified Email replaces OTP inbox hunting, and Restore Credentials signs users in automatically on a new device. Google Play will require Zero-Tap Sign-In by April 2027.
- **Seen in:** WhatsApp (passkeys for 1B+ users; contextual creation prompts, graceful fallback), Google Password Manager (passkey store), Google (Verified Email credential).
- **Fits:** Any app with accounts, especially commerce, fintech, social and subscriptions.
- **Avoid when:** Workspace or supervised accounts, which Verified Email doesn't support. Keep an OTP path for custom domains.
- **Implement:**
  - Credential Manager `getCredential()` covers passkeys, passwords and Sign in with Google.
  - Verified Email: the Digital Credential API, triggered on email-field focus or "Sign up" ("Agree and continue").
  - Create a passkey right after sign-up, tied to a contextual moment.
  - New devices: Restore Credentials API.
  - SMS OTP is delayed about 3 hours for API 37 targets; use SMS Retriever or User Consent.
- **Sources:** [57], [58], [59], [15]

### and-play-native-subscription-flows — Day-0 paywalls plus Play-native retention
- **Status:** rising
- **Momentum:** new
- **What:** Android's paywall gap is at the top of the funnel. Median D35 download-to-paid is 0.9% on Android vs 2.6% on iOS, while trial-to-paid is about the same (32.5%). Winning patterns: a Day-0 paywall after one value moment, a properly surfaced trial, and your own trial-end reminders. Google Play now owns more of the flow: retention offers and plan changes at cancellation, winback offers, in-app messaging, and billing-choice screens.
- **Seen in:** Google Play Store (cancellation-flow retention offers, winback offers, 60-day account recovery), RevenueCat (benchmarks across 115K+ apps).
- **Fits:** Subscription apps: productivity, health, education, creative tools.
- **Avoid when:** Network-effect or long-discovery products, where freemium converts later. Hard paywalls before any value are hostile.
- **Implement:**
  - Trial: confirm the Play offer has a free phase before redesigning anything.
  - Paywall timing: in the first session, after one value moment.
  - Trial end: build reminders yourself (Android sends none).
  - In-app messaging: PBL 9.0.0 price-increase messages show at most once every 7 days.
  - Billing choice: `getBillingChoiceInfoAsync()` (PBL 9.1.0). Custom choice screens are allowed in the US, UK and EEA under Google's UX guidelines.
  - Early-access Play features: Mixed Carts (unified checkout sheet), multi-quantity seats.
- **Sources:** [56], [52], [53], [51], [54], [55]

## Fading — now looks dated
- **Hamburger navigation drawer** — No longer recommended in M3E; use the expanded navigation rail, which adapts across breakpoints. [10]
- **Tall baseline navigation bar** — Replaced by the shorter flexible/short navigation bar, which supports horizontal items in medium windows. [11]
- **Bottom app bar** — Superseded by the docked toolbar (shorter, more flexible) and the floating toolbar. [12]
- **Fixed easing+duration tweens** — Material treats easing and duration tokens as legacy; springs handle interruption and gestures better. [4]
- **Portrait-locked, letterboxed phone UI on tablets and foldables** — Ignored on sw≥600dp, with no opt-out at API 37. [15][18]
- **Opaque or colored system bars and `windowOptOutEdgeToEdgeEnforcement`** — Disabled from API 36. [17]
- **Back handling via `onBackPressed` with no preview** — Not called for targetSdk 36. [17]
- **New XML/View screens, Fragments, RecyclerView for new features** — Maintenance mode; Material Views 1.14.0 is the final feature release. [19][2]
- **Custom RemoteViews and colorized "fake live" notifications** — Ineligible for Live Updates and memory-capped at API 37. [30][15]
- **XML RemoteViews widgets with static preview images** — Glance with generated previews is the norm. [35][36]
- **Email OTP verification steps and re-login after switching phones** — Replaced by Verified Email and Restore Credentials; Play will require Zero-Tap Sign-In from April 2027. [57][59]
- **`READ_CONTACTS` or location permission walls for simple picks** — Use the contact picker and location button. [14]
- **Four-color, page-container icon style (Google's previous look)** — Google itself moved to single-hue gradients with distinct shapes. [43][44]

## Watchlist — verify next month
- Compose Material3 **1.5.0 stable**: promised "later in 2026"; beta01 shipped 2026-10-07. Check whether emphasized typography, `MaterialShapes` and `LoadingIndicator` reach stable (their promotion was reverted in alpha19). (early)
- **Compose Styles API** integration into Material components: announced as ongoing, still experimental. (early)
- **Android 17 QPR2** (API 37.2, in beta): secondary reports mention lock-screen blur, native App Lock, wider Dynamic Color and customizable Quick Settings. (unverified)
- **Samsung One UI 9 / 9.5 "glass" UI** and pill-shaped tabs from One UI 8.5. Leaks only; naming varies. (unverified)
- **Google apps on iOS** adopting Liquid Glass alongside M3E; Gemini "Neural Expressive" design-language name. (unverified)
- **Google Play "Optimized for large screens" badge** (announced 2026-05-19): actual store display and criteria, and whether large-screen tiers affect search ranking. (unverified)
- **Googlebook** ship date: pre-orders referenced, no confirmed date. **Wear OS 7** stable rollout ("later this year"). (unverified)
- **Play in-app subscription management API** ("coming soon" at I/O 2026) and the full rollout of retention/winback offers. (early)
- **material3-a2ui 1.0.0-alpha01** (2026-09-23) and the Compose A2UI renderer maturity. (early)
- **Compose for XR beta** ("soon") and Jetpack Compose Glimmer availability for display glasses. (early)
- **Gemini Intelligence** system UI on Pixel 11 (HiLight indicator, cross-app tasks). Press reports only; UI specifics unverified. (unverified)
- **Monitoring change:** the Android Developers Blog moved to developer.android.com/blog; update feeds. (verified 2026-10-15) [65]

## Sources
1. [What's new at Google I/O 2026](https://m3.material.io/blog/whats-new-at-io26) — Material Design, 2026-05-19
2. [Material Android is Compose-first](https://m3.material.io/blog/material-is-compose-first) — Material Design, 2026-05-19
3. [Compose Material 3 release notes](https://developer.android.com/jetpack/androidx/releases/compose-material3) — Android Developers, 2026-10-07
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
25. [Navigation 3 release notes](https://developer.android.com/jetpack/androidx/releases/navigation3) — Android Developers, 2026-10-07
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
50. [Meet Google Play's target API level requirement](https://developer.android.com/google/play/requirements/target-sdk) — Android Developers, 2026-10-16
51. [Google Play Billing Library release notes](https://developer.android.com/google/play/billing/release-notes) — Android Developers, 2026-06-18
52. [Driving growth on Google Play: The next era of subscriptions](https://android-developers.googleblog.com/2026/09/unlocking-Google-play-subscription-growth.html) — Android Developers Blog, 2026-09-29
53. [I/O 2026: What's new in Google Play](https://android-developers.googleblog.com/2026/05/io-2026-whats-new-in-google-play.html) — Android Developers Blog, 2026-05-19
54. [Expanded billing choice and lower fees on Google Play](https://android-developers.googleblog.com/2026/06/play-expanded-billing.html) — Android Developers Blog, 2026-06-24
55. [New ways to drive smarter discovery, deeper engagement, and business growth on Google Play](https://android-developers.googleblog.com/2026/10/new-tools-for-discovery-and-engagement.html) — Android Developers Blog, 2026-10-13
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
68. [Compose release notes (versions table)](https://developer.android.com/jetpack/androidx/releases/compose) — Android Developers, 2026-10-07
