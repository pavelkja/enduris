'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import MonthlySection from '@/components/MonthlySection';
import SportSelector from '@/components/SportSelector';
import YTDSection from '@/components/YTDSection';
import DataCard from '@/components/DataCard';
import brandIcon from '@/pics/branding/enduris-ikona-web2.png';

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

type MonthlyData = {
  label: string;
  month: string;
  metrics: Metrics;
};

type PerformanceStatus = {
  trend: string;
  confidence: string;
  variability: number | null;
  stabilityLabel: 'Stable' | 'Moderate' | 'Volatile';
  variabilityInterpretation: string;
  efficiencyMessage: string;
  insightMessage: string;
}

const baseUrl = 'https://api.enduris.app';
const userId = 'b506b832-76f2-48f2-b1a1-e00ccef8b988';

export default function DashboardPage() {
  const [sport, setSport] = useState('cycling_overall');
  const [ytdData, setYtdData] = useState<YTDData[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlyData[]>([]);
  const [performanceStatus, setPerformanceStatus] = useState<PerformanceStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  function buildEfficiencyMessage(last5?: number | null, last10?: number | null) {
    if (last5 == null || last10 == null || last10 === 0) {
      return 'Efficiency trend unavailable for the last 10 activities.';
    }

    const deltaPercent = ((last5 - last10) / last10) * 100;
    const direction = deltaPercent >= 0 ? 'improving' : 'declining';
    return `Efficiency ${direction} by ${Math.abs(deltaPercent).toFixed(1)}% over last 10 activities.`;
  }

  function calculateVariabilityPercent(
    data?: Array<{ efficiency?: number | null }>,
    windowSize = 10
  ) {
    const recentValues = (Array.isArray(data) ? data : [])
      .map((entry) => entry?.efficiency)
      .filter((value): value is number => typeof value === 'number' && Number.isFinite(value))
      .slice(-windowSize);

    if (recentValues.length < 2) {
      return null;
    }

    const mean = recentValues.reduce((sum, value) => sum + value, 0) / recentValues.length;
    if (mean === 0) {
      return null;
    }

    const variance =
      recentValues.reduce((sum, value) => sum + (value - mean) ** 2, 0) / recentValues.length;
    const standardDeviation = Math.sqrt(variance);

    return (standardDeviation / mean) * 100;
  }

  function classifyStability(variabilityPercent: number | null) {
    if (variabilityPercent == null) {
      return {
        label: 'Moderate' as const,
        interpretation: 'Not enough data to determine stability.',
      };
    }

    if (variabilityPercent < 5) {
      return { label: 'Stable' as const, interpretation: 'Very stable (<5%).' };
    }

    if (variabilityPercent <= 10) {
      return { label: 'Moderate' as const, interpretation: 'Stable (5–10%).' };
    }

    return { label: 'Volatile' as const, interpretation: 'Volatile (>10%).' };
  }

  function buildInsightMessage(trend: string, stabilityLabel: 'Stable' | 'Moderate' | 'Volatile') {
    if (trend === 'improving') {
      if (stabilityLabel === 'Volatile') {
        return 'You are improving but performance is inconsistent.';
      }
      return 'You are improving with stable performance.';
    }

    if (trend === 'declining') {
      if (stabilityLabel === 'Volatile') {
        return 'Performance is declining and inconsistent.';
      }
      return 'Performance is declining but remains relatively stable.';
    }

    if (stabilityLabel === 'Volatile') {
      return 'Performance is steady overall but activity-to-activity output is inconsistent.';
    }

    return 'Performance is stable with consistent activity execution.';
  }

  useEffect(() => {
    async function fetchDashboardData() {
      setLoading(true);
      setError(null);

      try {
        const ytdUrl = `${baseUrl}/api/dashboard/ytd?user_id=${userId}&sport=${sport}`;
        const monthsUrl = `${baseUrl}/api/dashboard/months?user_id=${userId}&sport=${sport}`;

        const sportTypeBySport: Record<string, string> = {
          ride: 'Ride',
          run: 'Run',
          cycling_overall: 'Ride',
        };
        const sportType = sportTypeBySport[sport] ?? 'Ride';
        const performanceUrl = `${baseUrl}/dashboard/efficiency-trend?user_id=${userId}&sport_type=${sportType}`;

        const [ytdResponse, monthsResponse, performanceResponse] = await Promise.all([
          fetch(ytdUrl),
          fetch(monthsUrl),
          fetch(performanceUrl),
        ]);

        if (!ytdResponse.ok || !monthsResponse.ok) {
          throw new Error('Request failed');
        }

        const ytdJson = await ytdResponse.json();
        const monthsJson = await monthsResponse.json();
        const performanceJson = performanceResponse.ok ? await performanceResponse.json() : null;
        const latestPerformanceData = Array.isArray(performanceJson?.data)
          ? performanceJson.data[performanceJson.data.length - 1]
          : null;
        const efficiencyMessage = buildEfficiencyMessage(
          latestPerformanceData?.efficiency_last_5,
          latestPerformanceData?.efficiency_last_10
        );
        const variability = calculateVariabilityPercent(performanceJson?.data);
        const stability = classifyStability(variability);
        const trend = String(performanceJson?.trend ?? 'stable');

        // ✅ správně: pole
        setYtdData(Array.isArray(ytdJson) ? ytdJson : []);
        setMonthlyData(Array.isArray(monthsJson) ? monthsJson : []);
        setPerformanceStatus({
          trend,
          confidence: String(performanceJson?.confidence ?? 'low'),
          variability,
          stabilityLabel: stability.label,
          variabilityInterpretation: stability.interpretation,
          efficiencyMessage,
          insightMessage: buildInsightMessage(trend, stability.label),
        });
      } catch (_err) {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, [sport]);

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="branding">
          <Image src={brandIcon} alt="Enduris logo" width={28} height={28} priority />
          <span className="branding-name">ENDURIS.APP</span>
        </div>

        <ul className="nav-list">
          <li>
            <Link className="nav-link active" href="/dashboard">
              Dashboard
            </Link>
          </li>
          <li>
            <Link className="nav-link" href="/">
              Home
            </Link>
          </li>
        </ul>
      </aside>

      <main className="page-content">
        <div className="container">
          <section className="section-card">
            <h1 className="section-title">Performance Dashboard</h1>
            <SportSelector value={sport} onChange={setSport} />
          </section>

          {loading && <p className="status-message">Loading...</p>}
          {error && <p className="status-message">{error}</p>}

          {!loading && !error && (
            <>
              <section className="section-card">
                <h2 className="section-title">Performance Status</h2>
                <div className="metrics-grid">
                  <DataCard title="Trend" value={performanceStatus?.trend ?? 'stable'} />
                  <DataCard title="Confidence" value={performanceStatus?.confidence ?? 'low'} />
                  <DataCard
                    title="Stability"
                    value={`${performanceStatus?.stabilityLabel ?? 'Moderate'}${
                      performanceStatus?.variability != null
                        ? ` (${performanceStatus.variability.toFixed(1)}%)`
                        : ''
                    }`}
                  />
                </div>
                <p className="status-message">{performanceStatus?.efficiencyMessage}</p>
                <p className="status-message">{performanceStatus?.variabilityInterpretation}</p>
                <p className="status-message">{performanceStatus?.insightMessage}</p>
              </section>

              {ytdData.length > 0 ? <YTDSection data={ytdData} /> : <p className="status-message">No YTD data</p>}

              {monthlyData.length > 0 ? (
                <MonthlySection data={monthlyData} />
              ) : (
                <p className="status-message">No monthly data</p>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
