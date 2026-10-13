# Native modules and config plugins — SDK 58

Verified 2026-10-13. SDK 58 is on the beta track; dependency authority is [sdk-versions.json](sdk-versions.json).

## Choose the smallest native boundary

- Existing Expo package: install with `npx expo install <package>`.
- A few app-specific native methods: a local module, or inline module if appropriate.
- Reusable native library: standalone Expo module with an example app.
- Native project configuration only: a config plugin; a plugin is not a runtime native module.

```sh
npx create-expo-module@latest --local
# For an independently distributed package, run outside the app:
npx create-expo-module@latest
```

Keep generated `expo-module.config.json` and platform registration in sync with native class names.
A module name passed to `requireNativeModule` must match the native export name.
Rebuild the development client after changing Swift/Kotlin or adding native dependencies.
Expo Go cannot dynamically load the new module.

## Expo Modules 2.0 is beta

SDK 58 brings the annotation-based module API to iOS and Android.
It is opt-in; the existing `definition()` DSL remains useful and supported.
Do not mechanically rename DSL constructs to guessed annotations.
Use the generator and types shipped with the installed package as the implementation authority.
A minimal Swift shape, after the generated module has its normal imports and registration:

```swift
import ExpoModulesCore

@ExpoModule
public final class SumModule {
  @JS
  func sum(left: Double, right: Double) -> Double {
    left + right
  }
}
```

For an existing module, move exports incrementally; 2.0 exports can coexist with `definition()`.
Keep a DSL implementation when a required facility has no documented 2.0 equivalent.
Verify Swift and Kotlin expose matching nullable values, argument names, async behavior, and errors.
Generate TypeScript declarations with the package's tooling when available; do not claim a hand-written interface proves native parity.

## Runtime contracts

- Prefer async native work for I/O; keep UI updates on the platform's UI thread.
- Release subscriptions and native resources when their owning JS object/screen is disposed.
- Handle absent hardware and permission denial as explicit results.
- `NativeArrayBuffer` is deprecated in favor of `ArrayBuffer`; audit ownership/lifetime at the native boundary.
- Android core now includes precompiled libraries. Measure actual builds before adding build overrides.
- With iOS 27 scenes, obtain window geometry from the active scene, not a process-wide screen singleton.

## Config plugin workflow

Use public mods such as `withInfoPlist` and `withAndroidManifest` from `expo/config-plugins`.
Make repeated runs idempotent. Avoid absolute paths and edits dependent on generated line numbers.
Use a dangerous mod only when no structured mod covers the required native file.

```sh
npx expo config --type public
npx expo config --type introspect
```

Inspect the generated diff in a disposable checkout before changing an existing native app.
Do not run `prebuild --clean` on hand-maintained native directories as a routine repair.
For manually managed AppDelegate overrides, use the scene lifecycle migration guide.
App Intents remain alpha and require their separate package/setup; they are not ordinary JS exports.

## Validation

Compile the native module on each supported platform and call every exported method from the example app.
Check event cleanup, cancellation, rejected promises, and native errors across a reload.
A TypeScript check alone cannot detect missing autolinking or binary incompatibility.

## Sources

- [Module creation](https://docs.expo.dev/modules/get-started/)
- [Modules API](https://docs.expo.dev/modules/module-api/)
- [Modules 2.0 design and migration](https://expo.dev/blog/an-early-look-at-expo-modules-2-0)
- [SDK 58 beta release notes](https://expo.dev/changelog/sdk-58-beta)
- [Config plugins](https://docs.expo.dev/config-plugins/introduction/)
- [Scene lifecycle migration](https://expo.fyi/ios-scene-lifecycle)
