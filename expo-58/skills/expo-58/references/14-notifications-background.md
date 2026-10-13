# Notifications and background tasks — SDK 58

Verified 2026-10-13 against docs and the published notification declarations. Pins: [sdk-versions.json](sdk-versions.json).

```sh
npx expo install expo-notifications expo-device expo-constants expo-task-manager expo-background-task
```

## Foreground behavior changed

In SDK 58, notifications are presented by default until a handler is set, and on handler timeout.
Set an explicit handler early when the app needs quiet or selective foreground presentation.
Return promptly; do not wait for a network fetch inside it.

```ts
import * as Notifications from 'expo-notifications';

Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowBanner: true,
    shouldShowList: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});
```

Passing `null` removes Expo's handler. Android then does not show foreground notifications; iOS delegates to another registered delegate when present.
Do not conflate an absent initial handler with explicitly removing it.

## Permission, channel, token

Configure the notification plugin and platform push credentials, then build the app.
On Android, create the notification channel before the permission/token flow.
Use a real development/preview build for remote push validation; Expo Go is not a portable push-test environment.

```ts
import Constants from 'expo-constants';

export async function expoPushToken() {
  const permission = await Notifications.requestPermissionsAsync();
  if (!permission.granted) return null;
  const projectId = Constants.expoConfig?.extra?.eas?.projectId ?? Constants.easConfig?.projectId;
  if (!projectId) throw new Error('Missing EAS project ID');
  return (await Notifications.getExpoPushTokenAsync({ projectId })).data;
}
```

Associate token registrations with the correct authenticated account and unregister/reassociate them on sign-out.
A successful push ticket means the service accepted the request; inspect delivery receipts and remove invalid device tokens.
Register response listeners with cleanup, and handle the initial response when a notification launches a terminated app.
Validate any URL/identifier from payload data before routing to authorized content.

SDK 58 supports iOS `threadIdentifier`, Android plugin `largeIcon`, and `delivery: 'alarmClock'` for compatible date/repeating triggers.
Exact-alarm permissions and platform scheduling rules still apply; inspect `getExactAlarmPermissionsAsync`/`requestExactAlarmPermissionsAsync` before using alarm-clock delivery.
Do not claim ordinary scheduled notifications are exact timers or bypass OS restrictions.

## Background work

Define `TaskManager.defineTask` at module scope in a module imported at application startup.
An OS-started task can run without mounting any screen or React hook.
Use `expo-background-task` for deferrable work; `expo-background-fetch` is deprecated.
Register with the package and return the appropriate `BackgroundTaskResult`.
Keep tasks bounded, restartable, and tolerant of unavailable connectivity.

Scheduling is opportunistic. A requested minimum interval is not a promised execution time.
Background location, notifications, and audio have specialized APIs and permission/native configuration needs.
Use those APIs for their purpose instead of a generic task attempting to keep JS alive.
Treat forced termination, power saving, reboot, and revoked permission as expected lifecycle states.

## Validation and sources

Test foreground, background, terminated launch, denied permission, duplicate responses, and expired push tokens.
Verify the correct build/project/environment before debugging credentials.

- [Notifications](https://docs.expo.dev/versions/v58.0.0/sdk/notifications/)
- [Published notification-handler contract](https://unpkg.com/expo-notifications@58.1.3/build/NotificationsHandler.d.ts)
- [Push setup](https://docs.expo.dev/push-notifications/push-notifications-setup/)
- [Push receipts](https://docs.expo.dev/push-notifications/sending-notifications/)
- [BackgroundTask](https://docs.expo.dev/versions/v58.0.0/sdk/background-task/)
- [TaskManager](https://docs.expo.dev/versions/v58.0.0/sdk/task-manager/)
