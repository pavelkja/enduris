'use client';

import { useEffect, useState } from 'react';

export default function HomePage() {
const [data, setData] = useState<unknown>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const userId = params.get('user_id');
    const sportType = params.get('sport_type');

    const endpoint = `/api/readiness?${new URLSearchParams({
      ...(userId ? { user_id: userId } : {}),
      ...(sportType ? { sport_type: sportType } : {}),
    }).toString()}`;

    fetch(endpoint)
    .then(async (res) => {
      const text = await res.text();

      try {
              return JSON.parse(text);
            } catch {
              return { error: 'Response is not valid JSON', status: res.status, raw: text };
            }
          })
          .then(setData)
          .catch((error) => setData({ error: 'Request failed', detail: String(error) }));
      }, []);

  if (!data) return <div>Loading...</div>;

   return <pre>{JSON.stringify(data, null, 2)}</pre>;
  }
