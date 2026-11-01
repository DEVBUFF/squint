---
platform: ios
period: 2026-11
researched_at: 2026-11-01
previous: 2026-10
sources: 68
---

# iOS — UI/UX trends · November 2026

## TL;DR
- Liquid Glass is no longer optional: the iOS 27 SDK ignores `UIDesignRequiresCompatibility`, and Apple's submit page says that from April 2027 every iOS upload must be built with the iOS 27 SDK (min target iOS 15). The opt-out ends with your first update after that date. [12][15][64]
- iPhone Duo is now a shipping device (on sale 2026-10-23, launched with iOS 27.1, which is Duo-only). The App Store shows a "Made for iPhone Duo" badge and curated collections, and Apple says 50+ third-party apps are or soon will be optimized. Unoptimized apps get black borders. Resizable layouts moved from "prepare" to "ship". [31][47][64][65][66][67]
- Brand color moves out of the bars and into the content. Use standard glass bars, keep the accent tint for meaning, and put full-bleed media underneath. Opaque brand-colored bars look dated. [19][33]
- iOS 27 "tuned" the glass (higher contrast, crisper edges, more opaque scroll edge, user transparency slider). Design and QA across the whole range. [4][8][10]
- Bottom-trailing `prominent` tab slot for search or the primary action, plus nav bars that minimize on scroll. Prioritized toolbars with a system overflow menu are the Duo-driven companion. [17][18][20][31]
- Siri AI makes App Intents, App Schemas, indexed entities and on-screen entity annotations the new discoverability layer. Named third-party adopters are still unverified. [3][23]
- Icons: reopen your `.icon` in the 2026 Icon Composer, lower translucency, and check clear and tinted appearances. [22][42]

## Platform baseline (expected now, not a trend)
- **iOS 26 SDK required since 2026-04-28. iOS 27 SDK and iOS 15+ deployment target required from April 2027.** Apple has published only the month, and only on the submit page. The "Upcoming Requirements" page did not list it when checked on 2026-11-01. Plan the Liquid Glass migration as a hard deadline. [14][15][61][63]
- **`UIDesignRequiresCompatibility` is dead for new builds.** The system ignores the key when you build for iOS 27 or later. An Apple DTS engineer confirmed it is still honored for apps linked against the iOS 26 SDK, even on iOS 27 devices. That loophole closes in April 2027. [12][13]
- **iOS 27 is the shipping OS.** Released 2026-09-14 for iPhone 11 and later. iOS 27.1 (2026-10-22) shipped only for iPhone Duo with no public changelog beyond bug fixes. Other iPhones are reported to move to 27.2 next. iOS 26 was on 79% of all iPhones as of 2026-06-07, and Apple has published no iOS 27 adoption figure. Support iOS 26 and 27 and design glass-first. [5][6][16][68]
- **UIScene lifecycle is mandatory.** Apps built with the latest SDK that lack a scene delegate won't launch. `UIScreen.main`, interface idiom and interface orientation are no longer valid layout inputs, because iPhone apps resize (iPhone Mirroring, iPad, iPhone Duo). [18]
- **Build with the iOS 27.1 SDK (Xcode 27.1) for Duo.** Apps built with it resize to fill the inner display. Others show black borders. Optimized apps can be submitted since 2026-10-05. [66][64]
- **Liquid Glass transparency slider plus accessibility modes.** Standard and custom glass respond to the user's slider, Reduce Transparency and Increase Contrast. Clear glass needs a ~35% dimming layer over bright media. [17][29]
- **Dynamic Type everywhere, including custom fonts.** Body text defaults to 17 pt with an 11 pt minimum. Custom fonts must support Bold Text. Wrap text instead of truncating it. [19][35]
- **Dark Mode plus clear and tinted appearances.** Icons need default, dark, clear light/dark and tinted light/dark looks. Widgets need full-color, accented and vibrant modes. [32][37]
- **The automatic scroll-edge effect has new, more opaque visuals.** iOS 26's soft fade is now opt-in (`.soft`). Re-check any overrides. [10][18][34]
- **Accessibility Nutrition Labels and the age-rating questionnaire.** Declaring accessibility support is optional but surfaces on the product page. The new age-rating answers have been required since 2026-01-31. [14][15]
- **App Store product-page header and search-result hero image or video** (iOS 27), managed via the Asset Library in App Store Connect. Adapty reports the tools were enabled 2026-10-05. Confirm in App Store Connect. [28][60]
- **Design kits.** The iOS/iPadOS 27 Figma kit was published 2026-09-17, with iPhone 18 and iPhone Duo bezels. [1]

