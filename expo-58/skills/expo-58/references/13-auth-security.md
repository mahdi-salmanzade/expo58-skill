# Authentication and protected local storage — SDK 58

Verified 2026-10-16. Versions: [sdk-versions.json](sdk-versions.json).

```sh
npx expo install expo-auth-session expo-web-browser expo-crypto expo-secure-store expo-local-authentication
```

## OAuth redirect contract

Use a development build with an explicit app scheme for native auth redirects.
Register the exact redirect URI with the provider; debug, production, and web clients can require different registrations.
Use the provider's current native-app guidance and discovery document.
`expo-auth-session` manages the authorization request; it does not create your backend session or authorize API access.

```ts
import * as AuthSession from 'expo-auth-session';
import * as WebBrowser from 'expo-web-browser';

WebBrowser.maybeCompleteAuthSession();
const redirectUri = AuthSession.makeRedirectUri({ scheme: 'myapp', path: 'oauth/callback' });
```

Use `useAuthRequest` with the provider's documented endpoints, client ID, scopes, and response type.
Wait until the request exists before allowing `promptAsync`; on web, launch it from a user gesture.
Use authorization code + PKCE for public clients where supported.
Never embed a confidential client secret in a mobile bundle or an `EXPO_PUBLIC_*` variable.
If the provider requires a confidential token exchange, perform it on the backend.
Handle success, cancellation, denial, token expiry, and network failure distinctly.
Avoid inventing an auth-proxy URL or obsolete provider-specific subpath from memory.

## Store only the appropriate secret material

```ts
import * as SecureStore from 'expo-secure-store';

const SESSION_KEY = 'session-token';
export async function saveSession(token: string) {
  await SecureStore.setItemAsync(SESSION_KEY, token);
}
export async function readSession() {
  return SecureStore.getItemAsync(SESSION_KEY);
}
export async function clearSession() {
  await SecureStore.deleteItemAsync(SESSION_KEY);
}
```

Keep large records and non-secret cache data out of SecureStore.
Plan recovery and server-side session revocation; secure local storage is not the sole source of truth for an account.
Persistence differs across uninstall/reinstall and backup flows; do not use it as a permanent user identity.
Authentication-protected values may become unreadable after biometric enrollment changes.

SDK 58 adds `requireConfirmation` on Android when `requireAuthentication` is enabled.
It defaults to `true` and applies to authenticated reads and writes. Setting it to `false` requests implicit confirmation where the biometric modality/system settings allow it.
It is a system hint for confirmation after authentication, not an app-level confirmation dialog or a guarantee.
Use consistent storage options on subsequent reads/updates and validate on physical devices.

## Biometrics and Apple sign-in

`expo-local-authentication` can check hardware/enrollment and call `authenticateAsync`.
A successful biometric prompt establishes local user presence; it does not authenticate a server request by itself.
Handle no enrollment, cancellation, lockout, and supported fallback explicitly.
Face ID usage descriptions require native configuration; Expo Go cannot validate the complete Face ID setup.

For Sign in with Apple, install `expo-apple-authentication` and configure its capability/plugin.
Use its native button and check availability. Verify credentials/tokens on the backend.
Persist profile fields when first supplied; do not assume name/email is returned on every sign-in.

## Navigation and checks

A route guard is a presentation rule. Enforce access to user data on every backend operation.
Resolve initial session loading before redirecting to avoid a sign-in flash.
On logout clear local tokens, reset account-specific caches, and perform the backend revocation supported by the product.
Test redirect handling from a cold launch, returning from the browser, expired sessions, and revoked biometrics.

## Sources

- [Authentication guide](https://docs.expo.dev/guides/authentication/)
- [AuthSession](https://docs.expo.dev/versions/v58.0.0/sdk/auth-session/)
- [SecureStore](https://docs.expo.dev/versions/v58.0.0/sdk/securestore/)
- [LocalAuthentication](https://docs.expo.dev/versions/v58.0.0/sdk/local-authentication/)
- [AppleAuthentication](https://docs.expo.dev/versions/v58.0.0/sdk/apple-authentication/)
- [WebBrowser](https://docs.expo.dev/versions/v58.0.0/sdk/webbrowser/)
