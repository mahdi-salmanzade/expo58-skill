# Development feedback and meaningful verification — SDK 58

Verified 2026-10-13. Use [sdk-versions.json](sdk-versions.json) for version evidence.

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
Detect the selected Xcode installation and installed runtime before assuming a simulator exists.

```sh
npx expo install expo-device-hub
npx expo start
```

The experimental `@expo/agent-cli` can inspect project compatibility and coordinate a development session.
Inspect its help before adopting it; preserve an existing CLI workflow unless replacing it is useful to the task.
Its agent setup/skill synchronization modifies project guidance, so use it as an intentional setup step.

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

## Observe and diagnostics

`expo-observe` exposes `Observe` and `ObserveErrorBoundary`; `AppMetrics` is deprecated.
`Observe.reportError` handles explicitly caught errors; configure automatic capture deliberately.
Inspect production data only when the task and account access support it.
Keep diagnostic payloads focused and avoid sending session tokens or full private records in logs.

## Sources

- [Development builds](https://docs.expo.dev/develop/development-builds/introduction/)
- [Unit testing](https://docs.expo.dev/develop/unit-testing/)
- [End-to-end testing](https://docs.expo.dev/eas/workflows/examples/e2e-tests/)
- [Observe](https://docs.expo.dev/versions/v58.0.0/sdk/observe/)
- [SDK 58 development tooling](https://expo.dev/changelog/sdk-58-beta)
