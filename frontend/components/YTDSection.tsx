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

function getTrend(current: number, previous?: number) {
  if (previous == null || previous === 0) {
    return undefined;
  }

  const change = ((current - previous) / previous) * 100;

  if (change <= 0) {
    return undefined;
  }

  return `+${change.toFixed(1)}% vs previous year`;
}

export default function YTDSection({ data }: YTDSectionProps) {
  if (!data || data.length === 0) {
    return <p className="status-message">No YTD data</p>;
  }

  const current = data[0];
  const previous = data[1];
  const metrics = current.metrics;

  return (
    <section className="section-card">
      <h2 className="section-title">Year to Date</h2>
      <div className="metrics-grid">
        <DataCard title="Year" value={formatValue(current.year)} />
        <DataCard
          title="Distance"
          value={formatDistance(metrics.distance)}
          trend={getTrend(metrics.distance, previous?.metrics.distance)}
        />
        <DataCard
          title="Rides"
          value={formatValue(metrics.rides)}
          trend={getTrend(metrics.rides, previous?.metrics.rides)}
        />
        <DataCard
          title="Elevation"
          value={formatElevation(metrics.elevation)}
          trend={getTrend(metrics.elevation, previous?.metrics.elevation)}
        />
        <DataCard
          title="Time"
          value={formatTime(metrics.time)}
          trend={getTrend(metrics.time, previous?.metrics.time)}
        />
        <DataCard title="Avg HR" value={formatHR(metrics.avg_hr)} />
      </div>
    </section>
  );
}
