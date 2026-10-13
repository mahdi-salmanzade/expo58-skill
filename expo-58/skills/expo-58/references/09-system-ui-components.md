# System bars, widgets, and native presentation — SDK 58

Verified 2026-10-13. Resolve dependencies with Expo and consult [sdk-versions.json](sdk-versions.json).

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
Use `updateSnapshot` for current state and `updateTimeline` for scheduled entries.
Images needed by an iOS widget must be accessible in its app group, not only the app sandbox.
Live Activities use `createLiveActivity` and their dedicated regions. They are not entries in the home-screen `widgets[]` list.
ActivityKit scheduling and update budgets remain system controlled.

SDK 58 adds Android home-screen widgets, verified in the published package changelog; the versioned Widgets guide remains primarily iOS-oriented.
Before implementing Android, inspect the installed package's Android examples and declarations; do not render SwiftUI on Android or invent a shared layout API.

## Adaptable native surfaces

Check platform/OS availability for `expo-glass-effect`, `expo-symbols`, and native controls.
Provide a readable fallback where an effect is unavailable or transparency is reduced.
Use current container size for layouts, especially iPhone Duo and iOS 27 resizable windows.
Keep safe areas, keyboard insets, and hinge geometry separate; they describe different constraints.
For SwiftUI/Compose component composition, continue to [03-expo-ui.md](03-expo-ui.md).

## Checks and sources

Test system appearance on cold launch, navigation, theme changes, and immersive views.
Test widgets while the application process is absent and in tinted/large-text modes.

- [StatusBar](https://docs.expo.dev/versions/v58.0.0/sdk/status-bar/)
- [NavigationBar](https://docs.expo.dev/versions/v58.0.0/sdk/navigation-bar/)
- [Widgets](https://docs.expo.dev/versions/v58.0.0/sdk/widgets/)
- [Published widget changelog](https://unpkg.com/expo-widgets@58.0.16/CHANGELOG.md)
- [GlassEffect](https://docs.expo.dev/versions/v58.0.0/sdk/glass-effect/)
- [SDK 58 beta](https://expo.dev/changelog/sdk-58-beta)
