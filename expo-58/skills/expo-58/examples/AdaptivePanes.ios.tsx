import { ArrangementView, Host, RNHostView, VStack } from '@expo/ui/swift-ui';
import { arrangementViewStyle, frame } from '@expo/ui/swift-ui/modifiers';
import { Platform } from 'react-native';
import AdaptivePanesFallback from './AdaptivePanesFallback';
import type { AdaptivePanesProps } from './AdaptivePanes.types';

const fill = frame({ maxWidth: Infinity, maxHeight: Infinity });

function hasArrangementOS(): boolean {
  const [major = 0, minor = 0] = String(Platform.Version).split('.').map(Number);
  return major > 27 || (major === 27 && minor >= 1);
}

export default function AdaptivePanes(props: AdaptivePanesProps) {
  // This capability branch is stable while the device folds or the window resizes.
  // An OS check alone cannot detect an older SDK's compiled-out implementation.
  if (!props.arrangementBuildVerified || !hasArrangementOS()) {
    return <AdaptivePanesFallback {...props} />;
  }
  return (
    <Host style={{ flex: 1 }}>
      <ArrangementView modifiers={[arrangementViewStyle('split', { axes: 'both' }), fill]}>
        <ArrangementView.Primary>
          <VStack spacing={0} modifiers={[fill]}>
            <RNHostView>{props.primary}</RNHostView>
          </VStack>
        </ArrangementView.Primary>
        <ArrangementView.Secondary>
          <VStack spacing={0} modifiers={[fill]}>
            <RNHostView>{props.secondary}</RNHostView>
          </VStack>
        </ArrangementView.Secondary>
      </ArrangementView>
    </Host>
  );
}
