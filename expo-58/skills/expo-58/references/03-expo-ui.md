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

The [SwiftUI gallery](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/) and [Compose gallery](https://docs.expo.dev/versions/v58.0.0/sdk/ui/jetpack-compose/) now show component screenshots alongside the API. Use them to choose the native control and check its platform/version limits before implementing it.

## Important changes since SDK 57

The package's [published changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.19) records these details:

- `Host` fills from the top rather than centering content. Unspecified `HStack`/`VStack`/`GlassEffectContainer` spacing now uses the system default; pass `spacing={0}` when zero is intentional.
- Native SwiftUI `NavigationStack`, `NavigationLink`, `NavigationDestination`, `Toolbar`, and `NavigationSplitView` provide navigation within SwiftUI content. They do not migrate a Router app automatically.
- From `58.0.6`, a single `frame()` accepts fixed `width`/`height` **or** flexible `min*`/`ideal*`/`max*` values. Separate modifiers if both behaviors are needed.
- `RNHostView.matchContents` supports per-axis sizing from `58.0.10`. A content-sized height with parent-proposed width is useful in a sheet. Do not propagate window width into a smaller pane. On Android, `RNHostView.style` was removed; put native container sizing in Compose `modifiers` and React Native child styling on the child.
- `ArrangementView`, arrangement modifiers, `onHingeChange`, and `useWorkletCallback` arrive in `58.0.13`. Earlier SDK 58 patches do not contain them.
- `58.0.16` fixes hosted-view measurement and a Duo sheet-width clipping issue. `58.0.18` corrects `Form`/`List` section insets beside the Duo rail.
- **`58.0.19` removes the precompiled iOS UI framework.** With Xcode 27.1+, `ArrangementView` and `onHingeChange` compile against that SDK without a `buildFromSource` override. Earlier precompiled artifacts can lack these implementations even when the app itself links iOS 27.1. Upgrade and rebuild before relying on them.
- `58.0.17` updates Compose UI/Foundation to **1.12.1** and Material3 to **1.5.0-beta01**. These are the published package's native dependencies, not a reason to mark all SDK 58 APIs beta or to override Gradle versions independently.

Use `npx expo install @expo/ui` in an SDK 58 app; the audited `expo@58.0.12` manifest selects `~58.0.19`. Verify the lockfile and rebuild after native changes. Select packages through the project's SDK manifest instead of assuming a moving `latest` tag is compatible with every app.

## Native controls and modifiers

The following additions are present in audited UI `58.0.19`; preserve their platform and OS boundaries.

| Surface | Use and migration detail |
| --- | --- |
| SwiftUI navigation | `NavigationStack`, `NavigationLink`, and `NavigationDestination` own native navigation within SwiftUI. `NavigationSplitView` supplies two or three columns. Set `navigationTitle` on the relevant content. `Toolbar`/`Toolbar.Content` contain `ToolbarItem` children; use `placement` for semantics and `visibilityPriority` for overflow priority (iOS 27+). A `Button` with `role="close"` and no label/children shows the system close icon on iOS 26+; supply an explicit label and `systemImage="xmark"` on older systems. |
| SwiftUI paint | `background`, `tint`, `border`, `strokeBorder`, `containerBackground`, `presentationBackground`, and `foregroundStyle` accept `ShapeStyle`, including materials and gradients. `Background` with `Background.Content` composes background views behind content. |
| SwiftUI scroll effects | `scrollClipDisabled` allows drawing beyond scroll bounds (iOS 17+). `scrollEdgeEffectStyle` controls the effect where scrolling content meets bars (iOS 26+). Neither replaces layout constraints or safe areas. |
| SwiftUI geometry and separators | `geometryGroup` isolates child geometry from its parent during layout animation (iOS 17+). `alignmentGuide` can place horizontal alignment guides, including row-separator edges; `listRowSeparatorTint` colors selected separator edges. |
| SwiftUI menus | `menuStyle` selects the native menu style and `menuIndicator` controls its indicator. Check platform availability in the modifier reference. |
| Compose additions | `Image` renders an image in a Compose tree. `DateRangePicker` and `DateRangePickerDialog` provide inline/dialog range selection; `VerticalSlider` supplies the vertical control. `DropdownMenu.cornerRadius` and `.shadowElevation` customize its surface. `RadioButton.enabled` controls interaction and `.colors` supplies state colors. |
| Universal additions | `BottomSheet.contentPadding` accepts one inset or per-edge values, and `containerColor` paints sheet chrome. Its `contentColor` is Android Compose-only and does not recolor React Native children; set child text colors explicitly. `ListItem.colors` is also Android-only. On web, the sheet uses an internal HTML `<dialog>` implementation instead of `vaul`; verify focus, dismissal, and keyboard behavior when replacing custom integrations. |

Sources: [Toolbar](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/toolbar/), [SwiftUI modifiers](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/modifiers/), [Compose components](https://docs.expo.dev/versions/v58.0.0/sdk/ui/jetpack-compose/), and published `58.0.19` declarations under `build/swift-ui`, `build/jetpack-compose`, and `build/universal` ([package](https://www.npmjs.com/package/@expo/ui/v/58.0.19)). A universal component can expose an option that only applies on one platform.

## Deprecated UI forms

- Replace SwiftUI `backgroundOverlay` with `background`; replace the `color` field of `border` and `strokeBorder` with `content`, which accepts a `ShapeStyle`.
- Replace element children passed to `List.ForEach` with its `data`, `keyExtractor`, and render-function form below.
- On Compose `HorizontalCenteredHeroCarousel`, replace `maxItemWidth` with `preferredItemWidth`.
- In `TimePickerElementColors`, replace `clockDialUnselectedContentColor` → `clockDialContentColor`, `periodSelectorUnselectedContainerColor` → `periodSelectorContainerColor`, `periodSelectorUnselectedContentColor` → `periodSelectorContentColor`, `timeSelectorUnselectedContainerColor` → `timeSelectorContainerColor`, and `timeSelectorUnselectedContentColor` → `timeSelectorContentColor`. Do not rename unrelated color fields such as `RadioButton.disabledUnselectedColor`.

Source: published UI `58.0.19` modifier, carousel, and `DatePicker` declarations and its [package changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.19).

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

## Hosted-view interaction fixes

SDK 58 measures `RNHostView` children at their native container placement, including safe-area offsets, instead of assuming the host's origin. Check `measure()` and touch targets inside `BottomSheet`, `Popover`, `AlertDialog`, and `DropdownMenu` before retaining older coordinate workarounds. Tapping outside a hosted text input dismisses its keyboard; dismissing a SwiftUI `Menu` no longer activates the view beneath it. Re-test keyboard and gesture expectations in these presentations after rebuilding. Sources: UI [package changelog](https://www.npmjs.com/package/@expo/ui/v/58.0.19) and the [RNHostView guide](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/rnhostview/).

## Duo integration

Use [Hinge and ArrangementView](22-hinge-arrangementview.md) for verified signatures, build/OS gates, old-OS fallback, and copyable examples. Use [iPhone Duo support](23-iphone-duo.md) for the app-level migration and QA workflow. Native system bars, custom React Native bars, safe-area padding, and interior reserved regions are separate mechanisms. Do not claim that wrapping a React Native screen in `Host` solves every Duo layout concern.
