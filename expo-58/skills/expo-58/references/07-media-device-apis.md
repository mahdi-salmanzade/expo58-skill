# Contacts, calendars, photos, and device feedback — SDK 58

Verified 2026-10-13. Install only the packages needed; [sdk-versions.json](sdk-versions.json) records the SDK snapshot.

```sh
npx expo install expo-contacts expo-calendar expo-media-library expo-haptics expo-asset
```

## Contacts: objects, selected fields, and pagination

The root `expo-contacts` API uses `Contact` objects. Legacy functions have a separate `expo-contacts/legacy` entry point.
Read selected fields for a bounded page; do not load an entire address book just to render one screen.
A contact's `id` is a record identifier, not its complete data.

```ts
import * as Contacts from 'expo-contacts';

export async function readNames() {
  const permission = await Contacts.requestPermissionsAsync();
  if (!permission.granted) return [];
  return Contacts.Contact.getAllDetails(
    [Contacts.ContactField.FULL_NAME],
    { limit: 30, offset: 0 }
  );
}
```

`patch` updates supplied fields; `update` replaces the record's fields. Choose deliberately for an edit form.
Limited iOS contact access is a usable state. `ContactAccessButton` can expand the accessible selection on supported iOS versions.
Configure the `contactsPermission` message through the package plugin and rebuild.

## Calendar: scope the access to the feature

The new API uses `ExpoCalendar`/event objects and module methods such as `getCalendars`.
The older suffixed methods belong to `expo-calendar/legacy`; check imports during migration.
Calendar is not supported in Expo Go in the SDK 58 docs; use a development build.

```ts
import * as Calendar from 'expo-calendar';

export async function readCalendars() {
  const permission = await Calendar.requestCalendarPermissions();
  if (!permission.granted) return [];
  return Calendar.getCalendars(Calendar.EntityTypes.EVENT);
}
```

For iOS add-only features, the plugin's `writeOnlyAccess` and `writeOnlyCalendarPermission` support write-only authorization.
Call `requestCalendarPermissions(true)` for that flow; it does not authorize reading existing calendar data or presenting a calendar picker.
System calendar dialogs may avoid broad access. Verify the selected dialog's platform contract.
Preserve time zones and all-day semantics instead of converting every event to the device's current zone.

## MediaLibrary: system assets are not cache files

Use `Asset`, `Album`, and `Query` from the root package; legacy module functions are under `/legacy`.
An image picker is usually enough for choosing a few photos; do not request the entire media library for that workflow.
For a photo-library browser:

```ts
import { AssetField, MediaType, Query, requestPermissionsAsync } from 'expo-media-library';

export async function firstPhotos() {
  const permission = await requestPermissionsAsync();
  if (!permission.granted) return [];
  return new Query().eq(AssetField.MEDIA_TYPE, MediaType.IMAGE).limit(24).exe();
}
```

Use asset getters for metadata; do not assume a native asset's `id` is a readable local file path.
Handle limited photo access, cloud-backed assets, empty results, and permission changes while the app is backgrounded.
Keep persistent app files and system photo-library records distinct when deleting or exporting.

## Feedback and assets

`import * as Haptics from 'expo-haptics'` exposes selection, impact, notification, and Android-specific feedback methods.
Trigger feedback for meaningful actions and allow hardware/power settings to suppress it.
`Asset` from `expo-asset` resolves bundled resources; await `downloadAsync()` before relying on `localUri`.
Check the asset extension and Metro configuration for nonstandard formats rather than assuming every file is bundled.

## Sources

- [Contacts](https://docs.expo.dev/versions/v58.0.0/sdk/contacts/)
- [Calendar](https://docs.expo.dev/versions/v58.0.0/sdk/calendar/)
- [MediaLibrary](https://docs.expo.dev/versions/v58.0.0/sdk/media-library/)
- [Haptics](https://docs.expo.dev/versions/v58.0.0/sdk/haptics/)
- [Asset](https://docs.expo.dev/versions/v58.0.0/sdk/asset/)
