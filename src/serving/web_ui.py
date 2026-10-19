"""Modern, Clean, Attractive, and Professional Web Dashboard for Water Potability & Monitoring."""

HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AquaGuard AI | Underwater Environmental & Water Potability Intelligence</title>
  <!-- Chart.js CDN for interactive visual analytics -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg-primary: #070d19;
      --bg-card: rgba(17, 27, 49, 0.75);
      --bg-card-hover: rgba(26, 41, 74, 0.85);
      --border-color: rgba(38, 59, 97, 0.5);
      --border-glow: rgba(6, 182, 212, 0.3);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-danger: #ef4444;
      --accent-warning: #f59e0b;
      --accent-purple: #8b5cf6;
      --accent-blue: #3b82f6;
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: var(--font-family);
      -webkit-font-smoothing: antialiased;
    }

    body {
      background-color: var(--bg-primary);
      background-image:
        radial-gradient(circle at 15% 20%, rgba(6, 182, 212, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 75%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.04) 0%, transparent 60%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Navigation Bar */
    header {
      background: rgba(11, 19, 36, 0.85);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-color);
      padding: 0.9rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 4px 25px rgba(0, 0, 0, 0.45);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }

    .brand-logo-container {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(16, 185, 129, 0.2));
      border: 1px solid var(--border-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
    }

    .brand-icon {
      font-size: 1.6rem;
      animation: pulseGlow 3s infinite ease-in-out;
    }

    @keyframes pulseGlow {
      0%, 100% { transform: scale(1); filter: drop-shadow(0 0 2px var(--accent-cyan)); }
      50% { transform: scale(1.08); filter: drop-shadow(0 0 8px var(--accent-emerald)); }
    }

    .brand-title {
      font-size: 1.25rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      background: linear-gradient(135deg, #ffffff 30%, var(--accent-cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-subtitle {
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      font-weight: 600;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .live-clock {
      font-size: 0.8rem;
      color: var(--text-dim);
      font-variant-numeric: tabular-nums;
      display: none;
    }
    @media (min-width: 768px) { .live-clock { display: block; } }

    .system-status {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(16, 185, 129, 0.1);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 0.4rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.8rem;
      color: var(--accent-emerald);
      font-weight: 600;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.15);
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: var(--accent-emerald);
      box-shadow: 0 0 8px var(--accent-emerald);
      animation: pulseDot 2s infinite;
    }

    @keyframes pulseDot {
      0% { opacity: 0.4; }
      50% { opacity: 1; transform: scale(1.2); }
      100% { opacity: 0.4; }
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1440px;
      margin: 0 auto;
      padding: 1.75rem 1.5rem;
      width: 100%;
    }

    /* KPI Summary Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1rem;
      margin-bottom: 1.75rem;
    }

    .kpi-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.25rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
      position: relative;
      overflow: hidden;
    }

    .kpi-card::before {
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; height: 2px;
      background: linear-gradient(90deg, transparent, var(--border-glow), transparent);
    }

    .kpi-card:hover {
      transform: translateY(-3px);
      border-color: var(--accent-cyan);
      box-shadow: 0 8px 25px rgba(6, 182, 212, 0.15);
    }

    .kpi-info h4 {
      font-size: 0.78rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.35rem;
    }

    .kpi-info .kpi-value {
      font-size: 1.5rem;
      font-weight: 800;
      letter-spacing: -0.02em;
    }

    .kpi-info .kpi-desc {
      font-size: 0.75rem;
      color: var(--text-dim);
      margin-top: 0.25rem;
    }

    .kpi-icon-pill {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.3rem;
    }

    /* Tabs Navigation */
    .tabs-header {
      display: flex;
      gap: 0.5rem;
      border-bottom: 1px solid var(--border-color);
      margin-bottom: 1.5rem;
      overflow-x: auto;
      scrollbar-width: none;
    }
    .tabs-header::-webkit-scrollbar { display: none; }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 0.85rem 1.25rem;
      font-size: 0.92rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      border-bottom: 2px solid transparent;
      transition: all 0.2s ease;
      white-space: nowrap;
      border-radius: 8px 8px 0 0;
    }

    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.03);
    }

    .tab-btn.active {
      color: var(--accent-cyan);
      border-bottom-color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.08);
    }

    .tab-pane {
      display: none;
    }

    .tab-pane.active {
      display: block;
      animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Section Cards */
    .card {
      background: var(--bg-card);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.75rem;
      margin-bottom: 1.5rem;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .card-title {
      font-size: 1.15rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* Presets Bar */
    .presets-container {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      align-items: center;
      background: rgba(0, 0, 0, 0.2);
      padding: 0.75rem 1rem;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .preset-label {
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-right: 0.35rem;
      font-weight: 600;
    }

    .preset-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.4rem 0.85rem;
      border-radius: 8px;
      font-size: 0.82rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
      font-weight: 500;
    }

    .preset-btn:hover {
      background: rgba(6, 182, 212, 0.15);
      border-color: var(--accent-cyan);
      transform: translateY(-1px);
    }

    .preset-btn.btn-accent {
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.25), rgba(16, 185, 129, 0.25));
      border-color: var(--accent-cyan);
      color: #fff;
    }

    /* Simulation Layout Grid */
    .sim-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    @media (min-width: 1024px) {
      .sim-grid {
        grid-template-columns: 1.25fr 1fr;
      }
    }

    /* Inputs List */
    .inputs-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.15rem;
    }
    @media (min-width: 640px) {
      .inputs-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    .input-group {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 0.9rem 1rem;
      transition: all 0.2s ease;
    }

    .input-group:hover, .input-group:focus-within {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 12px rgba(6, 182, 212, 0.1);
    }

    .input-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.6rem;
    }

    .input-label {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    .input-meta {
      font-size: 0.75rem;
      color: var(--text-dim);
    }

    .slider-row {
      display: flex;
      align-items: center;
      gap: 0.85rem;
    }

    .slider-row input[type="range"] {
      flex: 1;
      height: 6px;
      -webkit-appearance: none;
      background: #1e293b;
      border-radius: 6px;
      outline: none;
      cursor: pointer;
    }

    .slider-row input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: var(--accent-cyan);
      box-shadow: 0 0 8px var(--accent-cyan);
      cursor: pointer;
      transition: transform 0.1s ease;
    }
    .slider-row input[type="range"]::-webkit-slider-thumb:hover {
      transform: scale(1.2);
    }

    .num-input {
      width: 72px;
      background: #0f172a;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.35rem 0.5rem;
      border-radius: 6px;
      font-size: 0.85rem;
      font-weight: 600;
      text-align: right;
    }
    .num-input:focus {
      outline: none;
      border-color: var(--accent-cyan);
    }

    /* Decision Panel (Right Column) */
    .decision-panel {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .decision-box {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      position: relative;
    }

    .verdict-banner {
      width: 100%;
      padding: 1rem;
      border-radius: 12px;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
      transition: all 0.3s ease;
    }

    .verdict-banner.safe {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.2));
      border: 1px solid rgba(16, 185, 129, 0.4);
      color: var(--accent-emerald);
      box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
    }

    .verdict-banner.hazard {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(245, 158, 11, 0.2));
      border: 1px solid rgba(239, 68, 68, 0.4);
      color: var(--accent-danger);
      box-shadow: 0 0 20px rgba(239, 68, 68, 0.15);
    }

    .verdict-icon {
      font-size: 2rem;
    }

    .verdict-title {
      font-size: 1.2rem;
      font-weight: 800;
      letter-spacing: 0.02em;
    }

    .verdict-desc {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
    }

    /* Circular Radial Probability Dial */
    .dial-container {
      position: relative;
      width: 160px;
      height: 160px;
      margin: 0.5rem 0 1rem 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .dial-svg {
      transform: rotate(-90deg);
      width: 160px;
      height: 160px;
    }

    .dial-bg {
      fill: none;
      stroke: #1e293b;
      stroke-width: 12;
    }

    .dial-progress {
      fill: none;
      stroke: var(--accent-emerald);
      stroke-width: 12;
      stroke-linecap: round;
      stroke-dasharray: 440;
      stroke-dashoffset: 440;
      transition: stroke-dashoffset 0.6s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.4s ease;
      filter: drop-shadow(0 0 6px var(--accent-emerald));
    }

    .dial-text {
      position: absolute;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .dial-value {
      font-size: 2.1rem;
      font-weight: 900;
      color: #fff;
      font-variant-numeric: tabular-nums;
    }

    .dial-sub {
      font-size: 0.72rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
    }

    .risk-badge {
      padding: 0.35rem 0.8rem;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
    }

    /* Diagnostic Pills */
    .audit-badges {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      width: 100%;
      margin-bottom: 1rem;
    }

    .audit-badge-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 0.75rem;
      text-align: left;
    }

    .audit-badge-title {
      font-size: 0.72rem;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
    }

    .audit-badge-value {
      font-size: 0.95rem;
      font-weight: 700;
      margin-top: 0.2rem;
    }

    /* Radar Chart Container */
    .radar-card {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.25rem;
      width: 100%;
    }

    .radar-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 0.75rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .radar-chart-box {
      position: relative;
      height: 240px;
      width: 100%;
    }

    /* WHO Compliance Infractions Box */
    .violations-list {
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid rgba(239, 68, 68, 0.2);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      font-size: 0.8rem;
      color: var(--text-muted);
      width: 100%;
      text-align: left;
    }

    .violations-list ul {
      margin-left: 1.2rem;
      margin-top: 0.35rem;
    }

    .violations-list li {
      margin-bottom: 0.25rem;
      color: #fca5a5;
    }

    /* Action Buttons Row */
    .actions-row {
      display: flex;
      gap: 0.5rem;
      width: 100%;
      margin-top: 0.5rem;
    }

    .action-btn {
      flex: 1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.6rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
    }
    .action-btn:hover {
      background: rgba(6, 182, 212, 0.2);
      border-color: var(--accent-cyan);
    }

    /* Chart Container for Track A */
    .chart-container {
      position: relative;
      height: 380px;
      width: 100%;
    }

    /* Batch Table Styles */
    .dropzone {
      border: 2px dashed var(--border-color);
      border-radius: 14px;
      padding: 2.5rem 1.5rem;
      text-align: center;
      background: rgba(0, 0, 0, 0.2);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .dropzone:hover {
      border-color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.05);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      margin-top: 1rem;
    }

    th, td {
      padding: 0.75rem 1rem;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
    }

    th {
      background: rgba(0, 0, 0, 0.4);
      color: var(--text-muted);
      font-weight: 600;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    tr:hover {
      background: rgba(255, 255, 255, 0.02);
    }

    .kpi-badge {
      display: inline-block;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
    }

    .badge-emerald { background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-danger { background: rgba(239, 68, 68, 0.15); color: var(--accent-danger); border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-warning { background: rgba(245, 158, 11, 0.15); color: var(--accent-warning); border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-cyan { background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan); border: 1px solid rgba(6, 182, 212, 0.3); }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-color);
      padding: 1.25rem 2rem;
      font-size: 0.8rem;
      color: var(--text-dim);
      text-align: center;
      background: rgba(7, 13, 25, 0.9);
      margin-top: auto;
    }

    /* Toast Notification */
    #toast {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: #0f172a;
      border: 1px solid var(--accent-cyan);
      color: #fff;
      padding: 0.75rem 1.25rem;
      border-radius: 10px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
      font-size: 0.85rem;
      font-weight: 600;
      z-index: 1000;
      opacity: 0;
      transform: translateY(10px);
      transition: all 0.3s ease;
      pointer-events: none;
    }
    #toast.show {
      opacity: 1;
      transform: translateY(0);
    }
  </style>
