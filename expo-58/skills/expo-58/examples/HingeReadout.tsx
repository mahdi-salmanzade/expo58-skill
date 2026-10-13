import { addHingeListener, getHinge, isAvailable, useHinge, type Hinge } from 'expo-hinge';
import { useEffect, useState } from 'react';
import { Button, Text, View } from 'react-native';

function describe(hinge: Hinge | null, available: boolean): string {
  if (!available) return 'Hinge API unavailable in this build or OS';
  if (hinge === null) return 'No hinge reading for this window';
  return `${hinge.status} · ${Math.round(hinge.angle)}°`;
}

/** Live values, a deliberately frozen snapshot, and explicit event cleanup. */
export default function HingeReadout() {
  const live = useHinge(); // The hook owns and cleans up its own subscription.
  const available = isAvailable(); // OS/build capability, never hardware detection.
  const [snapshot, setSnapshot] = useState<Hinge | null>(getHinge);
  const [events, setEvents] = useState({ changes: 0, lastAngle: null as number | null });

  useEffect(() => {
    const subscription = addHingeListener(({ hinge }) => {
      // The event contains { hinge }, not angle/status at its root.
      // Losing a window's reading is a real event; do not turn null into 0°.
      setEvents((previous) => ({
        changes: previous.changes + 1,
        lastAngle: hinge?.angle ?? null,
      }));
    });
    return () => subscription.remove();
  }, []);

  return (
    <View style={{ padding: 20, gap: 12 }}>
      <Text>Live: {describe(live, available)}</Text>
      <Text>Snapshot: {describe(snapshot, available)}</Text>
      <Button title="Read a new snapshot" onPress={() => setSnapshot(getHinge())} />
      <Text>Change events since mounting: {events.changes}</Text>
      <Text>Last event angle: {events.lastAngle === null ? 'No reading' : `${Math.round(events.lastAngle)}°`}</Text>
    </View>
  );
}
