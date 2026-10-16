# Location, orientation, and device state — SDK 58

Verified 2026-10-16 against versioned docs and published `expo-location` declarations.
Package snapshot: [sdk-versions.json](sdk-versions.json).

```sh
npx expo install expo-location expo-sensors expo-screen-orientation
```

## Two location APIs coexist

Keep an existing `expo-location` implementation working while deciding whether the new beta API solves a need.
The root API still has `requestForegroundPermissionsAsync`, `getCurrentPositionAsync`, and `watchPositionAsync`.
The new `expo-location/next` entry point uses different result shapes and method names; do not combine them by accident.
It is included in the SDK 58 package snapshot and remains beta.

```ts
import { Location, RequestPermissionsAccuracyOption } from 'expo-location/next';

export async function approximatePosition() {
  const permission = await Location.requestForegroundPermissions({
    accuracy: RequestPermissionsAccuracyOption.REDUCED,
  });
  if (!permission.granted) return null;
  return Location.getPosition({ maxCachedAge: 30, timeout: 15 });
}
```

The next API's `timeout` and `maxCachedAge` are seconds; `position.timestamp` uses milliseconds.
`getPosition` can return null or an older fallback fix. Check timestamp and accuracy for freshness-critical work.
Read `position.coordinates`, not the root API's `position.coords`.
The default next permission request asks for precise access; select reduced accuracy when sufficient.
On iOS, `Location.requestForegroundPermissions({ accuracy: RequestPermissionsAccuracyOption.FULL })` can request temporary full accuracy when access is reduced.
The plugin writes its purpose string by default; setting `locationFullAccuracyPermission: false` removes it and skips that prompt.

`Location.watchPosition({ onPosition, onError, ... })` returns a `PositionWatchHandle`.
Pause on screen blur, resume on focus, and `dispose()` on unmount.
Screen focus and app foreground are different; a mounted tab can be invisible.
`Location.hasLocationServicesEnabled()` checks the device-wide service, separately from app authorization.
Android provider selection exists in the next API; keep its default fallback unless the product needs a specific provider.

## Background location

Request foreground authorization before background authorization when the chosen API needs both.
The next API reports `scope`; `LocationScope.ALWAYS` identifies background authorization.
Android next task delivery requires foreground and background permission plus `RECEIVE_BOOT_COMPLETED`.
iOS next task delivery uses `CLLocationUpdate.liveUpdates` and requires foreground permission plus the `location` background mode.
Configure the native requirements through `expo-location`'s plugin and use a development build.
For iOS geofencing alone, SDK 58 no longer requires `UIBackgroundModes: location`; enable that mode only when another location feature needs it.

Define `defineLocationTask` at module scope; control it with `LocationUpdatesHandle` from `expo-location/next`.
Import the task module at startup, including headless/background launches.
Use matching names when configuring more than one task.
Check `hasStarted()` on restart and call `stop()` when tracking ends.
On Android, `start()` may resolve even if the provider refuses updates; inspect `status()` rather than treating registration as delivery.

The next Android foreground service is separate from task registration.
Call `Location.ensureBackgroundSessionStarted(options)` while the app is foregrounded to maintain delivery outside the foreground; stop it with `Location.stopBackgroundSession()`.
A new session cannot start while backgrounded, though its options persist for the next foreground launch.
`Location.getBackgroundSessionStatus()` reports service state. Notification permission is separate: a denied permission can hide its drawer notification without preventing the service.
Use `Location.requestNotificationPermissions()` or `useNotificationPermissions` when the feature needs that notification.
On Android, `PositionWatchStatus.areUpdatesAllowed` reflects foreground/service eligibility; `canDeliverUpdates` reports provider availability. An active subscription alone proves neither.

For existing root-API background work, retain its `TaskManager` and `startLocationUpdatesAsync` contract until deliberately migrating.

## Sensors and orientation

Import hardware APIs such as `Accelerometer`, `Gyroscope`, and `DeviceMotion` from `expo-sensors`.
Check availability, request required permission, and remove listeners when measurement stops.
Pick an update interval based on the feature; high-rate samples should not trigger full React renders.
Keep physical-device coordinate frames distinct from screen layout dimensions.
Sensor readings can be unavailable, noisy, or paused in the background.

On iOS 27, `requireFullScreen` no longer guarantees a nonresizable app, and an orientation lock can be refused.
Use current window/container dimensions for layout instead of assuming landscape means a wide app surface.
Duo hinge/posture belongs to `expo-hinge`, not inferred accelerometer thresholds.
Keep orientation effects from remounting navigation, a recording session, or unsaved forms.

## Device state

Use `expo-network` for connectivity signals; see [06-filesystem-networking.md](06-filesystem-networking.md).
Battery, brightness, and cellular packages have platform-dependent availability and permissions.
Do not treat a charging state, carrier, or orientation as a reliable background-execution guarantee.

## Checks and sources

Test approximate-only permission, services disabled, stale fixes, denial, focus changes, and fold/unfold while tracking.

- [Location](https://docs.expo.dev/versions/v58.0.0/sdk/location/)
- [Location next](https://docs.expo.dev/versions/v58.0.0/sdk/location-next/)
- [Published next entry point](https://unpkg.com/expo-location@58.0.16/build/next/index.d.ts)
- [Location release and geofencing changes](https://unpkg.com/expo-location@58.0.16/CHANGELOG.md)
- [Sensors](https://docs.expo.dev/versions/v58.0.0/sdk/sensors/)
- [ScreenOrientation](https://docs.expo.dev/versions/v58.0.0/sdk/screen-orientation/)
