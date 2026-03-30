import { formatTime, formatDistance, formatElevation, formatHR } from '@/utils/format';
import React from 'react';

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
    <section className="card">
      <h2>Monthly</h2>

      {data.length === 0 ? (
        <p>No monthly data available.</p>
      ) : (
        data.map((month) => {
          const metrics = month.metrics;

          return (
            <article
              key={`${month.label}-${month.month}`}
              className="card"
              style={{ marginTop: 12 }}
            >
              <h3 style={{ marginTop: 0 }}>
                {month.label} ({month.month})
              </h3>

              <div className="metrics-grid">
                <div className="metric">
                  <div className="metric-label">Distance</div>
                  <div className="metric-value">
                    {formatDistance(metrics.distance)}
                  </div>
                </div>

                <div className="metric">
                  <div className="metric-label">Rides</div>
                  <div className="metric-value">
                    {formatValue(metrics.rides)}
                  </div>
                </div>

                <div className="metric">
                  <div className="metric-label">Elevation</div>
                  <div className="metric-value">
                    {formatElevation(metrics.elevation)}
                  </div>
                </div>

                <div className="metric">
                  <div className="metric-label">Time</div>
                  <div className="metric-value">
                    {formatTime(metrics.time)}
                  </div>
                </div>

                <div className="metric">
                  <div className="metric-label">Avg HR</div>
                  <div className="metric-value">
                    {formatHR(metrics.avg_hr)}
                  </div>
                </div>
              </div>
            </article>
          );
        })
      )}
    </section>
  );
}
