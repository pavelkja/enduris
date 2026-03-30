import { formatTime, formatDistance, formatElevation, formatHR } from '@/utils/format';
import React from 'react';
import DataCard from '@/components/DataCard';

type Metrics = {
  distance: number;
  rides: number;
  elevation: number;
  time: number;
  avg_hr: number | null;
};

type MonthlyData = {
  label: string;
  month: string;
  metrics: Metrics;
};

type MonthlySectionProps = {
  data: MonthlyData[];
};

function formatValue(value?: number | null) {
  if (value == null || Number.isNaN(value)) {
    return '0';
  }

  return Number(value).toLocaleString();
}

export default function MonthlySection({ data }: MonthlySectionProps) {
  return (
    <section className="section-card">
      <h2 className="section-title">Monthly</h2>

      {data.length === 0 ? (
        <p className="status-message">No monthly data available.</p>
      ) : (
        <div className="stack">
          {data.map((month) => {
            const metrics = month.metrics;

            return (
              <article key={`${month.label}-${month.month}`} className="section-card">
                <h3 className="section-title" style={{ marginBottom: 24 }}>
                  {month.label} ({month.month})
                </h3>

                <div className="metrics-grid">
                  <DataCard title="Distance" value={formatDistance(metrics.distance)} />
                  <DataCard title="Rides" value={formatValue(metrics.rides)} />
                  <DataCard title="Elevation" value={formatElevation(metrics.elevation)} />
                  <DataCard title="Time" value={formatTime(metrics.time)} />
                  <DataCard title="Avg HR" value={formatHR(metrics.avg_hr)} />
                </div>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
