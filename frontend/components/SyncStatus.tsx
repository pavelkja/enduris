import { readinessText } from '@/config/content';
import { SyncState } from '@/types/readiness';

const stateStyle: Record<SyncState, string> = {
  syncing: 'bg-blue-100 text-blue-800',
  processing: 'bg-amber-100 text-amber-800',
  ready: 'bg-green-100 text-green-800',
  error: 'bg-red-100 text-red-800',
};

export function SyncStatus({ syncStatus }: { syncStatus: SyncState }) {
  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">{readinessText.sections.sync}</h2>
      <span className={`mt-4 inline-flex rounded-full px-3 py-1 text-sm font-medium ${stateStyle[syncStatus]}`}>
        {readinessText.syncLabels[syncStatus]}
      </span>
    </section>
  );
}
