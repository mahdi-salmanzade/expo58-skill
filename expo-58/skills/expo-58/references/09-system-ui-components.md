# System bars, widgets, and native presentation — SDK 58

Verified 2026-10-16. Resolve dependencies with Expo and consult [sdk-versions.json](sdk-versions.json).

## System bars

```sh
npx expo install expo-status-bar expo-navigation-bar expo-system-ui
```

```tsx
import { View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { NavigationBar } from 'expo-navigation-bar';

export function DarkSurface() {
  return (
    <View style={{ flex: 1, backgroundColor: '#151515' }}>
      <StatusBar style="light" />
      <NavigationBar style="light" />
    </View>
  );
}
```

`NavigationBar` controls Android system navigation, not your app's tab bar.
Status bar behavior varies by OS; web and tvOS have no controllable phone status bar.
The `expo-status-bar` plugin sets initial `hidden`/`style`; the navigation plugin adds `enforceContrast`.
Runtime JSX does not replace build-time initial appearance configuration.
Check text/icon contrast over actual edge-to-edge content and account for safe-area insets.
Do not rely on legacy opaque system-bar colors to create layout padding.
RN 0.88 removes its old `StatusBar` props `backgroundColor`, `translucent`, and `networkActivityIndicatorVisible`; remove those uses rather than moving them into Expo’s component.

## Widgets and Live Activities

```sh
npx expo install expo-widgets @expo/ui
```

Use a development build with the package config plugin; widgets need generated native targets/configuration.
The plugin's widget `name` must match the string supplied to `createWidget`.
Prefer nested `ios.supportedFamilies`/`ios.contentMarginsDisabled`; the old top-level aliases are deprecated.
Supply `ios.bundleIdentifier` so the plugin can derive the shared app group.

```tsx
import { Text } from '@expo/ui/swift-ui';
import { createWidget } from 'expo-widgets';

const CountWidget = (props: { count: number }) => {
  'widget';
  return <Text>{props.count} saved items</Text>;
};

export const countWidget = createWidget('CountWidget', CountWidget, { count: 0 });
// From the application, after data changes:
// countWidget.updateSnapshot({ count: 12 });
```

A widget function runs in an isolated runtime. Pass serializable props; do not access app hooks, network work, or an app context inside it.
Use `updateSnapshot` for current state and `updateTimeline` for scheduled iOS entries.
For iOS 17+ configurable widgets, declare parameters in `ios.configuration` and read `environment.configuration`.
Mark an enum parameter `dynamic: true`, then call `setConfigurationParameterEnum(name, options)` to replace its choices at runtime; app-config choices remain the fallback.
Images needed by an iOS widget must be accessible in its app group, not only the app sandbox.
Live Activities use `createLiveActivity` and their dedicated regions. They are not entries in the home-screen `widgets[]` list.
ActivityKit scheduling and update budgets remain system controlled.
Pass an optional `Date` as `start(props, url, staleDate)` or `update(props, staleDate)` to mark aging Live Activity content.
A stale date lets the system de-emphasize old content; it does not schedule an app refresh.
SDK 58 preserves ActivityKit identifiers for reliable later updates.
Current widget packages rebuild the iOS widget JS bundle on each Xcode build, so ordinary JS edits do not require a clean build.

SDK 58 Android home-screen widgets use their own JS bundle and dedicated Hermes runtime, with interactions, Material Colors, and the `cornerRadius` modifier.
The published package changelog confirms Android support; the versioned Widgets guide remains primarily iOS-oriented.
Android widgets are opt-in: set the `expo-widgets` plugin option `enableAndroid: true`
(default `false` in 58.0.x; the option is slated for removal once Android is on by default) and rebuild.
Inside an Android widget, use `Button` from `@expo/ui/jetpack-compose` with `onClick`; returning updated props lets the widget refresh without React state. The app can observe interactions with `addUserInteractionListener` from `expo-widgets` and remove that subscription on cleanup.
Call `getMaterialColors()` inside the widget renderer and pass its palette to component colors, for example `colors={{ containerColor: palette.primary, contentColor: palette.onPrimary }}`; widget palettes do not support `seedColor`.
Apply `modifiers={[cornerRadius(16)]}` from `@expo/ui/jetpack-compose/modifiers` to the widget tree on Android 12+. This modifier is widget-only; ordinary Compose app views use `clip(Shapes.RoundedCorner(16))` instead.
Keep the platform renderers separate: the SwiftUI example above is for iOS.

## Adaptable native surfaces

Check platform/OS availability for `expo-glass-effect`, `expo-symbols`, and native controls.
On iOS 27+, `isLiquidGlassAvailable()` returns true for apps built with the iOS 27 SDK or newer even if `UIDesignRequiresCompatibility` is set; that old opt-out no longer disables glass.
Keep runtime API availability checks and readable fallbacks for unsupported systems or reduced transparency.
Use current container size for layouts, especially iPhone Duo and iOS 27 resizable windows.
Keep safe areas, keyboard insets, and hinge geometry separate; they describe different constraints.
For SwiftUI/Compose component composition, continue to [03-expo-ui.md](03-expo-ui.md).

## Checks and sources

Test system appearance on cold launch, navigation, theme changes, and immersive views.
Test widgets while the application process is absent and in tinted/large-text modes.

- [StatusBar](https://docs.expo.dev/versions/v58.0.0/sdk/status-bar/)
- [NavigationBar](https://docs.expo.dev/versions/v58.0.0/sdk/navigation-bar/)
- [Widgets](https://docs.expo.dev/versions/v58.0.0/sdk/widgets/)
- [Android widget palette runtime](https://unpkg.com/expo-widgets@58.0.19/bundle/modules/expo-ui.ts)
- [Published widget changelog](https://unpkg.com/expo-widgets@58.0.19/CHANGELOG.md)
- [GlassEffect](https://docs.expo.dev/versions/v58.0.0/sdk/glass-effect/)
- [Published glass availability fix](https://unpkg.com/expo-glass-effect@58.0.4/CHANGELOG.md)
- [SDK 58 release](https://expo.dev/changelog/sdk-58)
