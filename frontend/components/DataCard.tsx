import React from 'react';

type DataCardProps = {
  title: string;
  value: string;
  trend?: string;
};

export default function DataCard({ title, value, trend }: DataCardProps) {
  return (
    <div className="data-card">
      <div className="data-card-title">{title}</div>
      <div className="data-card-value">{value}</div>
      {trend ? <div className="data-card-trend">{trend}</div> : null}
    </div>
  );
}
