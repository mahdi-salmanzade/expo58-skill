# Hinge input and adaptive arrangements

Verified **2026-10-16** against stable SDK 58 documentation, `expo-hinge@58.0.1`, and `@expo/ui@58.0.19` published source/types. `ArrangementView` and `onHingeChange` first appear in UI `58.0.13`; use `58.0.19` or later for the iOS source-build fix described below.

## Install and establish capabilities

The published Expo 58.0.12 manifest includes these audited ranges. On an established SDK 58 project, install them explicitly when an older installation lacks the new APIs:

```sh
npx expo install @expo/ui@~58.0.19 expo-hinge@~58.0.1
```

Rebuild the development client after changing native dependencies. Verify the installed lockfile and the native build's actual SDK. SDK 58 is stable as of October 15; the feature still has build and OS requirements. See [sdk-versions.json](sdk-versions.json).

| Capability | Requirements and fallback |
| --- | --- |
| `expo-hinge` on Android | API 30+ and a hinge angle sensor; nullable reading otherwise |
| `expo-hinge` on iOS | iOS 27.1+ and binary built with iOS 27.1 SDK / Xcode 27.1+; nullable reading otherwise |
| `expo-hinge` on web | `isAvailable()` false, no hinge reading |
| SwiftUI `onHingeChange` | iOS 27.1+ and supported SDK linkage; no-op otherwise |
| SwiftUI `ArrangementView` | iOS 27.1+ plus compiled SDK support; older builds/systems render children without an arrangement container |

**UI `58.0.19` stops shipping a precompiled iOS framework**, so a build with Xcode 27.1+ includes the Duo implementations without a `buildFromSource` override. Versions `58.0.13`–`58.0.18` expose the JavaScript APIs but their precompiled iOS artifacts may omit the implementations. Upgrade the package and rebuild; updating JavaScript alone cannot repair that binary. Source: [UI 58.0.19 package changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.19).

