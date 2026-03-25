type DeviationInsight = {
  state: 'above' | 'normal' | 'below';
  today: number;
  baseline: number;
  deviation: number;
};

const fallbackInsight: DeviationInsight = {
  state: 'normal',
  today: 0,
  baseline: 0,
  deviation: 0,
};

function getHeadline(state: DeviationInsight['state']) {
  if (state === 'above') {
    return 'Today’s performance is above your usual level.';
  }

  if (state === 'below') {
    return 'Today’s performance is below your usual level.';
  }

  return 'Today’s performance is within your normal range.';
}

const BACKEND_URL = process.env.BACKEND_API_URL ?? 'http://localhost:8000/api';
const USER_ID = process.env.DEMO_USER_ID ?? '00000000-0000-0000-0000-000000000001';

async function getInsight(): Promise<DeviationInsight> {
  try {
    const response = await fetch(`${BACKEND_URL}/insight/deviation?user_id=${USER_ID}`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Deviation API unavailable');
    }

    return (await response.json()) as DeviationInsight;
  } catch {
    return fallbackInsight;
  }
}

export default async function HomePage() {
  const insight = await getInsight();
  const deviationPercent = Math.round(insight.deviation * 100);

  
  return (
      <main className="mx-auto max-w-2xl px-4 py-10 sm:px-6">
        
      <header>
        <h1 className="text-2xl font-semibold text-slate-900 sm:text-3xl">Main insight</h1>
      </header>

        <div className="mt-6 rounded-2xl bg-white p-6 shadow-sm">
          <h2 className="text-xl font-medium text-slate-900">{getHeadline(insight.state)}</h2>
          <p className="mt-2 text-sm text-slate-600">Compared to your last 10 activities.</p>
          <p className="mt-1 text-xs text-slate-500">
            Deviation: {deviationPercent > 0 ? '+' : ''}
            {deviationPercent}%
          </p>
      </div>
    </main>
  );
}
