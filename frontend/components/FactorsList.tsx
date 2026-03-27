import { readinessText } from '@/config/content';
import { ReadinessFactor } from '@/types/readiness';

export function FactorsList({ factors }: { factors: ReadinessFactor[] }) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">{readinessText.sections.factors}</h2>
      <ul className="mt-4 space-y-3">
        {factors.slice(0, 4).map((factor) => (
          <li key={factor.name} className="flex items-center justify-between rounded-xl border border-slate-200 px-3 py-2">
            <span className="text-sm font-medium text-slate-700">
              {readinessText.factorLabels[factor.name] ?? factor.name}
            </span>
            <span className="text-sm text-slate-500">{readinessText.factorStatuses[factor.status]}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
