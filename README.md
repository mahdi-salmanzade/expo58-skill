# Expo 58 + iPhone Duo skill

An unofficial **Expo SDK 58 reference skill** with iPhone Duo and Android foldable
support. Built from the Expo 56/57 skills, refreshed against SDK 58 documentation
and published packages, and integrated with the iPhone Duo skill's adaptation
workflow.

**Version 1.1.0 · Snapshot: October 16, 2026.** Expo SDK 58 is **stable**, released
October 15. The skill checks the project's actual SDK before applying its guidance.
See [Expo's release announcement](https://expo.dev/changelog/sdk-58)
and the [recorded package snapshot](expo-58/skills/expo-58/references/sdk-versions.json).

| Snapshot item | Version |
|---|---|
| Expo | 58.0.12 (SDK 58 stable) |
| React Native / React | 0.88.0 / 19.3.0 |
| Expo Router / Expo UI | 58.0.21 / 58.0.19 |
| Expo Hinge | 58.0.1 |
| Documented Node / iOS / Xcode minimum | 22.13.x / 16.4 / 26.4 |
| iPhone Duo hinge feature minimum | iOS 27.1 + Xcode 27.1 build |

The full manifest includes dependency ranges; use `npx expo install` to resolve
compatible packages. These figures describe the audit, not a forced downgrade
from newer compatible patches. Tooling requirements come from the
[SDK 58 compatibility table](https://docs.expo.dev/versions/v58.0.0/).

This update covers the stable release's App Intents capabilities and limits,
precompiled Android modules, agent CLI, Router server-output migration, recycling
lists, and the current Duo build path. Expo Modules 2.0 remains beta, App Intents
remains alpha, and the agent CLI remains experimental.

Expo Go's store release follows separately. For a new SDK 58 app, use
`npx create-expo-app@latest my-app --template default@sdk-58` and a development
build during that transition. To upgrade an existing SDK 57 app, Expo's command is
`npx expo install expo@^58.0.0 --fix`; follow the
[migration reference](expo-58/skills/expo-58/references/21-sdk-58-migration.md)
for application and native changes.

## Install

### Claude Code plugin

```text
/plugin marketplace add mahdi-salmanzade/expo58-skill
/plugin install expo-58
```

To refresh the marketplace:

```text
/plugin marketplace update expo58-skill
```

### Codex and other skill-compatible agents

From your app's repository, use the Skills CLI:

```sh
npx skills add mahdi-salmanzade/expo58-skill --skill expo-58 --agent codex
```

Omit `--agent codex` to choose another supported agent. Add `--global` for a personal
installation. Alternatively, copy the complete
[expo-58 skill folder](expo-58/skills/expo-58) into `.agents/skills/expo-58/` in your
project. Keep its references, examples, evaluations, and agent metadata together.

## Use

```text
Use $expo-58 to upgrade this Expo 57 app to SDK 58. Check the installed
dependencies, apply the migration, and verify the affected flows.
```

```text
Use $expo-58 to adapt this app for iPhone Duo. Preserve navigation and drafts
through resizing and folding, use the supported Expo APIs, and report what
was verified on a simulator or physical device.
```

```text
Use $expo-58 to add a hinge-driven interaction with a useful non-foldable
fallback. Keep layout responsive to the available window size.
```

Use the edition matching your app rather than loading the Expo 56, 57, and 58
skills together. This skill includes the 57→58 migration and routes SDK 56
upgrades through 57; it does not silently upgrade an existing app.

## What's included

- **23 focused references:** setup, migration, Router, Expo UI, native modules,
  Metro, device APIs, data, authentication, notifications, animation, EAS, testing,
  maps/web, and foldables.
- **Published package snapshot:** compatible package ranges and source metadata
  to keep API guidance tied to an actual SDK release.
- **Hinge support:** nullable state, event subscriptions, platform requirements,
  Android status differences, and a distinction between API and hardware availability.
- **ArrangementView support:** primary/secondary content, SwiftUI hosting,
  arrangement modifiers, and explicit fallback guidance.
- **iPhone Duo workflow:** app discovery, adaptive layout, state continuity,
  toolchain checks, and a device/simulator validation matrix.
- **Reusable examples and evaluation scenarios** for the SDK and foldable APIs.

Start with [SKILL.md](expo-58/skills/expo-58/SKILL.md) for the full reference map.
The references are selective engineering guidance, not an exhaustive API mirror.

## iPhone Duo companion

The Expo 58 skill includes the Expo-specific Duo guidance and works independently.
For broader Apple design, SwiftUI/UIKit migration, and the Apple documentation
download workflow, also install your existing companion:

```sh
npx skills add mahdi-salmanzade/iphone-duo-skill --skill iphone-duo --agent codex
```

The skills have separate responsibilities: Expo 58 supplies the SDK API boundary;
the [iPhone Duo skill](https://github.com/mahdi-salmanzade/iphone-duo-skill) supplies
the wider app adaptation workflow. Its earlier Expo notes must be checked against
the current SDK 58 packages.

Expo's base iOS minimum does not establish availability of Duo APIs. Hinge support
requires iOS 27.1 and a build using Xcode 27.1 or later. On earlier iOS versions,
ArrangementView renders children without an adaptive container, so provide a
usable fallback. See the [Hinge](https://docs.expo.dev/versions/v58.0.0/sdk/hinge/)
and [ArrangementView](https://docs.expo.dev/versions/v58.0.0/sdk/ui/swift-ui/arrangementview/)
documentation.

## Maintenance and verification

```sh
python3 scripts/validate_repository.py
```

This checks packaging, local document links, reference reachability, and the
version snapshot structure. Behavioral evaluation scenarios live in
[evals.json](expo-58/skills/expo-58/evals/evals.json); they are not a claim that every
scenario has been executed. Typechecking or reviewing an example does not prove
physical Duo behavior. The references distinguish source verification, native
builds, simulator checks, and hardware checks.

The [stable-release verification record](expo-58/skills/expo-58/evals/verification-2026-10-16.md)
records this update's checks. The
[original creation record](expo-58/skills/expo-58/evals/verification-2026-10-13.md)
preserves the historical beta snapshot and independent app-repair test. Neither
record claims physical Duo verification.

To refresh the manifest after reviewing release status and selecting compatible
Expo/template versions:

```sh
python3 scripts/update-sdk-snapshot.py \
  --expo-version 58.0.12 --comparison-version 57.0.30 \
  --template-version 58.0.21 --audited-at 2026-10-16 --release-status stable
```

The helper verifies npm tarball integrity and reads manifests without installing
or executing the packages. Refreshing JSON does not re-audit the prose or examples;
review the affected references and metadata before publishing an update.

## Sources and license

Primary sources are [Expo SDK 58 docs](https://docs.expo.dev/versions/v58.0.0/),
published npm package types/manifests, Expo release notes, and Apple's Duo guidance.
Each reference links the sources it uses. The user-supplied
[Expo UI hinge examples](https://github.com/SchroederNathan/expo-ui-examples/tree/main/src/examples/hinge)
inform the example review; package types and official docs determine supported APIs.

This repository succeeds [expo57-skill](https://github.com/mahdi-salmanzade/expo57-skill)
and [expo56-skill](https://github.com/mahdi-salmanzade/expo56-skill). Their original
repositories remain separate.

[MIT](LICENSE) © 2026 Mahdi Salmanzade. Independently written guidance; no Apple
documentation or artwork is redistributed. Unaffiliated with Expo or Apple.
