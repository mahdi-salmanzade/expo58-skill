# Files, transfers, and connectivity — SDK 58

Verified 2026-10-16. Install compatible packages with Expo; version pins live in [sdk-versions.json](sdk-versions.json).

```sh
npx expo install expo-file-system expo-network expo-document-picker
```

## File objects

Import `File`, `Directory`, and `Paths` from `expo-file-system`.
Constructing a reference does not create a file. Cache files are disposable; persist user data under `Paths.document`.
Use the `legacy` subpath only while migrating code that uses the old module functions.
Do not mix root object APIs with remembered `readAsStringAsync`/`writeAsStringAsync` calls.

```ts
import { File, Paths } from 'expo-file-system';

export async function saveNote(text: string) {
  const file = new File(Paths.document, 'note.txt');
  if (!file.exists) file.create();
  await file.write(text);
  return file.uri;
}
```

SDK 58 has asynchronous writes and explicit synchronous alternatives such as `writeSync`.
`copy` and `move` also return promises; await them before using the destination. Use `copySync`/`moveSync` only when intentional.
Avoid converting large files to base64 just to send or copy them.
For random access, use a file handle and close it in `finally`.

SDK 58 adds `File.digest()`; `File.md5` is deprecated.
For example, `await file.digest('SHA-256')` returns a lowercase hexadecimal digest.
It also adds `canPreview()` and `preview()` for native viewers:

```ts
export async function previewDocument(uri: string) {
  const file = new File(uri);
  if (!(await file.canPreview())) return false;
  await file.preview({ title: 'Document' });
  return true;
}
```

Android preview depends on installed MIME handlers. Preview resolution means presentation/handoff occurred, not that the viewer closed.
Handle missing/unreadable files and a `false` availability result separately.

## Pick and upload

```ts
import * as DocumentPicker from 'expo-document-picker';
import { File } from 'expo-file-system';
import { fetch } from 'expo/fetch';

export async function pickAndUpload(endpoint: string) {
  const selection = await DocumentPicker.getDocumentAsync({ copyToCacheDirectory: true });
  if (selection.canceled) return null;
  const form = new FormData();
  form.append('document', new File(selection.assets[0].uri));
  const response = await fetch(endpoint, { method: 'POST', body: form });
  if (!response.ok) throw new Error(`Upload failed: ${response.status}`);
  return response;
}
```

Let `FormData` set the multipart boundary; do not supply a bare multipart `Content-Type`.
For streamed responses, check `response.body`, read chunks, and cancel/release the reader on screen exit.
Use `AbortController` for cancellation. Distinguish transport failure from an HTTP error response.
Task-based transfers can be useful for progress/background workflows; verify their current declarations before using them.

## Connectivity

`useNetworkState` from `expo-network` tracks changes and cleans up its listener.
`isConnected` and `isInternetReachable` help explain UI state; neither proves that your API request will succeed.
Handle unknown state, captive portals, offline mutations, and retryable server failures in the data layer.
Android network-state permissions are installed automatically by the package.
Do not interpret a network type or IP address as a stable device/user identifier.

## Checks and sources

Test cancellation, a denied picker, an existing destination, offline upload, and a large file on a real device.

- [FileSystem](https://docs.expo.dev/versions/v58.0.0/sdk/filesystem/)
- [File implementation](https://github.com/expo/expo/blob/sdk-58/packages/expo-file-system/src/File.ts)
- [Expo fetch](https://docs.expo.dev/versions/v58.0.0/sdk/expo/#expofetch-api)
- [Network](https://docs.expo.dev/versions/v58.0.0/sdk/network/)
- [DocumentPicker](https://docs.expo.dev/versions/v58.0.0/sdk/document-picker/)
