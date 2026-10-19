---
platform: ios
period: 2026-10
researched_at: 2026-10-18
previous: null
sources: 63
---

# iOS — UI/UX trends · October 2026

## TL;DR
- Liquid Glass is no longer optional: the iOS 27 SDK ignores `UIDesignRequiresCompatibility`, and from April 2027 every App Store upload must be built with the iOS 27 SDK (min target iOS 15), so the opt-out ends with your next update after that date. [12][15]
- iOS 27 (shipped 2026-09-14) "tuned" the glass. It has higher contrast, crisper edges and a more opaque default scroll-edge effect, and users now set transparency themselves with a slider (Settings → Appearance → Liquid Glass). Design and QA across the whole range. [4][8][10]
- Brand color moves out of the bars and into the content. Use standard glass bars, keep the accent tint for meaning, and put full-bleed media underneath. Opaque brand-colored nav and tab bars now look dated. [19][33]
- The iPhone is now a resizable, foldable surface. iPhone Duo goes on sale in the US on 2026-10-23, and iOS 27 apps resize. Build on size classes, toolbar `visibilityPriority`, the system `ToolbarOverflowMenu`, and vertical bars on Duo. [17][31][47]
- A new bottom-trailing "prominent" slot (`Tab(role: .prominent)`) holds search or your primary action, and nav bars as well as tab bars now minimize on scroll. [17][18][20]
- Siri AI makes App Intents, App Schemas, indexed entities and on-screen entity annotations the new discoverability layer for iOS apps. [3][23]
- Icons: reopen your `.icon` in the 2026 Icon Composer. It has sharper specular highlights and new refraction controls, and you should lower translucency. Tinted and clear appearances are judged harder now. [22][42]

## Platform baseline (expected now, not a trend)
- **iOS 26 SDK required since 2026-04-28. iOS 27 SDK and iOS 15+ deployment target required from April 2027.** Apple has published only the month, not the day. Xcode 27 RC builds have been accepted since September 2026. Plan the Liquid Glass migration as a hard deadline, not a nice-to-have. [14][15][61][63]
- **`UIDesignRequiresCompatibility` is dead for new builds.** The system ignores the key when you build for iOS 27 or later. An Apple DTS engineer confirmed it is still honored for apps linked against the iOS 26 SDK, even on iOS 27 devices. That is a temporary loophole that closes in April 2027. [12][13]
- **iOS 27 is the shipping OS.** It was released 2026-09-14 and runs on iPhone 11 and later. iOS 26 was on 79% of all iPhones and 86% of iPhones from the last four years as of 2026-06-07. Apple has published no iOS 27 adoption figure yet. In practice you support iOS 26 and 27 and design glass-first. [5][6][16]
- **UIScene lifecycle is mandatory.** Apps built with the latest SDK that lack a scene delegate won't launch. `UIScreen.main`, interface idiom and interface orientation are no longer valid layout inputs, because iPhone apps resize (iPhone Mirroring, iPad, iPhone Duo). [18]
- **Liquid Glass transparency slider plus accessibility modes.** Standard and custom glass responds to the user's slider, Reduce Transparency and Increase Contrast. Clear glass needs a ~35% dimming layer over bright media. [17][29]
- **Dynamic Type everywhere, including custom fonts.** Body text defaults to 17 pt with an 11 pt minimum. The Dynamic Type spec now lists emphasized weights, and custom fonts must support Bold Text. Wrap text instead of truncating it. [19][35]
- **Dark Mode plus clear and tinted appearances.** Icons need default, dark, clear light/dark and tinted light/dark looks. Widgets need full-color, accented (tinted or clear glass) and vibrant modes. [32][37]
- **The automatic scroll-edge effect has new, more opaque visuals.** Beta coverage describes a hard blur with a bottom border. iOS 26's soft fade is now opt-in (`.soft`). Re-check any overrides. [10][18][34]
- **Accessibility Nutrition Labels and the age-rating questionnaire.** Declaring accessibility support in App Store Connect is optional but surfaces on the product page. The new age-rating answers have been required since 2026-01-31. [14][15]
- **App Store product-page header and search-result hero image or video.** This is new for iOS 27 and is managed through the Asset Library in App Store Connect. Apple said "this fall", and Adapty reports the tools were turned on 2026-10-05. Confirm in App Store Connect. [28][60]
- **Design kits.** The iOS/iPadOS 27 Figma kit was published 2026-09-17, alongside iPhone 18 and iPhone Duo bezels. [1]

## Trends

