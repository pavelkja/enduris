import { formatTime, formatDistance, formatElevation, formatHR } from '@/utils/format';
import React from 'react';

type Metrics = {
  distance: number;
  rides: number;
  elevation: number;
  time: number;
  avg_hr: number | null;
};

type YTDData = {
  year: number;
  metrics: Metrics;
};

type YTDSectionProps = {
  data: YTDData[];
};

function formatValue(value?: number | null) {
  if (value == null || Number.isNaN(value)) {
    return '0';
  }

  return Number(value).toLocaleString();
}

function formatTime(seconds?: number | null) {
  if (!seconds) return '0h';

  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);

  return `${h}h ${m}m`;
}

export default function YTDSection({ data }: YTDSectionProps) {
  if (!data || data.length === 0) {
    return <p>No YTD data</p>;
  }

  const current = data[0]; // vezmeme aktuální rok
  const metrics = current.metrics;

  return (
    <section className="card">
      <h2>YTD</h2>
      <div className="metrics-grid">
        <div className="metric">
          <div className="metric-label">Year</div>
          <div className="metric-value">{current.year}</div>
        </div>

        <div className="metric">
          <div className="metric-label">Distance (km)</div>
          <div className="metric-value">{formatValue(metrics.distance)}</div>
        </div>

        <div className="metric">
          <div className="metric-label">Rides</div>
          <div className="metric-value">{formatValue(metrics.rides)}</div>
        </div>

        <div className="metric">
          <div className="metric-label">Elevation (m)</div>
          <div className="metric-value">{formatValue(metrics.elevation)}</div>
        </div>

        <div className="metric">
          <div className="metric-label">Time</div>
          <div className="metric-value">{formatTime(metrics.time)}</div>
        </div>

        <div className="metric">
          <div className="metric-label">Avg HR</div>
          <div className="metric-value">{formatValue(metrics.avg_hr)}</div>
        </div>
      </div>
    </section>
  );
}
