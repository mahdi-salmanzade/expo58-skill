# Maps, browser surfaces, and sharing — SDK 58

Verified 2026-10-13. Package versions are centralized in [sdk-versions.json](sdk-versions.json).

## Maps are platform-specific

```sh
npx expo install expo-maps
```

`expo-maps` uses Apple Maps on iOS and Google Maps on Android.
It does not provide Google Maps on iOS or a web map renderer.
The current iOS implementation requires iOS 17; some selection and overlay interactions require iOS 18.
Gate the feature or choose a compatible alternative when supporting older devices.
Use a development build and retain an existing `react-native-maps` implementation unless the task calls for migrating it.

```tsx
import { AppleMaps, GoogleMaps } from 'expo-maps';
import { Platform, Text } from 'react-native';

export function MapSurface() {
  if (Platform.OS === 'android') return <GoogleMaps.View style={{ flex: 1 }} />;
  if (Platform.OS === 'ios' && Number.parseInt(String(Platform.Version), 10) >= 17) {
    return <AppleMaps.View style={{ flex: 1 }} />;
  }
  return <Text>Map view is unavailable on this device.</Text>;
}
```

On Android, enable Maps SDK for Android in the intended Google project and configure `android.config.googleMaps.apiKey`.
Restrict the key to the app's package/signing certificate; development and store signing can use different certificates.
Rebuild after native key/plugin changes.
Displaying a map does not itself require location permission; showing the user's location does.
Use `expo-location` for the location-access flow and keep denied access usable.

Markers are data props, not React Native `<Marker>` children from another library.
Custom icon properties expect an image reference such as one returned by `useImage` from `expo-image`.
A map in a Duo pane should size to that pane and preserve camera/selection state during layout changes.
Provide an accessible list/detail alternative for data that would otherwise only exist as map pins.

## External browser versus embedded web content

```sh
npx expo install expo-web-browser expo-linking react-native-webview
```

Use `WebBrowser.openBrowserAsync` for an external browser surface and its auth-session API for login flows.
Use `WebView` from `react-native-webview` when the product requires embedded content.
Do not build an OAuth flow by collecting credentials in an arbitrary WebView.
Treat `onMessage` data and incoming deep-link parameters as untrusted input.
Validate message shape/origin and allowlisted navigation targets before invoking privileged app actions.
Avoid mixing file access, injected scripts, and unrestricted remote navigation without an explicit need.
For web support, choose a browser-native implementation or fallback; the native WebView package is not a universal iframe.

## Files, sharing, and small utilities

```sh
npx expo install expo-sharing expo-clipboard expo-mail-composer expo-print
```

`Sharing.isAvailableAsync()` checks whether the sharing flow is supported.
On native, pass a readable local file URI to `Sharing.shareAsync`; remote URLs and local files are different inputs.
Web sharing depends on browser support and a secure context; do not assume a native cache URI can be shared by a browser.
For native file preview, `File.canPreview`/`preview` may be a better fit; see [06-filesystem-networking.md](06-filesystem-networking.md).

Use `Clipboard` from `expo-clipboard` for copy actions and show feedback only after success.
Check `MailComposer.isAvailableAsync` before opening a draft composer; do not claim the message was sent merely because the composer opened.
Generate printable/PDF content with `expo-print` and test fonts, page sizing, and file paths on each target platform.
For SMS or store review, check the dedicated API's availability and respect system presentation behavior.
These packages wrap system interactions; cancellation is a normal result.

## Checks and sources

Validate map-key configuration in both development and signed release builds.
Exercise no-location, unsupported platform, external-app cancellation, and untrusted incoming-link cases.

- [Maps](https://docs.expo.dev/versions/v58.0.0/sdk/maps/)
- [React Native Maps alternative](https://docs.expo.dev/versions/v58.0.0/sdk/map-view/)
- [WebBrowser](https://docs.expo.dev/versions/v58.0.0/sdk/webbrowser/)
- [WebView](https://docs.expo.dev/versions/v58.0.0/sdk/webview/)
- [Sharing](https://docs.expo.dev/versions/v58.0.0/sdk/sharing/)
- [MailComposer](https://docs.expo.dev/versions/v58.0.0/sdk/mail-composer/)
- [Print](https://docs.expo.dev/versions/v58.0.0/sdk/print/)
