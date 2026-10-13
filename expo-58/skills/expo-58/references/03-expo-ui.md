# Expo UI in SDK 58

Verified **2026-10-13** against `@expo/ui@58.0.16` source and declarations. Use [sdk-versions.json](sdk-versions.json) for the current beta package snapshot. The fact a page has `/v58.0.0/` in its URL does not establish stable-release status or prove an API existed in `58.0.0`.

## Choose the rendering surface

| Need | Import and boundary |
| --- | --- |
| Shared Android/iOS/web controls | `@expo/ui` universal components |
| SwiftUI controls, native navigation, arrangements | `@expo/ui/swift-ui` in Apple-specific files |
| SwiftUI modifiers | `@expo/ui/swift-ui/modifiers` |
| Android Compose controls | `@expo/ui/jetpack-compose` |
| Compose modifiers | `@expo/ui/jetpack-compose/modifiers` |
| Existing compatible third-party component replacement | The documented `@expo/ui/community/...` subpath |

`Host` crosses from React Native to the native UI toolkit. Yoga styles size the host; native stacks and modifiers size its content. `RNHostView` makes a deliberate boundary back to React Native. Keep these boundaries shallow and measured. SwiftUI components do not run on Android or web; use `.ios.tsx` plus a default fallback or choose universal primitives. Source: [Expo UI overview](https://docs.expo.dev/versions/v58.0.0/sdk/ui/).

## Important changes since SDK 57

The package's [published changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.16) records these details:

- `Host` fills from the top rather than centering content. Unspecified `HStack`/`VStack` spacing now uses the system default; pass `spacing={0}` when zero is intentional.
- Native SwiftUI `NavigationStack`, `NavigationLink`, `NavigationDestination`, `Toolbar`, and `NavigationSplitView` provide navigation within SwiftUI content. They do not migrate a Router app automatically.
- From `58.0.6`, a single `frame()` accepts fixed `width`/`height` **or** flexible `min*`/`ideal*`/`max*` values. Separate modifiers if both behaviors are needed.
- `RNHostView.matchContents` supports per-axis sizing from `58.0.10`. A content-sized height with parent-proposed width is useful in a sheet. Do not propagate window width into a smaller pane.
- `ArrangementView`, arrangement modifiers, `onHingeChange`, and `useWorkletCallback` arrive in `58.0.13`. Earlier SDK 58 patches do not contain them.
- `58.0.16` fixes hosted-view measurement and a Duo sheet-width clipping issue. It also rebuilds native artifacts after an Expo Modules JSI ABI change; keep the SDK dependency set coherent and rebuild the binary.

Use `npx expo install @expo/ui` ordinarily. For this snapshot's Duo examples, on an already established SDK 58 project, install `npx expo install @expo/ui@~58.0.16` and verify the lockfile. Do not install `@latest` blindly while the latest dist-tag points at SDK 57.

## State and measurements

SwiftUI `TextField.text` is an `ObservableState<string>`, not a string `value` prop. Create it with `useNativeState`, and use `onTextChange` for JS observation. Do not revive older `defaultValue` / `onValueChange` examples.

```tsx
import { Host, TextField, useNativeState } from '@expo/ui/swift-ui';
import { accessibilityLabel, padding } from '@expo/ui/swift-ui/modifiers';

export function NativeDraft() {
  const draft = useNativeState('');
  return (
    <Host matchContents>
      <TextField
        text={draft}
        placeholder="Draft"
        modifiers={[accessibilityLabel('Draft'), padding({ all: 16 })]}
      />
    </Host>
  );
}
```

`useNativeState` captures its seed once. Native state reads do not automatically subscribe React to render updates. JS writes are scheduled to the UI thread; do not treat a write immediately followed by a read as synchronous. Use the package's supported worklet callbacks only for a concrete UI-thread need, and clean up native change listeners with their owning component. Preserve task state above replaceable presentation branches. Sources: [useNativeState](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/usenativestate/) and published `build/State` declarations.

A full-screen native layout generally needs a bounded `Host style={{ flex: 1 }}`. `matchContents` asks the host to size itself to native content; it is not a substitute for constraints on a full-screen form. Check host/pane measurements after rotation, keyboard display, sheet resizing, and fold transitions. Apply safe-area ownership once at each actual boundary. Sources: [Host](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/host/), [RNHostView](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/rnhostview/).

## Duo integration

Use [Hinge and ArrangementView](22-hinge-arrangementview.md) for verified signatures, build/OS gates, old-OS fallback, and copyable examples. Use [iPhone Duo support](23-iphone-duo.md) for the app-level migration and QA workflow. Native system bars, custom React Native bars, safe-area padding, and interior reserved regions are separate mechanisms. Do not claim that wrapping a React Native screen in `Host` solves every Duo layout concern.
