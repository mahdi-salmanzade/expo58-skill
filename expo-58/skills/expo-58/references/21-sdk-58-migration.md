# Upgrade to SDK 58: execution and behavior changes

Audited **2026-10-16**. Stable target: `expo@58.0.12`, RN `0.88.0`, React `19.3.0`.
SDK 58 was released October 15. Exact package ranges and integrity-verified
provenance are in [sdk-versions.json](sdk-versions.json). Individual experimental
features retain their own maturity level; upgrading does not require adopting them.

## 1. Establish a recoverable baseline

Inspect the current SDK, package manager, lockfile, native ownership, runtime
policy, plugins, and custom build steps. Record existing failures before editing.
Keep a recoverable copy of app/native/config changes; do not discard uncommitted
work to obtain a clean checkout.

Use Node satisfying `^22.13.0 || ^24.3.0 || ^26.0.0 || >=27.0.0`.
SDK 58 compiles Android against 37 while targeting 36. Its generic iOS/Xcode
floor remains 16.4 / 26.4; native iOS 27 and Duo features need their newer toolchain.
New Architecture cannot be disabled on 55+.

## 2. For SDK 56, make a working SDK 57 checkpoint first

```sh
npx expo install expo@^57.0.30 --fix
npx expo-doctor@latest
npx expo install --check
```

