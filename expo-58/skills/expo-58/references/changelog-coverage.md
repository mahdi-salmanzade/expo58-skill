# SDK 58 release coverage

Audit: **2026-10-16**, skill **1.1.1**, against the
[SDK 58 announcement](https://expo.dev/changelog/sdk-58). This index maps the
announcement's engineering topics and named changes to actionable skill guidance.
Each destination links its primary documentation or published implementation.
Read the destinations relevant to the task; this index is not a required reading
sequence or a claim of native/device test coverage.

Version 1.1.0 covered the main release themes but omitted some smaller changes.
The 1.1.1 pass filled those gaps and corrected the strict-types deferral timeline.
The package snapshot remains Expo 58.0.12 / RN 0.88.0. Where the announcement still
links a React Native release candidate, the stable package/release governs actual
signatures and feature availability.

## Platform and new development capabilities

| Release item | Skill guidance |
|---|---|
| iOS 27 scene lifecycle and AppDelegate forwarding | [21 — native migration](21-sdk-58-migration.md) |
| Window-based geometry, resizing, `requireFullScreen`, orientation locks | [23 — Duo adaptation](23-iphone-duo.md), [15 — orientation](15-location-sensors.md) |
| `isLiquidGlassAvailable` and the linked iOS SDK | [09 — native presentation](09-system-ui-components.md) |
| Duo native navigation bars/rails and horizontal safe areas | [02 — navigation](02-expo-router.md), [23 — layout checks](23-iphone-duo.md) |
| `SceneGeometry.anchorPopover` | [23 — native integrations](23-iphone-duo.md) |
| Hinge hook, synchronous read, listener, nullable state, platform gates | [22 — Hinge](22-hinge-arrangementview.md) |
| `ArrangementView`, `onHingeChange`, worklet callback | [22 — adaptive arrangement](22-hinge-arrangementview.md) |
| Device Hub, browser device control, metrics and accessibility controls | [19 — development tools](19-dev-workflow-testing.md) |
| Upcoming EAS Simulator service | [19 — availability boundary](19-dev-workflow-testing.md) |
| App Intents setup, Swift declarations, JS invocation delivery | [04 — App Intents](04-expo-modules-api.md) |
| Spotlight, donations, `AppEntityView`, `appEntityIdentifier` | [04 — entity integration](04-expo-modules-api.md) |
| App Intents agent skill and forthcoming TaskManager execution | [04 — setup and execution limits](04-expo-modules-api.md) |
| Observe, automatic error capture option, `clientId` | [19 — diagnostics](19-dev-workflow-testing.md) |
| Experimental `command:ps`, `command:events`, changed debug output | [05 — agent diagnostics](05-cli-metro-bundling.md) |
| Agent CLI setup, status, dev, smoke, skill sync, alias and delegation | [05 — agent CLI](05-cli-metro-bundling.md) |
| Android widgets: separate runtime, interactions, colors and corners | [09 — widgets](09-system-ui-components.md) |
| Live Activity freshness, stable identifiers, widget configuration | [09 — Live Activities](09-system-ui-components.md) |
| SwiftPM preview and CocoaPods default | [10 — native builds](10-eas-build-brownfield.md) |
| Android prebuilt core libraries and source-build override | [10 — build configuration](10-eas-build-brownfield.md) |
| Faster iOS module calls and annotation-based Modules 2.0 beta | [04 — native module authoring](04-expo-modules-api.md) |
| Balanced fingerprint and native-patch implications | [08 — runtime compatibility](08-sqlite-updates-convex.md) |
| Experimental Noxcturnal transformer and Babel restrictions | [05 — bundling](05-cli-metro-bundling.md) |

## Expo UI and Router

| Release item | Skill guidance |
|---|---|
| Recycling List/Lazy stacks and Compose rows/columns | [03 — recycling lists](03-expo-ui.md) |
| Component visual galleries | [03 — choosing native components](03-expo-ui.md) |
| SwiftUI navigation stack, links/destinations, toolbars, title, close role, split view | [03 — native navigation](03-expo-ui.md) |
| ShapeStyle paints, Background, clipping/geometry/separator/alignment/menu/edge modifiers | [03 — SwiftUI additions](03-expo-ui.md) |
| Compose Image, date-range controls, VerticalSlider, menu/radio props | [03 — Compose additions](03-expo-ui.md) |
| Universal sheet/list colors and padding; web dialog implementation | [03 — universal surfaces](03-expo-ui.md) |
| RNHostView measurement/touches, outside-tap dismissal, Menu click-through | [03 — hosted React Native views](03-expo-ui.md) |
| Stable loaders, SSR, middleware, native tabs, toolbars and integration | [02 — stable surfaces](02-expo-router.md) |
| Loader HTTP caching, default server output, per-request HTML, static-plus-API alternative | [02 — web migration](02-expo-router.md), [05 — export configuration](05-cli-metro-bundling.md) |
| Web asynchronous routes and optional eager loading | [02 — route loading](02-expo-router.md) |
| Transitions, activities and screen error boundaries | [02 — transitions and activity](02-expo-router.md) |
| `extendRouter`, `extendRouterActions`, deterministic state and deferred dispatch | [02 — state integrations](02-expo-router.md) |
| Web safe-area CSS and optional UI/symbol peers | [02 — platform migration](02-expo-router.md) |
| Experimental analytics observer and its published export names | [02 — analytics integration](02-expo-router.md) |

## Connections, React Native, and service integration

| Release item | Skill guidance |
|---|---|
| Relative manifest URLs, proxies/Bonjour, runtime Metro port and port rollover | [05 — connection diagnosis](05-cli-metro-bundling.md) |
| Default Expo tunnel, login and legacy ngrok selection | [05 — tunnels](05-cli-metro-bundling.md) |
| RN 0.87/0.88 upgrade boundary and strict types | [21 — migration](21-sdk-58-migration.md) |
| `fontVariationSettings` and variable font loading | [16 — fonts](16-app-config-foundational.md) |
| TurboModule ArrayBuffer ownership; stable-versus-RC iOS differences | [04 — runtime contracts](04-expo-modules-api.md) |
| DevTools performance screenshots and WebSocket inspection channels | [19 — debugging availability](19-dev-workflow-testing.md) |
| PostHog EAS setup, mutation scope, release/update properties, SDK independence | [18 — service integration](18-eas-full-workflow.md) |
| Launch URL shape, reserved parameters, legacy compatibility, automation flags | [05 — launch URLs](05-cli-metro-bundling.md) |
| `unwrapDevLaunchURL` and single query-value decoding | [20 — linking](20-maps-web-utilities.md) |

## Other named package changes

| Release item | Skill guidance |
|---|---|
| Camera document scanning | [11 — scanning](11-camera-visual-media.md) |
| File digest algorithms, preview and preview capability | [06 — file operations](06-filesystem-networking.md) |
| Audio playlist lock-screen controls and AudioStream WAV/PCM recording | [12 — playback and recording](12-video-audio-playback.md) |
| Image cached-transition bypass and SVG variable/fallback behavior | [11 — image display](11-camera-visual-media.md) |
| SecureStore Android authentication confirmation | [13 — authenticated storage](13-auth-security.md) |
| URL IDNA/TR-46 handling and TextDecoder rewrite | [05 — built-in runtime APIs](05-cli-metro-bundling.md) |
| SQLite package skill, operation interruption, custom web FTS/WASM | [08 — SQLite](08-sqlite-updates-convex.md) |
| Variable fonts via hooks, loader and config plugin | [16 — font setup](16-app-config-foundational.md) |
| iOS notification delegate coexistence and grouping | [14 — notifications](14-notifications-background.md) |
| Android alarm-clock delivery and large notification icon | [14 — notification configuration](14-notifications-background.md) |
| Location next provider/watch/task/service APIs and temporary full accuracy | [15 — location](15-location-sensors.md) |
| iOS geofencing background-mode change | [15 — background requirements](15-location-sensors.md) |
| Metro environment-cache invalidation and library stack visibility | [05 — Metro diagnostics](05-cli-metro-bundling.md) |
| LogBox/terminal collapsed-stack visibility, Xcode log path, AVD/adb recovery | [05 — device diagnostics](05-cli-metro-bundling.md) |
| Update retention and channel switching | [08 — OTA storage](08-sqlite-updates-convex.md) |

## Deprecations, breaking changes, and toolchain

| Release item | Skill guidance |
|---|---|
| `File.md5` → `File.digest`; asynchronous `File.write` / `writeSync` | [06 — files](06-filesystem-networking.md), [21 — migration](21-sdk-58-migration.md) |
| `NativeArrayBuffer` → `ArrayBuffer` | [04 — module contracts](04-expo-modules-api.md) |
| `AppMetrics` → `Observe` | [19 — monitoring](19-dev-workflow-testing.md) |
| `withLayoutContext` → `integrateWithRouter` | [02 — navigation integration](02-expo-router.md) |
| SQLite `useLibSQL`, `syncLibSQL`, `libSQLOptions` removal/no-op | [08 — data migration](08-sqlite-updates-convex.md) |
| UI backgroundOverlay, border/stroke color, ForEach children migration | [03 — UI deprecations](03-expo-ui.md) |
| Compose carousel width and five TimePicker color renames | [03 — Compose compatibility](03-expo-ui.md) |
| RN deep imports/ref types, legacy opt-out timeline, removed APIs, ImageBackground | [21 — RN migration](21-sdk-58-migration.md) |
| macOS support boundary | [01 — environment gates](01-core-setup-upgrade.md) |
| iOS scene source ownership and native callback migration | [21 — native migration](21-sdk-58-migration.md) |
| Command-selected NODE_ENV and environment files | [05 — CLI modes](05-cli-metro-bundling.md), [16 — app configuration](16-app-config-foundational.md) |
| Android release R8 and ProGuard keep rules/opt-out | [10 — native builds](10-eas-build-brownfield.md), [21 — release checks](21-sdk-58-migration.md) |
| Router core, optional peers and server-rendering migration | [02 — Router](02-expo-router.md) |
| Foreground notification defaults and slow handlers | [14 — notification handling](14-notifications-background.md) |
| Balanced fingerprint default | [08 — updates](08-sqlite-updates-convex.md) |
| UI Host alignment, stack spacing, Android RNHostView modifiers | [03 — host migration](03-expo-ui.md) |
| iOS RTL via I18nManager | [16 — localization](16-app-config-foundational.md) |
| Photos current-video URI versus original asset | [07 — MediaLibrary](07-media-device-apis.md) |
| Browser-default login and rejection of development server exports | [05 — CLI](05-cli-metro-bundling.md) |
| Node release lines and AGP 9 compatibility | [01 — tooling](01-core-setup-upgrade.md) |
| Compose UI/Foundation and Material 3 versions | [03 — native dependency versions](03-expo-ui.md) |

## Creation, upgrade, and scope

| Release item | Skill guidance |
|---|---|
| Expo Go store transition, SDK 58-only future store client, explicit template | [01 — creation/runtime selection](01-core-setup-upgrade.md) |
| Dependency alignment, Doctor, native rebuild, CNG versus maintained source | [21 — upgrade execution](21-sdk-58-migration.md), [01 — native ownership](01-core-setup-upgrade.md) |
| Pod installation/native helper, optional upstream upgrade skills, full package changelogs and troubleshooting | [01 — native projects](01-core-setup-upgrade.md), [21 — further assistance](21-sdk-58-migration.md) |

The source page's credits, screenshots, demo narrative, office-hours invitation,
and numerical benchmark charts remain in the original announcement. This skill
documents their engineering implications without reproducing promotional material
or promising benchmark results for another app. Coverage is bounded to that
announcement as audited; the linked monorepo changelog contains additional
package-level changes and can include unreleased commits.