## Trends

### ios-liquid-glass-tuned-contrast — Tuned Liquid Glass (contrast-first glass and a user transparency slider)
- **Status:** mainstream
- **Momentum:** →
- **What:** iOS 27 reworked Liquid Glass after a year of legibility complaints. Content behind bars is diffused more, edges are more defined, specular highlights are brighter, glass is lighter in dark mode, and prominent glass buttons get better default tints. Users choose anything from ultra-clear to fully tinted. The default is the midpoint, and the tinted end is effectively opaque. [4][7][8][9][10]
- **Seen in:** Apple Podcasts, the App Store and Messages (system examples), and Google Photos, which ships its own "Default / More clear" translucency toggle. [8][9][49]
- **Fits:** Every app that uses standard bars. It matters most for media, photo, map and content-heavy apps.
- **Avoid when:** Don't rely on "clear" glass over text-heavy or low-contrast content. Don't stack glass on glass. Expect older adults and low-vision users to set the slider toward tinted, so custom glass must keep hierarchy when it turns opaque. [29][59]
- **Implement:** Use `.glassEffect(.regular)` by default and `Glass.clear` only over photos or video, with a ~35% black dim when the media is bright. Use `.buttonStyle(.glass)` and `.glassProminent`. In UIKit use `UIButton.Configuration.glass()` and `.prominentGlass()`, plus `UIGlassEffect`. Remove hand-made shadows and blurs behind bars. Test at both slider extremes and with Reduce Transparency and Increase Contrast. Keep `.scrollEdgeEffectStyle(.automatic, for:)` unless `.soft` is tested legible. [17][29][34][39][40]
- **Sources:** [4], [7], [8], [9], [10], [17], [29], [34], [59]

### ios-native-first-components — Native-first chrome (big brands drop custom bars)
- **Status:** rising
- **Momentum:** →
- **What:** The largest apps moved their navigation chrome onto system Liquid Glass components and kept customization for content. Apps that half-migrated, especially those keeping a custom bottom bar, visibly clash with the OS. [19][50]
- **Seen in:** WhatsApp (glass tab bar, wider rollout May 2026), Instagram (floating tab bar that shrinks on scroll, May 2026), Google Photos and Google Health (glass bottom bars over Material 3 Expressive, September 2026), and Spotify 9.1.90 (glass top bar, custom bottom bar kept and criticized, October 2026). [49][50][51][52]
- **Fits:** Utility, social, messaging and productivity apps, and any app whose users switch between many apps a day.
- **Avoid when:** Games and immersive or creative canvases can stay custom, but keep iOS sizes, placements and popover behaviors. Slack's custom toolbar is Apple's example. [19]
- **Implement:** Use `TabView`/`Tab`, `NavigationStack`, `.toolbar`, `.searchable` and system sheets and menus. iOS 27 adds `.swipeActions` on any scroll content via `.swipeActionsContainer()`, `.reorderable()` with `.reorderContainer(for:)`, and item-bound `confirmationDialog(_:item:)` and `alert(_:item:)`. [17][44]
- **Sources:** [17], [19], [44], [49], [50], [51], [52]

### ios-brand-in-content-layer — Brand expressed in the content layer, not the chrome
- **Status:** rising
- **Momentum:** →
- **What:** Apple's 2026 branding guidance says to apply the accent color sparingly (primary actions, status, unread badges, the selected tab) and to move brand color into the scrolling content so glass controls pick it up. Identity comes from full-bleed media, voice, custom display type and custom icons rather than painted bars or logos. [19][33]
- **Seen in:** Crumbl (pink moved into content, weekly hero video, Crumbl Sans headers), Slack (tint only for primary and unread items), NYT Cooking (logo only on Home, custom line icons), Gentler Streak (SF Rounded and width variants), and Moonlitt (2026 ADA winner, Interaction). [19][48][58]
- **Fits:** Consumer brands, food and retail, media, wellness.
- **Avoid when:** Don't color tab labels the same as a colorful content layer; go monochrome bars instead. Don't use a brand typeface for small body copy. [30][33]
- **Implement:** Use `.tint(brandAccent)` once at the root, not `.toolbarBackground(brandColor, for: .navigationBar)`. Place hero media under bars with `backgroundExtensionEffect()` (UIKit: `UIBackgroundExtensionView`). Use `Font.custom(_:size:relativeTo:)` for headlines only, with system fonts for body. Ship a real Dark Mode palette and carry it into widgets. [19][33][39]
- **Sources:** [19], [30], [33], [39], [48], [58]

