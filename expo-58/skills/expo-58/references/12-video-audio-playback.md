# Video and audio lifecycle — SDK 58

Verified 2026-10-16. Use [sdk-versions.json](sdk-versions.json) for compatible versions.

```sh
npx expo install expo-video expo-audio
```

## Video

Use `expo-video`; do not start new work with the old `expo-av` playback API.
A player owns playback state; `VideoView` is its rendering surface.

```tsx
import { useVideoPlayer, VideoView } from 'expo-video';

export function Clip({ uri }: { uri: string }) {
  const player = useVideoPlayer(uri, value => {
    value.loop = true;
  });
  return <VideoView player={player} style={{ width: '100%', aspectRatio: 16 / 9 }} />;
}
```

The hook releases its player on unmount. Imperatively created players require explicit lifecycle management.
Pause inactive feed items and decide whether background audio is a supported feature.
Drive custom controls from player events/status; changing a mutable player property does not itself cause a React render.
Use the package's current event hooks instead of polling every animation frame.
Handle loading/error/end states and source replacement without leaking players.
Configure picture-in-picture/background support through the config plugin before rebuilding.

## Audio playback

```tsx
import { Button } from 'react-native';
import { useAudioPlayer, useAudioPlayerStatus } from 'expo-audio';

export function AudioButton({ uri }: { uri: string }) {
  const player = useAudioPlayer(uri);
  const status = useAudioPlayerStatus(player);
  return (
    <Button
      title={status.playing ? 'Pause' : 'Play'}
      onPress={() => status.playing ? player.pause() : player.play()}
    />
  );
}
```

For replay after completion, seek to the beginning before playing again as the feature requires.
Configure `setAudioModeAsync` intentionally for interruptions, recording, silent-mode playback, and background behavior.
Background playback requires native configuration; lock-screen controls are not a substitute for it.
SDK 58 extends lock-screen playback controls to playlists.

## Recording

Use `useAudioRecorder(RecordingPresets.HIGH_QUALITY)` and `useAudioRecorderState`.
Request permission through `AudioModule.requestRecordingPermissionsAsync` when the user begins the recording feature.
Await `prepareToRecordAsync()` before `record()`, and await `stop()` before using the recording URI.
Configure `allowsRecording` with `setAudioModeAsync` for the recording session and restore the intended mode afterward.
Handle interrupted/denied sessions without pretending a usable recording exists.
Default recordings are cached; choose the documented `directory: 'document'` option or persist the result explicitly.

SDK 58's `AudioStream` adds `startFileRecordingAsync`/`stopFileRecordingAsync` for WAV/PCM files alongside streaming buffers.
Use this specialized API for buffer-processing workflows, not as a replacement for ordinary recording without a reason.
Confirm sample rate, channel count, and file options in the installed `AudioStream` declarations before creating a processing pipeline.

## Layout and platform constraints

Resizing a Duo window should resize the media surface while preserving player identity and playback position.
Avoid remounting the player just because the display changed from one pane to two.
Test Bluetooth/headphone disconnection, phone interruptions, screen lock, app backgrounding, and user-paused recordings.
A simulator does not establish microphone or background-session reliability.
Web autoplay/user-gesture rules differ from native playback.

## Sources

- [Video](https://docs.expo.dev/versions/v58.0.0/sdk/video/)
- [Audio](https://docs.expo.dev/versions/v58.0.0/sdk/audio/)
- [Audio package changelog](https://unpkg.com/expo-audio@58.0.9/CHANGELOG.md)
- [Audio declarations](https://unpkg.com/expo-audio@58.0.9/build/ExpoAudio.d.ts)
- [Screen capture controls](https://docs.expo.dev/versions/v58.0.0/sdk/screen-capture/)
