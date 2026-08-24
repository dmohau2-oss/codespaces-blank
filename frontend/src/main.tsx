import React, { useEffect, useMemo, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

type DashboardSummary = {
  row_count: number;
  total: number;
  average: number;
  min: number;
  max: number;
  median: number;
  stddev: number;
  categories: string[];
};

type DashboardPayload = {
  summary: DashboardSummary;
  rows: Array<Record<string, string | number>>;
  categories: string[];
};

type ChartPoint = {
  label: string;
  value: number;
};

const dashboardEndpoint = import.meta.env.DEV ? '/api/dashboard' : '/dashboard';

const formatNumber = (value: number, digits = 2) => new Intl.NumberFormat('en-US', {
  maximumFractionDigits: digits,
  minimumFractionDigits: digits,
}).format(value);

function BarChart({ data }: { data: ChartPoint[] }) {
  const maxValue = Math.max(...data.map((item) => item.value), 1);

  return (
    <svg viewBox="0 0 420 250" className="chart-svg" role="img" aria-label="Category chart">
      <defs>
        <linearGradient id="barGradient" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor="#7dd3fc" />
          <stop offset="100%" stopColor="#4f46e5" />
        </linearGradient>
      </defs>
      {data.map((item, index) => {
        const barWidth = 42;
        const gap = 22;
        const x = 36 + index * (barWidth + gap);
        const height = (item.value / maxValue) * 150;
        const y = 190 - height;

        return (
          <g key={item.label}>
            <rect x={x} y={y} width={barWidth} height={height} rx={8} className="chart-bar" />
            <text x={x + barWidth / 2} y={220} textAnchor="middle" className="chart-label">{item.label}</text>
            <text x={x + barWidth / 2} y={y - 8} textAnchor="middle" className="chart-value">{formatNumber(item.value, 1)}</text>
          </g>
        );
      })}
    </svg>
  );
}

function TrendChart({ data }: { data: ChartPoint[] }) {
  const maxValue = Math.max(...data.map((item) => item.value), 1);
  const minValue = Math.min(...data.map((item) => item.value), 0);
  const width = 420;
  const height = 220;
  const padding = 28;

  const points = data
    .map((item, index) => {
      const x = padding + (index * (width - padding * 2)) / Math.max(data.length - 1, 1);
      const y = height - padding - ((item.value - minValue) / Math.max(maxValue - minValue || 1, 1)) * (height - padding * 2);
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="chart-svg" role="img" aria-label="Value trend chart">
      <polyline points={points} className="trend-line" />
      {data.map((item, index) => {
        const x = padding + (index * (width - padding * 2)) / Math.max(data.length - 1, 1);
        const y = height - padding - ((item.value - minValue) / Math.max(maxValue - minValue || 1, 1)) * (height - padding * 2);
        return (
          <g key={`${item.label}-${index}`}>
            <circle cx={x} cy={y} r={4} className="trend-dot" />
            <text x={x} y={height - 8} textAnchor="middle" className="chart-label small">{item.label}</text>
          </g>
        );
      })}
    </svg>
  );
}

function App() {
  const [dashboard, setDashboard] = useState<DashboardPayload | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [dateFrom, setDateFrom] = useState<string>('');
  const [dateTo, setDateTo] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadDashboard = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams();
      if (categoryFilter !== 'all') params.set('category', categoryFilter);
      if (dateFrom) params.set('date_from', dateFrom);
      if (dateTo) params.set('date_to', dateTo);

      const response = await fetch(`${dashboardEndpoint}?${params.toString()}`);
      if (!response.ok) {
        throw new Error('Unable to load ETL dashboard data from the backend.');
      }

      const payload = (await response.json()) as DashboardPayload;
      setDashboard(payload);
    } catch (loadError) {
      setError(loadError instanceof Error ? loadError.message : 'Unable to load ETL dashboard data.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadDashboard();
  }, [categoryFilter, dateFrom, dateTo]);

  const categoryData = useMemo(() => {
    if (!dashboard?.rows?.length) return [] as ChartPoint[];

    const totals = new Map<string, number>();
    dashboard.rows.forEach((row) => {
      const category = String(row.category ?? 'Unassigned');
      totals.set(category, (totals.get(category) ?? 0) + Number(row.value ?? 0));
    });

    return Array.from(totals.entries()).map(([label, value]) => ({ label, value }));
  }, [dashboard]);

  const trendData = useMemo(() => {
    if (!dashboard?.rows?.length) return [] as ChartPoint[];
    return dashboard.rows.map((row, index) => ({
      label: String(row.name ?? `Row ${index + 1}`),
      value: Number(row.value ?? 0),
    }));
  }, [dashboard]);

  const summary = dashboard?.summary;

  const metrics = summary ? [
    { label: 'Rows processed', value: String(summary.row_count), change: 'filtered view' },
    { label: 'Value total', value: formatNumber(summary.total), change: 'ETL total' },
    { label: 'Average', value: formatNumber(summary.average), change: 'per record' },
    { label: 'Std dev', value: formatNumber(summary.stddev), change: 'variance' },
  ] : [];

  const categories = dashboard?.categories ?? ['A', 'B', 'C'];

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">DataFlow</div>
        <nav>
          <button className="nav-item active">Overview</button>
          <button className="nav-item">Pipelines</button>
          <button className="nav-item">Reports</button>
          <button className="nav-item">Settings</button>
        </nav>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="eyebrow">Operations</p>
            <h1>ETL pipeline overview</h1>
          </div>
          <button className="primary-button" onClick={() => void loadDashboard()}>Refresh data</button>
        </header>

        <section className="toolbar panel">
          <label>
            <span>Category</span>
            <select value={categoryFilter} onChange={(event) => setCategoryFilter(event.target.value)}>
              <option value="all">All categories</option>
              {categories.map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </label>

          <label>
            <span>From</span>
            <input type="date" value={dateFrom} onChange={(event) => setDateFrom(event.target.value)} />
          </label>

          <label>
            <span>To</span>
            <input type="date" value={dateTo} onChange={(event) => setDateTo(event.target.value)} />
          </label>
        </section>

        {error ? (
          <section className="panel warning-panel">
            <h2>Data source unavailable</h2>
            <p>{error}</p>
          </section>
        ) : null}

        {loading && !dashboard ? (
          <section className="panel empty-state">Loading ETL metrics...</section>
        ) : null}

        <section className="stats-grid">
          {metrics.map((metric) => (
            <article className="stat-card" key={metric.label}>
              <span>{metric.label}</span>
              <strong>{metric.value}</strong>
              <small>{metric.change}</small>
            </article>
          ))}
        </section>

        <section className="content-grid">
          <div className="panel">
            <div className="panel-header">
              <h2>Category totals</h2>
              <span className="chip success">{summary ? `Rows: ${summary.row_count}` : 'Loading...'}</span>
            </div>
            {categoryData.length ? <BarChart data={categoryData} /> : <div className="empty-state">No results for this filter.</div>}
          </div>

          <div className="panel">
            <div className="panel-header">
              <h2>Record values</h2>
              <span className="chip neutral">Live summary</span>
            </div>
            {trendData.length ? <TrendChart data={trendData} /> : <div className="empty-state">No processed rows available.</div>}
          </div>
        </section>

        <section className="panel insight-panel">
          <div className="panel-header">
            <h2>Pipeline insight</h2>
            <span className="chip neutral">API-backed</span>
          </div>
          {summary ? (
            <div className="insight-grid">
              <div>
                <span className="label">Minimum</span>
                <strong>{formatNumber(summary.min)}</strong>
              </div>
              <div>
                <span className="label">Maximum</span>
                <strong>{formatNumber(summary.max)}</strong>
              </div>
              <div>
                <span className="label">Median</span>
                <strong>{formatNumber(summary.median)}</strong>
              </div>
              <div>
                <span className="label">Categories</span>
                <strong>{summary.categories.join(', ') || 'None'}</strong>
              </div>
            </div>
          ) : (
            <div className="empty-state">Loading ETL metrics...</div>
          )}
        </section>
      </main>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
