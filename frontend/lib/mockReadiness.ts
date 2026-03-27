import { ReadinessResponse } from '@/types/readiness';

export const mockReadiness: ReadinessResponse = {
  score: 78,
  status: 'good',
  summary: 'Mild fatigue, stable performance',
  factors: [
    { name: 'efficiency', status: 'improving' },
    { name: 'hr_drift', status: 'worsening' },
    { name: 'load', status: 'high' },
    { name: 'variability', status: 'stable' },
  ],
  trend: [
    { date: '2026-03-01', value: 72 },
    { date: '2026-03-02', value: 75 },
    { date: '2026-03-03', value: 74 },
    { date: '2026-03-04', value: 76 },
    { date: '2026-03-05', value: 77 },
    { date: '2026-03-06', value: 79 },
    { date: '2026-03-07', value: 80 },
    { date: '2026-03-08', value: 77 },
    { date: '2026-03-09', value: 78 },
    { date: '2026-03-10', value: 78 },
  ],
  insight: {
    status: 'moderate_fatigue',
    summary: 'Your body shows signs of accumulated fatigue.',
    explanation: 'HR drift is increasing and recent load is above baseline.',
    guidance: 'You might benefit from lighter overall strain while recovery signals normalize.',
  },
  sync_status: 'ready',
};
