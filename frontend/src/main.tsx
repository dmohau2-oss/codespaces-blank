  <section className="ai-assistant" id="assistant"><div className="ai-intro"><p className="kicker">Your thoughtful co-pilot</p><h2>Meet your<br /><em>AI assistant.</em></h2><p>Turn scattered thoughts into clearer next steps, gentle reflections, and useful study plans while keeping your voice at the center.</p><a href="#assistant-prompt">Try a prompt <span>-&gt;</span></a></div><div className="ai-capabilities"><article><span className="ai-index">01</span><h3>Reflect</h3><p>Find the themes and feelings hiding in your recent signals.</p></article><article><span className="ai-index">02</span><h3>Plan</h3><p>Shape a realistic next step from whatever is on your mind.</p></article><article><span className="ai-index">03</span><h3>Learn</h3><p>Explore study ideas matched to your interests and rhythm.</p></article></div><div className="ai-prompt" id="assistant-prompt"><span className="ai-status"><i /> Assistant ready</span><p>What would you like help making sense of?</p><div className="ai-suggestions"><button type="button">Reflect on my signals</button><button type="button">Build a study plan</button></div></div></section>
import { FormEvent, useEffect, useMemo, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './styles.css';

type Signal = { id: number; note: string; mood: string; createdAt: string; color: string };
const moods = [
  { name: 'Bright', color: '#f6c453' },
  { name: 'Soft', color: '#8ec5a4' },
  { name: 'Electric', color: '#e87359' },
  { name: 'Quiet', color: '#8c9bb8' },
];
const daysAgo = (days: number) => new Date(Date.now() - days * 86400000).toISOString();
const seedSignals: Signal[] = [
  { id: 1, note: 'The barista remembered my order.', mood: 'Bright', createdAt: daysAgo(0), color: '#f6c453' },
  { id: 2, note: 'A song I forgot I loved came back around.', mood: 'Soft', createdAt: daysAgo(1), color: '#8ec5a4' },
  { id: 3, note: 'Finally sent the email I was avoiding.', mood: 'Electric', createdAt: daysAgo(3), color: '#e87359' },
];
const formatDate = (value: string) => new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(value));
const southAfricanUniversities = [
  { name: 'University of Cape Town', short: 'UCT', province: 'Western Cape', focus: 'Research, commerce, law', url: 'https://www.uct.ac.za/' },
  { name: 'University of the Witwatersrand', short: 'Wits', province: 'Gauteng', focus: 'Health, engineering, humanities', url: 'https://www.wits.ac.za/' },
  { name: 'Stellenbosch University', short: 'SU', province: 'Western Cape', focus: 'Science, business, agriculture', url: 'https://www.sun.ac.za/' },
  { name: 'University of Pretoria', short: 'UP', province: 'Gauteng', focus: 'Education, veterinary science, law', url: 'https://www.up.ac.za/' },
  { name: 'University of KwaZulu-Natal', short: 'UKZN', province: 'KwaZulu-Natal', focus: 'Medicine, agriculture, social science', url: 'https://ukzn.ac.za/' },
  { name: 'Rhodes University', short: 'RU', province: 'Eastern Cape', focus: 'Journalism, science, humanities', url: 'https://www.ru.ac.za/' },
  { name: 'University of Johannesburg', short: 'UJ', province: 'Gauteng', focus: 'Technology, design, business', url: 'https://www.uj.ac.za/' },
  { name: 'North-West University', short: 'NWU', province: 'North West', focus: 'Education, law, health science', url: 'https://www.nwu.ac.za/' },
];

function downloadFile(name: string, content: string, type: string) {
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([content], { type }));
  link.download = name;
  link.click();
  URL.revokeObjectURL(link.href);
}