This hop changes RN 0.85 → 0.86 and raises Expo's supported Node floor to 22.13.x.
Use current SDK 57 patches: the early-57 Hermes V1 memory regression is fixed only
in `expo` >= 57.0.9. The separate development-startup regression
([expo/expo#48298](https://github.com/expo/expo/issues/48298)) was fixed in
Expo 57.0.17 / RN 0.86.3 / Hermes 250829098.0.17, according to the
[maintainer's release confirmation](https://github.com/expo/expo/issues/48298#issuecomment-5437781055).
Do not generalize that fix to every later startup issue: record the exact binary
and investigate a reproducible failure. The audited 57 map aligns
Reanimated 4.5.1, Worklets 0.10.1, and Gesture Handler ~2.32.0. Keeping SDK 56's
Reanimated dependency with RN 0.86 is not a valid shortcut.

The SDK 57 prebuild default changed from additive generation to clean regeneration.
For CNG, regenerate after preserving changes. For hand-managed native code, apply
the [native upgrade diff](https://docs.expo.dev/bare/upgrade/) instead of deleting
source. Build and test this checkpoint before proceeding to 58.
If starting earlier than 56, include every intervening SDK's migration first.

Do not infer an SDK 57 codemod from the existence of an SDK 56 Router codemod.
Inspect the [SDK 57 release notes](https://expo.dev/changelog/sdk-57) and actual
app usage; do not run an unrelated source rewrite on the 57 → 58 step.

## 3. Align SDK 58 dependencies and native projects

```sh
npx expo install expo@^58.0.0 --fix
npx expo-doctor@latest
npx expo install --check
```

Preserve the package manager and inspect the lockfile diff. Confirm React 19.3.0,
RN 0.88.0, Reanimated 4.7.1, Worklets 0.13.0, and Gesture Handler ~3.3.0.
`expo@latest` now resolves to 58, but the major-constrained command preserves the
upgrade target when tags move. `next` currently points to an older patch; it is
not the stable upgrade recipe. Earlier SDK 58 beta apps also need dependency
realignment and a new native binary to replace their RN release candidate.

For CNG, run prebuild after preserving changes and rebuild the client. CLI58's
default remains destructive; `--no-clean` requests additive behavior. Maintained
native projects need the upgrade helper plus Pod/Gradle updates and lifecycle
changes below. Generating a disposable comparison project can make the diff clear.

`jest-expo@58.0.11` peers Jest `^29.0.0 || ^30.0.0` and
`@react-native/jest-preset@^0.88.0`. Upgrade existing test tooling as a coherent
set instead of keeping a 57 native Jest preset or suppressing peer conflicts.

The stable release precedes SDK 58's store Expo Go rollout. Use a development
build or confirm a matching Expo Go installer; a successful package upgrade does
not update the app already installed on a device.

## 4. Migrate React Native's strict TypeScript API

RN 0.87 made strict types the default; SDK 58 crosses both 0.87 and 0.88 changes.
Replace `react-native/Libraries/*` imports with public root exports or supported
alternatives. Native component refs now use instance types:

```tsx
import { useRef } from 'react';
import { TextInput, type TextInputInstance } from 'react-native';

export function SearchField() {
  const input = useRef<TextInputInstance>(null);
  return <TextInput ref={input} accessibilityLabel="Search" />;
}
```

Use the [RN strict API migration](https://reactnative.dev/docs/strict-typescript-api)
for codegen exports and other type changes. Check dependency updates before adding
type casts. A temporary deferral is `customConditions: ["react-native",
"react-native-legacy-deep-imports"]` while retaining `extends: "expo/tsconfig.base"`.
The legacy opt-out is scheduled for removal after RN 0.88; it does not restore
removed runtime APIs.

Search for `InteractionManager`, the root `Touchable` export, `NativeMethods`,
`Modal`'s `animated` prop, and obsolete `StatusBar` props. Replace deferred
InteractionManager work with appropriate idle scheduling and cleanup, `animated`
with supported Modal animation configuration, and status bar color layouts with
the intended edge-to-edge UI. `ImageBackground` is deprecated, not removed;
plan a `View` with a positioned `Image` when touching that code.
The [RN 0.88 release](https://github.com/react/react-native/releases/tag/v0.88.0)
and [RN 0.87 release](https://reactnative.dev/blog/2026/08/11/react-native-0.87)
give the removal context; inspect actual installed exports if docs change.

## 5. Preserve custom iOS startup and callback behavior

SDK 58 uses scene-based lifecycle. CNG generates `SceneDelegate.swift` and the
`UIApplicationSceneManifest`; the scene creates the window. A maintained iOS
project must add that scene setup, adopt `ExpoReactNativeFactoryProvider` in its
AppDelegate, and stop creating/starting the same window a second time.

Expo forwards events to `ExpoAppDelegate` overrides and subscribers. Custom
`UIApplicationDelegate` swizzling outside that path needs scene-aware handling.
Follow [Expo's scene migration guide](https://expo.fyi/ios-scene-lifecycle) and keep
custom launch behavior while merging the template changes.

Test cold and warm URLs, authentication return URLs, notification taps, background
and foreground transitions, quick actions, and Handoff when used. A black screen
on iOS 27 can be a missing scene declaration or unresolved scene delegate class.
Remove an old SDK 57 `expo-build-properties` plugin option `ios.enableSceneSupport`
(a plugin option, not a top-level app config `ios` key) after upgrading: 58 already
uses scene support. Avoid global screen geometry assumptions in custom modules.

## 6. Fix silent application behavior changes

Search the app for the relevant API before changing it. These are targeted checks,
not a requirement to rewrite untouched modules.

| Area | Required migration or regression check |
|---|---|
| File writes | `File.write()` is async; await completion before reads/shares, handle rejection, or intentionally use `writeSync()` for synchronous behavior. |
| SQLite libSQL | `syncLibSQL()` and `libSQLOptions` are removed; `useLibSQL` no longer enables support. Select an explicit supported synchronization path for an app using them. |
| Foreground notifications | Notifications display by default. Configure `setNotificationHandler` explicitly if the app previously relied on silence. Test slow handler behavior. |
| Fingerprint | Default `balanced` hashing can ignore package file edits/version-only app config changes. Review native patch handling and runtime decisions. |
| Expo UI Host | iOS content aligns at the top. Explicitly request old alignment where it was intentional. |
| Expo UI spacing | Omitted HStack/VStack/GlassEffectContainer spacing uses SwiftUI defaults; set `spacing={0}` only where zero spacing was intended. |
| Android RNHostView | Replace removed `style` usage with supported modifiers. |
| iOS RTL | Direction follows `I18nManager`; do not assume `supportsRTL` alone forces locale-derived layout. |
| Photos video URI | Default URI now refers to the current edited asset; pass `version: AssetUriVersion.ORIGINAL` when original bytes are required. Current `expo-media-library@58.0.9` exports this enum from both the root and `/next` entry points. |

Inspect the versioned references for [FileSystem](https://docs.expo.dev/versions/v58.0.0/sdk/filesystem/),
[SQLite](https://docs.expo.dev/versions/v58.0.0/sdk/sqlite/),
[Notifications](https://docs.expo.dev/versions/v58.0.0/sdk/notifications/),
[Fingerprint](https://docs.expo.dev/versions/v58.0.0/sdk/fingerprint/),
[Expo UI](https://docs.expo.dev/versions/v58.0.0/sdk/ui/),
[Localization](https://docs.expo.dev/versions/v58.0.0/sdk/localization/), and
[MediaLibrary](https://docs.expo.dev/versions/v58.0.0/sdk/media-library/).

Deprecations are separate from removals: `File.md5` → `File.digest()`, `AppMetrics`
→ `Observe`, and `NativeArrayBuffer` → `ArrayBuffer` can be scheduled according to
the task. Do not invent a migration urgency beyond the app's actual usage.

## 7. Test Android release optimization

The published 58.0.21 bare template sets
`android.enableMinifyInReleaseBuilds=true` and uses
`proguard-android-optimize.txt`. This is a new default, not a 57 behavior.
Reflection-heavy libraries can fail only in release builds; add the required keep
rules and test the actual feature. For a specific blocking regression, the
`expo-build-properties` plugin's `android.enableMinifyInReleaseBuilds: false`
is an explicit opt-out. Do not disable optimization preemptively for every app.

## 8. Review Router, gestures, and environment configuration

Read [Router's SDK 57 → 58 guide](https://docs.expo.dev/router/migrate/sdk-57-to-58/)
for custom navigators or `expo-router/react-navigation` imports. Route keys and
state are deterministic, navigation dispatch timing changed, and parts of the
forked React Navigation API disappeared. Avoid depending on private route shapes.
Check deep links, restored state, back gestures, tabs, drawer, and stack transitions.
`freezeOnBlur` has no effect in SDK 58; remove it and use `activityEnabled` on the
navigator or screen when inactive screens should keep state while pausing effects.

Unspecified `web.output` now means `"server"`, with HTML rendered per request.
To keep prerendered HTML plus API routes, use `web.output: "static"` with the
`expo-router` plugin's `apiRoutes: true`; the APIs still need a server deployment.
Web async routes also default to enabled; verify host routing and lazy chunks.
Update custom `+html.tsx` to include `useServerDocumentContext()` attributes,
`headNodes`, and `bodyNodes` (required for hydration), and move initial static
metadata to `generateMetadata()`. Web safe-area spacing now uses CSS
`env(safe-area-inset-*)`, not Router-provided Safe Area Context values.
See [02-expo-router.md](02-expo-router.md) for the complete web migration and
asynchronous Router testing changes. Use a production web export for `expo serve`;
it rejects development exports containing server code.
Some Router features need optional `@expo/ui` / `expo-symbols` peers. Install them
only if the app uses those features, through `npx expo install`.
Gesture Handler 3 introduces hooks but retains legacy builders; migrate interacting
groups together. See [17-animation-gesture-deps.md](17-animation-gesture-deps.md).

`expo login` now defaults to browser-based login; scripts that relied on the
prompt flow need `--no-browser` or `--username`/`--password`.

Expo CLI now sets NODE_ENV by command before `.env` and app config evaluation.
Move deployment selection away from inherited `NODE_ENV=test/staging`; use a
dedicated variable and inspect resolved config. See
[05-cli-metro-bundling.md](05-cli-metro-bundling.md) for current tunnel and mode behavior.

## 9. Verify Duo and ordinary devices separately

Adding Hinge or ArrangementView requires a native client that contains the updated
modules. Preserve compact-phone and unsupported-hardware fallbacks. Exercise
fold/unfold or available simulated posture controls, continuous window resizing,
rotation, keyboard visibility, and background/foreground without losing state.
Record which checks ran on hardware, simulator, or only static types.

An ordinary iPhone displaying the fallback is expected and does not validate hinge
events. No available Duo hardware is a limit on behavioral validation, not a reason
to fake support or block all ordinary SDK upgrade work.

## 10. Release and rollback boundary

Typecheck, lint, run existing meaningful tests, export the requested platforms,
and build native clients. Include an Android release build when testing R8-sensitive
code. Compare startup, navigation, persisted data, notifications, and authentication
against the baseline rather than reporting only a successful package installation.

Build a new runtime for SDK 58. Do not send 58 JavaScript to a 57 binary. Keep the
previous build/update runtime available and avoid irreversible local data migrations
until compatibility is understood. Rolling back a Git commit alone does not undo
data changes or a distributed native binary.

## Evidence

- [Official SDK 58 stable notes](https://expo.dev/changelog/sdk-58).
- [Expo 58.0.12 manifest](https://registry.npmjs.org/expo/58.0.12) and [SDK 57.0.30 manifest](https://registry.npmjs.org/expo/57.0.30).
- [Bare template 58.0.21](https://registry.npmjs.org/expo-template-bare-minimum/58.0.21), `android/gradle.properties` and `android/app/build.gradle`.
- [Jest Expo 58.0.11 peers](https://registry.npmjs.org/jest-expo/58.0.11).
- [Incremental upgrade guidance](https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/).
