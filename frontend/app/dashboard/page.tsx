'use client';

import { useEffect, useState } from 'react';
import MonthlySection from '@/components/MonthlySection';
import SportSelector from '@/components/SportSelector';
import YTDSection from '@/components/YTDSection';

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

const baseUrl = 'https://api.enduris.app';
const userId = 'b506b832-76f2-48f2-b1a1-e00ccef8b988';

export default function DashboardPage() {
  const [sport, setSport] = useState('cycling_overall');
  const [ytdData, setYtdData] = useState<YTDData[]>([]);
  const [monthlyData, setMonthlyData] = useState<MonthlyData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDashboardData() {
      setLoading(true);
      setError(null);

      try {
        const ytdUrl = `${baseUrl}/api/dashboard/ytd?user_id=${userId}&sport=${sport}`;
        const monthsUrl = `${baseUrl}/api/dashboard/months?user_id=${userId}&sport=${sport}`;

        const [ytdResponse, monthsResponse] = await Promise.all([
          fetch(ytdUrl),
          fetch(monthsUrl),
        ]);

        if (!ytdResponse.ok || !monthsResponse.ok) {
          throw new Error('Request failed');
        }

        const ytdJson = await ytdResponse.json();
        const monthsJson = await monthsResponse.json();

        // ✅ správně: pole
        setYtdData(Array.isArray(ytdJson) ? ytdJson : []);
        setMonthlyData(Array.isArray(monthsJson) ? monthsJson : []);

      } catch (_err) {
        setError('Failed to load data');
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, [sport]);

  return (
    <main>
      <h1>Enduris Dashboard</h1>
      <SportSelector value={sport} onChange={setSport} />

      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}

      {!loading && !error && (
        <>
          {ytdData.length > 0 ? (
            <YTDSection data={ytdData} />
          ) : (
            <p>No YTD data</p>
          )}

          {monthlyData.length > 0 ? (
            <MonthlySection data={monthlyData} />
          ) : (
            <p>No monthly data</p>
          )}
        </>
      )}
    </main>
  );
}
