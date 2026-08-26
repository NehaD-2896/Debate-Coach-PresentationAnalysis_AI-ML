import React, { useEffect, useRef, useState } from 'react';
import { CheckCircle2, FileText, Mic, Square, Upload, Loader2, RotateCcw, Sparkles, Gauge, MessageSquareText, Presentation, ShieldCheck } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8010';

function ScoreRing({ label, value }) {
  const safe = Math.max(0, Math.min(100, Number(value ?? 0)));
  const r = 37;
  const c = 2 * Math.PI * r;
  const offset = c - (safe / 100) * c;
  return (
    <div className="score-ring-card">
      <div className="ring-wrap">
        <svg width="104" height="104" viewBox="0 0 104 104">
          <circle cx="52" cy="52" r={r} className="ring-bg" />
          <circle cx="52" cy="52" r={r} className="ring-value" strokeDasharray={c} strokeDashoffset={offset} />
        </svg>
        <span className="ring-number">{Math.round(safe)}</span>
      </div>
      <div className="ring-label">{label}</div>
    </div>
  );
}

function App() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('idle');
  const [seconds, setSeconds] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
  const startedAtRef = useRef(null);
  const timerRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => () => {
    clearInterval(timerRef.current);
    streamRef.current?.getTracks().forEach(t => t.stop());
  }, []);

  const selectFile = (f) => {
    if (!f) return;
    const ok = /\.(pptx|pdf)$/i.test(f.name);
    if (!ok) {
      setError('Please upload a PPTX or PDF presentation.');
      return;
    }
    setFile(f);
    setResult(null);
    setError('');
  };

  const startRecording = async () => {
    if (!file) {
      setError('Upload your presentation first.');
      return;
    }
    setError('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const recorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      chunksRef.current = [];
      recorder.ondataavailable = e => { if (e.data.size > 0) chunksRef.current.push(e.data); };
      recorder.onstop = submitRecording;
      mediaRecorderRef.current = recorder;
      startedAtRef.current = Date.now();
      setSeconds(0);
      setStatus('recording');
      recorder.start();
      timerRef.current = setInterval(() => {
        setSeconds(Math.floor((Date.now() - startedAtRef.current) / 1000));
      }, 250);
    } catch (e) {
      setError('Microphone access is required. Please allow microphone access in your browser.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === 'recording') mediaRecorderRef.current.stop();
  };

  const submitRecording = async () => {
    clearInterval(timerRef.current);
    streamRef.current?.getTracks().forEach(t => t.stop());
    const duration = Math.max(0.1, (Date.now() - startedAtRef.current) / 1000);
    const audioBlob = new Blob(chunksRef.current, { type: 'audio/webm' });
    setStatus('analyzing');
    try {
      const form = new FormData();
      form.append('document', file, file.name);
      form.append('audio', audioBlob, 'presentation.webm');
      form.append('duration_seconds', String(duration));
      const res = await fetch(`${API_BASE}/api/v1/presentation/analyze-full`, { method: 'POST', body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Presentation analysis failed.');
      setResult(data);
      setStatus('complete');
    } catch (e) {
      setError(e.message || 'Could not analyze the presentation.');
      setStatus('idle');
    }
  };

  const reset = () => {
    setResult(null); setError(''); setStatus('idle'); setSeconds(0); setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const fmt = s => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  const delivery = result?.delivery_metrics;
  const metrics = result?.presentation_metrics;
  const content = result?.content_review;

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand"><div className="brand-icon"><Sparkles size={19}/></div><div><strong>Debate Coach</strong><span>Presentation Intelligence</span></div></div>
        <div className="status-pill"><span className="status-dot"/> AI Analysis Engine</div>
      </header>

      <main className="page">
        <section className="hero">
          <div className="eyebrow"><Presentation size={15}/> Presentation Analysis Engine</div>
          <h1>Present naturally.<br/><span>Get intelligent feedback.</span></h1>
          <p>Upload your slides, present them out loud, and receive one combined analysis of your speech delivery and presentation content.</p>
        </section>

        {!result && (
          <section className="workspace">
            <div className="panel upload-panel">
              <div className="step-title"><span>01</span><div><h2>Upload your presentation</h2><p>Use the PPTX or PDF you will present.</p></div></div>
              <input ref={fileInputRef} type="file" accept=".pptx,.pdf" hidden onChange={e => selectFile(e.target.files?.[0])}/>
              <button className={`dropzone ${file ? 'selected' : ''}`} onClick={() => fileInputRef.current?.click()}>
                <div className="drop-icon">{file ? <CheckCircle2/> : <Upload/>}</div>
                <div><strong>{file ? file.name : 'Choose your PPTX or PDF'}</strong><small>{file ? `${(file.size / 1024 / 1024).toFixed(1)} MB · Ready to present` : 'Click to browse your files'}</small></div>
              </button>
            </div>

            <div className="panel record-panel">
              <div className="step-title"><span>02</span><div><h2>Present it out loud</h2><p>Your browser records the microphone directly — no manual audio file or duration entry.</p></div></div>
              {status === 'idle' && <button className="record-button" disabled={!file} onClick={startRecording}><span className="mic"><Mic size={21}/></span>Start presenting</button>}
              {status === 'recording' && <div className="recording-state"><div className="live"><span className="pulse"/> Recording <strong>{fmt(seconds)}</strong></div><button className="stop-button" onClick={stopRecording}><Square size={17}/> Stop & analyze</button></div>}
              {status === 'analyzing' && <div className="analyzing"><Loader2 className="spin"/><div><strong>Analyzing your presentation...</strong><span>Transcribing speech and evaluating delivery + content.</span></div></div>}
              {error && <div className="error-box">{error}</div>}
              {status === 'complete' && <div className="complete-box"><CheckCircle2/> Analysis complete.</div>}
            </div>
          </section>
        )}

        {result && (
          <section className="results">
            <div className="result-header"><div><div className="eyebrow"><ShieldCheck size={15}/> Analysis complete</div><h2>{result.filename}</h2><p>{result.slide_count} slides/pages · {Math.round((result.presentation_metrics?.words_per_minute || 0))} WPM · {result.presentation_metrics?.pace_status} · {result.analysis_mode === 'advanced-llm' ? `Groq AI · ${result.llm_model || 'configured model'}` : 'Deterministic fallback'}</p></div><button className="secondary-button" onClick={reset}><RotateCcw size={16}/> New presentation</button></div>

            <div className="panel delivery-card">
              <div className="section-heading"><div><span className="section-kicker">DELIVERY</span><h3>How you presented</h3></div><div className="mini-stat"><Gauge size={17}/><span>{metrics?.words_per_minute ?? '—'} WPM</span></div></div>
              <div className="rings"><ScoreRing label="Clarity" value={delivery?.clarity_score}/><ScoreRing label="Confidence" value={delivery?.confidence_score}/><ScoreRing label="Engagement" value={delivery?.engagement_score}/><ScoreRing label="Pace" value={metrics?.pace_status === 'Optimal' ? 90 : metrics?.pace_status === 'Too Fast' ? 65 : 60}/></div>
              <div className="delivery-meta"><span><b>{metrics?.filler_word_count ?? 0}</b> filler words</span><span>•</span><span>{metrics?.pace_status || 'N/A'}</span></div>
              {delivery?.overall_feedback && <div className="feedback"><MessageSquareText size={17}/><p>{delivery.overall_feedback}</p></div>}
            </div>

            <div className="panel content-card">
              <div className="section-heading"><div><span className="section-kicker">CONTENT</span><h3>What was in your presentation</h3></div></div>
              <div className="content-grid">{[['Structure',content?.structure_score],['Clarity',content?.clarity_score],['Claim Support',content?.claim_support_score],['Flow',content?.flow_score]].map(([label,value]) => <div className="metric-tile" key={label}><span>{label}</span><strong>{Math.round(value ?? 0)}%</strong><div className="bar"><i style={{width:`${Math.max(0,Math.min(100,Number(value ?? 0)))}%`}}/></div></div>)}</div>
              {content?.overall_content_feedback && <p className="content-feedback">{content.overall_content_feedback}</p>}
              {content?.strengths?.length > 0 && <div className="content-feedback"><strong>Strengths:</strong> {content.strengths.join(' · ')}</div>}
              {content?.improvement_actions?.length > 0 && <div className="content-feedback"><strong>Improve next:</strong> {content.improvement_actions.join(' · ')}</div>}
              {content?.slide_feedback?.length > 0 && <div className="slide-feedback"><h4>Per-slide feedback</h4>{content.slide_feedback.map((s,i)=><div className="slide-row" key={i}><b>Slide {s.slide_number}</b><span><strong>Takeaway:</strong> {s.takeaway || 'Not available'}<br/><strong>Support:</strong> {s.supporting_detail || 'No explicit supporting detail found in extracted text.'}<br/><strong>Feedback:</strong> {s.feedback}{s.presentation_alignment ? <><br/><strong>Alignment:</strong> {s.presentation_alignment}</> : null}</span></div>)}</div>}
            </div>

            <div className="panel transcript-card"><div className="section-heading"><div><span className="section-kicker">TRANSCRIPT</span><h3>What the engine heard</h3></div></div><p>{result.transcript || 'No transcript available.'}</p></div>
          </section>
        )}

        {!result && <div className="privacy-note"><ShieldCheck size={16}/><span>Your browser records only when you press Start. The recording is sent to the analysis engine when you stop.</span></div>}
      </main>
    </div>
  );
}

export default App;
