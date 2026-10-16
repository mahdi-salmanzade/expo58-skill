# Expo UI in SDK 58

Verified **2026-10-16** against `@expo/ui@58.0.19` source and declarations in the stable SDK 58 dependency set. Use [sdk-versions.json](sdk-versions.json) for exact package provenance. SDK release status does not remove an individual API's experimental status or prove that an API existed in the first `58.0.0` package.

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

The package's [published changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.19) records these details:

- `Host` fills from the top rather than centering content. Unspecified `HStack`/`VStack` spacing now uses the system default; pass `spacing={0}` when zero is intentional.
- Native SwiftUI `NavigationStack`, `NavigationLink`, `NavigationDestination`, `Toolbar`, and `NavigationSplitView` provide navigation within SwiftUI content. They do not migrate a Router app automatically.
- From `58.0.6`, a single `frame()` accepts fixed `width`/`height` **or** flexible `min*`/`ideal*`/`max*` values. Separate modifiers if both behaviors are needed.
- `RNHostView.matchContents` supports per-axis sizing from `58.0.10`. A content-sized height with parent-proposed width is useful in a sheet. Do not propagate window width into a smaller pane.
- `ArrangementView`, arrangement modifiers, `onHingeChange`, and `useWorkletCallback` arrive in `58.0.13`. Earlier SDK 58 patches do not contain them.
- `58.0.16` fixes hosted-view measurement and a Duo sheet-width clipping issue. `58.0.18` corrects `Form`/`List` section insets beside the Duo rail.
- **`58.0.19` removes the precompiled iOS UI framework.** With Xcode 27.1+, `ArrangementView` and `onHingeChange` compile against that SDK without a `buildFromSource` override. Earlier precompiled artifacts can lack these implementations even when the app itself links iOS 27.1. Upgrade and rebuild before relying on them.
- Recycling data APIs cover SwiftUI `List`/lazy stacks and Compose lazy lists. Native navigation also includes two-/three-column `NavigationSplitView`, toolbar placement and visibility priority, and `navigationTitle`.
- SwiftUI color modifiers accept `ShapeStyle` materials/gradients. Compose adds `Image`, date-range pickers, and `VerticalSlider`; `58.0.17` renames carousel sizing to `preferredItemWidth` and deprecates `maxItemWidth`. Keep platform-specific imports explicit.

Use `npx expo install @expo/ui` in an SDK 58 app; the audited `expo@58.0.12` manifest selects `~58.0.19`. Verify the lockfile and rebuild after native changes. Select packages through the project's SDK manifest instead of assuming a moving `latest` tag is compatible with every app.

## Recycling large data sets

| Native container | Data child |
| --- | --- |
| SwiftUI `List` | `List.ForEach` |
| SwiftUI `LazyVStack` / `LazyHStack` | `LazyVStack.ForEach` / `LazyHStack.ForEach` |
| Compose `LazyColumn` / `LazyRow` | `LazyColumn.Items` / `LazyRow.Items` |

Supply `data`, stable string keys through `keyExtractor`, and a render function receiving `{ item, index }`. Do not build a large collection with `array.map()` and expect JavaScript row recycling. SwiftUI example for an Apple-specific file:

```tsx
import { Host, List, Text } from '@expo/ui/swift-ui';

type Article = { id: string; title: string };
const rowKey = (article: Article) => article.id;
const renderArticle = ({ item }: { item: Article }) => <Text>{item.title}</Text>;

export function ArticleList({ articles }: { articles: readonly Article[] }) {
  return (
    <Host style={{ flex: 1 }}>
      <List>
        <List.ForEach data={articles} keyExtractor={rowKey}>
          {renderArticle}
        </List.ForEach>
      </List>
    </Host>
  );
}
```

In an Android-specific file the same data pattern uses the Compose namespace:

```tsx
import { Host, LazyColumn, Text } from '@expo/ui/jetpack-compose';

type Article = { id: string; title: string };
const rowKey = (article: Article) => article.id;
const renderArticle = ({ item }: { item: Article }) => <Text>{item.title}</Text>;

export function ArticleList({ articles }: { articles: readonly Article[] }) {
  return (
    <Host style={{ flex: 1 }}>
      <LazyColumn>
        <LazyColumn.Items data={articles} keyExtractor={rowKey}>
          {renderArticle}
        </LazyColumn.Items>
      </LazyColumn>
    </Host>
  );
}
```

A recycled component can retain the previous item's local state. Store durable edits outside rows by item ID, or explicitly reset item-specific state when identity changes. Keep the render function stable and replace `data` rather than mutating it. Tune `estimatedItemSize` and `overscanCount` only after measuring placeholders and scroll behavior. SwiftUI `List` estimates exclude row insets and use points; Compose uses dp. Setting `recycling={false}` mounts all rows; switching it remounts them, so do not toggle it as the device folds. Supply a bounded host and test long lists with accessibility and resizing. Sources: [SwiftUI List](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/list/), [Compose LazyColumn](https://docs.expo.dev/versions/v58.0.0/sdk/ui/jetpack-compose/lazycolumn/).

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