### ios-concentric-geometry — Concentric, hardware-matched corner geometry
- **Status:** mainstream
- **Momentum:** →
- **What:** Corners nest concentrically from the device bezel through sheets, cards and controls. Hard-coded radii that fight the system's rounding read as off-platform, especially on custom sheets, Live Activities and widgets. [19][36]
- **Seen in:** Moonlitt (calendar with concentric sheet edges), Apple's system sheets, and Live Activities guidance. [19][36]
- **Fits:** Custom cards, sheets, floating panels, widgets, Live Activities, in-app media frames.
- **Avoid when:** Dense data tables and editorial layouts can stay square. Don't round everything into pills, since iOS 27 toned down overly round corners and sidebar bezels. [11]
- **Implement:** Use `ConcentricRectangle` and `Shape.rect(corners:isUniform:)` in SwiftUI, `ContainerRelativeShape` in widgets and Live Activities, and `UIView.cornerConfiguration` with `UICornerConfiguration` in UIKit. Keep even margins between nested shapes. Live Activity Lock Screen content uses 14 pt standard margins. [36][39]
- **Sources:** [11], [19], [36], [39]

### ios-minimizing-bars-on-scroll — Bars that get out of the way on scroll
- **Status:** mainstream
- **Momentum:** →
- **What:** iOS 26 introduced tab bars that minimize on scroll, with an inline bottom accessory such as a mini-player. iOS 27 extends this to navigation bars and lets one prominent tab stay visible while the bar collapses. [17][18][30]
- **Seen in:** Apple Music (MiniPlayer and minimized tab bar), Instagram (tab bar shrinks on scroll), and Apple's iOS 27 SwiftUI sample apps. [17][30][52]
- **Fits:** Feeds, reading, media, maps, long scrolling content.
- **Avoid when:** Task flows and forms where controls must stay visible. NN/g flagged appearing and disappearing controls as hurting learnability. [59]
- **Implement:** Use `.tabBarMinimizeBehavior(.onScrollDown)` and `.tabViewBottomAccessory { }`. iOS 27 adds `.toolbarMinimizeBehavior(.onScrollDown, for: .navigationBar)`. In UIKit, use `UITabBarController` `MinimizeBehavior` and `prominentTabIdentifier`, plus `UINavigationItem.barMinimizeBehavior` and `barMinimizationSafeAreaAdjustment`. Apple's session spells these inconsistently, so check the docs. [17][18][45]
- **Sources:** [17], [18], [30], [45], [52], [59]

### ios-toolbar-priority-overflow — Prioritized toolbars with a system overflow menu
- **Status:** emerging
- **Momentum:** ↑
- **What:** Bars must survive many widths: narrow resizable windows, side-by-side windows and vertical bars on iPhone Duo. iOS 27 lets you rank items, pin one trailing action, and push the rest into a single system overflow menu. Duo's launch made this a shipping requirement. [17][31][66]
- **Seen in:** Apple Mail (Compose kept visible), Apple Notes (New Note kept visible), Apple Calculator, and third-party TestFlight and GarageBand, which Apple says gained a vertical toolbar on Duo. [31][65]
- **Fits:** Editors, productivity, creation tools, any screen with more than three toolbar actions.
- **Avoid when:** Text-only bar buttons, which stay horizontal and won't compress. Don't use custom ellipsis menus. Don't override default vertical placement on Duo. [31]
- **Implement:** Wrap related items in `ToolbarItemGroup { }.visibilityPriority(.high)`. Use `ToolbarOverflowMenu { }`, `ToolbarItem(placement: .topBarPinnedTrailing)` and `ToolbarSpacer`. Give every item a `Label(title, systemImage:)`, since the title is used in overflow. In UIKit, use `UIBarButtonItem.visibilityPriority`, `UINavigationItem.additionalOverflowItems` and `UIMenuElement.preferredImageVisibility`. On Duo, choose `ToolbarVerticalCompressionBehavior`. [17][31][45][46]
- **Sources:** [17], [31], [45], [46], [65]

