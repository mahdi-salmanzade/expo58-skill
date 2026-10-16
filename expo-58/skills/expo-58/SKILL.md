---
name: expo-58
description: >-
  Build, debug, configure, and migrate Expo SDK 58 apps using version-checked
  APIs, including Expo Router, Expo UI, native modules, EAS, expo-hinge,
  ArrangementView, and iPhone Duo adaptation. Use for SDK 58 work, upgrading
  SDK 57 to 58, or adding foldable support to an Expo app; detect the installed
  SDK before applying this reference.
---

# Expo SDK 58 + iPhone Duo

An unofficial reference checked on **2026-10-16**. **Expo SDK 58 is stable**, released
October 15, 2026. The audited packages are Expo **58.0.12** and React Native
**0.88.0**. Check the current announcement and registry when the user asks for the
latest patch. Individual features keep their own status: Expo Modules 2.0 is beta,
App Intents is alpha, and the agent CLI is experimental.

## Establish the target

Read `package.json`, the lockfile, and installed `expo/package.json` when available.
A declared range does not establish the resolved patch. Inspect native projects,
app config, and navigation before selecting an implementation.

- **SDK 58:** apply the relevant references below and check installed signatures.
- **SDK 57 → 58:** use [the migration guide](references/21-sdk-58-migration.md).
- **SDK 56:** upgrade through 57 when an upgrade is requested; use its versioned
  docs for fixes that stay on 56. The older skills remain useful for those projects.
- **Other SDK or non-Expo app:** use its matching docs; do not apply 58 APIs merely
  because this skill is loaded.
- **New SDK 58 app:** use the explicit SDK 58 template in
  [setup](references/01-core-setup-upgrade.md), since `latest` may target another SDK.

Keep the user's chosen SDK and task scope. Loading this skill does not request an
upgrade, a navigation rewrite, or a store submission.

## Resolve versions and evidence

Use the project's installed types/source for callable imports and signatures, and
its `expo/bundledNativeModules.json` for compatible package ranges. Use
[versioned Expo docs](https://docs.expo.dev/versions/v58.0.0/) for documented
requirements and [release notes](https://expo.dev/changelog/sdk-58) for
migration and release status. Published package tarballs establish what shipped;
unpublished `main` changes do not.

[sdk-versions.json](references/sdk-versions.json) records the audited package and
template manifests. It is a dated snapshot, not an instruction to replace a newer
compatible patch. Resolve packages with `npx expo install`; after an upgrade run
`npx expo install --fix` and `npx expo-doctor@latest`. Native changes require a
rebuilt client. An OTA update cannot add a missing native API.

Read only references relevant to the task. The documents contain practical API
guidance, migration decisions, and official source links, rather than a complete
copy of each API manual. EAS infrastructure, Expo Go availability, and store
requirements are live state; verify them when they affect the work.

During the Expo Go store transition, use the explicit SDK 58 template and a
development build. The stable SDK release does not mean the store's Expo Go binary
already contains SDK 58. When migrating web apps, review the new default server
output before deploying an existing static export. See references 01, 05, and 21.

## iPhone Duo and foldables

Read [Hinge and ArrangementView](references/22-hinge-arrangementview.md) for the
Expo API boundary and [iPhone Duo](references/23-iphone-duo.md) for adaptation and
validation. The essential split is:

- Base layout on available window/container space, safe areas, and native layout
  facilities. Hinge angle is input for effects and interactions, not layout.
- Treat hinge state as nullable. API availability does not prove hinge hardware
  exists, and Android's status semantics differ from iOS.
- Separate Expo's base OS/toolchain floor from Duo feature requirements. The iOS
  hinge APIs require iOS 27.1 and a build using the iOS 27.1 SDK or later.
- Supply a usable older-iOS and non-iOS layout. ArrangementView's older-iOS
  behavior renders its children without the adaptive container.
- Preserve navigation, drafts, selection, scroll, and media state during resize,
  rotation, folding, and multitasking. Do not remount screens to change layout.

The included reference is usable on its own. When the companion `iphone-duo`
skill is installed and the task needs broader Apple design or native migration
work, use its discovery, framework, and validation references as well. Reconcile
its dated Expo notes against this SDK's installed types and current docs. Do not
require the companion merely to use `expo-hinge` or build a responsive Expo view.

## Reference map

| Task | Read |
|---|---|
| Setup, SDK detection, tooling, project creation | [01 — Core setup](references/01-core-setup-upgrade.md) |
| Routes, layouts, stacks, tabs, links, split navigation | [02 — Expo Router](references/02-expo-router.md) |
| SwiftUI, Jetpack Compose, hosting React Native views | [03 — Expo UI](references/03-expo-ui.md) |
| Native modules, inline modules, App Intents, config plugins | [04 — Modules API](references/04-expo-modules-api.md) |
| CLI, agent CLI, Metro, environment variables, prebuild | [05 — CLI and bundling](references/05-cli-metro-bundling.md) |
| Files, directories, upload/download, networking | [06 — Filesystem and networking](references/06-filesystem-networking.md) |
| Calendar, contacts, media library, haptics, assets | [07 — Device APIs](references/07-media-device-apis.md) |
| SQLite, Updates, runtime compatibility, Convex | [08 — Data and updates](references/08-sqlite-updates-convex.md) |
| System bars, widgets, symbols, dev client | [09 — System UI](references/09-system-ui-components.md) |
| Native builds, brownfield, build performance | [10 — Build and brownfield](references/10-eas-build-brownfield.md) |
| Camera, image picker, images, manipulation, GL | [11 — Visual media](references/11-camera-visual-media.md) |
| Audio/video playback and recording, screen capture | [12 — Audio and video](references/12-video-audio-playback.md) |
| Auth, secure storage, biometrics, protected routes | [13 — Authentication](references/13-auth-security.md) |
| Push notifications, tasks, background execution | [14 — Notifications and background](references/14-notifications-background.md) |
| Location, sensors, orientation, device state | [15 — Location and sensors](references/15-location-sensors.md) |
| App config, build properties, splash, fonts, links | [16 — App configuration](references/16-app-config-foundational.md) |
| Reanimated, Worklets, gestures, native dependencies | [17 — Animation dependencies](references/17-animation-gesture-deps.md) |
| EAS Build, Submit, Update, Workflows, credentials | [18 — EAS workflow](references/18-eas-full-workflow.md) |
| Development builds, debugging, Jest, E2E | [19 — Development and testing](references/19-dev-workflow-testing.md) |
| Maps, web, sharing, clipboard, utility modules | [20 — Maps, web, utilities](references/20-maps-web-utilities.md) |
| SDK 57 → 58 migration and SDK 56 starting points | [21 — SDK 58 migration](references/21-sdk-58-migration.md) |
| Hinge events, native adaptive arrangement, examples | [22 — Hinge and ArrangementView](references/22-hinge-arrangementview.md) |
| iPhone Duo adaptation, companion skill, verification | [23 — iPhone Duo](references/23-iphone-duo.md) |

## Verify the result

Choose checks that match the change: package alignment and typecheck for API work;
a native build for changed native dependencies/configuration; relevant device or
simulator flows for runtime behavior. For Duo, check available sizes and state
continuity as well as the feature's OS and build requirements.

Report what ran and what remains unverified. Typechecking a hinge example does
not establish hardware behavior; simulator layout evidence does not establish
physical hinge sensor behavior. Finish useful work even when hardware is absent.
