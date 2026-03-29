import React from 'react';

type MonthlyData = {
  label: string;
  month: number;
  distance: number;
  rides: number;
  elevation: number;
  time: number;
  avg_hr: number | null;
};

type MonthlySectionProps = {
  data: MonthlyData[];
};

function formatValue(value: number | null) {
  if (value === null || Number.isNaN(value)) {
    return 'N/A';
  }

  return value.toLocaleString();
}

export default function MonthlySection({ data }: MonthlySectionProps) {
  return (
    <section className="card">
      <h2>Monthly</h2>
      {data.length === 0 ? (
        <p>No monthly data available.</p>
      ) : (
        data.map((month) => (
          <article key={`${month.label}-${month.month}`} className="card" style={{ marginTop: 12 }}>
            <h3 style={{ marginTop: 0 }}>
              {month.label} (Month {month.month})
            </h3>
            <div className="metrics-grid">
              <div className="metric">
                <div className="metric-label">Distance</div>
                <div className="metric-value">{formatValue(month.distance)}</div>
              </div>
              <div className="metric">
                <div className="metric-label">Rides</div>
                <div className="metric-value">{formatValue(month.rides)}</div>
              </div>
              <div className="metric">
                <div className="metric-label">Elevation</div>
                <div className="metric-value">{formatValue(month.elevation)}</div>
              </div>
              <div className="metric">
                <div className="metric-label">Time</div>
                <div className="metric-value">{formatValue(month.time)}</div>
              </div>
              <div className="metric">
                <div className="metric-label">Avg HR</div>
                <div className="metric-value">{formatValue(month.avg_hr)}</div>
              </div>
            </div>
          </article>
        ))
      )}
    </section>
  );
}