### ios-liquid-glass-tuned-contrast — Tuned Liquid Glass (contrast-first glass and a user transparency slider)
- **Status:** mainstream
- **Momentum:** new
- **What:** iOS 27 reworked Liquid Glass after a year of legibility complaints. Complex content behind bars is diffused more, edges are more defined (borders and darker rims instead of drop shadows), specular highlights are brighter, glass is lighter in dark mode, and prominent glass buttons get better default tints. Users choose anything from ultra-clear to fully tinted. The default is the midpoint, and the fully tinted end is effectively opaque. [4][7][8][9][10]
- **Seen in:** Apple Podcasts, the App Store and Messages (system examples of the slider and the legibility fix), and Google Photos, which ships its own "Default / More clear" translucency toggle. [8][9][49]
- **Fits:** Every app that uses standard bars. It matters most for media, photo, map and content-heavy apps where glass sits over busy imagery.
- **Avoid when:** Don't rely on "clear" glass over text-heavy or low-contrast content. Don't stack glass on glass. Expect older adults and low-vision users to set the slider toward tinted, so your custom glass must not lose hierarchy when it turns opaque. [29][59]
- **Implement:** Use `.glassEffect(.regular)` as the default and `Glass.clear` only over photos or video, with a ~35% black dim when the media is bright. Use `.buttonStyle(.glass)` and `.glassProminent`. In UIKit use `UIButton.Configuration.glass()` and `.prominentGlass()`, plus `UIGlassEffect`. Remove hand-made shadows and blurs behind bars. Test at both slider extremes and with Reduce Transparency and Increase Contrast. Keep `.scrollEdgeEffectStyle(.automatic, for:)` unless `.soft` is tested legible. [17][29][34][39][40]
- **Sources:** [4], [7], [8], [9], [10], [17], [29], [34], [59]

### ios-native-first-components — Native-first chrome (big brands drop custom bars)
- **Status:** rising
- **Momentum:** new
- **What:** In 2026 the largest apps moved their navigation chrome onto system Liquid Glass components and kept customization for content. Apps that half-migrated, especially those that kept a custom bottom bar, now visibly clash with the OS. [19][50]
- **Seen in:** WhatsApp (glass tab bar and Chats top bar rolled out more widely in May 2026), Instagram (floating translucent tab bar that shrinks on scroll, staged rollout in May 2026), Google Photos and Google Health (glass bottom bars layered on Material 3 Expressive, September 2026), and Spotify 9.1.90 (glass top bar and menus, but the custom bottom bar was kept and criticized). [49][50][51][52]
- **Fits:** Utility, social, messaging and productivity apps, and any app whose users switch between many iOS apps a day.
- **Avoid when:** Games and fully immersive or creative canvases can stay custom. Even then, keep iOS sizes, placements and popover behaviors. Slack's custom toolbar is Apple's example. [19]
- **Implement:** Use `TabView`/`Tab`, `NavigationStack`, `.toolbar`, `.searchable` and system sheets and menus. When a custom layout is unavoidable, keep the native behaviors. iOS 27 adds `.swipeActions` on any scroll content via `.swipeActionsContainer()`, `.reorderable()` with `.reorderContainer(for:)`, and item-bound `confirmationDialog(_:item:)` and `alert(_:item:)`. [17][44]
- **Sources:** [17], [19], [44], [49], [50], [51], [52]

### ios-brand-in-content-layer — Brand expressed in the content layer, not the chrome
- **Status:** rising
- **Momentum:** new
- **What:** Apple's 2026 branding guidance says to apply the accent color sparingly, to primary actions, status, unread badges and the selected tab. Move brand color into the scrolling content so glass controls pick it up dynamically. Express identity through full-bleed media, voice, custom display type and custom icons rather than painted bars or logos. [19][33]
- **Seen in:** Crumbl (pink moved from the toolbar into content, weekly hero video, Crumbl Sans for headers), Slack (tint only for primary and unread items), NYT Cooking (logo only on Home, fading on scroll, custom line icons), Gentler Streak (hierarchy from SF Rounded and width variants), and Moonlitt (edge-to-edge gradient and 3D moon; 2026 ADA winner, Interaction). [19][48][58]
- **Fits:** Consumer brands, food and retail, media, and wellness. It is the default answer to "how do we keep our brand under Liquid Glass".
- **Avoid when:** Don't color tab labels the same as a colorful content layer; go monochrome bars instead. Don't use a brand typeface for body copy at small sizes. [30][33]
- **Implement:** Use `.tint(brandAccent)` once at the root, not `.toolbarBackground(brandColor, for: .navigationBar)`. Place hero media under bars with `backgroundExtensionEffect()` (UIKit: `UIBackgroundExtensionView`). For custom fonts use `Font.custom(_:size:relativeTo:)` for headlines only, with system fonts for body. Ship a real Dark Mode palette, and carry the palette into widgets. [19][33][39]
- **Sources:** [19], [30], [33], [39], [48], [58]

### ios-concentric-geometry — Concentric, hardware-matched corner geometry
- **Status:** mainstream
- **Momentum:** new
- **What:** Corners nest concentrically from the device bezel through sheets, cards and controls. Hard-coded radii that fight the system's rounding now read as off-platform, especially on custom sheets, Live Activities and widgets. [19][36]
- **Seen in:** Moonlitt (custom calendar on a glass backing with concentric sheet edges matching the hardware), Apple's system sheets, and Live Activities guidance. [19][36]
- **Fits:** Custom cards, sheets, floating panels, widgets, Live Activities, and in-app media frames.
- **Avoid when:** Dense data tables and editorial layouts can stay square. Don't round everything into pills, because iOS 27 itself toned down overly round corners and sidebar bezels. [11]
- **Implement:** Use `ConcentricRectangle` and `Shape.rect(corners:isUniform:)` in SwiftUI, `ContainerRelativeShape` inside widgets and Live Activities, and `UIView.cornerConfiguration` with `UICornerConfiguration` in UIKit. Keep even margins between nested shapes. Live Activity Lock Screen content uses 14 pt standard margins. [36][39]
- **Sources:** [11], [19], [36], [39]

