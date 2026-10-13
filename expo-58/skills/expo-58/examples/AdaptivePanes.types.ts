import type { ReactElement } from 'react';

export type AdaptivePanesProps = {
  primary: ReactElement;
  secondary: ReactElement;
  /** Set only after verifying this binary's @expo/ui includes the iOS 27.1 SDK implementation. */
  arrangementBuildVerified?: boolean;
};
