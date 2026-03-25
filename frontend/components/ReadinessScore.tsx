import { readinessText } from '@/config/content';
import { ReadinessStatus } from '@/types/readiness';

const statusStyles: Record<ReadinessStatus, string> = {
  good: 'text-readiness-good',
  moderate: 'text-readiness-moderate',
  high_fatigue: 'text-readiness-fatigue',
};

export function ReadinessScore({ score, status, summary }: { score: number; status: ReadinessStatus; summary: string }) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <p className="text-sm font-medium text-slate-500">{readinessText.sections.score}</p>
      <div className="mt-3 flex items-end gap-3">
        <span className={`text-6xl font-semibold leading-none ${statusStyles[status]}`}>{score}</span>
        <span className="mb-1 text-sm font-medium uppercase tracking-wide text-slate-500">
          {readinessText.statusLabels[status]}
        </span>
      </div>
      <p className="mt-4 text-sm text-slate-700">{summary}</p>
    </section>
  );
}
