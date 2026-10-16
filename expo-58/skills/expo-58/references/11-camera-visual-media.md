# Camera, scanning, images, and editing — SDK 58

Verified 2026-10-16 against SDK docs and published package declarations. Pins: [sdk-versions.json](sdk-versions.json).

```sh
npx expo install expo-camera expo-image expo-image-picker expo-image-manipulator
```

## Camera ownership and capture

Use `CameraView` and `useCameraPermissions` from `expo-camera`.
Render a loading state while permission is unknown, a request action when askable, and Settings guidance after permanent denial.
Mount only the active preview; navigating away or displaying another preview must release the first.
Wait for `onCameraReady` before capture. Keep the ref separate from permission/readiness state.

```ts
import { CameraView } from 'expo-camera';
import { useRef } from 'react';

export function useCameraCapture() {
  const camera = useRef<CameraView>(null);
  // Attach with <CameraView ref={camera} ... />; call only after onCameraReady.
  async function capture() {
    const picture = await camera.current?.takePictureAsync({ quality: 0.85 });
    return picture?.uri ?? null;
  }
  return { camera, capture };
}
```

Photos/videos initially live in cache. Move a selected result to persistent storage if it must survive cache eviction.
Enable microphone permission only for recording audio. Use the package plugin for native usage messages and rebuild.
Barcode scanning is a separate operation; debounce a successful scan before triggering navigation/mutations.

## New document scanner

`CameraView.scanDocumentAsync` invokes the platform scanning UI; it is a static method, not a preview-ref method.

```ts
import { CameraView } from 'expo-camera';

export async function scanPages() {
  if (!CameraView.isDocumentScannerAvailable) return null;
  const scan = await CameraView.scanDocumentAsync({ requestPdf: true });
  if (!scan) return null; // User canceled or the feature is unavailable.
  return { pageUris: scan.pages, pdfUri: scan.pdfUri };
}
```

The result has `pages: string[]` and optional `pdfUri`, not a picker-style `assets` array.
On Android, document scanning uses the native ML Kit flow; the JPEG `quality` option is iOS-only in effect.
Catch native failures separately from cancellation and test actual supported hardware.

## Selection and display

```ts
import * as ImagePicker from 'expo-image-picker';

export async function selectPhoto() {
  const result = await ImagePicker.launchImageLibraryAsync({ mediaTypes: ['images'] });
  return result.canceled ? null : result.assets[0];
}
```

Use `canceled`, not the obsolete `cancelled` field. Decide whether selection, editing, and multi-selection are compatible before combining options.
For display, import `Image` from `expo-image`; use `contentFit` and explicit layout bounds.
SDK 58 adds `transition.skipOnCacheHit` and `svgVariables` for supported SVG CSS variables.
Use placeholders/error fallback for remote media; a transition does not prevent layout shift.
For virtualized lists, keep identity/recycling behavior correct when image sources change.

## Editing and thumbnails

`useImageManipulator(uri)` returns a context with operations such as `resize` and `rotate`.
Call `renderAsync()`, then the returned image's `saveAsync({ format: SaveFormat.JPEG })`.
Keep original uploads separate from destructive edits and cap decoded dimensions for large photos.
For video thumbnails, prefer the thumbnail APIs in `expo-video`; `expo-video-thumbnails` is deprecated.
On Duo, keep preview fitting and crop calculations relative to the preview container as its size changes.

## Checks and sources

Check denied permissions, cancellation, camera navigation, rotation/resizing, large images, and an offline image source.

- [Camera](https://docs.expo.dev/versions/v58.0.0/sdk/camera/)
- [Published camera declarations](https://unpkg.com/expo-camera@58.0.10/build/CameraView.d.ts)
- [Image](https://docs.expo.dev/versions/v58.0.0/sdk/image/)
- [ImagePicker](https://docs.expo.dev/versions/v58.0.0/sdk/imagepicker/)
- [ImageManipulator](https://docs.expo.dev/versions/v58.0.0/sdk/imagemanipulator/)
- [Video](https://docs.expo.dev/versions/v58.0.0/sdk/video/)
