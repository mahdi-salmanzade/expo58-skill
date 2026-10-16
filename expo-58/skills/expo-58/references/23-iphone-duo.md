# iPhone Duo support for Expo 58

Checked **2026-10-16**. This reference is self-contained for an Expo compatibility pass. It adapts the supplied `iphone-duo` skill's workflow to SDK 58, replacing its September beta/toolchain snapshot with current verified package guidance.

If the separate [iphone-duo skill](https://github.com/mahdi-salmanzade/iphone-duo-skill) is installed, use it alongside this reference for a wider existing-app audit, Apple's illustration catalog, UIKit/SwiftUI modules, camera accessories, or native reserved-region work. Discover it through the environment's skill catalog; do not depend on the author's local absolute path. The companion is optional for the Expo workflow below. Its older framework snapshot must not override the current installed Expo contracts.

## Establish the app and the binary

Trace entry points, navigator ownership, shared layout wrappers, state stores, modals, camera/media flows, and existing tests. Locate the actual app in a monorepo and inspect uncommitted work. Fix shared constraints before duplicating fixes in every screen. A repository search identifies leads; reproduce the affected interaction when runtime access is available. Source-confirmed failures, such as dereferencing a nullable hinge value, can be repaired without a device; distinguish that evidence from reproduced platform behavior.

Record the Expo, React Native, Router, and UI versions; Xcode version/build; linked iOS SDK; deployment target; simulator runtime; and the local or EAS build path. SDK 58 was released on October 15, 2026. Its scene and geometry changes support the folded and open displays; hinge-specific interactions and arrangements still need the iOS 27.1 SDK and runtime. An OTA update cannot add a native module or change the SDK that linked the app.

For native Duo APIs, use an iOS 27.1-capable toolchain. The [EAS infrastructure page](https://docs.expo.dev/build-reference/infrastructure/) currently lists `macos-tahoe-26.6-xcode-27.1` as **Xcode 27.1 RC (27A9275)**. The `sdk-58` alias still selects `macos-tahoe-26.6-xcode-27.0` (Xcode 27.0, build 27A266a); `latest` still selects Xcode 26.6 in this snapshot. Verify the actual “Spin up build environment” log rather than relying on an alias or describing an RC as a final toolchain. Local builds use the selected Xcode. Expo Go and old development clients retain the native capabilities they were built with.

Pin the Duo-capable image in an existing EAS profile when using these APIs (merge with the project's other profile settings):

```json
{
  "build": {
    "duo-development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "image": "macos-tahoe-26.6-xcode-27.1" }
    }
  }
}
```

Use `@expo/ui@~58.0.19` from the current SDK manifest: it no longer ships the precompiled iOS UI framework, so Xcode 27.1 builds include `ArrangementView`/`onHingeChange` without a `buildFromSource` override. Rebuild after upgrading. `58.0.18` also fixes native `Form`/`List` insets next to the Duo rail. [Expo UI package changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.19)

Xcode 27 uses Device Hub in place of Simulator.app; current Expo CLI can boot and focus its devices. The optional `expo-device-hub` dev-tools plugin adds a local browser dashboard. SDK 58 Expo Go store releases were still pending in the release announcement; use a development build or verify the installed client's SDK before testing. [SDK 58 release](https://expo.dev/changelog/sdk-58)

SDK 58 adopts the scene lifecycle. Generated native projects gain `SceneDelegate.swift` and a scene manifest; hand-maintained projects and direct app-delegate hooks need the [scene migration guide](https://expo.fyi/ios-scene-lifecycle). Default scene support does **not** enable multiple app windows: Expo's manifest example sets `UIApplicationSupportsMultipleScenes` to false. Preserve native customizations; use config plugins for persistent generated changes and inspect the installed prebuild command before regenerating native folders.

## Adapt the existing task

Use live `useWindowDimensions()` for window-level decisions and `onLayout` for the space a pane, sheet, or modal actually owns. Include font scale when evaluating whether content fits. Avoid cached `Dimensions.get('screen')`, fixed device widths, model-name branches, `Platform.isPad`, and `expo-device.deviceType` as layout selectors. Duo remains a phone. Width can justify a content breakpoint; it cannot identify a physical fold. [React Native window dimensions](https://reactnative.dev/docs/usewindowdimensions), [Apple preparation guidance](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)

State belongs to the user task. Keep selected items, drafts, per-tab history, playback/session owners, and asynchronous work above replaceable layout branches. Do not key a provider, navigation root, or editor by width, orientation, or hinge angle. Reflow existing content while retaining its identity. Opening/closing normally resizes an existing scene; do not reset state on a resize or assume it will produce an app background event. Real scene disconnection still needs the application's restoration path. [Apple scenes and displays](https://developer.apple.com/videos/play/tech-talks/111464/)

Duo can move system navigation and tab bars into a vertical rail on either side. Use Router `Stack` and `NativeTabs`, or Expo UI's native SwiftUI navigation inside `Host`, so iOS positions those bars on the outer and inner displays. Keep native bars native when appropriate; install Router's correct dependencies and use its SDK 58 imports. Custom JavaScript bars need deliberate adaptation and do not acquire native overflow automatically. Give important bar actions both an icon and a label, check Back/Close and Done on short vertical bars, and test overflow with the keyboard open. Avoid hiding an essential custom or text-only action when bars switch axes. [Router reference](02-expo-router.md), [Apple bar guidance](https://developer.apple.com/videos/play/tech-talks/111462/)

## Safe areas and reserved regions

Update the safe-area package through `npx expo install react-native-safe-area-context` (the audited manifest selects `~5.10.1`). Inspect scroll-view content as well as outer screen wrappers: a `SafeAreaView` inside a scroll view may be needed to protect horizontal content from the rail. Apply only the edges owned by that wrapper and check that the navigator is not already providing the same inset. Source: [safe-area-context](https://docs.expo.dev/versions/v58.0.0/sdk/safe-area-context/).

Apply each safe-area edge independently: left/right can differ, especially with side bars and adjacent apps. Verify provider placement inside modals and native hosts. Do not double a left inset or add safe padding on top of a container that already applies it. Keep actionable foreground clear while allowing decorative backgrounds to extend when appropriate.

For native modules that present popovers, use `expo-modules-core`'s scene-aware `SceneGeometry.anchorPopover` helper on regular-width windows. Expo packages have replaced `UIScreen.main` geometry reads; follow the [module guidance](04-expo-modules-api.md) when maintaining custom native code rather than choosing an arbitrary screen or scene. [Native helper change](https://github.com/expo/expo/pull/50433)

Safe areas describe edges; they do not describe every interior camera occlusion or fold division. Do not invent a constant “hinge gap.” For paired content, prefer supported native arrangements; for a custom fold-aware view, verify scene-local reserved-region APIs in the installed SDK and whether the installed Expo wrapper exposes what is needed. Only introduce a narrow native module when a concrete missing capability requires one. Never fabricate a JavaScript reserved-region hook from a Swift API name. Sources: [Duo HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo), [SwiftUI reserved regions](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:)).

ArrangementView handles primary/secondary content, not routes. Keep it out of a surrounding navigation split view/list/scroll view; put scrolling inside its panes. Let its supported axes and the current container guide placement. An equal split is a product choice, not a hardware requirement. [Hinge and ArrangementView](22-hinge-arrangementview.md) provides package floors, exact signatures, fallbacks, and a state-preserving example.

Use hinge readings for optional interactions/effects. Ordinary adaptive layout must continue with no sensor, a null reading, or Android's unknown status. Do not remount layout branches on an angle threshold. Respect reduced motion and avoid accessibility announcements at sensor frequency.

## Other integrations only when in scope

Orientation locks do not establish stable window geometry. Check [Expo's iOS 27 orientation rules](https://docs.expo.dev/versions/v58.0.0/sdk/screen-orientation/#orientation-locks-on-ios-27-and-later) and the generated plist; `ios.requireFullScreen` is not a general exemption from resizing. Avoid removing compatibility settings without verifying the app's resulting behavior.

For camera work, `facing="front"` alone does not prove virtual-camera handover or capture continuity. Confirm native discovery and test preview, recording, rotation, interruption, and handoff on hardware. Use current SDK 58 lens objects correctly (`deviceType` for selection, `localizedName` for display). Camera accessories need native capability checks and physical hardware evidence; do not add a second competing capture session to make them appear. For authentication, use `supportedAuthenticationTypesAsync()` to choose copy instead of hardcoding Face ID. Sources: [Expo Camera](https://docs.expo.dev/versions/v58.0.0/sdk/camera/), [LocalAuthentication](https://docs.expo.dev/versions/v58.0.0/sdk/local-authentication/), [Apple camera accessories](https://developer.apple.com/documentation/avfoundation/registering-a-camera-capture-accessory-on-iphone-duo).

Multiwindow, camera accessories, advanced motion, and browser posture APIs are optional features, not prerequisites for Duo compatibility. If requested, use the companion skill's corresponding native guidance after rechecking its cited APIs and build prerequisites.

## Acceptance matrix

Run transitions while a user task is in progress; static screenshots alone do not prove continuity.

| Check | Observable acceptance |
| --- | --- |
| Outer → inner → partially folded → outer | Same selected item, route/back history, draft and active operation; no duplicate request/session |
| Rotate and resize; app on either Split View side | Content uses its own bounds; each safe edge and native bar remains correct |
| Editor with keyboard open during a transition | Caret/selection and draft survive; focused field, save and dismiss stay reachable |
| Sheet/menu/popover through resizing | Presentation stays anchored, usable, correctly measured, and dismissible |
| Large text, VoiceOver, long strings, RTL | Reading order, labels, targets and scrolling remain usable; do not assume hardware-side bars mirror |
| Reduced motion / unavailable hinge / ordinary phone | Neutral fallback and full functionality; no sensor-driven layout requirement |
| Background/resume or scene restoration | Sessions recover correctly; listeners and owned resources are not duplicated |
| Android/web and older supported iOS | Shared changes retain their supported fallback behavior |

Also test loading, empty, error, and populated states for the affected flow. Add regression coverage for demonstrated failures or meaningful transitions. For native dependencies, a TypeScript pass must be followed by a native build; for fold behavior, use the Duo runtime or hardware. A mocked hinge, browser resize, or iPad simulator covers only part of the problem.

Report each check as passed, failed, blocked, or not applicable with target/runtime, build configuration, steps, and observed result. Distinguish **verified on Duo simulator**, **verified on Duo hardware**, **verified on another target**, and **unverified**. Missing runtime/toolchain access leaves an explicit acceptance gap; complete independently useful layout fixes without inventing unsupported APIs or claiming device certification.