### ios-bottom-trailing-prominent-slot — Bottom-trailing prominent tab for search or primary action
- **Status:** emerging
- **Momentum:** →
- **What:** The separated trailing tab that iOS 26 reserved for search is generalized in iOS 27 as a `prominent` role for any tab, such as Create or Cart. Apple's 2026 search guidance puts search at the bottom: a bottom-toolbar field, a standard Search tab, or a prominent tab that opens the keyboard immediately. [10][17][20]
- **Seen in:** Apple Phone (prominent search tab), Apple TV (standard search tab), Apple Mail (search button expanding into a bottom field), Apple Music (inline library search). All are Apple apps. [20]
- **Fits:** Commerce (Cart or Sell), creation apps (New post), catalog apps where search is the main entry point.
- **Avoid when:** The destination isn't the main action. Tab bars are for navigation, so a "+" that opens a modal belongs in a toolbar. Bloomberg reported Apple folding search back into regular tabs (Watchlist). [30][57]
- **Implement:** Use `Tab(role: .prominent) { … }` (iOS 27) or `Tab(role: .search)` (iOS 26), and `prominentTabIdentifier` in UIKit. Show recent searches inline on focus with swipe-to-delete and Clear All. Use scope bars or filter chips; tokens only in addition to visible filters. For empty results use `ContentUnavailableView.search(text:)`. [18][20][44]
- **Sources:** [10], [17], [18], [20], [30], [44], [57]

### ios-resizable-foldable-layouts — Resizable iPhone apps and foldable-ready layouts
- **Status:** rising
- **Momentum:** ↑
- **What:** iPhone Duo (7.6" inner and 5.4" outer displays) went on sale 2026-10-23. Apple opened optimized-app submissions on 2026-10-05, added a "Made for iPhone Duo" badge and curated collections, and says 50+ third-party apps are or soon will be optimized. Launch-day press noted many popular apps still show black bars. Apps built on size classes and system containers adapt almost for free. Fixed widths and portrait locks break. Apple says Duo is sold out through the end of January, so the installed base will start small. [17][31][47][64][65][66][67]
- **Seen in:** Yelp (results and details side by side with the map), TestFlight and GarageBand (vertical toolbar), Apple Mail, Notes and Calculator. Netflix, Microsoft and MLB are reported as updated by a secondary source only. [31][65][67]
- **Fits:** Every app. Reading, mail, notes, commerce, maps and media gain the most from the inner display's extra hierarchy level.
- **Avoid when:** Don't design a bespoke layout per pose. Don't put navigation containers inside arrangement views. Avoid extreme rearrangement when the device folds. Don't prioritize it over iOS 27 SDK migration for a small install base. [31][46]
- **Implement:** Use `horizontalSizeClass` and local geometry, never idiom, orientation or `UIScreen.main`. Use `NavigationSplitView` or `UISplitViewController`, and `ArrangementView` or `UIArrangementViewController` for two-view layouts. Use `ReservedRegion` to avoid the fold and cameras, and `onHingeChange` or `UIHingeInteraction` for hinge state. Prefer even grid columns. Build with Xcode 27.1 (iOS 27.1 SDK) for full inner-display support, and test poses in Device Hub. Use `windowScene.effectiveGeometry` for available space. [18][31][46][66]
- **Sources:** [17], [18], [31], [46], [47], [64], [65], [66], [67]

### ios-purposeful-morph-motion — Purposeful morphing and zoom motion
- **Status:** mainstream
- **Momentum:** →
- **What:** Motion explains spatial relationships: glass shapes morph between states, tapped items zoom into detail views, and springs add emphasis. Apple frames delight as the result of craft, not decoration. Dropped frames and late loads count as brand damage. [19][21]
- **Seen in:** NYT Cooking (zoom transitions tied to the tap target), Gentler Streak (spring emphasis), Apple Music (tab bar to MiniPlayer morph). [19][30]
- **Fits:** Content browsing, media, fitness and habit apps, apps with state-changing glass controls.
- **Avoid when:** Motion for its own sake, which NN/g criticized in iOS 26. With Reduce Motion on, swap movement for fades. Live Activity animations are capped at 2 s and don't run on reduced-luminance Always-On displays. [36][59]
- **Implement:** Use `GlassEffectContainer` with `glassEffectID(_:in:)`, `glassEffectUnion` and `glassEffectTransition`, and `Glass.interactive()`. Use `.navigationTransition(.zoom(sourceID:in:))` and the iOS 27 `.navigationTransition(.crossFade)`. Use SF Symbols Draw On/Off and Magic Replace, and `@Environment(\.accessibilityReduceMotion)`. Use `.sensoryFeedback(_:trigger:)` only on meaningful state changes. [17][40][41][44]
- **Sources:** [17], [19], [21], [30], [36], [40], [41], [44], [59]

