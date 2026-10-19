# Research sources & coverage checklists

Used by `/squint:research` and the `trend-scout` agent. Each platform has a **coverage
checklist** (what a monthly run must look at) and **sources** (primary first). Feeds were checked on
2026-10-18. Fix broken ones in a PR.

General rules
- Primary sources first: the platform vendor, standards bodies, the studio or company that did the work.
- Look at what was **published since the previous period**; carry forward continuing trends by id.
- Galleries and curation sites (Awwwards, Mobbin, Land-book…) show *what ships*. Press shows
  *what's announced*. Keep the two apart.
- Some sites block automated access (e.g. Land-book, Lapa Ninja, SiteInspire, Are.na). Don't work
  around it: note the gap, or ask the user to share screenshots.

---

## iOS

**Coverage checklist**
- Apple design language status (current Liquid Glass generation, HIG "What's new" changes)
- SDK / App Store requirements with dates (build SDK deadlines, deprecated opt-outs, review rules)
- New SwiftUI/UIKit APIs that change UI (bars, tabs, toolbars, sheets, materials, typography, symbols)
- New devices/form factors and resizing rules
- Accessibility expectations (Dynamic Type, transparency/contrast settings, Accessibility Nutrition Labels)
- System surfaces: widgets, Live Activities, Controls, App Intents / Siri, notifications
- App icon formats and appearances (Icon Composer)
- Patterns in top apps: onboarding, paywalls, navigation, search; what now looks dated
- OS adoption numbers

**Sources**
| Source | Feed |
|---|---|
| Apple Developer News | https://developer.apple.com/news/rss/news.rss |
| Apple Design — What's new (HIG change log) | https://developer.apple.com/design/whats-new/ (no feed: diff monthly; HIG pages also exist as `.md`) |
| Apple Newsroom | https://www.apple.com/newsroom/rss-feed.rss |
| 9to5Mac | https://9to5mac.com/feed/ |
| MacRumors | https://feeds.macrumors.com/MacRumors-All |
| Swift with Majid (SwiftUI APIs) | https://swiftwithmajid.com/feed.xml |
| Swiftjectivec (UIKit/iOS additions) | https://swiftjectivec.com/feed.xml |
| Design for Native | https://designfornative.com/rss/ |
| Nielsen Norman Group | https://www.nngroup.com/feed/rss/ |
| RevenueCat blog (paywalls, subscriptions) | https://www.revenuecat.com/blog/rss.xml |
| Michael Tsai (developer reaction digest) | https://mjtsai.com/blog/feed/ |

---

## Android

**Coverage checklist**
- Material Design status (Material 3 Expressive components, shape, motion physics, type, colour)
- Android platform releases and what they enforce (edge-to-edge, predictive back, adaptive layouts,
  large-screen / desktop windowing requirements)
- Google Play policies with dates (target SDK deadlines, large-screen quality tiers, listing rules)
- Jetpack Compose / Material3 library releases and new UI APIs
- System surfaces: widgets (Glance), notifications / live updates, themed icons, Gemini surfaces
- Google's own apps as reference implementations; patterns in top apps; what now looks dated

**Sources**
| Source | Feed |
|---|---|
| Android Developers Blog (moved to developer.android.com/blog, 2026-10-15) | https://developer.android.com/static/blog/atom.xml |
| AndroidX release notes (Compose Material3, adaptive, Navigation, Glance) | https://developer.android.com/feeds/androidx-release-notes.xml |
| Material Design blog | https://m3.material.io/blog (its old RSS stopped in 2025; check the page, it needs a browser) |
| 9to5Google + its Material Design guide | https://9to5google.com/feed/ · https://9to5google.com/guides/material-design/feed/ |
| Android version pages (behaviour changes) | https://developer.android.com/about/versions (no feed) |
| Play target-SDK and adaptive quality pages | https://developer.android.com/google/play/requirements/target-sdk · https://developer.android.com/docs/quality-guidelines/adaptive-app-quality |
| Android Authority / Android Police | https://www.androidauthority.com · https://www.androidpolice.com (feeds refused automated requests in testing) |
| Google Design library | https://design.google/library (no feed) |
| RevenueCat blog (paywalls, subscriptions) | https://www.revenuecat.com/blog/rss.xml |

