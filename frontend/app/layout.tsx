import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Enduris Dashboard',
  description: 'Frontend dashboard for Enduris'
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
