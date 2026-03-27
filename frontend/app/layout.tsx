import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Readiness Dashboard',
  description: 'Simple readiness dashboard for Strava-based analytics',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
