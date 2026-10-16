# Native modules and config plugins — SDK 58

Verified 2026-10-16. SDK 58 is stable; dependency authority is [sdk-versions.json](sdk-versions.json).

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

SDK 58 also reduces iOS bridging overhead for simple values, strings, and promise creation/resolution.
Existing Expo modules receive those runtime improvements on upgrade; adopting the beta annotation API is not required, and app-level gains should be measured.

## Runtime contracts

- Prefer async native work for I/O; keep UI updates on the platform's UI thread.
- Release subscriptions and native resources when their owning JS object/screen is disposed.
- Handle absent hardware and permission denial as explicit results.
- `NativeArrayBuffer` is deprecated in favor of `ArrayBuffer`; audit ownership/lifetime at the native boundary.
- Android core now includes precompiled libraries. Measure actual builds before adding build overrides.
- With iOS 27 scenes, obtain window geometry from the active scene, not a process-wide screen singleton.

## TurboModule binary data

React Native's TurboModule `ArrayBuffer` support is separate from Expo's `NativeArrayBuffer` deprecation.
On Android, `com.facebook.react.bridge.ArrayBuffer` distinguishes owned from borrowed bytes.
Borrowed arguments expire when the receiving native call returns; copy with `ArrayBuffer.arrayBufferWithCopiedBytes` before retaining them or scheduling asynchronous work.
Returning an owning buffer can alias the original bytes through a different JS object, so coordinate concurrent access.
Use the generated bindings for the installed RN version: 0.88 stable restored Objective-C `NSMutableData *` signatures after the RC's `RCTArrayBuffer` change.
It also restored the previous C++ `EventEmitter<ArrayBuffer>` support; do not apply the RC-only rejection as a stable migration rule.

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

## App Intents remain alpha

`expo-app-intents` connects iOS Siri/Shortcuts and Spotlight to app-defined native intents/entities.
Install its compatible package, initialize the app-target Swift sources, and rebuild:

```sh
npx expo install expo-app-intents
npx expo-app-intents init
```

The optional `npx @expo/agent-cli@latest install expo-app-intents` command also sets up the package’s colocated agent skill.
The initializer adds the plugin and watches `app-intents` through `experiments.inlineModules.watchedDirectories`.
Declare intent/entity/query types and shortcut phrases in Swift; JavaScript cannot dynamically declare new intent types.
Use `import * as AppIntents from 'expo-app-intents'` for the JS APIs and gate with `isAvailable()`.
`setEntityCatalogAsync` replaces a named catalog; publish a compact relevant subset and keep stable entity IDs.
Indexed Swift registration enables Spotlight; ordinary catalog publication does not invent native registration.
For in-app actions that Siri should learn to suggest, register a Swift `DonatableAppIntent` and call `donateIntentAsync(name, params)` after the action succeeds.
Remove outdated donations with `deleteDonationsAsync`, including after deleting the associated entity or signing out.

`useAppIntents` delivers pending and live invocations. Apply actions idempotently by invocation `id`, then call `removePendingInvocationAsync(id)`.
The queue is bounded to 100 entries and does not remove handled items automatically.
Native dispatch can persist work while JS is stopped; it does not wait for a JS result for Siri.
Headless execution through TaskManager is announced as coming soon, so a background Siri response still needs a native implementation.

Associate visible content with `AppEntityView` for React Native or `appEntityIdentifier()` for Expo UI.
That association requires iOS 18.4+ and Xcode 27+; unsupported versions render the view without the association.
Test real-device shortcuts, a cold launch, duplicate delivery, sign-out/deleted entities, and unavailable platforms.

## Validation

Compile the native module on each supported platform and call every exported method from the example app.
Check event cleanup, cancellation, rejected promises, and native errors across a reload.
A TypeScript check alone cannot detect missing autolinking or binary incompatibility.

## Sources

- [Module creation](https://docs.expo.dev/modules/get-started/)
- [Modules API](https://docs.expo.dev/modules/module-api/)
- [Modules 2.0 design and migration](https://expo.dev/blog/an-early-look-at-expo-modules-2-0)
- [SDK 58 release notes](https://expo.dev/changelog/sdk-58)
- [AppIntents setup and native/JS boundary](https://docs.expo.dev/versions/v58.0.0/sdk/app-intents/)
- [Published AppIntents declarations](https://unpkg.com/expo-app-intents@0.5.8/build/index.d.ts)
- [RN 0.88 stable changes](https://github.com/react/react-native/releases/tag/v0.88.0)
- [Android buffer ownership](https://github.com/react/react-native/blob/v0.88.0/packages/react-native/ReactAndroid/src/main/java/com/facebook/react/bridge/ArrayBuffer.kt)
- [Config plugins](https://docs.expo.dev/config-plugins/introduction/)
- [Scene lifecycle migration](https://expo.fyi/ios-scene-lifecycle)
