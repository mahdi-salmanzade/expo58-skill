# SDK 58: animation, gestures, and native dependency alignment

Audited **2026-10-13** against the published Expo 58.0.8 bundle map and third-party
package sources. Read [sdk-versions.json](sdk-versions.json) for the complete map.
SDK 58 is beta and its React Native dependency remains `0.88.0-rc.4` at this audit.

## Treat these as a compatible set

| Library | SDK 58 | SDK 57 (`expo@57.0.28`) |
|---|---|---|
| Reanimated | `4.7.0` | `4.5.1` |
| Worklets | `0.13.0` | `0.10.1` |
| Gesture Handler | `~3.2.1` | `~2.32.0` |
| Screens | `~4.29.0` | `~4.26.0` |
| Safe Area Context | `~5.9.1` | `~5.7.0` |
| Keyboard Controller | `1.22.4` | `1.21.9` |
| Skia | `2.13.1` | `2.6.2` |
| SVG | `15.15.5` | `15.15.4` |

Install via Expo to use the map belonging to the app's actual SDK:

```sh
npx expo install react-native-reanimated react-native-worklets react-native-gesture-handler
npx expo install --check
```

Reanimated 4.7.0 peers Worklets `0.13.x` and RN `0.86 - 0.88`.
Worklets 0.13.0 peers RN `0.86 - 0.88`. The Expo-specified RC is the audited
combination; dependency managers may have prerelease-range quirks, which are not a
reason to install a different RN family or suppress all dependency validation.
Do not combine Reanimated 4.7 with SDK 57's Worklets 0.10.1.

## Babel and rebuilds

With `babel-preset-expo`, Worklets configuration is automatic after installation.
The 58.0.13 preset resolves `react-native-worklets/plugin`. Avoid duplicate manual
Reanimated/Worklets plugins copied from older guides.

After changing Babel configuration, restart Metro with `--clear`. After changing
these native packages, rebuild the development client. A JavaScript export or
Fast Refresh cannot update the native Worklets implementation in an installed app.
Check the resolved package tree when JavaScript, plugin, and native versions differ.

```sh
npm ls react-native react-native-reanimated react-native-worklets react-native-gesture-handler
```

Use the equivalent tree inspection for pnpm, Yarn, or Bun. Avoid duplicate Worklets
copies in a workspace. Debug with Hermes/React Native DevTools; old remote
JavaScriptCore debugging is not compatible with the native Reanimated runtime.

## Gesture Handler 3: choose the appropriate migration scope

The new API uses hooks such as `usePanGesture` and `useTapGesture`, configured with
objects. Published 3.2.1 still exports `Gesture` builders. Existing builder-based
code is not automatically invalid, but legacy types and rewritten wrapped
components need review. Migrate an interacting gesture group together; hooks and
legacy gestures cannot form cross-API relations.

Key API mappings for an intentional hook migration:

| Builder API | Hook API |
|---|---|
| `Gesture.Pan().minDistance(8)` | `usePanGesture({ minDistance: 8 })` |
| `onStart` | `onActivate` |
| `onEnd` | `onDeactivate` |
| `onTouchesCancelled` | `onTouchesCancel` |
| `onChange` | `onUpdate` with `change*` values |
| `Gesture.Race` | `useCompetingGestures` |
| `Gesture.Simultaneous` | `useSimultaneousGestures` |
| `Gesture.Exclusive` | `useExclusiveGestures` |

The old success argument becomes `event.canceled`, with inverted meaning. Use
`!event.canceled` when acting only on successful completion. Do not mechanically
rename callbacks while preserving `success === true` logic.

This original example uses the audited hooks API. Place it beneath the app's
`GestureHandlerRootView` (usually in the root layout):

```tsx
import Animated, {
  useAnimatedStyle, useSharedValue, withSpring,
} from 'react-native-reanimated';
import { GestureDetector, usePanGesture } from 'react-native-gesture-handler';

export function SpringHandle() {
  const offset = useSharedValue(0);
  const pan = usePanGesture({
    minDistance: 8,
    onUpdate: (event) => {
      offset.value = event.translationX;
    },
    onFinalize: () => {
      offset.value = withSpring(0);
    },
  });
  const style = useAnimatedStyle(() => ({
    transform: [{ translateX: offset.value }],
  }));
  return (
    <GestureDetector gesture={pan}>
      <Animated.View
        accessibilityLabel="Drag handle"
        style={[{ width: 80, height: 48, backgroundColor: '#3871C1' }, style]}
      />
    </GestureDetector>
  );
}
```

Do not use `minDistance` together with `activeOffsetX/Y` or `failOffsetX/Y` in the
3.2.1 hook configuration: the package validates and rejects those combinations.
Choose the activation model that matches the interaction.

## Native wrapper and composition traps

Inspect the installed package exports when old types stop compiling. The builder
`PanGesture` type is exported as `LegacyPanGesture`; the new unprefixed name
describes the hook API. `createNativeWrapper` becomes `legacy_createNativeWrapper`.
Wrapped scrolling and button components have new internals even where their public
name stays the same. Test nested scroll, taps, swipeables, and cancellation.

For gestures on SVG descendants, preserve the SVG hierarchy with
`InterceptingGestureDetector` and descendant `VirtualGestureDetector` as described
in the upstream detector docs. A native detector wrapper inserted among SVG nodes
can break rendering or gesture targets.

When using `ReanimatedSwipeable`, review `dragOffsetFromRight`: the new API expects
negative values. Check the Android ripple and pressed feedback when replacing
deprecated button components with `Touchable`; visual defaults differ.

## Resizing and fold posture

Animations must survive a container resize while active. Derive travel limits
from current layout measurements or `useWindowDimensions`, not a module-level
screen width or a guessed device model. Re-clamp offsets when their bounds change.
Keep task selection, input contents, and scroll position when the layout adapts.

Hinge values describe posture, not a gesture handler or a layout width. Avoid
sending every sensor update through expensive React render work. Subscribe only
where a visible effect needs it, clean up listeners, and use the Hinge support
fallback. Native ArrangementView events and low-level hinge sensor values serve
different purposes; choose one source of truth for each UI decision.

Use Safe Area Context for the current window, including nested presentations.
Do not turn a folded layout into hard-coded "half of the screen" constants.
Respect reduced motion and test keyboard changes during window resize.

## Verification with a rebuilt binary

Check one representative drag, cancellation, simultaneous scroll interaction,
modal or sheet, keyboard transition, and resize in the requested platforms.
Use a release build for performance or native optimization regressions. A Jest
mock cannot verify UI-thread behavior, native hit testing, or real fold telemetry.
Do not claim hardware validation unless it was performed.

## Sources

- [Expo Reanimated reference](https://docs.expo.dev/versions/v58.0.0/sdk/reanimated/).
- [Expo Gesture Handler reference](https://docs.expo.dev/versions/v58.0.0/sdk/gesture-handler/).
- [RNGH 3 migration guide](https://docs.swmansion.com/react-native-gesture-handler/docs/guides/upgrading-to-3/).
- [Gesture Handler 3.2.1 metadata and source tarball](https://registry.npmjs.org/react-native-gesture-handler/3.2.1): `src/index.ts`, `src/v3/types`, `src/v3/hooks/gestures/pan/usePanGesture.ts`.
- [Reanimated 4.7.0 metadata](https://registry.npmjs.org/react-native-reanimated/4.7.0).
- [Worklets 0.13.0 metadata](https://registry.npmjs.org/react-native-worklets/0.13.0).