### ios-minimizing-bars-on-scroll — Bars that get out of the way on scroll
- **Status:** mainstream
- **Momentum:** new
- **What:** iOS 26 introduced tab bars that minimize on scroll, with an inline bottom accessory such as a mini-player. iOS 27 extends this to navigation bars and lets one prominent tab stay visible while the bar collapses. [17][18][30]
- **Seen in:** Apple Music (MiniPlayer and minimized tab bar), Instagram (tab bar shrinks on scroll), and Apple's iOS 27 SwiftUI sample apps. [17][30][52]
- **Fits:** Feeds, reading, media, maps, and any long scrolling content.
- **Avoid when:** Task flows and forms where controls must stay visible. NN/g flagged appearing and disappearing controls as hurting learnability, so don't hide primary actions. [59]
- **Implement:** Use `.tabBarMinimizeBehavior(.onScrollDown)` and `.tabViewBottomAccessory { }`. iOS 27 adds `.toolbarMinimizeBehavior(.onScrollDown, for: .navigationBar)`. In UIKit, use `UITabBarController` `MinimizeBehavior` and `prominentTabIdentifier`, plus `UINavigationItem.barMinimizeBehavior` and `barMinimizationSafeAreaAdjustment`. Apple's own session spells these inconsistently, so check the docs. [17][18][45]
- **Sources:** [17], [18], [30], [45], [52], [59]

### ios-toolbar-priority-overflow — Prioritized toolbars with a system overflow menu
- **Status:** emerging
- **Momentum:** new
- **What:** Bars must now survive many widths, including narrow resizable windows, side-by-side windows and vertical bars on iPhone Duo. iOS 27 lets you rank items, pin one trailing action, and push the rest into a single system overflow menu instead of a custom "…" menu. [17][31]
- **Seen in:** Apple Mail (Compose kept visible), Apple Notes (New Note kept visible) and Apple Calculator (full-width layout without bars on Duo). These are Apple's reference apps in the Duo guidance. [31]
- **Fits:** Editors, productivity, creation tools, and any screen with more than three toolbar actions.
- **Avoid when:** Text-only bar buttons, which stay horizontal and won't compress. Don't use custom ellipsis menus. Don't override the default vertical placement on Duo. [31]
- **Implement:** Wrap related items in `ToolbarItemGroup { }.visibilityPriority(.high)`. Use `ToolbarOverflowMenu { }`, `ToolbarItem(placement: .topBarPinnedTrailing)` and `ToolbarSpacer`. Give every item a `Label(title, systemImage:)`, because the title is used in overflow. In UIKit, use `UIBarButtonItem.visibilityPriority`, `UINavigationItem.additionalOverflowItems` and `UIMenuElement.preferredImageVisibility`. On Duo, choose `ToolbarVerticalCompressionBehavior` (task screens keep the toolbar, navigation screens keep the tabs). [17][31][45][46]
- **Sources:** [17], [31], [45], [46]

### ios-bottom-trailing-prominent-slot — Bottom-trailing prominent tab for search or primary action
- **Status:** emerging
- **Momentum:** new
- **What:** The separated trailing tab that iOS 26 reserved for search is generalized in iOS 27 as a `prominent` role usable for any tab, such as Create or Cart. Apple's 2026 search guidance puts search at the bottom: a bottom-toolbar field, a standard Search tab for exploration, or a prominent tab that opens the keyboard immediately for known-item search. [10][17][20]
- **Seen in:** Apple Phone (prominent search tab), Apple TV (standard search tab with a browse landing page), Apple Mail (search button that expands into a bottom field), and Apple Music (inline library-scoped search). [20]
- **Fits:** Commerce (Cart or Sell), creation apps (New post), and catalog or content apps where search is the main entry point.
- **Avoid when:** Using the slot for a destination that isn't the main action. Tab bars are for navigation, not actions, so a "+" that opens a modal belongs in a toolbar unless it is truly a section. Bloomberg reported Apple folding search back into regular tabs in some apps (see Watchlist). [30][57]
- **Implement:** Use `Tab(role: .prominent) { … }` (iOS 27) or `Tab(role: .search)` (iOS 26), and `prominentTabIdentifier` in UIKit. Show recent searches inline on focus, with swipe-to-delete and Clear All. Use scope bars or filter chips, and treat tokens only as an addition to visible filters. For empty results use `ContentUnavailableView.search(text:)`. [18][20][44]
- **Sources:** [10], [17], [18], [20], [30], [44], [57]