---

## Web

**Coverage checklist**
- Visual trends on curation sites (Awwwards Sites of the Month, Godly/recent.design, Framer/Webflow showcases)
- Typography, colour (incl. colour of the year), layout and motion directions
- AI-native UX patterns in products (chat + canvas, agents, generative UI, trust/oversight patterns)
- SaaS/dashboard conventions (Linear-style shells, command palettes, density)
- Landing-page conversion patterns
- Web platform: newly Baseline features and Interop focus areas that unlock UI
- Accessibility & regulation (WCAG 2.2, European Accessibility Act enforcement, US ADA rules)
- Performance expectations (Core Web Vitals / INP); what now looks dated

**Sources**
| Source | Feed |
|---|---|
| web.dev (Baseline digests, blog) | https://web.dev/feed.xml |
| Web Platform Status | https://webstatus.dev (saved-search RSS; API `api.webstatus.dev/v1/features/{id}`) |
| Chrome for Developers blog | https://developer.chrome.com/static/blog/feed.xml |
| WebKit blog | https://webkit.org/feed/ |
| Mozilla Hacks / MDN BCD releases | https://hacks.mozilla.org/feed/ · https://github.com/mdn/browser-compat-data/releases.atom |
| Nielsen Norman Group | https://www.nngroup.com/feed/rss/ |
| Smashing Magazine | https://www.smashingmagazine.com/feed/ |
| Awwwards blog (+ Sites of the Month page) | https://www.awwwards.com/blog/feed/ |
| Creative Bloq | https://www.creativebloq.com/feeds/all |
| Figma blog | https://www.figma.com/blog/feed/atom.xml |
| Department of Product (SaaS teardowns) | https://departmentofproduct.substack.com/feed |
| Linear changelog · Tailwind blog | https://linear.app/rss/changelog.xml · https://tailwindcss.com/feeds/feed.xml |

---

## Branding & positioning

**Coverage checklist**
- Notable rebrands of the period and the reaction (critique, not just announcements)
- Identity-system directions: type-led, custom typefaces, motion-first, sonic, 3D vs flat, illustration,
  "human-made" vs AI aesthetics, retro, maximal vs minimal
- Colour forecasts (Pantone, WGSN/Coloro) and logo trend reports
- Verbal identity / tone-of-voice shifts
- How AI products position and brand themselves
- Startup/SaaS positioning and messaging patterns; App Store / Google Play listing practices
- What now looks dated

**Sources**
| Source | Feed |
|---|---|
| Brand New / UnderConsideration | https://www.underconsideration.com/brandnew/archives/category/reviewed (no working feed: check the page) |
| The Branding Journal weekly roundup | https://thebrandingupdate.substack.com/feed |
| LogoLounge news (+ annual trend report each June) | https://www.logolounge.com/rss |
| It's Nice That | https://www.itsnicethat.com/articles.rss |
| Fast Company Co.Design · Rebrand | https://www.fastcompany.com/co-design/rss · https://www.fastcompany.com/section/rebrand/rss |
| Creative Bloq | https://www.creativebloq.com/feeds/all |
| Design Week | https://www.designweek.co.uk/feed/ (needs a lenient XML parser) |
| Creative Review | https://www.creativereview.co.uk/feed/ |
| April Dunford (positioning) | https://aprildunford.substack.com/feed |
| Design Compass (rebrand facts and dates) | https://designcompass.org/feed/ |
| PRINT Magazine | https://www.printmag.com/feed/ |
| Phiture ASO Stack · Google Play "The Latest" | https://phiture.com/asostack/ · https://google.play/the-latest/ |
| Pantone Color of the Year · WGSN/Coloro | seasonal: Pantone announces in early December; WGSN/Coloro about two years ahead |
