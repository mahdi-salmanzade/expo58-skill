# Stable release verification — October 16, 2026

These checks cover skill version **1.1.0**, updated for the October 15 stable SDK 58
release. The [October 13 record](verification-2026-10-13.md) remains historical.
This record does not claim that every scenario in [evals.json](evals.json) ran.

## Release and package evidence

- Reviewed the [stable release](https://expo.dev/changelog/sdk-58), versioned docs,
  Router migration guide, and published package declarations/source.
- Regenerated the snapshot from Expo **58.0.12**, default template **58.0.21**, and
  SDK 57 comparison **57.0.30**. The helper verified npm tarball integrity and read
  manifests without installing or executing their contents.
- An independent rerun reproduced the complete snapshot exactly, including its
  124 bundled dependency ranges, provenance, and observed npm dist-tags.
- The published baseline now uses React Native **0.88.0**, React **19.3.0**, UI
  **58.0.19**, Router **58.0.21**, Hinge **58.0.1**, Reanimated **4.7.1**, Worklets
  **0.13.0**, and Gesture Handler **3.3.0**. The release post's older RC links do
  not override these published manifests.
- Rechecked CLI clean-by-default prebuild, tunnel selection, command diagnostics,
  environment handling, automatic Babel plugins, Jest peers, and Android R8 defaults
  against the selected published tooling artifacts.

## Consumer code checks

Strict, no-emit TypeScript checking passed for:

- All **six files** in `examples/` and **six Router/UI/Hinge documentation blocks**.
- **21 general API blocks**, assembled into 11 modules where adjacent blocks share
  imports, plus one additional module probing the updated API signatures.
- **Two migration/gesture blocks**, including the strict `TextInputInstance` ref
  and Gesture Handler 3 hook example.

The fresh example fixture used Node 26.0.0, npm 11.12.1, TypeScript 6.0.3,
`@types/react` 19.3.0, and the stable dependency set above. It inherited
`expo/tsconfig.base`; the API fixture used strict bundler resolution. Both used
`skipLibCheck`, so these checks validate consumer examples, not every upstream
declaration. Dependency installation disabled lifecycle scripts. Three JavaScript
configuration blocks passed Node syntax checks, and all fenced JSON parsed.

The API probes covered App Intents, location session/status APIs, SQLite
interrupt/configuration, asset URI options, widget freshness, build properties,
Observe, and development-launch URL unwrapping. Typechecking confirms signatures;
it does not establish native or background execution behavior.

## Packaging and review

- Repository validation passed for plugin/marketplace agreement, 23 routed
  references, local links, snapshot consistency, and 14 evaluation scenarios.
- Added checks for valid release status, matching snapshot/evaluation dates, and
  template/bundled React, RN, Reanimated, and Worklets alignment. Negative checks
  confirmed stale dates, an invalid status, and a mismatched RN dependency fail.
- The skill-creator frontmatter validator and `git diff --check` passed.
- Independent review caught and corrected the agent CLI source URL and a stale
  MediaLibrary import restriction: version 58.0.9 exports `AssetUriVersion` from
  both the root and `/next` entry points.
- Active release scenarios now distinguish stable SDK packages from experimental
  features and the pending store Expo Go rollout. New scenarios cover web output
  migration and App Intents' background execution limit. These scenario definitions
  were structurally validated; they were not all executed as agent evaluations.

## Not exercised

No native build, Duo simulator, physical hinge sensor, or on-device user flow ran.
App Intents, background delivery, R8 behavior, and adaptive state continuity still
need runtime checks in consuming apps. No Expo application or store binary is
shipped by this skill repository, and the October 13 app-repair evaluation was
not rerun for this documentation update.
