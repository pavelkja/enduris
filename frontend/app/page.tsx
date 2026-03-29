import Link from 'next/link';

export default function HomePage() {
  return (
    <main>
      <h1>Enduris Frontend</h1>
      <p>This MVP includes the dashboard page.</p>
      <p>
        Open <Link href="/dashboard">/dashboard</Link> to view the data.
      </p>
    </main>
  );
}
