# Frontend Architecture Review

## Scope
This document reviews the `frontend/` folder structure, component responsibilities, and notable weak spots that are good candidates for improvement.

## Folder Structure and Responsibilities

- `app/`
  - `layout.tsx`: Root HTML shell and metadata.
  - `page.tsx`: Main dashboard page, data loading orchestration, and composition of dashboard components.
  - `api/readiness/route.ts`: Server route that proxies backend readiness data with fallback behavior.
  - `globals.css`: Global visual baseline.
- `components/`
  - `ReadinessScore.tsx`: Primary KPI card for score + status.
  - `SyncStatus.tsx`: Data synchronization state badge.
  - `FactorsList.tsx`: List of major drivers.
  - `InsightBox.tsx`: Human-readable explanation and guidance.
  - `TrendChart.tsx`: Time-series chart for recent readiness trend.
- `config/content.ts`: Centralized UI copy and display labels.
- `types/readiness.ts`: Shared TypeScript contract for readiness payload and enums.
- `lib/`
  - `readiness.ts`: Payload normalization and fallback handling.
  - `mockReadiness.ts`: Local fallback data used by both client and API route.

## Components and Why They Exist

- `ReadinessScore`
  - Provides a quick, high-salience answer to “How ready am I now?” using large numeric value and semantic color.
  - Encapsulates status-to-style mapping so page code stays declarative.
- `SyncStatus`
  - Makes data freshness explicit (syncing/processing/ready/error) to improve trust in the displayed score.
- `FactorsList`
  - Surfaces top drivers behind readiness to avoid a “black-box score” experience.
  - Restricts list to first four factors for compactness and scannability.
- `InsightBox`
  - Converts data into action-oriented narrative (summary/explanation/guidance).
- `TrendChart`
  - Adds short historical context (last ~10 points) so users can detect trend direction, not just current state.

## Key Weak Spots and Suggested Improvements

1. **Duplicate normalization path (client + API) can diverge**
   - `app/page.tsx` fetches `/api/readiness` and normalizes again client-side, while `app/api/readiness/route.ts` already normalizes output.
   - Improvement: normalize in one place only (prefer API route), and make `page.tsx` consume a strongly-typed, already-normalized payload.

2. **Broad silent fallbacks hide operational issues**
   - Both page and API route swallow errors and return mock data without observability.
   - Improvement: add structured logging and include a `data_source` field (`backend` | `mock`) in responses to make degradation visible.

3. **Runtime validation is missing for external payloads**
   - `response.json()` is cast to typed objects without schema validation.
   - Improvement: introduce runtime schema checks (e.g., Zod) before normalization to guard against malformed backend responses.

4. **Type safety gap in factor labels**
   - `factorLabels` uses `Record<string, string>` instead of a tighter key union based on known factor names.
   - Improvement: define `FactorName` union in `types/readiness.ts` and use `Record<FactorName, string>`.

5. **Accessibility and internationalization are only partially addressed**
   - Cards and chart render well visually, but chart tooltip/axes semantics and color-only status signaling may be insufficient.
   - Improvement: add explicit ARIA descriptions, non-color cues (icons/text), and prepare content dictionary for i18n.

6. **Data-fetch strategy is client-only and limits SSR benefits**
   - `page.tsx` is `'use client'` and fetches after mount, which can cause layout shift and slower first contentful render.
   - Improvement: move primary fetch to server component or route handler + React Server Components, then hydrate interactive parts.

7. **Trend/date formatting is simplistic**
   - Chart label truncates date string by slicing (`YYYY-MM-DD` -> `MM-DD`), which assumes fixed format.
   - Improvement: parse date safely and format via `Intl.DateTimeFormat`.

8. **Testing coverage appears absent in `frontend/`**
   - No unit/component tests found for normalization, API route behavior, or rendering states.
   - Improvement: add tests for normalization edge cases, fallback logic, and component rendering for each status.

## Prioritized Next Steps

1. Add schema validation + source attribution in `/api/readiness` response.
2. Remove duplicate normalization from `page.tsx` and rely on server-normalized shape.
3. Strengthen type contracts (`FactorName`, stricter maps).
4. Add minimal test suite for `normalizeReadiness` and key components.
5. Improve accessibility cues for status and chart semantics.
