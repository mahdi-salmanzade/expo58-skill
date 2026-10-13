import { useState } from 'react';
import { KeyboardAvoidingView, Platform, View, useWindowDimensions } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import type { AdaptivePanesProps } from './AdaptivePanes.types';

export default function AdaptivePanesFallback({ primary, secondary }: AdaptivePanesProps) {
  const [containerWidth, setContainerWidth] = useState(0);
  const { fontScale } = useWindowDimensions();
  // Product breakpoint: two readable panes, with more room for larger text.
  // The actual content container may be much narrower than the whole window.
  const horizontal = containerWidth >= 680 * Math.max(1, fontScale);
  return (
    <SafeAreaView style={{ flex: 1 }} edges={['top', 'right', 'bottom', 'left']}>
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <View
          onLayout={(event) => setContainerWidth(event.nativeEvent.layout.width)}
          style={{ flex: 1, flexDirection: horizontal ? 'row' : 'column' }}>
          <View style={{ flex: 1, minWidth: 0, minHeight: 0 }}>{primary}</View>
          <View style={{ flex: 1, minWidth: 0, minHeight: 0 }}>{secondary}</View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}
