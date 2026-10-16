# App config, fonts, splash, and foundational packages — SDK 58

Verified 2026-10-16. Toolchain and package snapshot: [sdk-versions.json](sdk-versions.json).

## App configuration

Use `app.json` for static configuration or `app.config.ts` when configuration must be computed.
Preserve the project's existing approach instead of introducing another source of truth.
Dynamic config must return an Expo config object; preserve input config when extending it.

```ts
import type { ConfigContext, ExpoConfig } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: 'Field Notes',
  slug: 'field-notes',
  scheme: 'fieldnotes',
});
```

`ios.bundleIdentifier` and `android.package` identify installed apps; changing them creates a different application identity.
Plugin configuration is build-time input. A JS reload or OTA update cannot apply a new entitlement or native usage message.
Inspect the resolved config before building:

```sh
npx expo config --type public
npx expo config --type introspect
```

Do not log secrets while inspecting config. Values in public config and the client bundle are readable by users.
Use a separate variable such as `APP_VARIANT` for app variants; SDK 58 CLI controls `NODE_ENV` itself.
For `expo run:*`, the CLI derives `NODE_ENV` from the build configuration; non-Debug configurations use production.
EAS config evaluation, prebuild, and doctor run in production mode. Do not use `NODE_ENV` as a staging selector.
Keep EAS environment selection aligned across builds and updates.
See [18-eas-full-workflow.md](18-eas-full-workflow.md).

## Native permissions

Declare permissions/usage messages through each package's plugin where available.
Request runtime access when the relevant feature is used and support denied/limited states.
Avoid adding every permission from a sample app.
Inspect generated native output if a dependency introduces a permission the product does not need.
For localized iOS messages, use locale metadata with the actual usage-description keys.
Rebuild and test permission wording on a fresh installation or reset simulator permissions.

## Fonts and splash

```sh
npx expo install expo-font expo-splash-screen expo-asset
```

Embed app fonts through the `expo-font` plugin when known at build time, or load dynamically with `useFonts`/`loadAsync`.
SDK 58 supports variable fonts on Android, iOS, and web.
Confirm the font's family/axes and platform behavior; a file name is not always its iOS family name.
Use supported React Native font-variation settings only after checking the installed RN types.

A root layout can call `SplashScreen.preventAutoHideAsync()` at module scope.
Hide the splash when the app can render its initial useful screen, including a recoverable error state.
Do not keep the splash visible forever because an optional font or request failed.
Use the `expo-splash-screen` plugin for launch-image/background configuration and test in a release build.
Expo Go's launch screen does not prove your binary's splash assets are configured correctly.

## App/device facts

`Constants.expoConfig` is the resolved app config; access it defensively because not every execution environment exposes every field.
Use `Constants.easConfig?.projectId` / configured `extra.eas.projectId` for EAS project identity.
Use `expo-application` for native application/version facts and `expo-device` for device capabilities.
A development server's config version may differ from the installed native binary version.
Do not select a Duo layout by matching a device marketing name; use measured space and capabilities.

## Localization and RTL

Use `expo-localization` for locale facts and keep locale-aware formatting separate from navigation/layout state.
On iOS, SDK 58 no longer makes `supportsRTL` force RTL automatically from the device locale.
React Native's `I18nManager` controls direction; check existing `allowRTL`/`forceRTL` choices and test an actual relaunch.
Do not use a locale string as a substitute for verifying rendered writing direction.

## Validation

Check app identity, icon/splash, permission prompts, fonts, and environment-dependent endpoints in the actual binary.
Exercise large text, dark appearance, localization, RTL, and a resized window.
Verify source-controlled config reproduces the expected native output without undocumented manual steps.

## Sources

- [App config](https://docs.expo.dev/workflow/configuration/)
- [Versioned config reference](https://docs.expo.dev/versions/v58.0.0/config/app/)
- [Fonts](https://docs.expo.dev/versions/v58.0.0/sdk/font/)
- [SplashScreen](https://docs.expo.dev/versions/v58.0.0/sdk/splash-screen/)
- [Constants](https://docs.expo.dev/versions/v58.0.0/sdk/constants/)
- [Application](https://docs.expo.dev/versions/v58.0.0/sdk/application/)
- [Localization](https://docs.expo.dev/versions/v58.0.0/sdk/localization/)
- [SDK 58 migration details](https://expo.dev/changelog/sdk-58)
- [Environment variables](https://docs.expo.dev/guides/environment-variables/)
