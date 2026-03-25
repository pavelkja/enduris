export type ReadinessStatus = 'good' | 'moderate' | 'high_fatigue';

export type FactorStatus = 'improving' | 'stable' | 'worsening' | 'high' | 'low';

export type SyncState = 'syncing' | 'processing' | 'ready' | 'error';

export interface ReadinessFactor {
  name: string;
  status: FactorStatus;
}

export interface ReadinessTrendPoint {
  date: string;
  value: number;
}

export interface InsightPayload {
  status: string;
  summary: string;
  explanation: string;
  guidance: string;
}

export interface ReadinessResponse {
  score: number;
  status: ReadinessStatus;
  summary: string;
  factors: ReadinessFactor[];
  trend: ReadinessTrendPoint[];
  insight: InsightPayload;
  sync_status: SyncState;
}
