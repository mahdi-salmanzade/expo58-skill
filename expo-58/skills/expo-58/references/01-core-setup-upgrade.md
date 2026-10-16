# Expo SDK 58: platform, setup, and upgrade decisions

Audited **2026-10-16**. Expo SDK 58 is **stable**, released October 15, with
published `expo@58.0.12` and React Native `0.88.0`. The official
[SDK 58 release](https://expo.dev/changelog/sdk-58) and npm's `latest` tag now
identify SDK 58. `next` still points to the older 58.0.11 patch at this audit;
release-channel tags are not ordered version comparisons.

## Exact published baseline

The machine-readable authority is [sdk-versions.json](sdk-versions.json), captured
from npm tarballs with integrity verification. `bundledNativeModules` contains
Expo's recommended ranges; `toolingDependencies` contains `expo` dependencies,
not the package manager's final resolutions. A project's lockfile is the authority
for what is actually installed.

| Component | Audited SDK 58 value | SDK 57 comparison |
|---|---|---|
| `expo` | `58.0.12` | `57.0.30` |
| React Native | `0.88.0` | `0.86.3` |
| React / React DOM | `19.3.0` | `19.2.3` |
| React Native Web | `~0.21.4` | `~0.21.0` |
| Default template | `58.0.21` (`sdk-58` / `latest`) | `57.0.32` (`sdk-57`) |
| TypeScript in template | `~6.0.3` | — |
| `@expo/cli` range in Expo | `^58.1.10` | `^57.0.31` |
| `babel-preset-expo` | `~58.0.16` | `~57.0.16` |
| `@expo/ui` | `~58.0.19` | `~57.0.25` |
| `expo-hinge` | `~58.0.1` | absent |
| `expo-router` | `~58.0.21` | `~57.0.28` |

The [versioned compatibility table](https://docs.expo.dev/versions/v58.0.0/)
lists RN 0.88 and RN Web 0.21.0 at the family level. The published template and
bundled manifest above provide the exact patch. The stable release post retains
some RC-era links; the published manifest now pins stable RN 0.88.0. Do not keep
the beta RC or mechanically give every Expo package `~58.0.0`.

## Environment gates

| Requirement | SDK 58 baseline |
|---|---|
| Node | `^22.13.0 || ^24.3.0 || ^26.0.0 || >=27.0.0` in `expo@58.0.12` engines |
| iOS | 16.4+ |
| Xcode | 26.4+ for the general SDK baseline |
| Android runtime | Android 7+ / API 24+ |
| Android compilation | compile SDK 37, target SDK 36 |
| Architecture | New Architecture only |

Use a supported even-numbered Node LTS meeting that engine range. Node 20, 23,
and 25 do not satisfy it. A vague "Node 22+" hides unsupported releases.
Install Android SDK 37 for compilation; target 36 is a separate setting.
The generic Xcode floor is not proof that Xcode 26 can compile an iOS 27-only API.
For iPhone Duo native APIs, follow the feature's Xcode/iOS requirements and use a
matching simulator runtime or physical device.

[New Architecture guidance](https://docs.expo.dev/guides/new-architecture/) applies:
SDK 55+ cannot disable it. Removing a stale `newArchEnabled: false` is appropriate;
promising it will restore the bridge is not. Keep Hermes and Expo's matched native
packages unless the task specifically requires an engine experiment.

SDK 58 does not currently support macOS; Expo identifies React Native macOS 0.86+
as the prerequisite for returning support. Check that integration's actual release
before treating an iOS build as evidence of macOS support.

Expo's autolinking and module Gradle plugins support **AGP 9**. This compatibility
does not require upgrading every app's Gradle/AGP pair to 9; retain the versions
selected by its Expo/RN template and verify third-party plugins before changing
them. Sources: [autolinking compatibility](https://github.com/expo/expo/pull/46766),
[module plugin compatibility](https://github.com/expo/expo/pull/46769).
For the Compose and Material 3 versions, see [Expo UI](03-expo-ui.md).

## Create a 58 project intentionally

```sh
npx create-expo-app@latest my-app --template default@sdk-58
cd my-app
npx expo install --check
npx expo-doctor@latest
```

`default@sdk-58` resolves to template 58.0.21 at this audit; use
`default@58.0.21` for exact reproduction. During the Expo Go store transition,
the release instructions say unqualified `create-expo-app` still creates SDK 57
projects, even though the template's `latest` tag points to 58. Use the explicit
SDK tag and a development build. Do not use `default@next` for the stable target.
After creation, inspect `package.json` and the resolved `expo` version.

Use the existing package manager in a repository. Preserve its lockfile and
package-manager configuration; do not generate several competing lockfiles.
CLI is local to `expo`: use `npx expo`, not the retired global `expo-cli`.

## Select the native workflow before upgrading

Read `app.json` / `app.config.*`, `package.json`, native directories, and their
Git status. Classify the native directories by ownership, not existence alone:

- **CNG-generated:** app config and config plugins reproduce all native changes.
  Regenerate after dependency alignment.
- **Hand-maintained or brownfield:** the native files are application source.
  Apply the native upgrade diff and preserve custom native code.
- **Uncertain:** inspect history and config plugins before running prebuild.

In published CLI 58.1.10, `expo prebuild` uses `clean: !args['--no-clean']`.
**It deletes and recreates native folders by default**, as on SDK 57.
`--no-clean` requests additive behavior but does not make plugin edits harmless or
perform the entire manual native migration. Generate a scratch native project for
comparison if deleting the current folders would lose application source.

## Upgrade an existing SDK 57 app

```sh
npx expo install expo@^58.0.0 --fix
npx expo-doctor@latest
npx expo install --check
```

These commands align dependencies; they do not migrate application APIs or verify
device behavior. Read [21-sdk-58-migration.md](21-sdk-58-migration.md) for RN strict
types, scene lifecycle, file writes, notifications, Router, Android R8, and other
behavior changes. Then rebuild the native client and run the app's relevant tests.
For SDK 56, use a verified 56 → 57 → 58 sequence, with a working checkpoint at 57.

For generated native projects, prebuild at a recoverable checkpoint after preserving any
uncommitted changes. For maintained projects, use the
[Native project upgrade helper](https://docs.expo.dev/bare/upgrade/) and run
`npx pod-install` after native dependency changes. Do not regenerate maintained
native source merely because CocoaPods reports a dependency conflict.

## Runtime and device selection

A 57 native binary cannot become a 58 native binary through EAS Update. Build new
iOS and Android clients and verify the new runtime/channel before publishing JS
updates. Clear Metro caches only after fixing incompatible dependencies.

Expo Go for SDK 58 is scheduled to reach the App Store and Google Play within a
few weeks of the stable release. Until the matching binary is available, use a
development build or a verified compatible Expo Go install. Check
[expo.dev/go](https://expo.dev/go) for the actual installer. A stable SDK release
does not upgrade an installed native client. The new store client will support
only SDK 58; an older app needs its matching client or a development build.
Hardware capability is a separate
check: a successful bundle does not prove Hinge events work on a simulator.

For iPhone Duo work, preserve current-window resizing, safe areas, route state, and
the non-foldable fallback. Use `expo-hinge` for posture input and native
`ArrangementView` where the requested UI needs it; neither is a blanket replacement
for responsive layouts or a reason to change every screen.

## Sources

- [Expo 58.0.12 metadata](https://registry.npmjs.org/expo/58.0.12), including tarball provenance.
- [Default template 58.0.21](https://registry.npmjs.org/expo-template-default/58.0.21).
- [Upgrade walkthrough](https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/) for incremental upgrade and native ownership decisions.
- [CLI 58.1.10](https://registry.npmjs.org/@expo/cli/58.1.10), `build/src/prebuild/index.js` for clean-by-default behavior.
