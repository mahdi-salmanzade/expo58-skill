# EAS build, update, and distribution workflow — SDK 58

Verified 2026-10-16. EAS is a service/CLI with its own release cadence; SDK dependencies are in [sdk-versions.json](sdk-versions.json).
Run only the operations required by the user's task and existing authorization.

## Establish the intended target

Inspect `eas.json`, app identity, EAS project ID, account, branch, and working tree before a remote operation.
Reuse the linked project unless a new one is intended.

```sh
eas whoami
eas project:info
npx expo install --check
npx expo-doctor
```

For a new EAS project, `eas init` links it and `eas build:configure` creates build configuration.
Those are setup operations, not mandatory repairs for every build failure.
Use the project's established CLI version or current EAS CLI help if a flag is unfamiliar.

## Build profiles

A small `eas.json` starting point, to merge with existing configuration:

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "environment": "development"
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview",
      "environment": "preview"
    },
    "production": {
      "channel": "production",
      "environment": "production"
    }
  }
}
```

A development profile requires `expo-dev-client` installed in the application.
A simulator build is a separate iOS artifact configuration, not a device-installable IPA.
Choose current build images for toolchain needs; do not paste an SDK 57 image into SDK 58 by habit.
Cloud image, simulator runtime, and store-distributed Expo Go availability evolve independently of SDK 58's stable npm release.
Check the infrastructure catalog for required Xcode/runtime support before scheduling a build or a Duo test.

```sh
eas build --platform ios --profile preview
eas build:list --platform ios
```

Inspect build completion and the actual artifact. A queued build is not a verified distributable.
Do not trigger store submission just because a build succeeds.
When submission is requested, select the intended build explicitly and inspect the submission result.
Store review/availability is separate from successful upload.

## Updates

For initial setup, install `expo-updates` and run `eas update:configure`.
Review the native runtime policy and build a binary containing the configuration before testing OTA behavior.

```sh
eas update --channel preview --environment preview --message "Fix saved-note layout"
```

Publishing is an external mutation; keep the selected channel/environment within the requested scope.
A channel selects the update stream; runtime version enforces native compatibility.
Use matching environment inputs for Build and Update so the JS bundle does not point at the wrong backend.
For runtime policy and fingerprint caveats, read [08-sqlite-updates-convex.md](08-sqlite-updates-convex.md).
Verify update ID/runtime/channel on an installed preview build and test a cold launch.
Plan rollback using the installed EAS CLI's supported update controls before promoting a risky change.

## Environment and automation

`EXPO_PUBLIC_*` values are compiled into client code and are public.
EAS secret visibility protects build/service inputs, not values embedded in an app.
Use `eas env:pull --environment preview` when the task requires local parity; preserve local overrides deliberately.
If CI is requested, use scoped credentials and project-specific EAS Workflows or existing CI.
Do not create a second release pipeline merely because a sample workflow exists.

## Optional PostHog integration

This EAS CLI integration works across SDK versions; adopt it when PostHog is part of the requested analytics work:

```sh
eas integrations:posthog:connect
```

It creates/links a PostHog project, installs SDK/native dependencies, adds `posthog-react-native/expo`, and writes local/EAS environment variables.
Choose the intended US/EU region and analytics/replay/error-tracking features. Dynamic app configs require adding the printed plugin entry manually; rebuild for native changes.
Finish the provider and release-tagging setup in the guide. Connecting alone does not insert the React provider or register every event property.
Use `eas/update_id`, `eas/channel`, and `eas/runtime_version` from `expo-updates` as event properties; `eas/build_id` comes from a workflow build job, not an automatic in-app API.
PostHog recognizes those names for release context and links identifiers to Expo. Development/Expo Go events have no update/channel identity.
Error tracking also needs its source-map setup; keep its private CLI key out of public app configuration.
`eas integrations:posthog:disconnect` removes the Expo integration link, leaving PostHog projects/data intact.

## Sources

- [PostHog integration and release tagging](https://docs.expo.dev/guides/using-posthog/)
- [EAS CLI reference](https://docs.expo.dev/eas/cli/)
- [Build configuration](https://docs.expo.dev/build/eas-json/)
- [Build infrastructure](https://docs.expo.dev/build-reference/infrastructure/)
- [Update setup](https://docs.expo.dev/eas-update/getting-started/)
- [EAS environment variables](https://docs.expo.dev/eas/environment-variables/)
- [EAS Workflows](https://docs.expo.dev/eas/workflows/introduction/)