### ios-layered-glass-icons — Layered Liquid Glass app icons, second generation
- **Status:** mainstream
- **Momentum:** →
- **What:** Icons are layered `.icon` files built in Icon Composer and rendered by the system with specular highlights, refraction, translucency and shadows across six appearances. The 2026 Icon Composer adds refraction controls, sharper specular highlights, a vertical light angle and chromatic or neutral shadows. iOS 27 reduces default translucency and draws icons sharper. [1][22][32][42][43]
- **Seen in:** Apple Podcasts, Apple Maps (sharper layered icon in iOS 27), Apple Photos (the HIG reference icon). All are Apple apps. [7][22][32]
- **Fits:** All apps. Flat 2D marks can gain material presence through layer separation instead of fake 3D.
- **Avoid when:** Photos, text, thin lines, feathered edges, or baked-in gloss and shadows. Clear-mode icon glass ignores the user slider, so contrast must come from the artwork. [22][32]
- **Implement:** Use a 1024×1024 px canvas with full-canvas SVG or PDF layers (PNG for raster or mesh gradients). Group layers that share glass settings. Set specular to inside when the foreground is darker than the background and outside otherwise. Reduce translucency, keep part of the foreground near-white for tint mode, and give the mono annotation a high dynamic range. Put the `.icon` file next to the asset catalog and remove the old icon set. Requires macOS Tahoe 26.4 or later. [22][32][42]
- **Sources:** [1], [7], [22], [32], [42], [43]

### ios-siri-ai-app-schemas — Siri AI-ready apps (App Schemas, indexed entities, on-screen context)
- **Status:** emerging
- **Momentum:** →
- **What:** Siri AI (English first, opened from the Dynamic Island) answers using on-screen content and acts across apps. Third-party apps take part by modeling content as App Entities with schemas, indexing them semantically, and annotating what's on screen. This replaces "deep links plus Shortcuts" as the integration baseline. [3][5][23]
- **Seen in:** Apple Messages, Mail and Photos (system schema domains), and the Ask Siri button that appears automatically in UIKit menus when relevant content exists. Named third-party adopters are not verified. [18][23]
- **Fits:** Messaging, notes, docs, tasks, photos, commerce catalogs, travel, fitness: apps with clear nouns and verbs.
- **Avoid when:** Exposing destructive or irreversible actions without confirmation. Siri AI isn't yet available in the EU (iOS) or China. [3][38]
- **Implement:** Use `@AppEntity(schema: .messages.message)` and the equivalent for your domain, `IndexedEntity` with `@Property(indexingKey:)`, and `EntityStringQuery`. Annotate on-screen content with `.appEntityIdentifier(EntityIdentifier(for:identifier:))` and `NSUserActivity`. Use `Transferable` with `IntentValueRepresentation`, `SyncableEntity`, and `RelevantEntities`. `LongRunningIntent` shows a Live Activity with a stop button. Test with AppIntentsTesting. Follow the HIG Snippets and App Shortcuts pages for result UI. [1][23][24]
- **Sources:** [1], [3], [5], [18], [23], [24], [38]