function App() {
  const [signals, setSignals] = useState<Signal[]>(() => {
    const saved = localStorage.getItem('small-signals');
    if (!saved) return seedSignals;
    return (JSON.parse(saved) as Array<Signal & { date?: string }>).map((signal) => ({ ...signal, createdAt: signal.createdAt ?? new Date().toISOString() }));
  });
  const [note, setNote] = useState('');
  const [mood, setMood] = useState(moods[0]);
  const [activeView, setActiveView] = useState<'garden' | 'archive'>('garden');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [filterMood, setFilterMood] = useState('All moods');
  const [shareStatus, setShareStatus] = useState('Share constellation');
  const [reflectionSeed, setReflectionSeed] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOrder, setSortOrder] = useState<'newest' | 'oldest'>('newest');
  const [universityQuery, setUniversityQuery] = useState('');
  useEffect(() => localStorage.setItem('small-signals', JSON.stringify(signals)), [signals]);

  const resetForm = () => { setNote(''); setEditingId(null); setMood(moods[0]); };
  const saveSignal = (event: FormEvent) => {
    event.preventDefault();
    if (!note.trim()) return;
    if (editingId !== null) {
      setSignals((current) => current.map((signal) => signal.id === editingId ? { ...signal, note: note.trim(), mood: mood.name, color: mood.color } : signal));
    } else {
      setSignals((current) => [{ id: Date.now(), note: note.trim(), mood: mood.name, createdAt: new Date().toISOString(), color: mood.color }, ...current]);
    }
    resetForm();
  };
  const editSignal = (signal: Signal) => { setEditingId(signal.id); setNote(signal.note); setMood(moods.find((option) => option.name === signal.mood) ?? moods[0]); setActiveView('garden'); window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }); };
  const deleteSignal = (id: number) => setSignals((current) => current.filter((signal) => signal.id !== id));
  const exportJson = () => downloadFile('small-signals.json', JSON.stringify(signals, null, 2), 'application/json');
  const exportCsv = () => downloadFile('small-signals.csv', ['note,mood,createdAt', ...signals.map((signal) => [signal.note, signal.mood, signal.createdAt].map((value) => `"${value.replace(/"/g, '""')}"`).join(','))].join('\n'), 'text/csv');
  const shareConstellation = async () => {
    const shareUrl = `${window.location.origin}${window.location.pathname}#constellation=${btoa(JSON.stringify(signals))}`;
    try { await navigator.clipboard.writeText(shareUrl); setShareStatus('Link copied'); } catch { setShareStatus('Copy link unavailable'); }
    window.setTimeout(() => setShareStatus('Share constellation'), 2200);
  };
  const filteredSignals = signals
    .filter((signal) => filterMood === 'All moods' || signal.mood === filterMood)
    .filter((signal) => signal.note.toLowerCase().includes(searchTerm.toLowerCase().trim()))
    .sort((first, second) => sortOrder === 'newest'
      ? new Date(second.createdAt).getTime() - new Date(first.createdAt).getTime()
      : new Date(first.createdAt).getTime() - new Date(second.createdAt).getTime());
  const constellation = useMemo(() => signals.slice(0, 12).map((signal, index) => ({ ...signal, left: 8 + ((index * 37 + 11) % 84), top: 10 + ((index * 53 + 7) % 74), size: 7 + ((index * 3) % 7) })), [signals]);
  const reflection = useMemo(() => {
    const readings = [
      'There is more light here than you are giving yourself credit for.',
      'Something small is asking to become a habit.',
      'Your attention keeps returning to the gentle things.',
      'The pattern is not loud, but it is definitely a pattern.',
    ];
    return readings[(signals.length + reflectionSeed) % readings.length];
  }, [reflectionSeed, signals.length]);
  const matchingUniversities = southAfricanUniversities.filter((university) => `${university.name} ${university.province} ${university.focus}`.toLowerCase().includes(universityQuery.toLowerCase().trim()));

  return <main className="shell">
      <div className="personal-header"><div>Daniel Modise</div><span>AI for Assistant</span></div>
      <header className="topbar"><a className="wordmark" href="#top">NORTHSTAR<span>UNIVERSITY</span></a><nav className="nav" aria-label="Main navigation"><button className={activeView === 'garden' ? 'active' : ''} onClick={() => setActiveView('garden')}>The garden</button><button className={activeView === 'archive' ? 'active' : ''} onClick={() => setActiveView('archive')}>Your archive <span className="count">{signals.length}</span></button></nav><div className="profile">SS <span>Sam's space</span></div></header>
    <section className="intro" id="top"><div><p className="kicker">A place for the in-between</p><h1>Notice what<br /><em>moves you.</em></h1><p className="lede">The tiny moments are doing more work than you think. Leave a signal here and see what shape your days take.</p></div><div className="today-note"><span className="sun">*</span><strong>{formatDate(new Date().toISOString())}</strong><span>Good day to look closer.</span></div></section>
    {activeView === 'garden' ? <>
      <section className="garden-layout"><div className="constellation" aria-label="Your signal constellation"><div className="field-label">your constellation <span>{signals.length} signals</span></div>{constellation.map((signal) => <span className="star" key={signal.id} title={signal.note} style={{ left: `${signal.left}%`, top: `${signal.top}%`, width: signal.size, height: signal.size, background: signal.color, boxShadow: `0 0 20px ${signal.color}` }} />)}<div className="axis-label axis-one">small moments</div><div className="axis-label axis-two">big feeling</div><button className="share-button" onClick={() => void shareConstellation()}>{shareStatus} <span>-&gt;</span></button></div>
        <form className="capture" onSubmit={saveSignal}><p className="kicker">{editingId === null ? 'Add to the garden' : 'Shape this signal'}</p><label htmlFor="note">What is glimmering?</label><textarea id="note" value={note} onChange={(event) => setNote(event.target.value)} placeholder="A detail worth keeping..." maxLength={140} /><div className="form-footer"><div className="mood-picker" aria-label="Choose a feeling">{moods.map((option) => <button type="button" className={mood.name === option.name ? 'selected' : ''} key={option.name} onClick={() => setMood(option)}><span style={{ background: option.color }} />{option.name}</button>)}</div><button className="send" type="submit">{editingId === null ? 'Plant it' : 'Save changes'} <span>-&gt;</span></button>{editingId !== null && <button className="cancel" type="button" onClick={resetForm}>Cancel editing</button>}</div></form>
      </section>
      <section className="bottom-grid"><div className="recent panel"><div className="section-heading"><h2>Recent signals</h2><button onClick={() => setActiveView('archive')}>See all -&gt;</button></div>{signals.slice(0, 3).map((signal) => <article className="signal-row" key={signal.id}><span className="dot" style={{ background: signal.color }} /><div><p>{signal.note}</p><small>{signal.mood} <span>/</span> {formatDate(signal.createdAt)}</small></div></article>)}</div><div className="rhythm panel"><div className="section-heading"><h2>Your rhythm</h2><span className="period">this month</span></div><div className="rhythm-number">{Math.min(signals.length + 2, 12)}<span> days noticing</span></div><div className="bars">{[3, 5, 4, 7, 6, 9, 8, 10, 7, 11, 9, 12, 10, 13].map((height, index) => <i key={index} style={{ height: `${height * 4}px` }} />)}</div><p className="rhythm-caption">A little attention, every day, adds up.</p></div><div className="weather panel"><div className="section-heading"><h2>Signal weather</h2><span className="period">a reading</span></div><div className="weather-mark">*</div><p className="reflection">{reflection}</p><button className="refresh-reading" onClick={() => setReflectionSeed((current) => current + 1)}>Read the sky again -&gt;</button></div></section>
    </> : <section className="archive panel"><div className="section-heading"><h2>Everything you noticed</h2><span className="period">{filteredSignals.length} shown</span></div><div className="archive-tools"><input aria-label="Search signals" placeholder="Search your signals..." value={searchTerm} onChange={(event) => setSearchTerm(event.target.value)} /><select aria-label="Filter by mood" value={filterMood} onChange={(event) => setFilterMood(event.target.value)}><option>All moods</option>{moods.map((option) => <option key={option.name}>{option.name}</option>)}</select><select aria-label="Sort signals" value={sortOrder} onChange={(event) => setSortOrder(event.target.value as 'newest' | 'oldest')}><option value="newest">Newest first</option><option value="oldest">Oldest first</option></select><div><button onClick={exportJson}>Export JSON</button><button onClick={exportCsv}>Export CSV</button></div></div>{filteredSignals.length ? filteredSignals.map((signal) => <article className="signal-row archive-row" key={signal.id}><span className="dot" style={{ background: signal.color }} /><div><p>{signal.note}</p><small>{signal.mood} <span>/</span> {formatDate(signal.createdAt)}</small></div><div className="row-actions"><button onClick={() => editSignal(signal)} aria-label={`Edit ${signal.note}`}>Edit</button><button onClick={() => deleteSignal(signal.id)} aria-label={`Delete ${signal.note}`}>Delete</button></div></article>) : <p className="no-results">Nothing matches that search yet.</p>}</section>}
    <section className="sa-universities" id="south-africa"><div className="section-heading"><div><p className="kicker">Study closer to home</p><h2>South Africa's universities</h2></div><span className="period">{matchingUniversities.length} of {southAfricanUniversities.length}</span></div><div className="university-tools"><input aria-label="Search South African universities" placeholder="Search by university, province, or subject" value={universityQuery} onChange={(event) => setUniversityQuery(event.target.value)} /><span>Explore the places shaping what comes next.</span></div><div className="university-grid">{matchingUniversities.map((university, index) => <article className="university-card" key={university.short}><span className="university-number">0{index + 1}</span><div className="university-monogram">{university.short}</div><h3>{university.name}</h3><p>{university.province}</p><small>{university.focus}</small><a href={university.url} target="_blank" rel="noreferrer">Visit university <span>↗</span></a></article>)}</div>{matchingUniversities.length === 0 && <p className="university-empty">No universities match that search.</p>}</section>
    <footer><a className="wordmark" href="#top">NORTHSTAR<span>UNIVERSITY</span></a><span>© 2026 Northstar University</span><span>Made for what comes next.</span></footer>
  </main>;
}
ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