The `@expo/ui` native implementation checks `canImport(SwiftUICore, _version: 8.0.85)` as well as runtime availability. Its source explains that compiler version alone is insufficient because SDKs shipped in the same Xcode can differ. Do not infer support from a version comparison in JavaScript alone. Sources: [Hinge](https://docs.expo.dev/versions/v58.0.0/sdk/hinge/), [ArrangementView](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/arrangementview/), published UI `ios/ArrangementViewView.swift`.

## Hinge data contract

```ts
import { addHingeListener, getHinge, isAvailable, useHinge } from 'expo-hinge';
import type { Hinge, HingeChangeEvent, HingeStatus } from 'expo-hinge';

// Hinge: { angle: number; status: HingeStatus }
// HingeStatus: 'closed' | 'partiallyOpen' | 'fullyOpen' | 'unknown'
// HingeChangeEvent: { hinge: Hinge | null }
```

| API | Meaning |
| --- | --- |
| `isAvailable(): boolean` | This build/OS can supply data; does not identify hinge hardware |
| `getHinge(): Hinge \| null` | Synchronous current snapshot; no subscription |
| `useHinge(): Hinge \| null` | Current cached value with live re-renders and managed cleanup |
| `addHingeListener(callback)` | Changes delivered as `{ hinge }`; unsubscribe with returned `.remove()` |

Keep `null`, `unknown`, and a valid zero-degree reading distinct. A null reading can mean no hinge, missing support, a window without hinge updates, or a missing Android angle sensor. Do not label every null reading “device closed.” Updates can become null later. There is no guaranteed event frequency or precision. Degrees, not radians, are exposed by both Expo hinge wrappers. See [HingeReadout.tsx](../examples/HingeReadout.tsx) for live observation, deliberately frozen snapshots, and an explicitly removed event listener. Source: published `expo-hinge@58.0.1` `src/Hinge.ts` and `src/Hinge.types.ts`.

**Android:** status never becomes `closed`. Outside a window that spans the fold it is `unknown`, even while angle readings continue. If a product interaction truly needs closed detection, use an app/device-validated near-zero angle threshold; there is no universal threshold. Do not use it to choose the layout. Source: [Android status semantics](https://docs.expo.dev/versions/v58.0.0/sdk/hinge/#status-on-android).

For a single SwiftUI subtree, use `onHingeChange((oldContext, newContext) => ...)`; each context has a nullable `hinge`. The first callback has a null old hinge. This callback differs from the module's `{ hinge }` event. It can also accept a `useWorkletCallback` result for continuous native effects. Keep a neutral unavailable state and avoid announcing every angle update to VoiceOver. Source: published UI `build/swift-ui/modifiers/hingeObservation.d.ts`.

## Arrangement composition

Layout follows the current container and native reserved regions, independently of angle data. Keep navigation outside arrangements. Do not nest an arrangement within a `NavigationSplitView`, list, or scroll view; put scrollable content **inside its panes** when needed and verify mixed React Native/SwiftUI containment. Apple documents axis restrictions that can leave only the primary visible, so ensure essential secondary controls remain reachable. [Apple preparation guide](https://developer.apple.com/documentation/technologyoverviews/preparing-your-app-for-iphone-duo)

The two slots are `ArrangementView.Primary` and `.Secondary`. Apply `arrangementViewStyle` to the arrangement, and sizing/edge preferences to the content inside the relevant slot:

```ts
import {
  arrangementViewStyle,
  splitArrangementLayoutRatio,
  splitArrangementLayoutSize,
  splitArrangementFixedLayoutSize,
  overlayArrangementEdge,
} from '@expo/ui/swift-ui/modifiers';

arrangementViewStyle('split', { axes: 'both' });
arrangementViewStyle('overlay', { axes: 'both' });
splitArrangementLayoutRatio(0.4);
splitArrangementLayoutRatio({ minHorizontal: 0.3, idealHorizontal: 0.4, maxHorizontal: 0.5 });
splitArrangementLayoutSize({ minWidth: 240, idealWidth: 320, maxWidth: 440 });
splitArrangementFixedLayoutSize({ horizontal: true, vertical: false });
overlayArrangementEdge('bottom');
```

These numbers are illustrative product preferences, not Duo geometry. `'automatic'` takes no options and resolves to split. Split can choose horizontal/vertical placement; overlay starts with primary over secondary and can separate around the fold. Preferences do not guarantee fixed pane dimensions. Source: published UI `build/swift-ui/modifiers/arrangementModifiers.d.ts` and [ArrangementView guide](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/arrangementview/).

## Copyable adaptive example

Copy the related files together into a non-route component directory:

- [AdaptiveNotes.tsx](../examples/AdaptiveNotes.tsx) owns selection and per-note drafts above the presentation.
- [AdaptivePanes.ios.tsx](../examples/AdaptivePanes.ios.tsx) keeps one arrangement tree during fold/resize transitions.
- [AdaptivePanes.tsx](../examples/AdaptivePanes.tsx), [AdaptivePanesFallback.tsx](../examples/AdaptivePanesFallback.tsx), and [AdaptivePanes.types.ts](../examples/AdaptivePanes.types.ts) provide Android/web and unsupported-build/OS behavior.

Mount below the app's existing `SafeAreaProvider`. `arrangementBuildVerified` defaults to false: set it to true in the integration only after verifying UI package version, binary linkage, and target SDK support. It is build metadata, never a feature derived from a hinge reading or device model; keep it stable throughout a session. The fallback measures its own container, allows more width for larger text, and changes a style without replacing its child tree. Its 680-point breakpoint is an example content threshold. Reconcile safe-area and keyboard ownership with the containing navigator to avoid duplicate padding.

The examples demonstrate state ownership and API usage; they are not a full persisted notes product. Verify focus, selection ranges, scroll position, keyboard access, and real fold transitions on the delivered target before claiming compatibility. See [Duo validation](23-iphone-duo.md#acceptance-matrix).

The supplied [community hinge example](https://github.com/SchroederNathan/expo-ui-examples/tree/main/src/examples/hinge) was reviewed for session observation and arrangement composition. Its demo-specific overlays, height constants, and vertical-only workaround are context for investigation, not universal layout rules. These examples are newly written and use published package contracts as the authority.
