'use client';

import { FactorsList } from '@/components/FactorsList';
import { InsightBox } from '@/components/InsightBox';
import { ReadinessScore } from '@/components/ReadinessScore';
import { SyncStatus } from '@/components/SyncStatus';
import { TrendChart } from '@/components/TrendChart';
import { readinessText } from '@/config/content';
import { mockReadiness } from '@/lib/mockReadiness';
import { normalizeReadiness } from '@/lib/readiness';
import { ReadinessResponse } from '@/types/readiness';
import { useEffect, useState } from 'react';

export default function HomePage() {
  const [data, setData] = useState<ReadinessResponse>(mockReadiness);

  useEffect(() => {
    const loadReadiness = async () => {
      try {
        const response = await fetch('/api/readiness', { cache: 'no-store' });
        if (!response.ok) {
          throw new Error('Readiness API unavailable');
        }
        const payload = (await response.json()) as Partial<ReadinessResponse>;
        setData(normalizeReadiness(payload));
      } catch {
        setData(mockReadiness);
      }
    };

    void loadReadiness();
  }, []);

  return (
    <main className="mx-auto max-w-5xl px-4 py-6 sm:px-6 sm:py-10">
      <header>
        <h1 className="text-2xl font-semibold text-slate-900 sm:text-3xl">{readinessText.pageTitle}</h1>
        <p className="mt-2 text-sm text-slate-600">{readinessText.pageSubtitle}</p>
      </header>

      <div className="mt-6 grid gap-4 sm:gap-5 md:grid-cols-2">
        <ReadinessScore score={data.score} status={data.status} summary={data.summary} />
        <SyncStatus syncStatus={data.sync_status} />
        <FactorsList factors={data.factors} />
        <InsightBox insight={data.insight} />
        <div className="md:col-span-2">
          <TrendChart trend={data.trend} />
        </div>
      </div>
    </main>
  );
}
