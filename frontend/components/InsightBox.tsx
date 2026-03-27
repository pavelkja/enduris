import { readinessText } from '@/config/content';
import { InsightPayload } from '@/types/readiness';

export function InsightBox({ insight }: { insight: InsightPayload }) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">{readinessText.sections.insight}</h2>
      <div className="mt-4 space-y-2 text-sm text-slate-700">
        <p className="font-medium text-slate-900">{insight.summary}</p>
        <p>{insight.explanation}</p>
        <p className="text-slate-600">{insight.guidance}</p>
      </div>
    </section>
  );
}
