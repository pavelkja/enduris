import { FactorStatus, ReadinessStatus, SyncState } from '@/types/readiness';

export const readinessText = {
  pageTitle: 'Readiness Dashboard',
  pageSubtitle: 'A simple view of current readiness and what may be driving it.',
  sections: {
    score: 'Readiness Score',
    factors: 'Key Factors',
    trend: 'Recent Trend',
    insight: 'Insight',
    sync: 'Sync Status',
  },
  statusLabels: {
    good: 'Good',
    moderate: 'Moderate',
    high_fatigue: 'High Fatigue',
  } satisfies Record<ReadinessStatus, string>,
  factorLabels: {
    efficiency: 'Efficiency',
    hr_drift: 'HR Drift',
    load: 'Load',
    variability: 'Variability',
  } as Record<string, string>,
  factorStatuses: {
    improving: 'Improving',
    stable: 'Stable',
    worsening: 'Worsening',
    high: 'High',
    low: 'Low',
  } satisfies Record<FactorStatus, string>,
  syncLabels: {
    syncing: 'Syncing',
    processing: 'Processing',
    ready: 'Ready',
    error: 'Error',
  } satisfies Record<SyncState, string>,
  guidanceTemplates: {
    fallbackSummary: 'Current signals appear generally stable.',
    fallbackExplanation: 'Available indicators do not show a strong change from your baseline.',
    fallbackGuidance: 'You might benefit from continuing with a balanced approach while monitoring trends.',
  },
};
