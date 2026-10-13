# Creation verification — October 13, 2026

These are the checks actually performed for version 1.0.0. This is not an
aggregate benchmark result or a claim that every scenario in
[evals.json](evals.json) ran.

## Packaging and source snapshot

- The repository validator passed: plugin/marketplace agreement, 23 routed
  references, local document/example links, snapshot structure, and evaluation
  scenario structure.
- A negative check confirmed that removing a referenced example makes validation
  fail. The skill-creator frontmatter validator passed.
- Skills CLI local discovery found the single `expo-58` skill without installing it.
- The snapshot refresh helper reproduced the recorded JSON from published npm
  artifacts with integrity verification. Wrong SDK versions and unpinned tags
  were rejected before writing output.

## TypeScript

All six files in `examples/`, plus the Router/UI documentation snippets, passed
strict no-emit checking with Expo 58.0.8, UI 58.0.16, Hinge 58.0.1, Router 58.0.18,
React Native 0.88.0-rc.4, React/types 19.3.0, Safe Area Context 5.9.1, and
TypeScript 6.0.3.

The general API references' TypeScript snippets also passed against the published
SDK 58 declarations. Snippets sharing an import across adjacent blocks were
assembled as one example. Checks used bundler resolution, strict mode, and
`skipLibCheck`; they checked consumer examples, not all upstream implementation
code. No app build is included in this repository.

## Independent forward-test

An independent agent received the skill and a small Expo 58 fixture with a
draft editor, a nullable hinge access, and layout-dependent component identity.
It was asked to fix crashes and draft loss while retaining the two-pane task.

The resulting patch handled absent hinge readings, removed remounting during
resize, retained draft state above presentation, and measured available space
with font-scale-aware layout. It added safe-area, scrolling, and keyboard handling.
The fixture's strict TypeScript check passed without dependency changes.

Using only the snapshot, the agent correctly identified SDK 58 as beta and chose
`default@sdk-58` (or `default@58.0.17` for exact reproduction).

The review prompted one wording correction: source-confirmed JavaScript failures
can be repaired without runtime reproduction, while platform behavior still needs
runtime evidence. No other material instruction gap was reported in this test.

## Not exercised

No native build, Duo simulator, physical hinge sensor, or on-device user flow ran.
Focus, caret/selection, keyboard behavior, reserved regions, and real fold
transitions remain runtime checks for consuming apps. The independent fixture
is not a shipped application or device certification. Other evaluation scenarios
remain available for future runs.