### ios-resizable-foldable-layouts — Resizable iPhone apps and foldable-ready layouts
- **Status:** emerging
- **Momentum:** new
- **What:** iOS 27 makes iPhone apps resizable, and iPhone Duo (7.6" inner and 5.4" outer displays, US availability 2026-10-23) adds poses, a fold, two cameras and toolbars and tab bars on the vertical axis. Apps that use size classes and system containers adapt almost for free. Apps that use fixed widths or lock to portrait break. [17][31][47]
- **Seen in:** Apple Mail (list on the outer display, list plus message on the inner display), Apple Notes (split panes rebalance when partly folded), and Apple Calculator (5×4 grid on the outer display). [31]
- **Fits:** Every app. Reading, mail, notes, commerce and media get the most from the inner display's extra hierarchy level.
- **Avoid when:** Don't design a bespoke layout per pose. Don't put navigation containers inside arrangement views. Avoid extreme rearrangement when the device folds. [31][46]
- **Implement:** Use `horizontalSizeClass` and local geometry, never idiom, orientation or `UIScreen.main`. Use `NavigationSplitView` or `UISplitViewController`, and `ArrangementView` or `UIArrangementViewController` for two-view layouts. Use `ReservedRegion` to avoid the fold and cameras, and `onHingeChange` or `UIHingeInteraction` for hinge state. Prefer even grid columns. Build with Xcode 27.1 or later for full-screen Duo support and test poses in Device Hub. Use `windowScene.effectiveGeometry` for available space. [18][31][46]
- **Sources:** [17], [18], [31], [46], [47]

### ios-purposeful-morph-motion — Purposeful morphing and zoom motion
- **Status:** mainstream
- **Momentum:** new
- **What:** Motion is used to explain spatial relationships: glass shapes morph between states, tapped items zoom into detail views, and springs add emphasis. Apple frames delight as the result of craft rather than decoration, with no confetti. Dropped frames and late loads count as brand damage. [19][21]
- **Seen in:** NYT Cooking (zoom transitions tied to the tap target), Gentler Streak (spring emphasis), and Apple Music (tab bar to MiniPlayer morph). [19][30]
- **Fits:** Content browsing, media, fitness and habit apps, and any app that uses glass controls that change state.
- **Avoid when:** Motion for its own sake, which NN/g criticized in iOS 26. With Reduce Motion on, swap movement for fades. Live Activity animations are capped at 2 s and don't run on reduced-luminance Always-On displays. [36][59]
- **Implement:** Use `GlassEffectContainer` with `glassEffectID(_:in:)`, `glassEffectUnion` and `glassEffectTransition` for morphs, and `Glass.interactive()` for touch response. Use `.navigationTransition(.zoom(sourceID:in:))`, plus the new iOS 27 `.navigationTransition(.crossFade)`. Use SF Symbols Draw On/Off and Magic Replace, and `@Environment(\.accessibilityReduceMotion)`. Use haptics through `.sensoryFeedback(_:trigger:)` only on meaningful state changes. [17][40][41][44]
- **Sources:** [17], [19], [21], [30], [36], [40], [41], [44], [59]

