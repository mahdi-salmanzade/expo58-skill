# Expo Router in SDK 58

Verified **2026-10-16** against published `expo-router@58.0.21` declarations and the [SDK 57 → 58 migration guide](https://docs.expo.dev/router/migrate/sdk-57-to-58/). SDK 58 was released on October 15; see [the version snapshot](sdk-versions.json) for the audited dependency set.

## Installation and imports

In an SDK 58 app, resolve compatible dependencies with `npx expo install expo-router react-native-safe-area-context react-native-screens expo-linking expo-constants expo-status-bar`. Keep `main: "expo-router/entry"`; put routes in `src/app` (or `app`) and shared code outside the route directory. Native dependency changes require a rebuilt development client.

| API | Public import |
| --- | --- |
| `Stack`, `Link`, `router`, `useRouter`, `useLocalSearchParams`, `useFocusEffect` | `expo-router` |
| `ThemeProvider`, `DefaultTheme`, `DarkTheme`, `useTheme`, `usePreventRemove`, `useLoaderData` | `expo-router` |
| `NativeTabs` | `expo-router/native-tabs` |
| `Tabs` | `expo-router/js-tabs` |
| `Drawer` | `expo-router/drawer` |
| `createNativeStackNavigator` | `expo-router/native-stack` |
| `Head` (default export) | `expo-router/head` |
| `Metadata`, loader helpers | `expo-router/server` |
| `ScrollViewStyleReset`, `useServerDocumentContext` | `expo-router/html` |

The published package has an **exports map**. Use supported subpaths; SDK 57's root-shim assumptions are obsolete. `unstable-native-tabs` remains an exported compatibility path, but new SDK 58 code uses `native-tabs`. `Tabs` at the root remains deprecated. `ExperimentalStack` and `unstable-split-view` remain experimental surfaces; a stable NativeTabs path does not stabilize those APIs. Source: [published package](https://www.npmjs.com/package/expo-router/v/58.0.21).

## Stable server and navigation features

Data loaders, server rendering, middleware, native tabs, toolbars, and standard navigation integration are stable in SDK 58. This does not change the status of `ExperimentalStack`, split view, React Server Components, or the experimental analytics observer. [SDK 58 release](https://expo.dev/changelog/sdk-58)

Remove the Router plugin options `unstable_useServerRendering`, `unstable_useServerDataLoaders`, and `unstable_useServerMiddleware`; they are deprecated even when set to false. Choose rendering behavior through `web.output`, and use `Cache-Control` response headers to control loader reuse through the platform HTTP cache. An omitted `web.output` now means `server`. Web routes are asynchronously split by default; set the Router plugin's `asyncRoutes: { web: false }` when synchronous loading is required. Native production route loading remains synchronous. Sources: [server rendering](https://docs.expo.dev/router/web/server-rendering/), [data loaders](https://docs.expo.dev/router/web/data-loaders/), [async routes](https://docs.expo.dev/router/web/async-routes/).

## Native tabs

Use compound label/icon components, and declare every tab to display. Do not infer NativeTabs behavior from JavaScript tab-bar props.

```tsx
import { NativeTabs } from 'expo-router/native-tabs';

export default function TabsLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="house" md="home" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="settings">
        <NativeTabs.Trigger.Label>Settings</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="gearshape" md="settings" />
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

Install `expo-symbols` for Android `md` icons. Android `Stack.Toolbar` needs `@expo/ui`; both are optional Router peers. Keep a web implementation where a native navigation surface is unsupported. API reference: [Native tabs](https://docs.expo.dev/versions/v58.0.0/sdk/router/native-tabs/).

## Migration decisions that affect existing apps

- Navigate to complete hrefs; `screen`, `params`, and `initial` are ordinary parameters now. Include descendant parameters explicitly in the href.
- Remove navigator `initialRouteName`; put deep-link back destinations in layout `unstable_settings.anchor`. The launch URL chooses the initial page. Use `{ withAnchor: true }` for imperative navigation that needs the anchor.
- Tabs and drawers display only declared screens. Replace screen `redirect` with route `Redirect` or protected-route `redirectTo`; supply parameter defaults in route code instead of `initialParams`.
- Remove ineffective `freezeOnBlur`. `activityEnabled` preserves state while hiding content and cleaning effects; stacks also accept a numeric depth threshold.
- `web.output: "server"` now renders on requests. Static HTML metadata needs route `generateMetadata`; `Head` still handles client updates. To retain prerendered HTML plus APIs, use static output and the Router plugin's `apiRoutes: true`; API routes still need a deployed server.
- Custom `+html.tsx` must render the attributes and nodes from `useServerDocumentContext()`, including `bodyNodes` for hydration. Read its route props rather than calling navigation hooks there. On web, move safe-area spacing to CSS `env(safe-area-inset-*)`.
- Router tests require `@testing-library/react-native` 14+. Await `renderRouter` and asynchronous `testRouter` navigation helpers; replace removed `renderRouterAsync` with `renderRouter`.

These are migration prompts, not permission to refactor every navigator. Follow the relevant sections of the [official migration guide](https://docs.expo.dev/router/migrate/sdk-57-to-58/) and test deep links, restoration, guards, and back behavior.

## Transitions and activity

The experimental navigation transition API can retain the current screen while another loads; only preloads use transitions by default. Configure the [transition policy](https://docs.expo.dev/router/advanced/navigation-transitions/) for the app's loading UX rather than assuming every navigation is wrapped. [`NavigationAwareActivity`](https://docs.expo.dev/router/advanced/react-activity/) can hide a subtree while preserving state and cleaning up effects. For a screen-level fallback that leaves its navigator mounted, use `unstable_settings.screenErrorBoundary` or `Stack`'s `unstable_screenErrorBoundary` prop; the option names retain their `unstable` prefix. [Error handling](https://docs.expo.dev/router/error-handling/)

## Advanced state integrations

Use URL hooks for route information instead of depending on navigation-state internals. In `58.0.21`, `dispatch` is deferred after the React commit, accepts an action object rather than a function, and has an explicit `dispatchSync` escape hatch. `beforeRemove` is replaced by removal/prevention events. `usePreventRemove` receives `repeat`; update the prevention condition before repeating an action. Persisted navigation state must be complete at every level; the old partial-state restoration contract is gone. `useNavigation` requires navigator context. Review custom routers through the current `extendRouter` API and declarations instead of carrying a React Navigation implementation over unchanged. Source: [SDK 58 Router implementation](https://github.com/expo/expo/tree/main/packages/expo-router) and the installed package's `build/react-navigation` declarations; verify the installed patch before using moving `main` examples.

## Duo navigation

Retain one owner for route history and selected content while space changes. Do not key a navigator by hinge angle, orientation, window width, or device model. Use native containers when they fit the app, but verify actual side bars and overflow in the binary built with the iOS 27.1 SDK. JavaScript custom bars do not gain native adaptation from an Expo version upgrade.

Read [iPhone Duo support](23-iphone-duo.md) for build prerequisites, per-edge safe areas, state continuity, and acceptance checks. Read [Hinge and ArrangementView](22-hinge-arrangementview.md) for adaptive content inside a screen; an arrangement does not replace route navigation.
