# SDK 58: CLI, Metro, environment, and bundling

Audited **2026-10-13** against `expo@58.0.8`, `@expo/cli@58.1.7`,
`@expo/metro-config@58.0.12`, and `babel-preset-expo@58.0.13` published artifacts.
See [sdk-versions.json](sdk-versions.json) for dependency ranges and provenance.
Beta notes can describe an earlier implementation than the installed package.

## Keep SDK and CLI identity separate

```sh
node -p "require('expo/package.json').version"
npx expo --version
npx expo install --check
```

The first reads the SDK package; the second reports its local CLI. Do not interpret
CLI 58.1.x as a different Expo SDK or globally install `expo-cli` to match it.
Use the repository's package manager and inspect its lockfile when a dependency
range can resolve to more than one patch.

| Command | Material behavior |
|---|---|
| `npx expo start --dev-client` | Start Metro for a development build |
| `npx expo start --clear` | Clear bundler cache; does not rebuild native modules |
| `npx expo run:ios` / `run:android` | Build a local native client; missing native folders can trigger prebuild |
| `npx expo prebuild` | Delete and regenerate native folders by default |
| `npx expo prebuild --no-clean` | Apply generation to existing native folders |
| `npx expo export --platform web` | Produce web output using production mode by default |
| `npx expo config --type public` | Resolve public config; inspect its environment before sharing output |

Prebuild's `--platform ios` or `--platform android` scopes generation, not the
ownership decision. Preserve manual native code and compare a scratch generated
project for maintained native apps. `--no-clean` is not a substitute for migration.

## Environment mode now belongs to the command

SDK 58 initializes the environment mode before loading `.env` and dynamic app
config. An inherited `NODE_ENV=test` no longer makes `expo start` load `.env.test`.
Start uses development mode unless explicitly starting production mode; export
normally uses production. `expo config` resolves its contextual mode, with
development outside EAS Build and production for EAS Build at this CLI patch.

Use a dedicated deployment variable such as `APP_VARIANT=preview` for app IDs,
backend selection, or icons. Keep that separate from bundling optimization mode.
Validate resolved config with the same variables used by the intended build.
Jest's own test environment remains a separate concern.

```js
// app.config.js: choose a deployment target without overloading NODE_ENV.
export default ({ config }) => ({
  ...config,
  name: process.env.APP_VARIANT === 'preview' ? 'My App Preview' : 'My App',
});
```

Only values intentionally public belong in `EXPO_PUBLIC_*`. They are inlined into
client code and are not a secret storage mechanism. Preserve statically accessible
`process.env.EXPO_PUBLIC_NAME` expressions so Expo can replace them. Read the
[environment guide](https://docs.expo.dev/guides/environment-variables/) for the
current `.env` cascade and EAS environment handling.

## SDK 58 tunnel behavior: audit the current patch

At CLI **58.1.7**, `npx expo start --tunnel` selects the Expo tunnel by default.
Its help accepts `--tunnel [provider]`; `--tunnel ngrok` is the legacy provider.
The beta announcement's `EXPO_UNSTABLE_TUNNEL_V2=1` recipe is historical at this
patch: do not require that flag or install `@expo/ngrok` for the default tunnel.

```sh
npx expo login
npx expo start --dev-client --tunnel
```

Expo-account login is required for the normal Expo tunnel. Browser login is the
CLI default; use supported non-browser options only if the environment requires
them. Do not put credentials into source or recorded command lines.
When diagnosing a connection, check the actual advertised URL and native client's
SDK first. Port fallback in non-interactive runs means 8081 is not guaranteed.

The scene-era native template can read `RCTMetroPort` from Info.plist. A JavaScript
cache clear cannot apply a missing native template change to an older client.
Xcode 27 uses Device Hub; a script hard-coded to foreground Simulator.app may need
updating even when `simctl` device control still works.

## Start with Expo's Metro configuration

```js
const { getDefaultConfig } = require('expo/metro-config');

module.exports = getDefaultConfig(__dirname);
```

Extend this config for an actual resolver or transform requirement. Do not replace
it with an unversioned React Native template. Inspect existing aliases, SVG
transformers, workspace packages, and custom resolver delegation before removing
them during an upgrade. Metro has Expo-specific resolution and serializer logic.

The audited config sets `resolver.useWatchman = null` to inherit its watcher
selection; it should not be described as a forced `true`. Avoid adding historical
monorepo `watchFolders` recipes by habit. Resolve the observed import failure and
verify both development and production exports.

## Babel and experimental Rust transforms

Use `babel-preset-expo`. Its published preset automatically finds the installed
Worklets plugin and `@expo/ui/babel-plugin`; do not add duplicate plugins from old
tutorials. A custom Babel config still needs to preserve the Expo preset.

```js
module.exports = function (api) {
  api.cache(true);
  return { presets: ['babel-preset-expo'] };
};
```

`experiments.noxcturnalTransformWorker` opts into the experimental Rust transformer.
It is not a required migration or a promised 2× improvement for this app. The
beta implementation falls back to Babel for worklet transforms and has restrictions
around custom plugins, presets, and transform workers. Test a production export
with the real configuration before enabling it for build pipelines.

Changing Babel or Metro configuration requires a dev-server restart; changing
native module versions also requires a new native binary. Treat these as different
operations when diagnosing a Worklets version mismatch.

## Router web exports and async chunks

Router 58 enables asynchronous routes on web by default. Test direct navigation,
reloads, and lazy-loaded chunks against the deployment path, not only the Metro
homepage. An existing host's fallback rules or asset caching may be wrong for
new output. `asyncRoutes: { web: false }` in the Router plugin can preserve eager
loading while diagnosing an actual problem; do not turn it off automatically.

SDK 58's fingerprint preset defaults to `balanced`. Package content edits that do
not change the native package version may no longer affect a fingerprint. If an
app patches native package files, explicitly inspect its runtime policy and the
[fingerprint preset documentation](https://docs.expo.dev/versions/v58.0.0/sdk/fingerprint/).
Never use a cached fingerprint as proof of native compatibility after an SDK hop.

## Verify only what the task needs

For configuration changes, resolve app config under the intended deployment
variables and run the relevant export. For dependency changes, add `expo-doctor`
and a rebuilt native smoke test. For a tunnel issue, verify an actual client
connection; an HTTP response from Metro alone does not demonstrate it.

## Sources

- [Published CLI 58.1.7](https://registry.npmjs.org/@expo/cli/58.1.7): `build/src/start/index.js`, `start/resolveOptions.js`, `start/server/BundlerDevServer.js`, `prebuild/index.js`, `utils/nodeEnv.js`.
- [Metro config 58.0.12](https://registry.npmjs.org/@expo/metro-config/58.0.12): `build/ExpoMetroConfig.js`.
- [Babel preset 58.0.13](https://registry.npmjs.org/babel-preset-expo/58.0.13): `build/configs/expo.js`.
- [Metro configuration reference](https://docs.expo.dev/versions/v58.0.0/config/metro/).
- [Router 57 → 58 migration](https://docs.expo.dev/router/migrate/sdk-57-to-58/).
- [SDK 58 beta release notes](https://expo.dev/changelog/sdk-58-beta).
