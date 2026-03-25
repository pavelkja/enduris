import { mockReadiness } from '@/lib/mockReadiness';
import { normalizeReadiness } from '@/lib/readiness';
import { NextResponse } from 'next/server';

const BACKEND_URL = process.env.READINESS_API_URL ?? 'http://localhost:8000/api/readiness';

export async function GET() {
  try {
    const response = await fetch(BACKEND_URL, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error('Backend response was not OK');
    }

    const payload = await response.json();
    return NextResponse.json(normalizeReadiness(payload));
  } catch {
    return NextResponse.json(mockReadiness);
  }
}
