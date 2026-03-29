import React from 'react';

type YTDData = {
  year: number;
  distance: number;
  rides: number;
  elevation: number;
  time: number;
  avg_hr: number | null;
};

type YTDSectionProps = {
  data: YTDData;
};

function formatValue(value: number | null) {
  if (value === null || Number.isNaN(value)) {
    return 'N/A';
  }

  return value.toLocaleString();
}

export default function YTDSection({ data }: YTDSectionProps) {
  return (
    <section className="card">
      <h2>YTD</h2>
      <div className="metrics-grid">
        <div className="metric">
          <div className="metric-label">Year</div>
          <div className="metric-value">{data.year}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Distance</div>
          <div className="metric-value">{formatValue(data.distance)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Rides</div>
          <div className="metric-value">{formatValue(data.rides)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Elevation</div>
          <div className="metric-value">{formatValue(data.elevation)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Time</div>
          <div className="metric-value">{formatValue(data.time)}</div>
        </div>
        <div className="metric">
          <div className="metric-label">Avg HR</div>
          <div className="metric-value">{formatValue(data.avg_hr)}</div>
        </div>
      </div>
    </section>
  );
}
