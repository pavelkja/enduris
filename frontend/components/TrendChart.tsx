'use client';

import { readinessText } from '@/config/content';
import { ReadinessTrendPoint } from '@/types/readiness';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

export function TrendChart({ trend }: { trend: ReadinessTrendPoint[] }) {
  const chartData = trend.slice(-10).map((point) => ({
    ...point,
    label: point.date.slice(5),
  }));

  return (
    <section className="rounded-2xl bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-900">{readinessText.sections.trend}</h2>
      <div className="mt-4 h-52 w-full">
        <ResponsiveContainer>
          <LineChart data={chartData}>
            <XAxis dataKey="label" tickLine={false} axisLine={false} fontSize={12} />
            <YAxis hide domain={[0, 100]} />
            <Tooltip formatter={(value) => [`${value}`, 'Readiness']} />
            <Line type="monotone" dataKey="value" stroke="#0f172a" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
