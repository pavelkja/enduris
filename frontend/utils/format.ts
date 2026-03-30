export function formatTime(seconds?: number | null) {
  if (!seconds) return '0h';

  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);

  return `${h}h ${m}m`;
}

export function formatDistance(meters?: number | null) {
  if (!meters) return '0 km';

  return `${(meters / 1000).toFixed(1)} km`;
}

export function formatElevation(meters?: number | null) {
  if (!meters) return '0 m';

  return `${Math.round(meters)} m`;
}

export function formatHR(hr?: number | null) {
  if (!hr) return '-';

  return `${Math.round(hr)} bpm`;
}
