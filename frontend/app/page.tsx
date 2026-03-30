import Link from 'next/link';

export default function HomePage() {
  return (
    <main className="page-content">
      <div className="container">
        <section className="section-card">
          <h1 className="section-title">Enduris Frontend</h1>
          <p className="status-message">This MVP includes the dashboard page.</p>
          <p className="status-message">
            Open <Link href="/dashboard" style={{ color: 'var(--color-primary)', fontWeight: 600 }}>/dashboard</Link> to view your metrics.
          </p>
        </section>
      </div>
    </main>
  );
}
