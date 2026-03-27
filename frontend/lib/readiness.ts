import { readinessText } from '@/config/content';
import { mockReadiness } from '@/lib/mockReadiness';
import { ReadinessResponse } from '@/types/readiness';

export function normalizeReadiness(data: Partial<ReadinessResponse>): ReadinessResponse {
  return {
    score: data.score ?? mockReadiness.score,
    status: data.status ?? mockReadiness.status,
    summary: data.summary ?? readinessText.guidanceTemplates.fallbackSummary,
    factors: data.factors?.length ? data.factors : mockReadiness.factors,
    trend: data.trend?.length ? data.trend.slice(-10) : mockReadiness.trend,
    insight: {
      status: data.insight?.status ?? mockReadiness.insight.status,
      summary: data.insight?.summary ?? readinessText.guidanceTemplates.fallbackSummary,
      explanation: data.insight?.explanation ?? readinessText.guidanceTemplates.fallbackExplanation,
      guidance: data.insight?.guidance ?? readinessText.guidanceTemplates.fallbackGuidance,
    },
    sync_status: data.sync_status ?? mockReadiness.sync_status,
  };
}