### ios-layered-glass-icons — Layered Liquid Glass app icons, second generation
- **Status:** mainstream
- **Momentum:** new
- **What:** Icons are layered `.icon` files built in Icon Composer, rendered by the system with specular highlights, refraction, translucency and shadows across six iOS appearances. The 2026 Icon Composer (announced as "Icon Composer 2 beta") adds refraction controls, sharper inside/outside specular highlights, a vertical light angle and chromatic or neutral shadows. iOS 27 reduces default translucency and draws icons sharper. [1][22][32][42][43]
- **Seen in:** Apple Podcasts (plus-lighter blend on a dark background), Apple Maps (sharper layered icon in iOS 27), and Apple Photos (the HIG's reference layered icon). [7][22][32]
- **Fits:** All apps. Brands with flat 2D marks can add material presence through layer separation instead of fake 3D.
- **Avoid when:** Photos, text, thin lines, feathered edges, or baked-in gloss and shadows. Clear-mode icon glass ignores the user slider, so contrast must come from the artwork. [22][32]
- **Implement:** Use a 1024×1024 px square canvas with full-canvas SVG or PDF layers (PNG for raster or mesh gradients). Group layers that share glass settings. Set specular to inside when the foreground is darker than the background and outside when the background is darker. Reduce translucency, keep part of the foreground white or near-white for tint mode, and give the mono annotation a high dynamic range. Put the `.icon` file next to the asset catalog and remove the old asset-catalog icon. Requires macOS Tahoe 26.4 or later. [22][32][42]
- **Sources:** [1], [7], [22], [32], [42], [43]

### ios-siri-ai-app-schemas — Siri AI-ready apps (App Schemas, indexed entities, on-screen context)
- **Status:** emerging
- **Momentum:** new
- **What:** Siri AI (beta, English first, opened by swiping down from the Dynamic Island) answers questions using on-screen content and acts across apps. Third-party apps take part by modeling content as App Entities with schemas, indexing them semantically, and annotating what's on screen. This replaces "deep links plus Shortcuts" as the system-integration baseline. [3][5][23]
- **Seen in:** Apple Messages, Mail and Photos (system schema domains that Siri AI understands), and the Ask Siri button that appears automatically in UIKit menus when relevant content exists. Named third-party adopters are not verified yet. [18][23]
- **Fits:** Messaging, notes, docs, tasks, photos, commerce catalogs, travel, and fitness: apps with clear nouns (entities) and verbs (intents).
- **Avoid when:** Exposing destructive or irreversible actions without confirmation. Siri AI isn't yet available in the EU (iOS) or China. [3][38]
- **Implement:** Use `@AppEntity(schema: .messages.message)` and the equivalent for your domain, `IndexedEntity` with `@Property(indexingKey:)`, and `EntityStringQuery` for server-side data. Annotate on-screen content with `.appEntityIdentifier(EntityIdentifier(for:identifier:))` and `NSUserActivity`. Use `Transferable` with `IntentValueRepresentation`, `SyncableEntity` for cross-device continuity, and `RelevantEntities` for proactive suggestions. `LongRunningIntent` automatically shows a Live Activity with a stop button. Test with AppIntentsTesting. Follow the new HIG Snippets and App Shortcuts (app schemas) pages for result UI. [1][23][24]
- **Sources:** [1], [3], [5], [18], [23], [24], [38]

### ios-glanceable-surfaces-everywhere — Glanceable surfaces beyond the app (widgets and Live Activities across contexts)
- **Status:** rising
- **Momentum:** new
- **What:** One widget or Live Activity now renders in many places. Widgets appear on the Home Screen (full color, tinted or clear glass), the Lock Screen, StandBy, CarPlay, Mac, Apple Watch and Apple HomeView (launching 2026-11-13). Live Activities appear in a Dynamic Island that now also shows in landscape, plus CarPlay, the Mac menu bar and Watch. iOS 27 adds an extra-large portrait widget size. [7][25][26][36][37][56]
- **Seen in:** Apple Calendar, Photos and Music (extra-large widgets that fill a Home Screen page), Crumbl (branded pastel widgets), and the Apple Timer Live Activity (live data in the minimal presentation). [7][19][36]
- **Fits:** Delivery, rideshare, sports, travel, fitness, finance tickers and media: anything with a defined start and end or a glanceable status.
- **Avoid when:** Ads or promos in Live Activities, which the HIG forbids. Showing sensitive data on the Lock Screen. Full-color images in tinted or clear modes (keep them for album art). Interactive controls in CarPlay layouts, where they are disabled. [36][37]
- **Implement:** Use `systemExtraLargePortrait` (iOS/iPadOS 27), `.widgetAccentable()` and `.widgetAccentedRenderingMode(.fullColor)` for media only. Read `@Environment(\.isDynamicIslandLimitedInWidth)` and fit compact and minimal views into a 28 pt circle. Use `.supplementalActivityFamilies([.small])` for Watch and CarPlay, `activityBackgroundTint`, `LiveActivityIntent` buttons, and `ContainerRelativeShape`. End activities promptly with a 15–30 minute dismissal. [25][26][36][37]
- **Sources:** [7], [19], [25], [26], [36], [37], [56]

### ios-genai-refine-feedback-ux — Generative-AI UX with refine, retry and honest progress
- **Status:** rising
- **Momentum:** new
- **What:** As on-device and Private Cloud Compute models spread (the 2026 Foundation Models framework adds a rebuilt on-device model, image input, and PCC access at no API cost below 2M first-time downloads), Apple's June 2026 HIG update standardizes how AI output is presented. Put Edit, Undo, Retry and Adjust next to results, acknowledge corrections, show specific progress text, offer alternatives, and collect voluntary thumbs up or down. [2][38][62]
- **Seen in:** Apple Image Playground (multiple variants, coaching on blocked prompts), Apple Photos Clean Up (Fast, High Quality and Auto modes), and Apple Writing Tools (inline drafting and proofreading). [3][6][7][38]
- **Fits:** Writing, photo and video editing, summarization, recipe and travel planning, and coaching.
- **Avoid when:** The output is factual, health-related or irreversible without confirmation. You have no non-AI fallback when the model is unavailable because of device, region, battery or network. Never let AI pass as human. [21][38]
- **Implement:** Label AI features clearly. Replace "Processing…" with task-specific copy, such as "Summarizing key themes from your notes". Keep refine controls adjacent to the output. Check model availability before showing the entry point (FoundationModels `SystemLanguageModel.default.availability`). Use `Attachment(...)` for image prompts and `PrivateCloudComputeLanguageModel` for heavier tasks, and budget tokens with `contextSize` and `tokenCount(for:)`. Design a loading or background state for latency, and disclose any server processing. [38][62]
- **Sources:** [2], [3], [6], [7], [21], [38], [62]

### ios-value-first-onboarding-late-paywall — Value-first onboarding with a late paywall and transparent plans
- **Status:** mainstream
- **Momentum:** new
- **What:** Paywalls sit at the end of onboarding, after a value moment or a "plan ready" summary. In a 40-flow sample, the median relative position was 0.894, none opened with a paywall, and 77.5% were in the final third. The share of apps using trials of 4 days or less rose to 46.5%, yet 55.4% of 3-day-trial cancellations happen on Day 0, which pushes teams to get users to the "aha" moment in the first session. Apple's new monthly-billed 12-month commitment plan adds a new price layout to design. [27][53][54]
- **Seen in:** Instacart, Grammarly, Up Ahead and ChargePoint (tracked late-paywall flows), and Adobe, the early-paywall outlier at step 3 of 13. [54]
- **Fits:** Subscription consumer apps (wellness, language, productivity, AI tools). Personalization quizzes are a deliberate bet, found in only ~16% of ~751 apps and concentrated in wellness and language. [55]
- **Avoid when:** A paywall on screen 1, or quiz questions that don't change anything. Don't hide the total commitment price; the App Store shows its own disclosure sheet once per account. [27][55]
- **Implement:** Use `SubscriptionStoreView` with `.preferredSubscriptionPricingTerms { … billingPlanType == .monthly }`. In custom UI show `pricingTerms.billingDisplayPrice` together with `commitmentInfo.price`, and purchase with `.billingPlanType(.monthly)` (iOS 26.5 SDK, OS 26.4 or later). Use `.manageSubscriptionsSheet`, and replace legacy offer-code calls with `offerCodeRedemption(options:isPresented:)`. A/B test 7-day or longer trials against 3-day ones. Make sure the paywall close button is visible over custom backgrounds. [10][27][53]
- **Sources:** [10], [27], [53], [54], [55]

## Fading — now looks dated
- **Opaque, brand-colored navigation and tab bars** — Apple now explicitly moves brand color into the content layer. Painted bars fight Liquid Glass and look like iOS 18. [19][33]
- **Custom bottom tab bars beside system glass** — half-migrated apps show the clash (Spotify's custom bottom bar was singled out in October 2026). [50]
- **Logos in nav bars and branded splash or launch screens** — the HIG says launch screens are not for branding and logos waste space. Logo-only-on-Home (NYT Cooking) is the new norm. [19][33]
- **Glass in the content layer** (glass cards, glass list rows, glass on glass) — the HIG reserves glass for the control layer, and overuse muddies hierarchy. [29]
- **iOS 26.0-style maximal clear glass and soft fades over busy content** — iOS 27 moved the default to higher contrast and a more opaque scroll edge after NN/g-style legibility criticism. [7][10][59]
- **Baked-in icon effects** (pre-rendered gloss, shadows, bevels, photos, text) **and flat single-layer icons** — the system now renders material dynamically, and static effects look muddy in tinted or clear modes. [22][32]
- **Portrait-locked, idiom- or orientation-based layouts and `UIScreen.main`** — these break on resizable iPhone apps and iPhone Duo. [18][31]
- **Custom "…" overflow menus and text-only bar buttons** — they should be replaced by `ToolbarOverflowMenu` and symbol-plus-title items. [31]
- **Hard-coded corner radii on sheets, cards and Live Activities** — non-concentric corners read as off-platform. [36]
- **A top-of-screen search bar as the iPhone default** — Apple's 2026 guidance prefers the bottom toolbar or a search tab, with the top only when the bottom is blocked. [20]
- **`UIDesignRequiresCompatibility` as a strategy** — it is ignored for iOS 27 SDK builds, which become mandatory in April 2027. [12][15]
- **Paywall-first onboarding with a 3-day trial on screen 1** — Day-0 cancellations dominate, and late paywalls are the norm. [53][54]
- **"Confetti" delight bolted on at the end** — Apple's 2026 principles reframe delight as the outcome of craft. [21]

## Watchlist — verify next month
- Search tab merged back into the regular tab group in Apple's Podcasts, TV, Music, Health and News, reported by Bloomberg before WWDC [57]. Whether this shipped in iOS 27 is unverified.
- iOS 27 adoption numbers. Apple has published none yet, and it usually publishes early in the year. Unverified.
- Exact April 2027 date for the iOS 27 SDK requirement [15][61]. Apple has given only the month. Unverified.
- Apple HomeView (launching 2026-11-13) as a third-party widget surface. The developer agreement mentions CarPlay apps and widgets on HomeView [56], but which third-party widgets appear is unverified.
- YouTube and YouTube Music Liquid Glass UI and Live Activities, seen in feature flags (Android Authority, 2026-08-26). Unverified.
- Gmail and Google Maps adoption of Liquid Glass. They had not adopted it as of 2026-09-26 [49]. Watch for an update.
- Full WhatsApp chat-screen and bubble redesign completion. Rollout is staggered [51]. Partly verified.
- SF Symbols naming: announced as "SF Symbols 8 beta" in June 2026 [1][43], but the current download is named "SF-Symbols-27" [41]. Version branding is unverified.
- Exact App Store header and search-image specs (a 16:9 PNG at 5244×2950 was cited in a secondary summary), and confirmation that the tools are live in all storefronts [28][60]. Unverified.
- Bundles and Suites subscription program details, due "later in 2026" [27]. Early.
- Siri AI language and region expansion (EU on iOS, more languages) [3]. Early.
- A public API for reading the user's Liquid Glass slider position: none found. Unverified.
- Claim that iOS 27 removed the tilt-based icon shimmer (WebProNews secondary report). Unverified.

## Sources
1. [What's new — Design](https://developer.apple.com/design/whats-new/) — Apple Developer, 2026-10-13
2. [Apple unveils next generation of Apple Intelligence, Siri AI, and more](https://www.apple.com/newsroom/2026/06/apple-unveils-next-generation-of-apple-intelligence-siri-ai-and-more/) — Apple Newsroom, 2026-06-08
3. [Apple introduces Siri AI, a profoundly more capable and personal assistant](https://www.apple.com/newsroom/2026/06/apple-introduces-siri-ai-a-profoundly-more-capable-and-personal-assistant/) — Apple Newsroom, 2026-06-08
4. [iOS 27](https://www.apple.com/os/ios/) — Apple, accessed 2026-10-18
5. [Apple confirms iOS 27 release date: September 14](https://9to5mac.com/2026/09/09/apple-confirms-ios-27-release-date-september-14/) — 9to5Mac, 2026-09-09
6. [Apple Releases iOS 27 and iPadOS 27 With Siri AI and Liquid Glass Update](https://www.macrumors.com/2026/09/14/apple-releases-ios-27/) — MacRumors, 2026-09-14
7. [iOS 27: Everything We Know](https://www.macrumors.com/roundup/ios-27/) — MacRumors, 2026-09-14
8. [iOS 27 adds new Liquid Glass slider on iPhone, here's what it lets you do](https://9to5mac.com/2026/06/15/ios-27-adds-new-liquid-glass-slider-on-iphone-heres-what-it-lets-you-do/) — 9to5Mac, 2026-06-15
9. [iOS 27 fixes Liquid Glass, and not just with a slider](https://9to5mac.com/2026/06/12/ios-27-fixes-liquid-glass-and-not-just-with-a-slider/) — 9to5Mac, 2026-06-12
10. [What Designers Need to Know About iOS 27](https://designfornative.com/what-designers-need-to-know-about-ios-27/) — Design for Native, 2026-06-10
11. [WWDC 2026 recap: iOS 27, all-new Siri, Liquid Glass fixed, and more](https://www.tapsmart.com/news/wwdc26-recap/) — TapSmart, 2026-06-08
12. [UIDesignRequiresCompatibility](https://developer.apple.com/documentation/bundleresources/information-property-list/uidesignrequirescompatibility) — Apple Developer Documentation, accessed 2026-10-18
13. [Clarification on the planned removal of UIDesignRequiresCompatibility](https://developer.apple.com/forums/thread/832543) — Apple Developer Forums (DTS reply, June 2026), accessed 2026-10-18
14. [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) — Apple Developer, accessed 2026-10-18
15. [Submit your iOS apps to the App Store](https://developer.apple.com/ios/submit/) — Apple Developer, accessed 2026-10-18
16. [Apple Reveals How Many iPhones Were Running iOS 26 Before WWDC](https://www.macrumors.com/2026/06/09/ios-26-adoption-stats-wwdc/) — MacRumors, 2026-06-09
17. [What's new in SwiftUI (WWDC26 session 269)](https://developer.apple.com/videos/play/wwdc2026/269/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
18. [Modernize your UIKit app (WWDC26 session 278)](https://developer.apple.com/videos/play/wwdc2026/278/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
19. [Communicate your brand identity on iOS (WWDC26 session 251)](https://developer.apple.com/videos/play/wwdc2026/251/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
20. [Design intuitive search experiences (WWDC26 session 292)](https://developer.apple.com/videos/play/wwdc2026/292/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
21. [Principles of great design (WWDC26 session 250)](https://developer.apple.com/videos/play/wwdc2026/250/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
22. [Icon Composer for Beginners Group Lab (WWDC26 session 8012)](https://developer.apple.com/videos/play/wwdc2026/8012/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
23. [Build intelligent Siri experiences with App Schemas (WWDC26 session 240)](https://developer.apple.com/videos/play/wwdc2026/240/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
24. [Discover new capabilities in the App Intents framework (WWDC26 session 345)](https://developer.apple.com/videos/play/wwdc2026/345/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
25. [Live Activities essentials (WWDC26 session 223)](https://developer.apple.com/videos/play/wwdc2026/223/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
26. [WidgetKit foundations (WWDC26 session 277)](https://developer.apple.com/videos/play/wwdc2026/277/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
27. [What's new in Apple In-App Purchase (WWDC26 session 210)](https://developer.apple.com/videos/play/wwdc2026/210/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
28. [Enhance your presence on the App Store (WWDC26 session 205)](https://developer.apple.com/videos/play/wwdc2026/205/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
29. [HIG: Materials](https://developer.apple.com/design/human-interface-guidelines/materials) — Apple Developer, accessed 2026-10-18
30. [HIG: Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) — Apple Developer, 2026-06-08
31. [HIG: Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) — Apple Developer, 2026-09-09
32. [HIG: App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) — Apple Developer, 2026-06-08
33. [HIG: Branding](https://developer.apple.com/design/human-interface-guidelines/branding) — Apple Developer, 2026-09-09
34. [HIG: Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views) — Apple Developer, 2026-06-08
35. [HIG: Typography](https://developer.apple.com/design/human-interface-guidelines/typography) — Apple Developer, 2025-12-16
36. [HIG: Live Activities](https://developer.apple.com/design/human-interface-guidelines/live-activities) — Apple Developer, 2026-10-13
37. [HIG: Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets) — Apple Developer, 2026-10-13
38. [HIG: Generative AI](https://developer.apple.com/design/human-interface-guidelines/generative-ai) — Apple Developer, 2026-06-08
39. [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) — Apple Developer Documentation, accessed 2026-10-18
40. [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views) — Apple Developer Documentation, accessed 2026-10-18
41. [SF Symbols](https://developer.apple.com/sf-symbols/) — Apple Developer, accessed 2026-10-18
42. [Icon Composer](https://developer.apple.com/icon-composer/) — Apple Developer, accessed 2026-10-18
43. [Apple lance SF Symbols 8 et Icon Composer 2 pour les développeurs](https://iphonesoft.fr/2026/06/15/apple-sf-symbols-8-icon-composer-2-developpeurs) — iPhoneSoft, 2026-06-15
44. [What is new in SwiftUI after WWDC26](https://swiftwithmajid.com/2026/06/08/what-is-new-in-swiftui-after-wwdc26/) — Swift with Majid, 2026-06-08
45. [iOS 27: Notable UIKit Additions](https://swiftjectivec.com/iOS-27-Notable-UIKit-Additions/) — Swiftjectivec (Jordan Morgan), 2026-06-08
46. [iPhone Duo First Developer Good to Knows](https://swiftjectivec.com/iPhone-Duo-First-Developer-Good-to-Knows/) — Swiftjectivec (Jordan Morgan), 2026-09-09
47. [Apple unveils iPhone Duo](https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/) — Apple Newsroom, 2026-09-09
48. [Apple reveals winners of the 2026 Apple Design Awards](https://www.apple.com/newsroom/2026/06/apple-reveals-winners-of-the-2026-apple-design-awards/) — Apple Newsroom, 2026-06-02
49. [Google combines Material 3 Expressive & Liquid Glass on the iPhone](https://9to5google.com/2026/09/26/material-3-liquid-glass/) — 9to5Google, 2026-09-26
50. [Spotify adopte enfin Liquid Glass, mais fait le minimum sur iPhone](https://iphonesoft.fr/2026/10/09/spotify-adopte-enfin-liquid-glass-minimum-iphone) — iPhoneSoft, 2026-10-09
51. [WhatsApp rollt Liquid Glass auf iOS jetzt breiter aus](https://www.apfelpatient.de/news/whatsapp-rollt-liquid-glass-auf-ios-jetzt-breiter-aus) — Apfelpatient, 2026-05-16
52. [Instagram : le Liquid Glass arrive doucement, la version iPad remaniée](https://www.igen.fr/app-store/2026/05/instagram-le-liquid-glass-arrive-doucement-la-version-ipad-remaniee-156005) — iGeneration, 2026-05-11
53. [The State of Subscription Apps in 10 minutes: lessons, trends, and benchmarks for 2026](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026) — RevenueCat, 2026-03-19
54. [How far into onboarding do apps place the paywall?](https://www.lazyweb.com/research/how-far-into-onboarding-do-apps-place-the-paywall) — Lazyweb Research, 2026-07-07
55. [How many apps run a personalization quiz during onboarding?](https://www.lazyweb.com/research/how-many-apps-use-onboarding-personalization-quiz) — Lazyweb Research, 2026-07-07
56. [Apple HomeView Has These 15 Apps, Some CarPlay Apps and Widgets Also Supported](https://www.macrumors.com/2026/10/14/apple-homeview-apps-carplay/) — MacRumors, 2026-10-14
57. [iOS 27 to make key design changes to streamline Liquid Glass: report](https://9to5mac.com/2026/05/12/ios-27-to-make-key-design-changes-to-streamline-liquid-glass-report/) — 9to5Mac, 2026-05-12
58. [Apple spotlights third-party apps adopting Liquid Glass in iOS 26 and more](https://9to5mac.com/2025/11/06/apple-spotlights-third-party-apps-adopting-liquid-glass-in-ios-26-and-more/) — 9to5Mac, 2025-11-06
59. [Liquid Glass Is Cracked, and Usability Suffers in iOS 26](https://www.nngroup.com/articles/liquid-glass/) — Nielsen Norman Group, 2025-10-10
60. [App Store creative assets: what's new in iOS 27](https://adapty.io/blog/app-store-creative-assets/) — Adapty, 2026-08-06
61. [Exact date Xcode 27/iOS 27 SDK becomes mandatory for App Store submissions](https://developer.apple.com/forums/thread/839939) — Apple Developer Forums (DTS reply, July 2026), accessed 2026-10-18
62. [What's new in the Foundation Models framework (WWDC26 session 241)](https://developer.apple.com/videos/play/wwdc2026/241/) — Apple Developer (WWDC26, June 2026), accessed 2026-10-18
63. [App Store submissions now open for the latest OS releases](https://www.mactech.com/2026/09/10/app-store-submissions-now-open-for-the-latest-os-releases/) — MacTech, 2026-09-10
