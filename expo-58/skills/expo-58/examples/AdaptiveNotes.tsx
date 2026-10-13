import { useState } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, TextInput } from 'react-native';
import AdaptivePanes from './AdaptivePanes';

const notes = [
  { id: 'trip', title: 'Trip ideas' },
  { id: 'books', title: 'Books to read' },
] as const;
type NoteId = (typeof notes)[number]['id'];

/** Mount below the app's existing SafeAreaProvider; keep navigation outside it. */
export default function AdaptiveNotes({ arrangementBuildVerified = false }: {
  arrangementBuildVerified?: boolean;
}) {
  // Selection and drafts belong to the task, above the adaptive presentation.
  const [selected, setSelected] = useState<NoteId>('trip');
  const [drafts, setDrafts] = useState<Record<NoteId, string>>({ trip: '', books: '' });
  const title = notes.find((note) => note.id === selected)!.title;

  return (
    <AdaptivePanes
      arrangementBuildVerified={arrangementBuildVerified}
      primary={
        <ScrollView style={styles.pane} contentContainerStyle={styles.content}>
          <Text accessibilityRole="header" style={styles.heading}>Notes</Text>
          {notes.map((note) => (
            <Pressable
              key={note.id}
              accessibilityRole="button"
              accessibilityState={{ selected: selected === note.id }}
              onPress={() => setSelected(note.id)}
              style={[styles.row, selected === note.id && styles.selected]}>
              <Text>{note.title}</Text>
            </Pressable>
          ))}
        </ScrollView>
      }
      secondary={
        <ScrollView
          style={styles.pane}
          contentContainerStyle={styles.content}
          keyboardShouldPersistTaps="handled">
          <Text accessibilityRole="header" style={styles.heading}>{title}</Text>
          <TextInput
            accessibilityLabel={`${title} draft`}
            multiline
            value={drafts[selected]}
            onChangeText={(text) => setDrafts((previous) => ({ ...previous, [selected]: text }))}
            placeholder="Write a note"
            style={styles.input}
          />
          <Text>Change the window size while editing. Your draft stays with this note.</Text>
        </ScrollView>
      }
    />
  );
}

const styles = StyleSheet.create({
  pane: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 20, gap: 12 },
  heading: { fontSize: 22, fontWeight: '600' },
  row: { minHeight: 44, padding: 12, borderRadius: 8 },
  selected: { backgroundColor: '#e4eaff' },
  input: { minHeight: 120, padding: 12, borderWidth: 1, borderColor: '#777', borderRadius: 8, textAlignVertical: 'top' },
});
