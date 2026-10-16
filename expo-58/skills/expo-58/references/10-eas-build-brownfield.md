# Native builds and brownfield integration — SDK 58

Verified 2026-10-16. Use [sdk-versions.json](sdk-versions.json) for the SDK/toolchain baseline.

## Choose a build path

| Need | Path |
| --- | --- |
| Iterate on custom native APIs | Development build with `expo-dev-client` |
| Reproduce an iOS/Android native failure locally | `npx expo run:ios` / `npx expo run:android` |
| Signed distributable or managed cloud build | EAS Build |
| Add Expo packages to an existing React Native project | `npx install-expo-modules@latest`, review native diff |
| Embed React Native screens in a native host | Brownfield integration |

```sh
npx expo install expo-dev-client
npx expo run:ios
```

Native dependency/config-plugin changes need a new binary. Restarting Metro is insufficient.
Use the existing package manager and lockfile. Diagnose installation alignment with `npx expo install --check`.
For shared build/release configuration, continue to [18-eas-full-workflow.md](18-eas-full-workflow.md).

## SDK 58 build changes

Android `expo-modules-core` ships precompiled native libraries for all four ABIs in debug and release variants, reducing clean-build compilation work.
Keep the prebuilt path unless native patches or compiler compatibility require source builds.
For that case, set `android.buildExpoModulesCoreFromSource: true` in the `expo-build-properties` plugin configuration and rebuild.
Android release builds now enable R8 by default. Check startup and reflection-dependent libraries in release, not only debug.
Fix missing keep rules when possible; `android.enableMinifyInReleaseBuilds: false` is an explicit plugin opt-out when needed.

CocoaPods remains the supported default iOS path. Expo's autolinking integration with `npx react-native spm` is a preview, not a required migration.
Pick an EAS image from the current image catalog when a specific Xcode SDK is needed; SDK release status alone does not identify an installed image.
Features tied to iOS 27 or iPhone Duo need an appropriate build SDK and runtime, not merely an SDK 58 JS package.

## Continuous Native Generation versus owned native projects

If native folders are generated, express required changes in app config/config plugins.
If they are maintained by hand, merge upgrade changes into them and preserve custom targets/capabilities.
`prebuild --clean` regenerates native folders: first account for any native edits that would be lost.
Build-property overrides belong in `expo-build-properties` where supported, not ad hoc edits to generated files.
Do not lower deployment targets below package requirements to silence a build error.

## Brownfield contract

```sh
npx expo install expo-brownfield
npx expo-brownfield --help
```

`expo-brownfield` provides a config plugin, communication APIs, and artifact-building CLI.
Treat the host app and the embedded React Native feature as separate owners of lifecycle and dependencies.
Agree on the root component name, initial props, message schema, navigation ownership, and error boundary.
Send versioned, serializable messages; do not assume native and JS components become ready simultaneously.

For iOS, review scene lifecycle integration and preserve host AppDelegate/SceneDelegate behavior.
For Android, align host versions of React Native, Hermes, Kotlin, and any shared UI/image libraries.
Inspect duplicate classes and native libraries before choosing fused artifacts.
A fat AAR does not mean all dependencies, including the runtime, should be embedded twice.
The package supports XCFramework and Maven workflows; read `build:ios --help` / `build:android --help` before choosing output flags.
Building and publishing are separate concerns, even when a particular CLI subcommand can do both.

## Failure triage

1. Find the first native compilation/linking exception, rather than the final EAS summary.
2. Confirm package versions, selected build profile/environment, platform, and native source state.
3. Check generated plugin output and whether a binary rebuild actually occurred.
4. Reproduce in a small app or the native module's example when host integration is the variable.
5. Clear caches only when evidence points to stale generated artifacts.

## Validation and sources

Exercise embedded screen mount/unmount, background/foreground, deep links, and process restart.
A successful artifact build does not prove it loads in the intended host application.

- [EAS Build](https://docs.expo.dev/build/introduction/)
- [Build infrastructure](https://docs.expo.dev/build-reference/infrastructure/)
- [Brownfield](https://docs.expo.dev/versions/v58.0.0/sdk/brownfield/)
- [SDK 58 build changes](https://expo.dev/changelog/sdk-58)
- [Build properties](https://docs.expo.dev/versions/v58.0.0/sdk/build-properties/)
- [Prebuilt Expo modules](https://docs.expo.dev/guides/prebuilt-expo-modules/)
- [Scene lifecycle migration](https://expo.fyi/ios-scene-lifecycle)