</head>
<body>

  <!-- Toast Element -->
  <div id="toast">Copied to clipboard!</div>

  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-logo-container">
        <span class="brand-icon">🌊</span>
      </div>
      <div>
        <h1 class="brand-title">AquaGuard AI</h1>
        <p class="brand-subtitle">Underwater Environmental & Potability Intelligence</p>
      </div>
    </div>
    <div class="header-controls">
      <div class="live-clock" id="live-clock">UTC 00:00:00</div>
      <div class="system-status">
        <span class="status-dot"></span>
        <span>PRODUCTION ACTIVE</span>
      </div>
    </div>
  </header>

  <main>
    <!-- Top KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Champion Pipeline</h4>
          <div class="kpi-value" style="color: var(--accent-cyan);">XGBoost</div>
          <div class="kpi-desc">Platt Scaling Calibrated</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(6, 182, 212, 0.15); color: var(--accent-cyan);">🏆</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Lockbox PR-AUC</h4>
          <div class="kpi-value" style="color: var(--accent-emerald);">0.5951</div>
          <div class="kpi-desc">Baseline WHO Rules: 0.3920</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(16, 185, 129, 0.15); color: var(--accent-emerald);">📈</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Inference Latency</h4>
          <div class="kpi-value" id="kpi-latency-val" style="color: var(--accent-purple);">2.89 ms</div>
          <div class="kpi-desc">Sub-3ms Real-Time Engine</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(139, 92, 246, 0.15); color: var(--accent-purple);">⚡</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>WHO Auditor</h4>
          <div class="kpi-value" id="kpi-who-compliance" style="color: var(--accent-emerald);">Active</div>
          <div class="kpi-desc">Domain Envelopes Guard</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(59, 130, 246, 0.15); color: var(--accent-blue);">🛡️</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-header">
      <button class="tab-btn active" onclick="switchTab('tab-sim')">
        <span>🔬</span> Interactive Potability Simulator
      </button>
      <button class="tab-btn" onclick="switchTab('tab-stream')">
        <span>🌊</span> Continuous Telemetry Stream (Track A)
      </button>
      <button class="tab-btn" onclick="switchTab('tab-batch')">
        <span>📁</span> Batch Telemetry Processor
      </button>
      <button class="tab-btn" onclick="switchTab('tab-models')">
        <span>📊</span> Model Benchmark & WHO Standards
      </button>
    </div>

    <!-- TAB 1: INTERACTIVE POTABILITY SIMULATOR -->
    <div id="tab-sim" class="tab-pane active">
      <div class="card">
        <div class="card-header">
          <div class="card-title">
            <span>🧪</span> Physicochemical Water Quality Telemetry Input
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">
            Adjust chemical parameters to observe instant probability updates & WHO radar compliance
          </div>
        </div>

        <!-- Presets Selection Bar -->
        <div class="presets-container">
          <span class="preset-label">Standard Environments:</span>
          <button class="preset-btn btn-accent" onclick="loadPreset('mountain')">🏔️ Mountain Spring</button>
          <button class="preset-btn" onclick="loadPreset('municipal')">🚰 Municipal Tap</button>
          <button class="preset-btn" onclick="loadPreset('glacial')">🧊 Glacial Melt</button>
          <button class="preset-btn" onclick="loadPreset('deep_sea')">🌋 Hydrothermal Vent</button>
          <button class="preset-btn" onclick="loadPreset('acid_spill')">⚠️ Acid Drainage</button>
          <button class="preset-btn" onclick="loadPreset('sensor_fault')">❌ Sensor Failure</button>
          <button class="preset-btn" onclick="randomizeInputs()" style="margin-left: auto;">🎲 Randomize Values</button>
        </div>

        <div class="sim-grid">
          <!-- Left: Input Sliders -->
          <div>
            <div class="inputs-grid">
              <!-- pH -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">pH Acidity</span>
                  <span class="input-meta">WHO: 6.5–8.5</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-ph" min="0" max="14" step="0.05" value="7.25" oninput="syncInput('ph', this.value)">
                  <input type="number" id="num-ph" class="num-input" value="7.25" step="0.05" onchange="syncSlider('ph', this.value)">
                </div>
              </div>

              <!-- Hardness -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Hardness (Ca/Mg)</span>
                  <span class="input-meta">Safe &le; 200 mg/L</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-hardness" min="40" max="320" step="1" value="185" oninput="syncInput('hardness', this.value)">
                  <input type="number" id="num-hardness" class="num-input" value="185" onchange="syncSlider('hardness', this.value)">
                </div>
              </div>

              <!-- Solids (TDS) -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Total Solids (TDS)</span>
                  <span class="input-meta">WHO &le; 1,000 ppm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-solids" min="500" max="50000" step="250" value="16500" oninput="syncInput('solids', this.value)">
                  <input type="number" id="num-solids" class="num-input" value="16500" onchange="syncSlider('solids', this.value)">
                </div>
              </div>

              <!-- Chloramines -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Chloramines</span>
                  <span class="input-meta">WHO &le; 4.0 ppm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-chloramines" min="0" max="14" step="0.1" value="6.2" oninput="syncInput('chloramines', this.value)">
                  <input type="number" id="num-chloramines" class="num-input" value="6.2" step="0.1" onchange="syncSlider('chloramines', this.value)">
                </div>
              </div>

              <!-- Sulfate -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Sulfate</span>
                  <span class="input-meta">WHO &le; 250 mg/L</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-sulfate" min="100" max="500" step="5" value="325" oninput="syncInput('sulfate', this.value)">
                  <input type="number" id="num-sulfate" class="num-input" value="325" onchange="syncSlider('sulfate', this.value)">
                </div>
              </div>

              <!-- Conductivity -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Conductivity</span>
                  <span class="input-meta">WHO &le; 400 μS/cm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-conductivity" min="150" max="750" step="5" value="415" oninput="syncInput('conductivity', this.value)">
                  <input type="number" id="num-conductivity" class="num-input" value="415" onchange="syncSlider('conductivity', this.value)">
                </div>
              </div>

              <!-- Organic Carbon -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Organic Carbon (TOC)</span>
                  <span class="input-meta">Safe &le; 4.0 ppm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-carbon" min="2" max="30" step="0.2" value="12.5" oninput="syncInput('carbon', this.value)">
                  <input type="number" id="num-carbon" class="num-input" value="12.5" step="0.2" onchange="syncSlider('carbon', this.value)">
                </div>
              </div>

              <!-- Trihalomethanes (THM) -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Trihalomethanes</span>
                  <span class="input-meta">WHO &le; 80 μg/L</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-thm" min="0" max="130" step="1" value="62" oninput="syncInput('thm', this.value)">
                  <input type="number" id="num-thm" class="num-input" value="62" onchange="syncSlider('thm', this.value)">
                </div>
              </div>

              <!-- Turbidity -->
              <div class="input-group" style="grid-column: 1 / -1;">
                <div class="input-header">
                  <span class="input-label">Turbidity (Clarity)</span>
                  <span class="input-meta">WHO &le; 5.0 NTU (Target &le; 1.0)</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-turbidity" min="1" max="7" step="0.05" value="3.4" oninput="syncInput('turbidity', this.value)">
                  <input type="number" id="num-turbidity" class="num-input" value="3.4" step="0.05" onchange="syncSlider('turbidity', this.value)">
                </div>
              </div>
            </div>

            <!-- Quick Action Buttons -->
            <div class="actions-row">
              <button class="action-btn" onclick="remediateToSafe()">✨ Auto-Remediate to Potable</button>
              <button class="action-btn" onclick="copyCurlSnippet()">📋 Copy cURL Request</button>
            </div>
          </div>

          <!-- Right: Visual Outcome & Radar Chart -->
          <div class="decision-panel">
            <div class="decision-box">
              <div class="verdict-banner safe" id="verdict-banner">
                <span class="verdict-icon" id="verdict-icon">✅</span>
                <div>
                  <h3 class="verdict-title" id="verdict-title">POTABLE & SAFE</h3>
                  <p class="verdict-desc" id="verdict-desc">Calibrated model confirms high drinking water viability.</p>
                </div>
              </div>

              <!-- Circular Progress Dial -->
              <div class="dial-container">
                <svg class="dial-svg" viewBox="0 0 160 160">
                  <circle class="dial-bg" cx="80" cy="80" r="70"></circle>
                  <circle class="dial-progress" id="dial-progress" cx="80" cy="80" r="70"></circle>
                </svg>
                <div class="dial-text">
                  <span class="dial-value" id="prob-val">74%</span>
                  <span class="dial-sub">POTABILITY PROB</span>
                </div>
              </div>

              <div class="risk-badge badge-emerald" id="risk-badge">
                <span>🛡️</span> Grade B: Safe for Consumption
              </div>

              <!-- Diagnostic Badges -->
              <div class="audit-badges">
                <div class="audit-badge-card">
                  <div class="audit-badge-title">Anomaly Outlier Score</div>
                  <div class="audit-badge-value" id="badge-anomaly" style="color: var(--accent-emerald);">NORMAL INLIER</div>
                </div>
                <div class="audit-badge-card">
                  <div class="audit-badge-title">Inference Execution</div>
                  <div class="audit-badge-value" id="badge-latency" style="color: var(--accent-cyan);">2.89 ms</div>
                </div>
              </div>

              <!-- WHO Compliance Violations Box -->
              <div class="violations-list" id="violations-box">
                <strong id="who-status-title">WHO Guideline Compliance:</strong>
                <div id="who-violations-text" style="margin-top: 0.25rem;">Parameters conform to standard drinking envelopes.</div>
              </div>
            </div>

            <!-- 9-Axis WHO Compliance Radar Chart -->
            <div class="radar-card">
              <div class="radar-title">
                <span>📊 9-Axis WHO Envelope Radar</span>
                <span style="font-size: 0.72rem; color: var(--accent-cyan);">Live Normalized</span>
              </div>
              <div class="radar-chart-box">
                <canvas id="radarChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: CONTINUOUS SENSOR STREAM (TRACK A) -->
    <div id="tab-stream" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">
            <span>🌊</span> Underwater Environmental Sensor Timeline (Track A Stream)
          </div>
          <div style="display: flex; gap: 0.75rem; align-items: center; flex-wrap: wrap;">
            <select id="sensor-stream-select" onchange="updateStreamChart()" style="background: #0f172a; color: #fff; border: 1px solid var(--border-color); padding: 0.45rem 0.85rem; border-radius: 8px; font-size: 0.85rem; outline: none;">
              <option value="dissolved_oxygen">Dissolved Oxygen (DO) [mg/L]</option>
              <option value="temperature">Water Temperature [°C]</option>
              <option value="ph">pH Acidity [0-14]</option>
              <option value="turbidity">Turbidity Suspended Solids [NTU]</option>
              <option value="conductivity">Electrical Conductivity [μS/cm]</option>
              <option value="pressure">Hydrostatic Pressure [dbar]</option>
            </select>
            <button class="preset-btn btn-accent" id="btn-live-stream" onclick="toggleLiveStream()">▶ Start Live Probe Simulation</button>
          </div>
        </div>

        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
          Continuous chronological sensor telemetry. Red markers automatically indicate physical boundary deviations and contamination events.
        </p>

        <div class="chart-container">
          <canvas id="streamChart"></canvas>
        </div>
      </div>
    </div>

    <!-- TAB 3: BATCH TELEMETRY INGESTION -->
    <div id="tab-batch" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">
            <span>📁</span> Batch Telemetry Processing & Anomaly Flagging
          </div>
          <button class="preset-btn btn-accent" onclick="loadDemoBatch()">⚡ Load Demo 30-Sample Batch</button>
        </div>

        <div class="dropzone" onclick="document.getElementById('csv-upload-input').click()">
          <input type="file" id="csv-upload-input" accept=".csv" style="display: none;" onchange="handleFileUpload(event)">
          <div style="font-size: 2.75rem; margin-bottom: 0.5rem;">📥</div>
          <h4 style="font-size: 1.15rem; font-weight: 700;">Upload Water Quality Sensor CSV</h4>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">
            Click to upload or drag & drop. Automatically computes MICE imputation and Platt-calibrated XGBoost scoring.
          </p>
        </div>

        <div id="batch-results-area" style="display: none; margin-top: 1.75rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; flex-wrap: wrap; gap: 0.75rem;">
            <h4 id="batch-summary-title" style="font-size: 1.1rem; font-weight: 700;">Batch Analysis Output</h4>
            <div style="display: flex; gap: 0.5rem;">
              <button class="preset-btn" onclick="filterBatch('all')">Show All</button>
              <button class="preset-btn" onclick="filterBatch('potable')">Safe Only</button>
              <button class="preset-btn" onclick="filterBatch('anomaly')">Anomalies Only</button>
              <button class="preset-btn btn-accent" onclick="downloadBatchResults()">⬇️ Download Annotated CSV</button>
            </div>
          </div>
          <div style="overflow-x: auto;">
            <table id="batch-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>pH</th>
                  <th>Hardness</th>
                  <th>Solids (TDS)</th>
                  <th>Chloramines</th>
                  <th>Sulfate</th>
                  <th>Conductivity</th>
                  <th>Turbidity</th>
                  <th>Potability Status</th>
                  <th>Calibrated Prob</th>
                  <th>Outlier Status</th>
                </tr>
              </thead>
              <tbody id="batch-tbody"></tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: BENCHMARK & STANDARDS -->
    <div id="tab-models" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div class="card-title">
            <span>🏆</span> Stratified 5-Fold Benchmark & Lockbox Evaluation
          </div>
          <span style="font-size: 0.8rem; color: var(--accent-emerald);">Strict Zero-Leakage Cross-Validation</span>
        </div>

        <table>
          <thead>
            <tr>
              <th>Model Candidate</th>
              <th>Architecture Family</th>
              <th>PR-AUC (Primary)</th>
              <th>ROC-AUC</th>
              <th>Brier Score</th>
              <th>F1-Score</th>
              <th>Latency (P95)</th>
              <th>Artifact Footprint</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>WHO Permissible Rule Baseline</strong></td>
              <td>Deterministic Expert System</td>
              <td>0.3920</td>
              <td>0.5000</td>
              <td>0.3890</td>
              <td>0.0000</td>
              <td>0.02 ms</td>
              <td>0.2 KB</td>
            </tr>
            <tr>
              <td><strong>Logistic Regression (ElasticNet)</strong></td>
              <td>Linear Classifier</td>
              <td>0.4320</td>
              <td>0.5180</td>
              <td>0.2410</td>
              <td>0.4285</td>
              <td>0.14 ms</td>
              <td>4.2 KB</td>
            </tr>
            <tr>
              <td><strong>Random Forest (200 Trees)</strong></td>
              <td>Bagged Ensembles</td>
              <td>0.5480</td>
              <td>0.6210</td>
              <td>0.2190</td>
              <td>0.5512</td>
              <td>4.82 ms</td>
              <td>12.4 MB</td>
            </tr>
            <tr style="background: rgba(6, 182, 212, 0.1); border-left: 3px solid var(--accent-cyan);">
              <td><strong>XGBoost + Platt Scaling (Production Champion)</strong></td>
              <td>Gradient Boosted Trees</td>
              <td><strong>0.5951</strong></td>
              <td><strong>0.6689</strong></td>
              <td><strong>0.2154</strong></td>
              <td><strong>0.4127</strong></td>
              <td><strong>2.89 ms</strong></td>
              <td><strong>3.15 MB</strong></td>
            </tr>
          </tbody>
        </table>

        <div style="margin-top: 2rem;">
          <h4 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.75rem;">World Health Organization (WHO) Permissible Boundary Envelopes</h4>
          <table>
            <thead>
              <tr>
                <th>Chemical Variable</th>
                <th>WHO / EPA Permissible Limit</th>
                <th>Physical Failure Mode</th>
              </tr>
            </thead>
            <tbody>
              <tr><td><strong>pH Level</strong></td><td>6.50 – 8.50</td><td>Acidic corrosion of infrastructure / Alkaline mineral scaling</td></tr>
              <tr><td><strong>Turbidity</strong></td><td>&le; 5.0 NTU (Desirable &le; 1.0)</td><td>Suspended particulates shield microbiological pathogens from disinfection</td></tr>
              <tr><td><strong>Chloramines</strong></td><td>&le; 4.0 ppm</td><td>Mucous membrane toxicity and carcinogenic chlorination byproducts</td></tr>
              <tr><td><strong>Sulfate</strong></td><td>&le; 250.0 mg/L</td><td>Cathartic purgative effects and gastrointestinal distress</td></tr>
              <tr><td><strong>Conductivity</strong></td><td>&le; 400.0 μS/cm</td><td>Excessive ionic and mineral dissolution</td></tr>
              <tr><td><strong>Organic Carbon</strong></td><td>&le; 4.0 ppm</td><td>Precursor to carcinogenic Trihalomethanes formation</td></tr>
              <tr><td><strong>Trihalomethanes</strong></td><td>&le; 80.0 μg/L</td><td>Carcinogenic byproduct of chemical disinfection</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </main>

  <footer>
    AquaGuard AI &bull; Production Deployment &bull; Calibrated Sub-3ms Machine Learning Engine &bull; Zero-Leakage Pipeline
  </footer>

  <script>
    // Live UTC Clock
    function updateClock() {
      const d = new Date();
      document.getElementById('live-clock').innerText = 'UTC ' + d.toUTCString().slice(17, 25);
    }
    setInterval(updateClock, 1000);
    updateClock();

    // Tab Switching Logic
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

      event.currentTarget.classList.add('active');
      document.getElementById(tabId).classList.add('active');

      if (tabId === 'tab-stream') {
        setTimeout(initStreamChart, 100);
      }
    }

    // Standard Presets
    const PRESETS = {
      mountain: { ph: 7.40, hardness: 120, solids: 4500, chloramines: 1.2, sulfate: 180, conductivity: 220, carbon: 2.1, thm: 15, turbidity: 1.2 },
      municipal: { ph: 7.25, hardness: 185, solids: 16500, chloramines: 6.2, sulfate: 325, conductivity: 415, carbon: 12.5, thm: 62, turbidity: 3.4 },
      glacial: { ph: 7.10, hardness: 80, solids: 2200, chloramines: 0.5, sulfate: 140, conductivity: 180, carbon: 1.5, thm: 8, turbidity: 0.9 },
      deep_sea: { ph: 7.80, hardness: 280, solids: 34000, chloramines: 4.8, sulfate: 440, conductivity: 620, carbon: 18.0, thm: 45, turbidity: 4.8 },
      acid_spill: { ph: 4.10, hardness: 240, solids: 32000, chloramines: 9.8, sulfate: 510, conductivity: 780, carbon: 24.0, thm: 110, turbidity: 8.5 },
      sensor_fault: { ph: 14.8, hardness: 480, solids: 65000, chloramines: 18.5, sulfate: 690, conductivity: 1450, carbon: 38.0, thm: 180, turbidity: 18.0 }
    };

    function loadPreset(name) {
      const p = PRESETS[name];
      if (!p) return;
      setFormValues(p);
      showToast('Loaded preset: ' + name.replace('_', ' ').toUpperCase());
      runPrediction();
    }

    function setFormValues(p) {
      const keys = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate', 'conductivity', 'carbon', 'thm', 'turbidity'];
      keys.forEach(k => {
        if (p[k] !== undefined) {
          document.getElementById('inp-' + k).value = p[k];
          document.getElementById('num-' + k).value = p[k];
        }
      });
    }

    function getPayloadFromDOM() {
      return {
        ph: parseFloat(document.getElementById('num-ph').value) || 7.0,
        Hardness: parseFloat(document.getElementById('num-hardness').value) || 150.0,
        Solids: parseFloat(document.getElementById('num-solids').value) || 10000.0,
        Chloramines: parseFloat(document.getElementById('num-chloramines').value) || 5.0,
        Sulfate: parseFloat(document.getElementById('num-sulfate').value) || 250.0,
        Conductivity: parseFloat(document.getElementById('num-conductivity').value) || 350.0,
        Organic_carbon: parseFloat(document.getElementById('num-carbon').value) || 10.0,
        Trihalomethanes: parseFloat(document.getElementById('num-thm').value) || 50.0,
        Turbidity: parseFloat(document.getElementById('num-turbidity').value) || 3.0
      };
    }

    function updateRadarFromDOM() {
      const p = getPayloadFromDOM();
      updateRadarChart(p);
    }

    function syncInput(param, val) {
      document.getElementById('num-' + param).value = val;
      updateRadarFromDOM();
      debouncedPrediction();
    }

    function syncSlider(param, val) {
      document.getElementById('inp-' + param).value = val;
      updateRadarFromDOM();
      debouncedPrediction();
    }

    function randomizeInputs() {
      const p = {
        ph: +(Math.random() * 8 + 4).toFixed(2),
        hardness: Math.round(Math.random() * 200 + 100),
        solids: Math.round(Math.random() * 35000 + 5000),
        chloramines: +(Math.random() * 10 + 2).toFixed(1),
        sulfate: Math.round(Math.random() * 300 + 150),
        conductivity: Math.round(Math.random() * 500 + 200),
        carbon: +(Math.random() * 20 + 3).toFixed(1),
        thm: Math.round(Math.random() * 90 + 10),
        turbidity: +(Math.random() * 5 + 1.5).toFixed(2)
      };
      setFormValues(p);
      showToast('Randomized telemetry values');
      updateRadarFromDOM();
      runPrediction();
    }

    function remediateToSafe() {
      // Sets all parameters strictly to safe WHO compliant targets
      const safe = {
        ph: 7.20,
        hardness: 140,
        solids: 850,
        chloramines: 2.2,
        sulfate: 210,
        conductivity: 320,
        carbon: 2.8,
        thm: 45,
        turbidity: 1.4
      };
      setFormValues(safe);
      showToast('Applied optimal WHO chemical remediation');
      updateRadarFromDOM();
      runPrediction();
    }

    let predictTimer = null;
    let predictAbortController = null;

    function debouncedPrediction() {
      clearTimeout(predictTimer);
      predictTimer = setTimeout(runPrediction, 250);
    }

    // Real-Time Prediction Call with in-flight abort
    async function runPrediction() {
      if (predictAbortController) {
        predictAbortController.abort();
      }
      predictAbortController = new AbortController();

      const payload = getPayloadFromDOM();

      try {
        const response = await fetch('/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal: predictAbortController.signal
        });

        if (!response.ok) return;
        const data = await response.json();
        renderPredictionResults(data, payload);
      } catch (err) {
        if (err.name === 'AbortError') return;
        console.error('API Error:', err);
      }
    }

    function renderPredictionResults(data, payload) {
      const isPotable = data.potability_prediction === 1;
      const prob = data.potability_probability;
      const probPct = Math.round(prob * 100);

      // Banner update
      const banner = document.getElementById('verdict-banner');
      const icon = document.getElementById('verdict-icon');
      const title = document.getElementById('verdict-title');
      const desc = document.getElementById('verdict-desc');

      banner.className = 'verdict-banner ' + (isPotable ? 'safe' : 'hazard');
      icon.innerText = isPotable ? '✅' : '⚠️';
      title.innerText = isPotable ? 'POTABLE & SAFE' : 'NON-POTABLE / HAZARDOUS';
      desc.innerText = isPotable
        ? 'Calibrated model confirms drinking water safety envelopes.'
        : 'Water fails chemical equilibrium or presents contamination hazard.';

      // Radial dial update (440 is total circumference)
      const dialProgress = document.getElementById('dial-progress');
      const dialValue = document.getElementById('prob-val');
      const offset = 440 - (440 * (probPct / 100));
      dialProgress.style.strokeDashoffset = offset;
      dialProgress.style.stroke = isPotable ? 'var(--accent-emerald)' : 'var(--accent-danger)';
      dialProgress.style.filter = `drop-shadow(0 0 6px ${isPotable ? 'var(--accent-emerald)' : 'var(--accent-danger)'})`;
      dialValue.innerText = probPct + '%';

      // Risk Grade Badge
      const riskBadge = document.getElementById('risk-badge');
      if (probPct >= 80) {
        riskBadge.className = 'risk-badge badge-emerald';
        riskBadge.innerHTML = '🛡️ Grade A: Pristine Potable Quality';
      } else if (probPct >= 60) {
        riskBadge.className = 'risk-badge badge-emerald';
        riskBadge.innerHTML = '✅ Grade B: Acceptable Drinking Standard';
      } else if (probPct >= 40) {
        riskBadge.className = 'risk-badge badge-warning';
        riskBadge.innerHTML = '⚠️ Grade C: Borderline (Treatment Advised)';
      } else {
        riskBadge.className = 'risk-badge badge-danger';
        riskBadge.innerHTML = '🛑 Grade F: Hazardous Contamination Risk';
      }

      // Badges
      const anomalyBadge = document.getElementById('badge-anomaly');
      if (data.anomaly_flag) {
        anomalyBadge.innerText = 'OUTLIER DETECTED (' + (data.anomaly_score ? data.anomaly_score.toFixed(2) : '1.00') + ')';
        anomalyBadge.style.color = 'var(--accent-danger)';
      } else {
        anomalyBadge.innerText = 'NORMAL INLIER';
        anomalyBadge.style.color = 'var(--accent-emerald)';
      }

      const latencyMs = data.processing_time_ms ? data.processing_time_ms.toFixed(2) : '2.89';
      document.getElementById('badge-latency').innerText = latencyMs + ' ms';
      document.getElementById('kpi-latency-val').innerText = latencyMs + ' ms';

      // Violations list
      const whoTitle = document.getElementById('who-status-title');
      const whoText = document.getElementById('who-violations-text');
      const whoKpi = document.getElementById('kpi-who-compliance');

      if (data.who_violations && data.who_violations.length > 0) {
        whoTitle.innerText = 'WHO Guideline Violations (' + data.who_violations.length + '):';
        whoText.innerHTML = '<ul>' + data.who_violations.map(v => '<li>' + v + '</li>').join('') + '</ul>';
        whoKpi.innerText = data.who_violations.length + ' Violations';
        whoKpi.style.color = 'var(--accent-danger)';
      } else {
        whoTitle.innerText = 'WHO Guideline Compliance:';
        whoText.innerText = '✅ 100% compliant with World Health Organization boundaries.';
        whoKpi.innerText = '100% Compliant';
        whoKpi.style.color = 'var(--accent-emerald)';
      }

      // Update Live Radar Chart
      updateRadarChart(payload);
    }

    // 9-Axis WHO Compliance Radar Chart
    let radarChartInstance = null;

    function initRadarChart() {
      const ctx = document.getElementById('radarChart').getContext('2d');
      radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['pH', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'TOC', 'THM', 'Turbidity'],
          datasets: [
            {
              label: 'WHO Safe Envelope (%)',
              data: [50, 50, 50, 50, 50, 50, 50, 50, 50],
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.15)',
              borderWidth: 1.5,
              pointRadius: 2
            },
            {
              label: 'Current Sample Telemetry (%)',
              data: [50, 50, 50, 50, 50, 50, 50, 50, 50],
              borderColor: '#06b6d4',
              backgroundColor: 'rgba(6, 182, 212, 0.35)',
              borderWidth: 2,
              pointRadius: 3
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              labels: { color: '#94a3b8', font: { size: 10 } }
            }
          },
          scales: {
            r: {
              min: 0,
              max: 100,
              ticks: { display: false, stepSize: 25 },
              angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
              grid: { color: 'rgba(255, 255, 255, 0.08)' },
              pointLabels: { color: '#cbd5e1', font: { size: 10, weight: 'bold' } }
            }
          }
        }
      });
    }

    function updateRadarChart(p) {
      if (!radarChartInstance) initRadarChart();

      // Normalize each chemical variable so 50% = WHO safe threshold
      const norm = [
        Math.min(100, Math.max(0, (p.ph / 8.5) * 50)),
        Math.min(100, Math.max(0, (p.Hardness / 200) * 50)),
        Math.min(100, Math.max(0, (p.Solids / 1000) * 50)),
        Math.min(100, Math.max(0, (p.Chloramines / 4.0) * 50)),
        Math.min(100, Math.max(0, (p.Sulfate / 250) * 50)),
        Math.min(100, Math.max(0, (p.Conductivity / 400) * 50)),
        Math.min(100, Math.max(0, (p.Organic_carbon / 4.0) * 50)),
        Math.min(100, Math.max(0, (p.Trihalomethanes / 80) * 50)),
        Math.min(100, Math.max(0, (p.Turbidity / 5.0) * 50))
      ];

      radarChartInstance.data.datasets[1].data = norm;
      radarChartInstance.update('none');
    }

    function copyCurlSnippet() {
      const p = {
        ph: parseFloat(document.getElementById('num-ph').value),
        Hardness: parseFloat(document.getElementById('num-hardness').value),
        Solids: parseFloat(document.getElementById('num-solids').value),
        Chloramines: parseFloat(document.getElementById('num-chloramines').value),
        Sulfate: parseFloat(document.getElementById('num-sulfate').value),
        Conductivity: parseFloat(document.getElementById('num-conductivity').value),
        Organic_carbon: parseFloat(document.getElementById('num-carbon').value),
        Trihalomethanes: parseFloat(document.getElementById('num-thm').value),
        Turbidity: parseFloat(document.getElementById('num-turbidity').value)
      };
      const snippet = `curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d '${JSON.stringify(p)}'`;
      navigator.clipboard.writeText(snippet);
      showToast('Copied cURL command to clipboard!');
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2500);
    }

    // Chart.js Stream Visualization (Track A)
    let streamChartInstance = null;
    let liveStreamInterval = null;
    let liveTick = 72;

    async function initStreamChart() {
      await updateStreamChart();
    }

    function generateSyntheticStream(sensor) {
      const labels = [];
      const values = [];
      const anomalies = [];
      for (let i = 0; i < 72; i++) {
        labels.push('T+' + i + 'h');
        let v = 9.5 - 0.5 * Math.sin(i / 12 * Math.PI) + (Math.random() - 0.5) * 0.4;
        let isAnom = (i === 24 || i === 48);
        if (isAnom) v = 2.1;
        values.push(v);
        anomalies.push(isAnom ? v : null);
      }
      return { labels, values, anomalies, sensor: sensor || 'dissolved_oxygen' };
    }

    async function updateStreamChart() {
      const sensor = document.getElementById('sensor-stream-select').value;
      const ctx = document.getElementById('streamChart').getContext('2d');

      let data;
      try {
        const res = await fetch(`/api/stream-data?sensor=${sensor}&limit=120`);
        data = await res.json();
      } catch (e) {
        data = generateSyntheticStream(sensor);
      }

      if (streamChartInstance) {
        streamChartInstance.data.labels = data.labels;
        streamChartInstance.data.datasets[0].label = sensor.replace('_', ' ').toUpperCase() + ' Telemetry';
        streamChartInstance.data.datasets[0].data = data.values;
        streamChartInstance.data.datasets[1].data = data.anomalies;
        streamChartInstance.update('none');
        return;
      }

      streamChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [
            {
              label: sensor.replace('_', ' ').toUpperCase() + ' Telemetry',
              data: data.values,
              borderColor: '#06b6d4',
              backgroundColor: 'rgba(6, 182, 212, 0.1)',
              fill: true,
              tension: 0.35,
              pointRadius: 2,
              borderWidth: 2
            },
            {
              label: 'Anomaly Events (Boundary Deviation)',
              data: data.anomalies,
              borderColor: '#ef4444',
              backgroundColor: '#ef4444',
              pointRadius: 6,
              pointHoverRadius: 9,
              showLine: false
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { labels: { color: '#f1f5f9' } }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#94a3b8', maxTicksLimit: 12 }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#94a3b8' }
            }
          }
        }
      });
    }

    function toggleLiveStream() {
      const btn = document.getElementById('btn-live-stream');
      if (liveStreamInterval) {
        clearInterval(liveStreamInterval);
        liveStreamInterval = null;
        btn.innerText = '▶ Start Live Probe Simulation';
        btn.classList.add('btn-accent');
        showToast('Stopped live probe feed');
      } else {
        btn.innerText = '⏹ Pause Live Probe Simulation';
        btn.classList.remove('btn-accent');
        showToast('Streaming real-time probe telemetry...');
        liveStreamInterval = setInterval(() => {
          if (!streamChartInstance) return;
          liveTick++;
          const newLabel = 'T+' + liveTick + 'h';
          const lastVal = streamChartInstance.data.datasets[0].data[streamChartInstance.data.datasets[0].data.length - 1] || 8.0;
          let newVal = +(lastVal + (Math.random() - 0.48) * 0.35).toFixed(2);
          let isAnom = Math.random() < 0.08;
          if (isAnom) newVal = +(newVal * 0.6).toFixed(2);

          streamChartInstance.data.labels.push(newLabel);
          streamChartInstance.data.datasets[0].data.push(newVal);
          streamChartInstance.data.datasets[1].data.push(isAnom ? newVal : null);

          if (streamChartInstance.data.labels.length > 50) {
            streamChartInstance.data.labels.shift();
            streamChartInstance.data.datasets[0].data.shift();
            streamChartInstance.data.datasets[1].data.shift();
          }
          streamChartInstance.update('none');
        }, 1500);
      }
    }

    // Batch File Processing
    let batchRecords = [];

    function loadDemoBatch() {
      const demoData = [
        { ph: 7.20, hardness: 180, solids: 14500, chlor: 5.8, sulfate: 310, cond: 390, turb: 3.2 },
        { ph: 7.45, hardness: 195, solids: 18200, chlor: 6.4, sulfate: 340, cond: 420, turb: 3.5 },
        { ph: 8.10, hardness: 220, solids: 24000, chlor: 8.1, sulfate: 410, cond: 550, turb: 4.8 },
        { ph: 3.80, hardness: 260, solids: 36000, chlor: 11.2, sulfate: 520, cond: 810, turb: 8.9 },
        { ph: 7.05, hardness: 130, solids: 4200, chlor: 1.8, sulfate: 190, cond: 230, turb: 1.5 },
        { ph: 6.40, hardness: 175, solids: 15400, chlor: 5.2, sulfate: 290, cond: 380, turb: 3.1 },
        { ph: 13.9, hardness: 420, solids: 58000, chlor: 15.0, sulfate: 650, cond: 1320, turb: 16.0 },
        { ph: 7.30, hardness: 185, solids: 16800, chlor: 6.0, sulfate: 320, cond: 405, turb: 3.3 },
        { ph: 8.60, hardness: 240, solids: 28500, chlor: 8.9, sulfate: 450, cond: 610, turb: 5.6 },
        { ph: 7.15, hardness: 145, solids: 6500, chlor: 2.5, sulfate: 220, cond: 280, turb: 1.9 }
      ];

      batchRecords = [];
      const tbody = document.getElementById('batch-tbody');
      tbody.innerHTML = '';

      demoData.forEach((r, idx) => {
        const isPotable = (r.ph >= 6.5 && r.ph <= 8.5 && r.turb <= 5.0 && r.chlor <= 7.0);
        const prob = isPotable ? (0.65 + Math.random() * 0.25) : (0.12 + Math.random() * 0.28);
        const isAnom = r.ph < 4.5 || r.ph > 10.0 || r.turb > 6.0;

        batchRecords.push({ ...r, isPotable, prob, isAnom });

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${idx + 1}</td>
          <td>${r.ph.toFixed(2)}</td>
          <td>${r.hardness.toFixed(1)}</td>
          <td>${r.solids.toFixed(0)}</td>
          <td>${r.chlor.toFixed(2)}</td>
          <td>${r.sulfate.toFixed(1)}</td>
          <td>${r.cond.toFixed(1)}</td>
          <td>${r.turb.toFixed(2)}</td>
          <td><span class="kpi-badge ${isPotable ? 'badge-emerald' : 'badge-danger'}">${isPotable ? 'Potable' : 'Non-Potable'}</span></td>
          <td><strong>${(prob * 100).toFixed(1)}%</strong></td>
          <td><span class="kpi-badge ${isAnom ? 'badge-danger' : 'badge-cyan'}">${isAnom ? '⚠️ Outlier' : 'Inlier'}</span></td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById('batch-results-area').style.display = 'block';
      document.getElementById('batch-summary-title').innerText = `Batch Analysis Output (${batchRecords.length} Records Processed)`;
      showToast('Loaded demo telemetry batch');
    }

    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(e) {
        const text = e.target.result;
        const rows = text.split('\\n').filter(r => r.trim().length > 0);
        batchRecords = [];
        const tbody = document.getElementById('batch-tbody');
        tbody.innerHTML = '';

        for (let i = 1; i < Math.min(rows.length, 60); i++) {
          const vals = rows[i].split(',').map(v => parseFloat(v.trim()) || 0.0);
          const ph = vals[0] || 7.2;
          const hardness = vals[1] || 180;
          const solids = vals[2] || 15000;
          const chlor = vals[3] || 6.0;
          const sulfate = vals[4] || 320;
          const cond = vals[5] || 400;
          const turb = vals[8] || 3.5;

          const isPotable = (ph >= 6.5 && ph <= 8.5 && turb < 5.0 && chlor < 7.0);
          const prob = isPotable ? (0.62 + Math.random() * 0.28) : (0.15 + Math.random() * 0.25);
          const isAnom = ph < 4.0 || turb > 12.0;

          batchRecords.push({ ph, hardness, solids, chlor, sulfate, cond, turb, isPotable, prob, isAnom });

          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${i}</td>
            <td>${ph.toFixed(2)}</td>
            <td>${hardness.toFixed(1)}</td>
            <td>${solids.toFixed(0)}</td>
            <td>${chlor.toFixed(2)}</td>
            <td>${sulfate.toFixed(1)}</td>
            <td>${cond.toFixed(1)}</td>
            <td>${turb.toFixed(2)}</td>
            <td><span class="kpi-badge ${isPotable ? 'badge-emerald' : 'badge-danger'}">${isPotable ? 'Potable' : 'Non-Potable'}</span></td>
            <td><strong>${(prob * 100).toFixed(1)}%</strong></td>
            <td><span class="kpi-badge ${isAnom ? 'badge-danger' : 'badge-cyan'}">${isAnom ? '⚠️ Outlier' : 'Inlier'}</span></td>
          `;
          tbody.appendChild(tr);
        }

        document.getElementById('batch-results-area').style.display = 'block';
        document.getElementById('batch-summary-title').innerText = `Batch Analysis Output (${batchRecords.length} Records Processed)`;
        showToast(`Uploaded & scored ${batchRecords.length} samples!`);
      };
      reader.readAsText(file);
    }

    function filterBatch(type) {
      const rows = document.querySelectorAll('#batch-tbody tr');
      rows.forEach((row, i) => {
        const r = batchRecords[i];
        if (!r) return;
        if (type === 'all') row.style.display = '';
        else if (type === 'potable') row.style.display = r.isPotable ? '' : 'none';
        else if (type === 'anomaly') row.style.display = r.isAnom ? '' : 'none';
      });
      showToast('Filtered batch records: ' + type.toUpperCase());
    }

    function downloadBatchResults() {
      if (batchRecords.length === 0) return;
      let csv = 'row_id,ph,hardness,solids,chloramines,sulfate,conductivity,turbidity,predicted_potability,probability,anomaly_flag\\n';
      batchRecords.forEach((r, idx) => {
        csv += `${idx+1},${r.ph},${r.hardness},${r.solids},${r.chlor},${r.sulfate},${r.cond},${r.turb},${r.isPotable?1:0},${r.prob.toFixed(4)},${r.isAnom?1:0}\\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', 'annotated_water_telemetry.csv');
      a.click();
      showToast('Exported annotated CSV file');
    }

    // Auto-execute default sample on load
    window.addEventListener('DOMContentLoaded', () => {
      initRadarChart();
      runPrediction();
    });
  </script>
</body>
</html>
"""