### ios-glanceable-surfaces-everywhere — Glanceable surfaces beyond the app (widgets and Live Activities across contexts)
- **Status:** rising
- **Momentum:** →
- **What:** One widget or Live Activity renders in many places. Widgets appear on the Home Screen (full color, tinted or clear glass), Lock Screen, StandBy, CarPlay, Mac, Apple Watch and Apple HomeView (launching 2026-11-13). Live Activities appear in a Dynamic Island that also shows in landscape, plus CarPlay, the Mac menu bar and Watch. iOS 27 adds an extra-large portrait widget size. [7][25][26][36][37][56]
- **Seen in:** Apple Calendar, Photos and Music (extra-large widgets), Crumbl (branded pastel widgets), and the Apple Timer Live Activity. [7][19][36]
- **Fits:** Delivery, rideshare, sports, travel, fitness, finance tickers and media.
- **Avoid when:** Ads or promos in Live Activities (HIG forbids). Sensitive data on the Lock Screen. Full-color images in tinted or clear modes (keep for album art). Interactive controls in CarPlay layouts. [36][37]
- **Implement:** Use `systemExtraLargePortrait` (iOS/iPadOS 27), `.widgetAccentable()` and `.widgetAccentedRenderingMode(.fullColor)` for media only. Read `@Environment(\.isDynamicIslandLimitedInWidth)` and fit compact and minimal views into a 28 pt circle. Use `.supplementalActivityFamilies([.small])` for Watch and CarPlay, `activityBackgroundTint`, `LiveActivityIntent` buttons and `ContainerRelativeShape`. End activities promptly with a 15–30 minute dismissal. [25][26][36][37]
- **Sources:** [7], [19], [25], [26], [36], [37], [56]

### ios-genai-refine-feedback-ux — Generative-AI UX with refine, retry and honest progress
- **Status:** rising
- **Momentum:** →
- **What:** As on-device and Private Cloud Compute models spread (the 2026 Foundation Models framework adds a rebuilt on-device model, image input and PCC access), Apple's June 2026 HIG update standardizes AI output: Edit, Undo, Retry and Adjust next to results, acknowledged corrections, specific progress text, alternatives, and voluntary thumbs up or down. [2][38][62]
- **Seen in:** Apple Image Playground, Photos Clean Up (Fast, High Quality, Auto), and Writing Tools. All are Apple apps. [3][6][7][38]
- **Fits:** Writing, photo and video editing, summarization, planning, coaching.
- **Avoid when:** The output is factual, health-related or irreversible without confirmation. You have no non-AI fallback when the model is unavailable. Never let AI pass as human. [21][38]
- **Implement:** Label AI features clearly. Replace "Processing…" with task-specific copy. Keep refine controls adjacent to output. Check `SystemLanguageModel.default.availability` before showing the entry point. Use `Attachment(...)` for image prompts and `PrivateCloudComputeLanguageModel` for heavier tasks, and budget tokens with `contextSize` and `tokenCount(for:)`. Design a loading or background state and disclose server processing. [38][62]
- **Sources:** [2], [3], [6], [7], [21], [38], [62]

### ios-value-first-onboarding-late-paywall — Value-first onboarding with a late paywall and transparent plans
- **Status:** mainstream
- **Momentum:** →
- **What:** Paywalls sit at the end of onboarding, after a value moment. In a 40-flow sample the median relative position was 0.894, none opened with a paywall, and 77.5% were in the final third. 55.4% of 3-day-trial cancellations happen on Day 0, which pushes teams toward the "aha" moment in the first session. Apple's monthly-billed 12-month commitment plan adds a new price layout to design. [27][53][54]
- **Seen in:** Instacart, Grammarly, Up Ahead and ChargePoint (late-paywall flows), and Adobe, the early-paywall outlier at step 3 of 13. [54]
- **Fits:** Subscription consumer apps (wellness, language, productivity, AI). Personalization quizzes appear in only ~16% of ~751 apps, mostly wellness and language. [55]
- **Avoid when:** A paywall on screen 1, or quiz questions that change nothing. Don't hide the total commitment price; the App Store shows its own disclosure sheet once per account. [27][55]
- **Implement:** Use `SubscriptionStoreView` with `.preferredSubscriptionPricingTerms { … billingPlanType == .monthly }`. In custom UI show `pricingTerms.billingDisplayPrice` with `commitmentInfo.price`, and purchase with `.billingPlanType(.monthly)` (iOS 26.5 SDK, OS 26.4 or later). Use `.manageSubscriptionsSheet` and `offerCodeRedemption(options:isPresented:)`. A/B test 7-day or longer trials against 3-day ones. Keep the paywall close button visible over custom backgrounds. [10][27][53]
- **Sources:** [10], [27], [53], [54], [55]

