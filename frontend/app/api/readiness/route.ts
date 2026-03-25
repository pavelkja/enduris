import { NextRequest, NextResponse } from 'next/server';

function toAbsoluteUrl(input: string): string {
  if (/^https?:\/\//i.test(input)) {
    return input;
  }

  return `http://${input}`;
}

function buildReadinessEndpoint(baseUrl: string, userId: string, sportType: string): string {
  const normalizedBase = toAbsoluteUrl(baseUrl.trim());
  const base = new URL(normalizedBase);

  const endpoint = base.pathname.endsWith('/dashboard/readiness')
    ? new URL(base.toString())
    : new URL('/api/dashboard/readiness', `${base.origin}/`);

  endpoint.searchParams.set('user_id', userId);
  endpoint.searchParams.set('sport_type', sportType);

  return endpoint.toString();
}

const BACKEND_BASE_URL =
  process.env.BACKEND_API_URL ?? process.env.READINESS_API_URL ?? 'http://localhost:8000/api';

export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;
  const userId = params.get('user_id') ?? process.env.USER_ID;
  const sportType = params.get('sport_type') ?? process.env.SPORT_TYPE;

  if (!userId || !sportType) {
    return NextResponse.json(
      {
        error: 'Missing required query params for readiness endpoint.',
        hint: 'Use /?user_id=<USER_ID>&sport_type=<SPORT_TYPE> or set USER_ID and SPORT_TYPE env vars.',
      },
      { status: 400 },
    );
  }

  let endpoint: string;
  try {
    endpoint = buildReadinessEndpoint(BACKEND_BASE_URL, userId, sportType);
  } catch (error) {
    return NextResponse.json(
      {
        error: 'Invalid backend URL configuration.',
        detail: String(error),
      },
      { status: 500 },
    );
  }

   try {

     const response = await fetch(endpoint, { cache: 'no-store' });
     const text = await response.text();

     if (!response.ok) {

       return NextResponse.json({ error: text || 'Backend response was not OK' }, { status: response.status });
       }

     try {
           return NextResponse.json(JSON.parse(text));
         } catch (error) {
           return NextResponse.json(
             { error: 'Backend returned non-JSON response.', detail: String(error), raw: text },
             { status: 502 },
           );
         }
       } catch (error) {
         return NextResponse.json({ error: 'Failed to fetch backend readiness data', detail: String(error) }, { status: 502 });
       }
     }
