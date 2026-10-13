# Local data and compatible OTA updates — SDK 58

Verified 2026-10-13. Package versions are centralized in [sdk-versions.json](sdk-versions.json).

```sh
npx expo install expo-sqlite expo-updates
```

## SQLite baseline

```ts
import * as SQLite from 'expo-sqlite';

export async function openNotes() {
  const db = await SQLite.openDatabaseAsync('notes.db');
  await db.execAsync(`
    PRAGMA journal_mode = WAL;
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY NOT NULL,
      body TEXT NOT NULL
    );
  `);
  return db;
}

export async function addNote(body: string) {
  const db = await openNotes();
  return db.runAsync('INSERT INTO notes (body) VALUES (?)', body);
}
```

`execAsync` executes SQL text without escaping values; bind user input with `runAsync`, query parameters, or prepared statements.
Use `SQLiteProvider`/`useSQLiteContext` to share a database in React.
Track schema migrations with `PRAGMA user_version`; test upgrade paths against existing user data.
Finalize prepared statements in `finally`, even when execution fails.

`withTransactionAsync` can include queries issued elsewhere while its async work is pending.
When isolation matters on supported platforms, use `withExclusiveTransactionAsync` and its transaction object.
Do not assume the exclusive API works on web; check platform support and serialize writes where necessary.
Web SQLite needs its documented WASM/Metro and cross-origin isolation setup.
`expo-sqlite/kv-store` is useful for non-secret preferences; it is not SecureStore.

SDK 58 removes libSQL support: `syncLibSQL()` and the `libSQLOptions` open option are gone.
The deprecated `useLibSQL` plugin setting only warns and has no effect; remove it and choose a supported sync strategy before upgrading a libSQL-dependent app.
The package also ships its own agent guidance. Consult installed guidance for advanced database work.

## OTA compatibility is a native contract

EAS Update ships JS/assets compatible with an installed native runtime.
Adding a native module, capability, extension, or incompatible native dependency requires a new binary.
An update cannot add Hinge, a widget extension, or a camera entitlement to an older binary.

```json
{
  "expo": {
    "runtimeVersion": { "policy": "fingerprint" }
  }
}
```

Choose a runtime policy based on the app's release process; do not switch an existing app casually.
SDK 58's fingerprint default uses the balanced preset. Native package files are not all hashed by content under that preset.
For native patches or custom build inputs, review fingerprint configuration so the runtime changes when the binary contract changes.
Runtime version, channel, branch, platform, and update environment must all match the intended installation.
See [18-eas-full-workflow.md](18-eas-full-workflow.md) for operational commands.

`checkForUpdateAsync`, `fetchUpdateAsync`, and `reloadAsync` come from `expo-updates`.
Use an update-ready UI instead of unexpectedly interrupting an edit or checkout.
OTA behavior should be tested in a suitable release/preview build; Expo Go is not a production-update test.

## Server data and Convex

Convex is optional third-party backend infrastructure, not part of the Expo SDK version contract.
Keep a project's existing backend unless the task calls for changing it.
When chosen, follow Convex's current React Native setup and its generated API types.
Keep authentication and authorization on the backend; a protected client route does not secure a query.
Define whether SQLite is a cache, an offline source of truth, or unrelated storage before combining the two.
Avoid duplicating optimistic updates across both layers without a reconciliation strategy.

## Validation and sources

Exercise migration, rollback after a failing transaction, app restart, and update/binary mismatch.

- [SQLite](https://docs.expo.dev/versions/v58.0.0/sdk/sqlite/)
- [Published SQLite migration notes](https://unpkg.com/expo-sqlite@58.0.12/CHANGELOG.md)
- [Updates and runtime policies](https://docs.expo.dev/versions/v58.0.0/sdk/updates/)
- [Fingerprint](https://docs.expo.dev/versions/v58.0.0/sdk/fingerprint/)
- [SDK 58 beta](https://expo.dev/changelog/sdk-58-beta)
- [Convex React Native setup](https://docs.convex.dev/quickstart/react-native)
