# Development feedback and meaningful verification — SDK 58

Verified 2026-10-16. Use [sdk-versions.json](sdk-versions.json) for version evidence.

## Match the test environment to the feature

| Feature | Useful environment |
| --- | --- |
| Layout and navigation | Simulator/emulator, plus supported web if applicable |
| New native package/config plugin | Rebuilt development client |
| Push, biometrics, camera, location, audio behavior | Physical device where practical |
| R8/minification, startup, release entitlements | Release/preview binary |
| iPhone Duo posture | Supported Duo simulator/device; resize fallback separately |
| OTA compatibility | Binary with `expo-updates` configured |

A passing JS bundle is necessary but does not prove a native feature works.
Keep native compilation, type checking, and interactive behavior as distinct evidence.
As of the October 15 stable announcement, SDK 58's store-distributed Expo Go was still pending and unqualified `create-expo-app` still selected SDK 57.
Use the explicit SDK 58 template/development-build workflow in [01-core-setup-upgrade.md](01-core-setup-upgrade.md); check current availability rather than assuming the store client is ready.

## Fast local loop

```sh
npx expo install --check
npx expo-doctor
npx tsc --noEmit
npx expo start --dev-client
```

Use the scripts/package manager already present in the app.
After native changes, rebuild with `npx expo run:ios` / `npx expo run:android` or the configured EAS development profile.
For bundling failures, capture the first actionable error and reproduce the exact platform entry point.
Use `npx expo start --clear` when stale Metro state is a plausible cause; avoid cache deletion as a universal first step.

## SDK 58 tools

`expo-device-hub` is an optional dev-tools plugin for viewing/controlling local simulators and emulators in a browser.
Xcode 27 uses Device Hub instead of the older Simulator application; Expo CLI supports that workflow.
The local dashboard streams devices with touch/typing and boot/shutdown controls, CPU/memory/network metrics, and appearance/Liquid Glass/text-size/accessibility toggles.
Detect the selected Xcode installation and installed runtime before assuming a simulator exists.
EAS Simulator is separately announced as an upcoming cloud service; do not substitute it for an available local test runtime without checking service access.

```sh
npx expo install expo-device-hub
npx expo start
```

The experimental `@expo/agent-cli` can inspect compatibility and coordinate development sessions; see [05-cli-metro-bundling.md](05-cli-metro-bundling.md) for commands and setup boundaries.
SDK 58 also standardizes launch parameters shared by Expo Go and development clients.
`__expo_disable_onboarding=1`, `__expo_disable_fab=1`, and `__expo_disable_auto_launch=1` help deterministic device tests.
`EXPO_NO_DEV_MENU=1` asks the CLI to include those flags; noninteractive runs already disable that UI by default.
Use `EXPO_NO_DEV_MENU=0` when intentionally testing the development UI. Keep the returned launch URL, including its actual server port.

## Test behavior at the right level

- Unit tests: transformations, reducers, migrations, validation, and other deterministic logic.
- Component tests: accessible controls, state transitions, errors, and user-visible outcomes.
- End-to-end tests: important flows across navigation and native integration.
- Manual/device checks: OS surfaces, layout transitions, and hardware-dependent behavior.

Use `jest-expo` when the project chooses Jest. Install SDK-compatible test tooling rather than copying old versions.
Mock native boundaries only where necessary; a mock passing is not proof of native registration or permissions.
For automation, use an existing Maestro/device-test setup if available instead of introducing a competing framework.
Save screenshots with the viewport/device state when comparing foldable or adaptive layouts.

## Duo regression pass

Exercise compact, expanded, partially folded, and flat states supported by the available hardware/runtime.
Resize while an editor has unsaved text, a list is scrolled, a modal is open, and media is playing.
Verify focus, selection, navigation history, and scroll state survive.
Use actual hinge APIs for posture; a wide screenshot alone does not validate hardware behavior.
Record unavailable device/runtime cases as untested instead of passing them by assumption.

## React Native DevTools

RN 0.88 adds performance screenshots in the experimental channel and WebSocket-event inspection in the canary Network panel.
Verify the installed DevTools/release-channel capability before depending on either; their presence in the release notes does not make every stable build expose the UI.
The debugging protocol also exposes `Page.captureScreenshot` for supported attached app targets.
Use Xcode/Android Studio for native-layer debugging and a release build for production performance conclusions.

## Observe and diagnostics

Expo Observe captures startup/navigation performance, JavaScript errors, and native crashes.
`expo-observe` exposes `Observe` and `ObserveErrorBoundary`; `AppMetrics` is deprecated.
`Observe.reportError` handles explicitly caught errors; `errorHandlingEnabled: false` disables automatic unhandled-JS capture.
`Observe.clientId` can correlate an installation with other diagnostics; handle its nullable value and avoid using it as authentication.
Inspect production data only when the task and account access support it.
Keep diagnostic payloads focused and avoid sending session tokens or full private records in logs.

## Sources

- [Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [Unit testing](https://docs.expo.dev/develop/unit-testing/)
- [End-to-end testing](https://docs.expo.dev/eas/workflows/examples/e2e-tests/)
- [React Native DevTools](https://reactnative.dev/docs/react-native-devtools)
- [RN 0.88 feature channels](https://github.com/react/react-native/releases/tag/v0.88.0)
- [Observe](https://docs.expo.dev/versions/v58.0.0/sdk/observe/)
- [SDK 58 development tooling](https://expo.dev/changelog/sdk-58)