## Fading — now looks dated
- **Opaque, brand-colored navigation and tab bars** — Apple moves brand color into the content layer. Painted bars fight Liquid Glass. [19][33]
- **Custom bottom tab bars beside system glass** — half-migrated apps show the clash (Spotify, October 2026). [50]
- **Logos in nav bars and branded splash or launch screens** — the HIG says launch screens are not for branding. Logo-only-on-Home is the new norm. [19][33]
- **Glass in the content layer** (glass cards, list rows, glass on glass) — the HIG reserves glass for the control layer. [29]
- **iOS 26.0-style maximal clear glass and soft fades over busy content** — iOS 27 moved to higher contrast and a more opaque scroll edge. [7][10][59]
- **Baked-in icon effects and flat single-layer icons** — static effects look muddy in tinted or clear modes. [22][32]
- **Portrait-locked, idiom- or orientation-based layouts and `UIScreen.main`** — these break on resizable iPhone apps and now on shipping Duo hardware (black bars). [18][31][66]
- **Custom "…" overflow menus and text-only bar buttons** — replace with `ToolbarOverflowMenu` and symbol-plus-title items. [31]
- **Hard-coded corner radii on sheets, cards and Live Activities** — non-concentric corners read as off-platform. [36]
- **A top-of-screen search bar as the iPhone default** — Apple's guidance prefers the bottom toolbar or a search tab. [20]
- **`UIDesignRequiresCompatibility` as a strategy** — ignored for iOS 27 SDK builds, which become mandatory in April 2027. [12][15]
- **Paywall-first onboarding with a 3-day trial on screen 1** — Day-0 cancellations dominate. [53][54]
- **"Confetti" delight bolted on at the end** — Apple reframes delight as the outcome of craft. [21]

## Watchlist — verify next month
- Search tab merged back into the regular tab group in Apple's Podcasts, TV, Music, Health and News, reported by Bloomberg before WWDC [57]. Whether this shipped is unverified.
- iOS 27 adoption numbers. Apple has published none (unverified).
- Exact April 2027 day for the iOS 27 SDK requirement [15][61]. The "Upcoming Requirements" page didn't list it on 2026-11-01 [14]. Watch for the entry.
- A claim that from April 2027 new apps must include iPhone Duo screenshots, seen only in a search summary. Not found on Apple's pages. Unverified.
- iOS 27.2: reported next release for non-Duo iPhones after 27.1 was Duo-only [68]. Contents unverified.
- Apple HomeView (launching 2026-11-13) as a third-party widget surface [56]. Which third-party widgets appear is unverified.
- Netflix, Microsoft and MLB Duo updates, reported only by a secondary outlet. Apple named Yelp, TestFlight and GarageBand [65]. Unverified.
- YouTube and YouTube Music Liquid Glass UI, seen in feature flags (Android Authority, 2026-08-26). Unverified.
- Gmail and Google Maps adoption of Liquid Glass. Not adopted as of 2026-09-26 [49].
- Full WhatsApp chat-screen redesign completion. Rollout is staggered [51].
- SF Symbols naming: "SF Symbols 8 beta" in June 2026 [1][43], but the download is named "SF-Symbols-27" [41]. Unverified.
- Exact App Store header and search-image specs (a 16:9 PNG at 5244×2950 was cited in a secondary summary) [28][60]. Unverified.
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
14. [Upcoming Requirements](https://developer.apple.com/news/upcoming-requirements/) — Apple Developer, accessed 2026-11-01
15. [Submit your iOS apps to the App Store](https://developer.apple.com/ios/submit/) — Apple Developer, accessed 2026-11-01
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
64. [Apple's App Store Adds New Badge for Apps Optimized for iPhone Duo](https://www.thurrott.com/?p=343134) — Thurrott, 2026-10-22
65. [Apple says that more than 50 third-party apps are optimized or soon will be for the iPhone Duo](https://www.mactech.com/2026/10/22/apple-says-that-more-than-50-third-party-apps-are-optimized-or-soon-will-be-for-the-iphone-duo/) — MacTech, 2026-10-22
66. [Apple Announces iPhone Duo Apps Can Now Be Submitted to App Store](https://www.macrumors.com/2026/10/05/apple-opens-iphone-duo-app-submissions/) — MacRumors, 2026-10-05
67. [iPhone Duo apps: Netflix, Microsoft, MLB update for foldable](https://t2online.in/tech/tech-news/iphone-duo-apps--netflix--microsoft--mlb-update-for-foldable/2008793) — T2 Online (secondary), 2026-10
68. [Apple Releases iOS 27.1](https://www.macrumors.com/2026/10/22/apple-releases-ios-27-1/) — MacRumors, 2026-10-22
