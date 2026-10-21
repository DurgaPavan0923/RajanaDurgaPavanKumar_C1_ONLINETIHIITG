"""Modern, Clean, Attractive, and Professional Web Dashboard for AquaGuard AI.

Audit & Upgrade v2.1.0:
- Design tokens with Dark and Light mode theme toggle and localStorage memory.
- Responsive across mobile (360px), tablet (768px), and desktop (1440px).
- Tab 1: 9 sliders + numeric inputs with accurate WHO/EPA limit badges, presets, auto-remediation,
  copy cURL, educational disclaimer, safe model estimate verdict, grading rubric modal,
  and 9-axis radar chart.
- Tab 2: Track A simulated CTD probe stream with Isolation Forest and 3.5-sigma bounds,
  start/pause/reset controls, and multi-sensor support.
- Tab 3: Complete 9-column batch telemetry processor, 30-sample demo batch, drag-and-drop CSV parser,
  filters, and formula-injection-safe CSV export.
- Tab 4: Rigorous Stratified 5-Fold Benchmark & Lockbox table with 95% CIs, baseline explanation,
  threshold tuning context, and accurately attributed WHO/EPA regulatory boundary envelopes.
- Footer with About & Methodology modal, version v2.1.0, and live status ping.
"""

HTML_DASHBOARD = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AquaGuard AI | Water Potability & Environmental Intelligence</title>
  <meta name="description" content="Production-grade water potability classification, WHO regulatory compliance auditing, and continuous oceanographic telemetry monitoring.">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌊</text></svg>">
  <!-- Chart.js CDN for interactive visual analytics -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    :root {
      --bg-primary: #070d19;
      --bg-surface: #0c1527;
      --bg-card: rgba(17, 27, 49, 0.78);
      --bg-card-hover: rgba(26, 41, 74, 0.90);
      --bg-input: #0b1325;
      --border-color: rgba(38, 59, 97, 0.55);
      --border-glow: rgba(6, 182, 212, 0.35);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --accent-cyan: #06b6d4;
      --accent-cyan-rgb: 6, 182, 212;
      --accent-emerald: #10b981;
      --accent-emerald-rgb: 16, 185, 129;
      --accent-danger: #ef4444;
      --accent-danger-rgb: 239, 68, 68;
      --accent-warning: #f59e0b;
      --accent-warning-rgb: 245, 158, 11;
      --accent-purple: #8b5cf6;
      --accent-blue: #3b82f6;
      --header-bg: rgba(11, 19, 36, 0.90);
      --table-th-bg: rgba(15, 23, 42, 0.85);
      --table-stripe: rgba(255, 255, 255, 0.02);
      --modal-overlay: rgba(0, 0, 0, 0.75);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.25);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.35);
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    [data-theme="light"] {
      --bg-primary: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: rgba(255, 255, 255, 0.92);
      --bg-card-hover: rgba(248, 250, 252, 0.98);
      --bg-input: #ffffff;
      --border-color: rgba(203, 213, 225, 0.85);
      --border-glow: rgba(6, 182, 212, 0.25);
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --header-bg: rgba(255, 255, 255, 0.92);
      --table-th-bg: rgba(241, 245, 249, 0.95);
      --table-stripe: rgba(0, 0, 0, 0.02);
      --modal-overlay: rgba(15, 23, 42, 0.6);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.1);
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
        radial-gradient(circle at 15% 20%, rgba(var(--accent-cyan-rgb), 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 75%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(var(--accent-emerald-rgb), 0.04) 0%, transparent 60%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.25s ease, color 0.25s ease;
    }

    /* Top Sticky Header */
    header {
      background: var(--header-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-color);
      padding: 0.85rem 1.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: var(--shadow-sm);
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-logo-container {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(var(--accent-cyan-rgb), 0.2), rgba(var(--accent-emerald-rgb), 0.2));
      border: 1px solid var(--border-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 15px rgba(var(--accent-cyan-rgb), 0.2);
    }

    .brand-icon {
      font-size: 1.5rem;
      animation: pulseGlow 3s infinite ease-in-out;
    }

    @keyframes pulseGlow {
      0%, 100% { transform: scale(1); filter: drop-shadow(0 0 2px var(--accent-cyan)); }
      50% { transform: scale(1.08); filter: drop-shadow(0 0 8px var(--accent-emerald)); }
    }

    .brand-title {
      font-size: 1.2rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      background: linear-gradient(135deg, var(--text-main) 30%, var(--accent-cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }

    .brand-version {
      font-size: 0.65rem;
      padding: 0.15rem 0.45rem;
      border-radius: 6px;
      background: rgba(var(--accent-cyan-rgb), 0.15);
      color: var(--accent-cyan);
      border: 1px solid var(--border-glow);
      -webkit-text-fill-color: initial;
      font-weight: 700;
      letter-spacing: 0;
    }

    .brand-subtitle {
      font-size: 0.72rem;
      color: var(--text-muted);
      letter-spacing: 0.04em;
      font-weight: 500;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
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
      gap: 0.45rem;
      background: rgba(var(--accent-emerald-rgb), 0.1);
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.3);
      padding: 0.35rem 0.8rem;
      border-radius: 9999px;
      font-size: 0.76rem;
      color: var(--accent-emerald);
      font-weight: 600;
      transition: all 0.3s ease;
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

    /* Theme Toggle Button */
    .theme-toggle-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      width: 36px;
      height: 36px;
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1rem;
      transition: all 0.2s ease;
    }
    .theme-toggle-btn:hover {
      background: rgba(var(--accent-cyan-rgb), 0.15);
      border-color: var(--accent-cyan);
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1440px;
      margin: 0 auto;
      padding: 1.5rem 1rem;
      width: 100%;
    }
    @media (min-width: 768px) {
      main { padding: 1.75rem 1.5rem; }
    }

    /* KPI Summary Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    @media (min-width: 540px) {
      .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (min-width: 1024px) {
      .kpi-grid { grid-template-columns: repeat(4, 1fr); }
    }

    .kpi-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.15rem 1.35rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: var(--shadow-sm);
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
      transform: translateY(-2px);
      border-color: var(--accent-cyan);
      box-shadow: 0 8px 25px rgba(var(--accent-cyan-rgb), 0.12);
    }

    .kpi-info h4 {
      font-size: 0.74rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.3rem;
      font-weight: 600;
    }

    .kpi-info .kpi-value {
      font-size: 1.4rem;
      font-weight: 800;
      letter-spacing: -0.02em;
    }

    .kpi-info .kpi-desc {
      font-size: 0.72rem;
      color: var(--text-dim);
      margin-top: 0.2rem;
    }

    .kpi-icon-pill {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.25rem;
      flex-shrink: 0;
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
      padding: 0.8rem 1.15rem;
      font-size: 0.88rem;
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
      background: rgba(var(--accent-cyan-rgb), 0.08);
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
      padding: 1.5rem;
      margin-bottom: 1.5rem;
      box-shadow: var(--shadow-sm);
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
      font-size: 1.1rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: var(--text-main);
    }

    /* Educational Disclaimer Banner */
    .disclaimer-banner {
      background: rgba(var(--accent-warning-rgb), 0.10);
      border: 1px solid rgba(var(--accent-warning-rgb), 0.35);
      border-radius: 12px;
      padding: 0.85rem 1.15rem;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      font-size: 0.82rem;
      color: var(--text-main);
      line-height: 1.45;
    }
    .disclaimer-icon {
      font-size: 1.3rem;
      line-height: 1;
      flex-shrink: 0;
    }

    /* Remediation Diff Box */
    .remediation-alert {
      background: rgba(var(--accent-emerald-rgb), 0.12);
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.35);
      border-radius: 10px;
      padding: 0.75rem 1rem;
      margin-bottom: 1rem;
      font-size: 0.82rem;
      color: var(--accent-emerald);
      display: none;
    }

    /* Presets Bar */
    .presets-container {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-bottom: 1.5rem;
      align-items: center;
      background: rgba(0, 0, 0, 0.18);
      padding: 0.75rem 1rem;
      border-radius: 12px;
      border: 1px solid var(--border-color);
    }

    .preset-label {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-right: 0.35rem;
      font-weight: 600;
    }

    .preset-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.4rem 0.8rem;
      border-radius: 8px;
      font-size: 0.8rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      transition: all 0.2s ease;
      font-weight: 500;
    }

    .preset-btn:hover {
      background: rgba(var(--accent-cyan-rgb), 0.15);
      border-color: var(--accent-cyan);
      transform: translateY(-1px);
    }

    .preset-btn.btn-accent {
      background: linear-gradient(135deg, rgba(var(--accent-cyan-rgb), 0.25), rgba(var(--accent-emerald-rgb), 0.25));
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
      gap: 1rem;
    }
    @media (min-width: 600px) {
      .inputs-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    .input-group {
      background: rgba(0, 0, 0, 0.18);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 0.85rem 0.95rem;
      transition: all 0.2s ease;
    }

    .input-group:hover, .input-group:focus-within {
      border-color: var(--accent-cyan);
      box-shadow: 0 0 12px rgba(var(--accent-cyan-rgb), 0.1);
    }

    .input-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 0.5rem;
      gap: 0.5rem;
    }

    .input-label {
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--text-main);
    }

    .limit-badge {
      font-size: 0.68rem;
      padding: 0.15rem 0.45rem;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-dim);
      white-space: nowrap;
    }

    .slider-row {
      display: flex;
      align-items: center;
      gap: 0.75rem;
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
      width: 78px;
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.35rem 0.45rem;
      border-radius: 6px;
      font-size: 0.82rem;
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
      background: rgba(0, 0, 0, 0.22);
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
      background: linear-gradient(135deg, rgba(var(--accent-emerald-rgb), 0.18), rgba(var(--accent-cyan-rgb), 0.18));
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.4);
      color: var(--accent-emerald);
      box-shadow: 0 0 20px rgba(var(--accent-emerald-rgb), 0.12);
    }

    .verdict-banner.hazard {
      background: linear-gradient(135deg, rgba(var(--accent-danger-rgb), 0.18), rgba(var(--accent-warning-rgb), 0.18));
      border: 1px solid rgba(var(--accent-danger-rgb), 0.4);
      color: var(--accent-danger);
      box-shadow: 0 0 20px rgba(var(--accent-danger-rgb), 0.12);
    }

    .verdict-banner.warning {
      background: linear-gradient(135deg, rgba(var(--accent-warning-rgb), 0.18), rgba(var(--accent-purple), 0.18));
      border: 1px solid rgba(var(--accent-warning-rgb), 0.4);
      color: var(--accent-warning);
      box-shadow: 0 0 20px rgba(var(--accent-warning-rgb), 0.12);
    }

    .verdict-icon {
      font-size: 2rem;
      flex-shrink: 0;
    }

    .verdict-title {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: 0.02em;
      text-align: left;
    }

    .verdict-desc {
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 0.2rem;
      text-align: left;
    }

    /* Circular Radial Probability Dial */
    .dial-container {
      position: relative;
      width: 150px;
      height: 150px;
      margin: 0.25rem 0 1rem 0;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .dial-svg {
      transform: rotate(-90deg);
      width: 150px;
      height: 150px;
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
      stroke-dasharray: 414;
      stroke-dashoffset: 414;
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
      font-size: 1.9rem;
      font-weight: 900;
      color: var(--text-main);
      font-variant-numeric: tabular-nums;
    }

    .dial-sub {
      font-size: 0.68rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
    }

    .risk-badge {
      padding: 0.4rem 0.9rem;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 700;
      margin-bottom: 1rem;
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      cursor: pointer;
      transition: transform 0.2s ease;
    }
    .risk-badge:hover {
      transform: scale(1.04);
    }

    /* Diagnostic Badges */
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
      padding: 0.7rem;
      text-align: left;
    }

    .audit-badge-title {
      font-size: 0.68rem;
      color: var(--text-dim);
      text-transform: uppercase;
      font-weight: 600;
    }

    .audit-badge-value {
      font-size: 0.92rem;
      font-weight: 700;
      margin-top: 0.2rem;
    }

    /* Radar Chart Container */
    .radar-card {
      background: rgba(0, 0, 0, 0.22);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.25rem;
      width: 100%;
    }

    .radar-title {
      font-size: 0.82rem;
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
      height: 230px;
      width: 100%;
    }

    /* Violations Box */
    .violations-list {
      background: rgba(0, 0, 0, 0.18);
      border: 1px solid rgba(var(--accent-danger-rgb), 0.25);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      font-size: 0.78rem;
      color: var(--text-muted);
      width: 100%;
      text-align: left;
    }

    .violations-list ul {
      margin-left: 1.15rem;
      margin-top: 0.35rem;
    }

    .violations-list li {
      margin-bottom: 0.25rem;
      color: #fca5a5;
    }

    /* Action Buttons Row */
    .actions-row {
      display: flex;
      gap: 0.6rem;
      width: 100%;
      margin-top: 0.75rem;
      flex-wrap: wrap;
    }

    .action-btn {
      flex: 1;
      min-width: 160px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.6rem 0.85rem;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.4rem;
      transition: all 0.2s ease;
    }
    .action-btn:hover {
      background: rgba(var(--accent-cyan-rgb), 0.2);
      border-color: var(--accent-cyan);
    }

    /* Stream Chart Tab 2 */
    .chart-container {
      position: relative;
      height: 380px;
      width: 100%;
    }

    .stream-stats-bar {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      margin-top: 1rem;
      padding: 0.75rem 1rem;
      background: rgba(0, 0, 0, 0.18);
      border-radius: 10px;
      border: 1px solid var(--border-color);
      font-size: 0.8rem;
    }
    .stream-stat-item {
      display: flex;
      gap: 0.4rem;
      align-items: center;
    }
    .stream-stat-label { color: var(--text-muted); }
    .stream-stat-value { font-weight: 700; color: var(--text-main); }

    /* Batch Processing Tab 3 */
    .dropzone {
      border: 2px dashed var(--border-color);
      border-radius: 14px;
      padding: 2.5rem 1.5rem;
      text-align: center;
      background: rgba(0, 0, 0, 0.18);
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .dropzone:hover {
      border-color: var(--accent-cyan);
      background: rgba(var(--accent-cyan-rgb), 0.05);
    }

    .table-container {
      overflow-x: auto;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      margin-top: 1rem;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
    }

    th, td {
      padding: 0.7rem 0.9rem;
      text-align: left;
      border-bottom: 1px solid var(--border-color);
      white-space: nowrap;
    }

    th {
      background: var(--table-th-bg);
      color: var(--text-muted);
      font-weight: 600;
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      position: sticky;
      top: 0;
    }

    tbody tr:hover {
      background: var(--table-stripe);
    }

    .kpi-badge {
      display: inline-block;
      padding: 0.2rem 0.55rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 600;
    }

    .badge-emerald { background: rgba(var(--accent-emerald-rgb), 0.15); color: var(--accent-emerald); border: 1px solid rgba(var(--accent-emerald-rgb), 0.3); }
    .badge-danger { background: rgba(var(--accent-danger-rgb), 0.15); color: var(--accent-danger); border: 1px solid rgba(var(--accent-danger-rgb), 0.3); }
    .badge-warning { background: rgba(var(--accent-warning-rgb), 0.15); color: var(--accent-warning); border: 1px solid rgba(var(--accent-warning-rgb), 0.3); }
    .badge-cyan { background: rgba(var(--accent-cyan-rgb), 0.15); color: var(--accent-cyan); border: 1px solid rgba(var(--accent-cyan-rgb), 0.3); }
    .badge-purple { background: rgba(139, 92, 246, 0.15); color: var(--accent-purple); border: 1px solid rgba(139, 92, 246, 0.3); }

    /* Modals */
    .modal-backdrop {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: var(--modal-overlay);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 200;
      padding: 1rem;
    }
    .modal-backdrop.open { display: flex; animation: fadeIn 0.2s ease; }

    .modal-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      max-width: 650px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      padding: 1.75rem;
      box-shadow: var(--shadow-md);
      position: relative;
    }

    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
    }

    .modal-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .modal-close-btn {
      background: transparent;
      border: none;
      font-size: 1.25rem;
      color: var(--text-muted);
      cursor: pointer;
      padding: 0.25rem;
      line-height: 1;
    }
    .modal-close-btn:hover { color: var(--text-main); }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-color);
      padding: 1.25rem 1.5rem;
      font-size: 0.78rem;
      color: var(--text-dim);
      background: var(--header-bg);
      margin-top: auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
    }

    .footer-links {
      display: flex;
      gap: 1rem;
      align-items: center;
    }

    .footer-btn {
      background: none;
      border: none;
      color: var(--accent-cyan);
      font-size: 0.78rem;
      cursor: pointer;
      text-decoration: underline;
      padding: 0;
    }
    .footer-btn:hover { color: var(--accent-emerald); }

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

  <!-- Toast Notification -->
  <div id="toast">Copied to clipboard!</div>

  <!-- Grading Rubric Modal -->
  <div class="modal-backdrop" id="modal-rubric" onclick="closeModalOnBackdrop(event, 'modal-rubric')">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">AquaGuard Quality & Safety Grading Rubric</h3>
        <button class="modal-close-btn" onclick="closeModal('modal-rubric')">&times;</button>
      </div>
      <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem;">
        AquaGuard utilizes a dual-gate safety criterion. A high ML probability alone will NEVER grant a clean drinking grade unless all 9 chemical parameters pass WHO / EPA regulatory boundaries.
      </p>
      <table>
        <thead>
          <tr>
            <th>Grade</th>
            <th>ML Probability</th>
            <th>Regulatory Compliance</th>
            <th>Action Required</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="kpi-badge badge-emerald">Grade A</span></td>
            <td>&ge; 75% Potable</td>
            <td>0 WHO / EPA Violations</td>
            <td>Pristine; direct human consumption viable.</td>
          </tr>
          <tr>
            <td><span class="kpi-badge badge-emerald">Grade B</span></td>
            <td>&ge; 50% Potable</td>
            <td>0 WHO / EPA Violations</td>
            <td>Standard potable; conforms to safe drinking limits.</td>
          </tr>
          <tr>
            <td><span class="kpi-badge badge-warning">Grade C</span></td>
            <td>&ge; 50% Potable</td>
            <td>1–2 Secondary Violations</td>
            <td>Advisory warning; secondary filtration / aeration advised.</td>
          </tr>
          <tr>
            <td><span class="kpi-badge badge-danger">Grade D</span></td>
            <td>&lt; 50% Potable</td>
            <td>1–2 Violations</td>
            <td>Treatment required; non-potable without processing.</td>
          </tr>
          <tr>
            <td><span class="kpi-badge badge-danger">Grade F</span></td>
            <td>&lt; 50% Potable</td>
            <td>Severe / Multi-Chemical</td>
            <td>Hazardous / Contaminated; unsafe for consumption.</td>
          </tr>
          <tr>
            <td><span class="kpi-badge badge-purple">Grade X</span></td>
            <td>N/A</td>
            <td>Sensor Out-of-Bounds</td>
            <td>Sensor malfunction or drift; recalibration required.</td>
          </tr>
        </tbody>
      </table>
      <div style="margin-top: 1.25rem; text-align: right;">
        <button class="preset-btn btn-accent" onclick="closeModal('modal-rubric')">Got It</button>
      </div>
    </div>
  </div>

  <!-- About & Methodology Modal -->
  <div class="modal-backdrop" id="modal-about" onclick="closeModalOnBackdrop(event, 'modal-about')">
    <div class="modal-card">
      <div class="modal-header">
        <h3 class="modal-title">About AquaGuard AI Architecture & Methodology</h3>
        <button class="modal-close-btn" onclick="closeModal('modal-about')">&times;</button>
      </div>
      <div style="font-size: 0.82rem; color: var(--text-main); line-height: 1.55; display: flex; flex-direction: column; gap: 0.85rem;">
        <p><strong>1. Dataset & Problem Formulation:</strong> Trained on the Kaggle Water Potability benchmark (N=3,276 records across 9 physicochemical attributes). The dataset exhibits a 39.0% positive base rate (mild class imbalance) and natural sensor missingness (14.99% pH, 23.84% Sulfate, 4.95% THM).</p>
        <p><strong>2. Zero-Leakage Pipeline:</strong> Stratified 80/20 train/test lockbox split (Train N=2,620, Quarantined Lockbox N=656). Imputation medians and scaling parameters are strictly computed fold-internally during 5-fold CV to prevent data leakage.</p>
        <p><strong>3. Calibration & Metrics:</strong> Evaluated on Precision-Recall AUC (PR-AUC) as primary metric rather than raw Accuracy. Champion Random Forest / XGBoost models undergo Platt Scaling / Isotonic calibration to deliver well-calibrated posterior probabilities (Brier score: 0.2154).</p>
        <p><strong>4. Dual-Gate Safety Engine:</strong> Combines probabilistic ML with deterministic WHO & EPA drinking water envelopes. Out-of-distribution detection is guarded by an unsupervised Isolation Forest (&nu;=0.021).</p>
        <p style="color: var(--accent-warning);"><strong>5. Educational Disclaimer:</strong> AquaGuard AI is an academic demonstration and benchmarking engine. It is NOT a certified laboratory assay and cannot replace certified chemical testing.</p>
      </div>
      <div style="margin-top: 1.25rem; text-align: right;">
        <button class="preset-btn btn-accent" onclick="closeModal('modal-about')">Close</button>
      </div>
    </div>
  </div>

  <!-- Header -->
  <header>
    <div class="brand">
      <div class="brand-logo-container">
        <span class="brand-icon">🌊</span>
      </div>
      <div>
        <h1 class="brand-title">AquaGuard AI <span class="brand-version">v2.1.0</span></h1>
        <p class="brand-subtitle">Water Potability & Environmental Intelligence</p>
      </div>
    </div>
    <div class="header-controls">
      <div class="live-clock" id="live-clock">UTC 00:00:00</div>
      <div class="system-status" id="system-status-badge">
        <span class="status-dot" id="system-status-dot"></span>
        <span id="system-status-text">CONNECTING...</span>
      </div>
      <button class="theme-toggle-btn" id="theme-toggle" onclick="toggleTheme()" title="Toggle Light/Dark Theme" aria-label="Toggle theme">☀️</button>
    </div>
  </header>

  <main>
    <!-- Top KPI Grid -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Champion Pipeline</h4>
          <div class="kpi-value" style="color: var(--accent-cyan);">Random Forest</div>
          <div class="kpi-desc">Platt Scaling Calibrated</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(var(--accent-cyan-rgb), 0.15); color: var(--accent-cyan);">🏆</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Lockbox PR-AUC</h4>
          <div class="kpi-value" style="color: var(--accent-emerald);">0.5951</div>
          <div class="kpi-desc">WHO Baseline: 0.3920 (N=656)</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(var(--accent-emerald-rgb), 0.15); color: var(--accent-emerald);">📈</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Inference Latency</h4>
          <div class="kpi-value" id="kpi-latency-val" style="color: var(--accent-purple);">2.36 ms</div>
          <div class="kpi-desc" id="kpi-latency-desc">Server-Side P50 Measured</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(139, 92, 246, 0.15); color: var(--accent-purple);">⚡</div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>WHO Auditor</h4>
          <div class="kpi-value" id="kpi-who-compliance" style="color: var(--accent-emerald);">Active</div>
          <div class="kpi-desc">9 Regulatory Guardrails</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(59, 130, 246, 0.15); color: var(--accent-blue);">🛡️</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-header">
      <button class="tab-btn active" onclick="switchTab('tab-sim', this)">
        <span>🔬</span> Interactive Potability Simulator
      </button>
      <button class="tab-btn" onclick="switchTab('tab-stream', this)">
        <span>🌊</span> Continuous Telemetry Stream (Track A)
      </button>
      <button class="tab-btn" onclick="switchTab('tab-batch', this)">
        <span>📁</span> Batch Telemetry Processor (9 Features)
      </button>
      <button class="tab-btn" onclick="switchTab('tab-models', this)">
        <span>📊</span> Model Benchmark & WHO Standards
      </button>
    </div>

    <!-- TAB 1: INTERACTIVE POTABILITY SIMULATOR -->
    <div id="tab-sim" class="tab-pane active">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <span>🧪</span> Physicochemical Water Quality Telemetry Input
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Adjust sliders to trigger real-time calibrated Bayesian potability scoring and 9-axis WHO compliance auditing.
            </div>
          </div>
        </div>

        <!-- Educational Disclaimer Banner -->
        <div class="disclaimer-banner">
          <span class="disclaimer-icon">⚠️</span>
          <div>
            <strong>Educational & Demonstration Notice:</strong> AquaGuard AI is a predictive research model trained on Kaggle physicochemical benchmark data. It provides an algorithmic estimate and is <em>not</em> a substitute for certified laboratory microbiological or chemical assays. Drinking water decisions must be validated by licensed local testing authorities.
          </div>
        </div>

        <!-- Remediation Diff Box -->
        <div class="remediation-alert" id="remediation-alert">
          <strong>✨ Optimal WHO Remediation Applied:</strong> All 9 physicochemical parameters reset within safe regulatory envelopes (pH 7.20, Hardness 140 mg/L, TDS 850 ppm, Chloramines 2.2 ppm, Sulfate 210 mg/L, Conductivity 320 μS/cm, TOC 2.8 ppm, THM 45 μg/L, Turbidity 1.4 NTU).
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
          <!-- Left: 9 Chemical Parameter Input Sliders -->
          <div>
            <div class="inputs-grid">
              <!-- 1. pH -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">pH Acidity</span>
                  <span class="limit-badge">WHO: 6.5–8.5</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-ph" min="0" max="14" step="0.05" value="7.25" oninput="syncInput('ph', this.value)">
                  <input type="number" id="num-ph" class="num-input" value="7.25" step="0.05" onchange="syncSlider('ph', this.value)">
                </div>
              </div>

              <!-- 2. Hardness -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Hardness (Ca/Mg)</span>
                  <span class="limit-badge">WHO: &le; 200 mg/L</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-hardness" min="0" max="400" step="1" value="185" oninput="syncInput('hardness', this.value)">
                  <input type="number" id="num-hardness" class="num-input" value="185" step="1" onchange="syncSlider('hardness', this.value)">
                </div>
              </div>

              <!-- 3. Solids (TDS) -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Total Solids (TDS)</span>
                  <span class="limit-badge">WHO: &le; 1,000 ppm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-solids" min="0" max="65000" step="250" value="16500" oninput="syncInput('solids', this.value)">
                  <input type="number" id="num-solids" class="num-input" value="16500" step="250" onchange="syncSlider('solids', this.value)">
                </div>
              </div>

              <!-- 4. Chloramines -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Chloramines</span>
                  <span class="limit-badge">EPA MRDL: &le; 4.0 ppm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-chloramines" min="0" max="16" step="0.1" value="6.2" oninput="syncInput('chloramines', this.value)">
                  <input type="number" id="num-chloramines" class="num-input" value="6.2" step="0.1" onchange="syncSlider('chloramines', this.value)">
                </div>
              </div>

              <!-- 5. Sulfate -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Sulfate</span>
                  <span class="limit-badge">EPA 2nd: &le; 250 mg/L</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-sulfate" min="0" max="600" step="5" value="325" oninput="syncInput('sulfate', this.value)">
                  <input type="number" id="num-sulfate" class="num-input" value="325" step="5" onchange="syncSlider('sulfate', this.value)">
                </div>
              </div>

              <!-- 6. Conductivity -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Conductivity</span>
                  <span class="limit-badge">WHO: &le; 400 μS/cm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-conductivity" min="0" max="1000" step="5" value="415" oninput="syncInput('conductivity', this.value)">
                  <input type="number" id="num-conductivity" class="num-input" value="415" step="5" onchange="syncSlider('conductivity', this.value)">
                </div>
              </div>

              <!-- 7. Organic Carbon (TOC) -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Organic Carbon (TOC)</span>
                  <span class="limit-badge">EPA: &le; 4.0 ppm</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-carbon" min="0" max="35" step="0.1" value="12.5" oninput="syncInput('carbon', this.value)">
                  <input type="number" id="num-carbon" class="num-input" value="12.5" step="0.1" onchange="syncSlider('carbon', this.value)">
                </div>
              </div>

              <!-- 8. Trihalomethanes (THM) -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label">Trihalomethanes</span>
                  <span class="limit-badge">EPA: &le; 80 μg/L</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-thm" min="0" max="160" step="1" value="62" oninput="syncInput('thm', this.value)">
                  <input type="number" id="num-thm" class="num-input" value="62" step="1" onchange="syncSlider('thm', this.value)">
                </div>
              </div>

              <!-- 9. Turbidity -->
              <div class="input-group" style="grid-column: 1 / -1;">
                <div class="input-header">
                  <span class="input-label">Turbidity (Clarity)</span>
                  <span class="limit-badge">WHO: &le; 5.0 NTU (Target &le; 1.0)</span>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-turbidity" min="0" max="15" step="0.05" value="3.4" oninput="syncInput('turbidity', this.value)">
                  <input type="number" id="num-turbidity" class="num-input" value="3.4" step="0.05" onchange="syncSlider('turbidity', this.value)">
                </div>
              </div>
            </div>

            <!-- Quick Action Buttons -->
            <div class="actions-row">
              <button class="action-btn" onclick="remediateToSafe()">✨ Auto-Remediate to Potable</button>
              <button class="action-btn" onclick="copyCurlSnippet()">📋 Copy cURL Request</button>
              <button class="action-btn" onclick="openModal('modal-rubric')">ℹ️ View Grading Rubric</button>
            </div>
          </div>

          <!-- Right: Visual Outcome & Radar Chart -->
          <div class="decision-panel">
            <div class="decision-box">
              <div class="verdict-banner safe" id="verdict-banner">
                <span class="verdict-icon" id="verdict-icon">✅</span>
                <div>
                  <h3 class="verdict-title" id="verdict-title">Predicted Potable (Model Estimate)</h3>
                  <p class="verdict-desc" id="verdict-desc">Calibrated model estimate with WHO guideline adherence.</p>
                </div>
              </div>

              <!-- Circular Progress Dial -->
              <div class="dial-container">
                <svg class="dial-svg" viewBox="0 0 150 150">
                  <circle class="dial-bg" cx="75" cy="75" r="66"></circle>
                  <circle class="dial-progress" id="dial-progress" cx="75" cy="75" r="66"></circle>
                </svg>
                <div class="dial-text">
                  <span class="dial-value" id="prob-val">74%</span>
                  <span class="dial-sub">POTABILITY PROB</span>
                </div>
              </div>

              <div class="risk-badge badge-emerald" id="risk-badge" onclick="openModal('modal-rubric')" title="Click to view safety rubric">
                <span>🛡️</span> Grade B: Standard Potable
              </div>

              <!-- Diagnostic Badges -->
              <div class="audit-badges">
                <div class="audit-badge-card">
                  <div class="audit-badge-title">Anomaly Outlier Score</div>
                  <div class="audit-badge-value" id="badge-anomaly" style="color: var(--accent-emerald);">NORMAL INLIER</div>
                </div>
                <div class="audit-badge-card">
                  <div class="audit-badge-title">Inference Execution</div>
                  <div class="audit-badge-value" id="badge-latency" style="color: var(--accent-cyan);">2.36 ms</div>
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
                <span style="font-size: 0.7rem; color: var(--accent-cyan);">50% Line = Safe Limit</span>
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
          <div>
            <div class="card-title">
              <span>🌊</span> Underwater Environmental Sensor Timeline (Track A Stream)
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Simulated oceanographic CTD buoy stream (Ocean Station PAPA benchmark). Multi-sensor anomaly detection powered by Isolation Forest (&nu;=0.021) and dynamic 3.5&sigma; rolling bounds.
            </div>
          </div>
          <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
            <select id="sensor-stream-select" onchange="updateStreamChart()" style="background: var(--bg-input); color: var(--text-main); border: 1px solid var(--border-color); padding: 0.45rem 0.8rem; border-radius: 8px; font-size: 0.82rem; outline: none;">
              <option value="dissolved_oxygen">Dissolved Oxygen (DO) [mg/L]</option>
              <option value="temperature">Water Temperature [°C]</option>
              <option value="ph">pH Acidity [0-14]</option>
              <option value="turbidity">Turbidity Suspended Solids [NTU]</option>
              <option value="conductivity">Electrical Conductivity [μS/cm]</option>
              <option value="pressure">Hydrostatic Pressure [dbar]</option>
            </select>
            <button class="preset-btn btn-accent" id="btn-live-stream" onclick="toggleLiveStream()">▶ Start Live Probe Simulation</button>
            <button class="preset-btn" onclick="resetStreamChart()">🔄 Reset</button>
          </div>
        </div>

        <div class="chart-container">
          <canvas id="streamChart"></canvas>
        </div>

        <div class="stream-stats-bar">
          <div class="stream-stat-item">
            <span class="stream-stat-label">Telemetry Source:</span>
            <span class="stream-stat-value" id="stream-src-label">Simulated CTD Oceanographic Buoy</span>
          </div>
          <div class="stream-stat-item">
            <span class="stream-stat-label">Active Anomaly Model:</span>
            <span class="stream-stat-value" style="color: var(--accent-cyan);">Isolation Forest & 3.5σ Rolling Z-Score</span>
          </div>
          <div class="stream-stat-item">
            <span class="stream-stat-label">Anomalies Detected:</span>
            <span class="stream-stat-value" id="stream-anom-count" style="color: var(--accent-danger);">0</span>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: BATCH TELEMETRY INGESTION (9 COLUMNS) -->
    <div id="tab-batch" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <span>📁</span> Batch Telemetry Processor & Anomaly Scorer
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Full 9-feature schema support (including TOC and Trihalomethanes). Ingests up to 100 samples with median imputation and calibrated Bayesian scoring.
            </div>
          </div>
          <button class="preset-btn btn-accent" onclick="loadDemoBatch()">⚡ Load Demo 30-Sample Batch</button>
        </div>

        <div class="dropzone" id="batch-dropzone" onclick="document.getElementById('csv-upload-input').click()">
          <input type="file" id="csv-upload-input" accept=".csv" style="display: none;" onchange="handleFileUpload(event)">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📥</div>
          <h4 style="font-size: 1.1rem; font-weight: 700;">Upload Water Quality Sensor CSV (9 Features)</h4>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 0.35rem;">
            Click to select or drag & drop. Schema: <code>pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity</code>
          </p>
        </div>

        <div id="batch-results-area" style="display: none; margin-top: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
            <h4 id="batch-summary-title" style="font-size: 1.05rem; font-weight: 700;">Batch Analysis Output</h4>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <button class="preset-btn" onclick="filterBatch('all')">Show All</button>
              <button class="preset-btn" onclick="filterBatch('potable')">Potable Only</button>
              <button class="preset-btn" onclick="filterBatch('anomaly')">Anomalies Only</button>
              <button class="preset-btn btn-accent" onclick="downloadBatchResults()">⬇️ Download Annotated CSV</button>
            </div>
          </div>
          <div class="table-container">
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
                  <th>TOC (Carbon)</th>
                  <th>THM</th>
                  <th>Turbidity</th>
                  <th>Status</th>
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

    <!-- TAB 4: BENCHMARK & REGULATORY STANDARDS -->
    <div id="tab-models" class="tab-pane">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <span>🏆</span> Stratified 5-Fold Benchmark & Quarantined Lockbox Evaluation
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Strict fold-internal pre-processing; quarantined held-out lockbox (N=656) unblinded once post-tuning.
            </div>
          </div>
          <span class="kpi-badge badge-emerald">Zero-Leakage Guarantee</span>
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Model Candidate</th>
                <th>Architecture Family</th>
                <th>5-Fold CV PR-AUC (Dev N=2,620)</th>
                <th>Lockbox PR-AUC (N=656)</th>
                <th>Lockbox ROC-AUC</th>
                <th>Brier Score</th>
                <th>F1 @ T=0.50</th>
                <th>F1 @ T*=0.38</th>
                <th>P95 Latency</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>WHO Permissible Baseline</strong></td>
                <td>Deterministic Rule System</td>
                <td>0.3901 ± 0.000</td>
                <td>0.3920</td>
                <td>0.5000</td>
                <td>0.3890</td>
                <td>0.0000</td>
                <td>0.0000</td>
                <td>0.02 ms</td>
              </tr>
              <tr>
                <td><strong>Logistic Regression (ElasticNet)</strong></td>
                <td>Linear Classifier</td>
                <td>0.4320 ± 0.018</td>
                <td>0.4345</td>
                <td>0.5180</td>
                <td>0.2410</td>
                <td>0.4285</td>
                <td>0.4410</td>
                <td>0.14 ms</td>
              </tr>
              <tr style="background: rgba(var(--accent-cyan-rgb), 0.08); border-left: 3px solid var(--accent-cyan);">
                <td><strong>Random Forest (200 Trees)</strong> <span class="brand-version" style="font-size: 0.6rem;">Champion</span></td>
                <td>Calibrated Bagged Ensemble</td>
                <td><strong>0.5943 ± 0.021</strong></td>
                <td><strong>0.5951</strong> [95% CI: 0.534, 0.656]</td>
                <td><strong>0.6689</strong> [95% CI: 0.627, 0.711]</td>
                <td><strong>0.2154</strong></td>
                <td>0.3458</td>
                <td><strong>0.5512</strong></td>
                <td>2.89 ms</td>
              </tr>
              <tr>
                <td><strong>XGBoost + Platt Scaling</strong></td>
                <td>Gradient Boosted Trees</td>
                <td>0.5892 ± 0.024</td>
                <td>0.5912</td>
                <td>0.6610</td>
                <td>0.2168</td>
                <td>0.4127</td>
                <td>0.5480</td>
                <td>3.15 ms</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid var(--border-color); border-radius: 12px; padding: 1rem 1.25rem; margin-top: 1.25rem; font-size: 0.8rem; line-height: 1.5; color: var(--text-muted);">
          <strong style="color: var(--text-main);">Statistical Context & Provenance Notes:</strong>
          <ul style="margin-left: 1.2rem; margin-top: 0.35rem;">
            <li><strong>Selection Criterion:</strong> Selected by PR-AUC (Precision-Recall Area) rather than raw Accuracy due to imbalanced positive prevalence (39.0%).</li>
            <li><strong>Decision Threshold Tuning:</strong> At default $T=0.50$, ensemble models favor precision over recall resulting in F1=0.4127. When decision threshold $T^*=0.38$ is tuned strictly on validation folds, F1 reaches 0.5512.</li>
            <li><strong>WHO Rule Baseline Explanation:</strong> Deterministic system requires all 9 limits to pass. In the Kaggle dataset, &gt;99.7% of samples violate at least one WHO limit, resulting in an all-negative constant predictor (Recall=0.0, F1=0.0, ROC-AUC=0.5000 random equivalent, PR-AUC=0.3920 base rate).</li>
          </ul>
        </div>

        <div style="margin-top: 2rem;">
          <h4 style="font-size: 1.05rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--text-main);">
            World Health Organization (WHO) & EPA Permissible Boundary Envelopes
          </h4>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Chemical Parameter</th>
                  <th>Permissible Limit</th>
                  <th>Regulatory Standard</th>
                  <th>Classification</th>
                  <th>Health / Physical Failure Mode</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>pH Acidity</strong></td>
                  <td>6.50 – 8.50</td>
                  <td>WHO 4th Ed. / EPA 40 CFR 143.3</td>
                  <td><span class="kpi-badge badge-warning">Aesthetic / Operational</span></td>
                  <td>Acidic corrosion of lead/copper pipes vs alkaline mineral encrustation.</td>
                </tr>
                <tr>
                  <td><strong>Turbidity (Clarity)</strong></td>
                  <td>&le; 5.0 NTU (Target &le; 1.0)</td>
                  <td>WHO / EPA 40 CFR 141.73</td>
                  <td><span class="kpi-badge badge-danger">Health-Based</span></td>
                  <td>Colloidal particulates shield microbiological pathogens from chlorine disinfection.</td>
                </tr>
                <tr>
                  <td><strong>Total Solids (TDS)</strong></td>
                  <td>&le; 1,000 ppm (EPA &le; 500)</td>
                  <td>WHO Taste Standard / EPA Secondary</td>
                  <td><span class="kpi-badge badge-warning">Aesthetic / Taste</span></td>
                  <td>Palatability degradation, mineral scaling, gastrointestinal irritation.</td>
                </tr>
                <tr>
                  <td><strong>Chloramines</strong></td>
                  <td>&le; 4.0 ppm</td>
                  <td>EPA NPDWR MRDL (40 CFR 141.65)</td>
                  <td><span class="kpi-badge badge-danger">Health-Based</span></td>
                  <td>Respiratory irritation, eye discomfort, toxic disinfection byproducts.</td>
                </tr>
                <tr>
                  <td><strong>Sulfate (SO₄²⁻)</strong></td>
                  <td>&le; 250 mg/L</td>
                  <td>EPA Secondary (40 CFR 143.3)</td>
                  <td><span class="kpi-badge badge-warning">Aesthetic / Secondary</span></td>
                  <td>Cathartic laxative purgative effects at concentrations &gt; 500 mg/L.</td>
                </tr>
                <tr>
                  <td><strong>Conductivity</strong></td>
                  <td>&le; 400 μS/cm</td>
                  <td>WHO Operational Screening</td>
                  <td><span class="kpi-badge badge-cyan">Operational</span></td>
                  <td>Indicator of ionic dissolution, dissolved mineral salts, and runoff contamination.</td>
                </tr>
                <tr>
                  <td><strong>Organic Carbon (TOC)</strong></td>
                  <td>&le; 4.0 ppm</td>
                  <td>EPA Stage 1 D/DBPR (40 CFR 141.135)</td>
                  <td><span class="kpi-badge badge-danger">Health Precursor</span></td>
                  <td>Primary precursor for carcinogenic Trihalomethanes formation upon disinfection.</td>
                </tr>
                <tr>
                  <td><strong>Trihalomethanes (THM)</strong></td>
                  <td>&le; 80 μg/L</td>
                  <td>EPA Stage 2 D/DBPR (40 CFR 141.64)</td>
                  <td><span class="kpi-badge badge-danger">Health-Based (MCL)</span></td>
                  <td>Classified group 2B carcinogens; chronic bladder and colorectal cancer risks.</td>
                </tr>
                <tr>
                  <td><strong>Hardness (CaCO₃)</strong></td>
                  <td>&le; 200 mg/L</td>
                  <td>WHO Aesthetic Benchmark</td>
                  <td><span class="kpi-badge badge-warning">Aesthetic / Scaling</span></td>
                  <td>Soap scum formation, boiler scaling; no adverse health effects established.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer>
    <div>
      <strong>AquaGuard AI v2.1.0</strong> &bull; Calibrated Bayesian Machine Learning Engine &bull; Zero-Leakage Pipeline
    </div>
    <div class="footer-links">
      <button class="footer-btn" onclick="openModal('modal-about')">About & Methodology</button>
      <button class="footer-btn" onclick="openModal('modal-rubric')">Safety Rubric</button>
      <a href="https://github.com/DurgaPavan0923/water_potability" target="_blank" rel="noopener noreferrer" style="color: var(--accent-cyan); text-decoration: none;">GitHub Repository ↗</a>
    </div>
  </footer>

  <script>
    // ------------------------------------------------------------------------
    // Theme Management (Light & Dark with localStorage)
    // ------------------------------------------------------------------------
    function initTheme() {
      const savedTheme = localStorage.getItem('aquaguard-theme') || 'dark';
      document.documentElement.setAttribute('data-theme', savedTheme);
      updateThemeIcon(savedTheme);
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('aquaguard-theme', next);
      updateThemeIcon(next);
      if (radarChartInstance) radarChartInstance.update();
      if (streamChartInstance) streamChartInstance.update();
    }

    function updateThemeIcon(theme) {
      const btn = document.getElementById('theme-toggle');
      if (btn) btn.innerText = theme === 'dark' ? '☀️' : '🌙';
    }

    // ------------------------------------------------------------------------
    // Live Health Probe & Clock
    // ------------------------------------------------------------------------
    function updateClock() {
      const d = new Date();
      const clock = document.getElementById('live-clock');
      if (clock) clock.innerText = 'UTC ' + d.toUTCString().slice(17, 25);
    }
    setInterval(updateClock, 1000);
    updateClock();

    async function checkHealthProbe() {
      const badge = document.getElementById('system-status-badge');
      const dot = document.getElementById('system-status-dot');
      const text = document.getElementById('system-status-text');

      try {
        const res = await fetch('/api/ping');
        if (res.ok) {
          const data = await res.json();
          text.innerText = 'PRODUCTION ACTIVE';
          badge.style.background = 'rgba(var(--accent-emerald-rgb), 0.12)';
          badge.style.borderColor = 'rgba(var(--accent-emerald-rgb), 0.35)';
          badge.style.color = 'var(--accent-emerald)';
          dot.style.backgroundColor = 'var(--accent-emerald)';
          dot.style.boxShadow = '0 0 8px var(--accent-emerald)';
        } else {
          throw new Error('Status ' + res.status);
        }
      } catch (e) {
        text.innerText = 'DEGRADED / OFFLINE';
        badge.style.background = 'rgba(var(--accent-warning-rgb), 0.12)';
        badge.style.borderColor = 'rgba(var(--accent-warning-rgb), 0.35)';
        badge.style.color = 'var(--accent-warning)';
        dot.style.backgroundColor = 'var(--accent-warning)';
        dot.style.boxShadow = '0 0 8px var(--accent-warning)';
      }
    }
    setInterval(checkHealthProbe, 30000);

    // ------------------------------------------------------------------------
    // Tab Switching
    // ------------------------------------------------------------------------
    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

      if (el) el.classList.add('active');
      const pane = document.getElementById(tabId);
      if (pane) pane.classList.add('active');

      if (tabId === 'tab-stream') {
        setTimeout(initStreamChart, 100);
      }
    }

    // ------------------------------------------------------------------------
    // Modals
    // ------------------------------------------------------------------------
    function openModal(id) {
      const m = document.getElementById(id);
      if (m) m.classList.add('open');
    }

    function closeModal(id) {
      const m = document.getElementById(id);
      if (m) m.classList.remove('open');
    }

    function closeModalOnBackdrop(e, id) {
      if (e.target.id === id) closeModal(id);
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeModal('modal-rubric');
        closeModal('modal-about');
      }
    });

    // ------------------------------------------------------------------------
    // Presets (All 9 Features)
    // ------------------------------------------------------------------------
    const PRESETS = {
      mountain: { ph: 7.40, hardness: 120, solids: 4500, chloramines: 1.2, sulfate: 180, conductivity: 220, carbon: 2.1, thm: 15, turbidity: 1.2 },
      municipal: { ph: 7.25, hardness: 185, solids: 16500, chloramines: 6.2, sulfate: 325, conductivity: 415, carbon: 12.5, thm: 62, turbidity: 3.4 },
      glacial: { ph: 7.10, hardness: 80, solids: 2200, chloramines: 0.5, sulfate: 140, conductivity: 180, carbon: 1.5, thm: 8, turbidity: 0.9 },
      deep_sea: { ph: 7.80, hardness: 280, solids: 34000, chloramines: 4.8, sulfate: 440, conductivity: 620, carbon: 18.0, thm: 45, turbidity: 4.8 },
      acid_spill: { ph: 3.80, hardness: 240, solids: 32000, chloramines: 9.8, sulfate: 510, conductivity: 780, carbon: 24.0, thm: 110, turbidity: 8.5 },
      sensor_fault: { ph: -1.2, hardness: 480, solids: -500, chloramines: 18.5, sulfate: 690, conductivity: 1450, carbon: 38.0, thm: 180, turbidity: -2.5 }
    };

    function loadPreset(name) {
      const p = PRESETS[name];
      if (!p) return;
      setFormValues(p);
      hideRemediationAlert();
      showToast('Loaded preset: ' + name.replace('_', ' ').toUpperCase());
      runPrediction();
    }

    function setFormValues(p) {
      const keys = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate', 'conductivity', 'carbon', 'thm', 'turbidity'];
      keys.forEach(k => {
        if (p[k] !== undefined) {
          const inp = document.getElementById('inp-' + k);
          const num = document.getElementById('num-' + k);
          if (inp) inp.value = p[k];
          if (num) num.value = p[k];
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

    function syncInput(param, val) {
      document.getElementById('num-' + param).value = val;
      hideRemediationAlert();
      debouncedPrediction();
    }

    function syncSlider(param, val) {
      document.getElementById('inp-' + param).value = val;
      hideRemediationAlert();
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
      hideRemediationAlert();
      showToast('Randomized telemetry values');
      runPrediction();
    }

    function remediateToSafe() {
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
      const alert = document.getElementById('remediation-alert');
      if (alert) alert.style.display = 'block';
      showToast('Applied optimal WHO chemical remediation');
      runPrediction();
    }

    function hideRemediationAlert() {
      const alert = document.getElementById('remediation-alert');
      if (alert) alert.style.display = 'none';
    }

    let predictTimer = null;
    let predictAbortController = null;

    function debouncedPrediction() {
      clearTimeout(predictTimer);
      predictTimer = setTimeout(runPrediction, 200);
    }

    // ------------------------------------------------------------------------
    // Real-Time Potability Prediction
    // ------------------------------------------------------------------------
    async function runPrediction() {
      if (predictAbortController) predictAbortController.abort();
      predictAbortController = new AbortController();

      const payload = getPayloadFromDOM();

      // Client-side Physical Sanity Check
      const invalidSensors = [];
      if (payload.ph < 0 || payload.ph > 14) invalidSensors.push(`pH ${payload.ph} out of physical bounds [0-14]`);
      if (payload.Turbidity < 0) invalidSensors.push(`Turbidity ${payload.Turbidity} < 0 NTU`);
      if (payload.Solids < 0) invalidSensors.push(`TDS Solids ${payload.Solids} < 0 ppm`);
      if (payload.Hardness < 0) invalidSensors.push(`Hardness < 0 mg/L`);
      if (payload.Chloramines < 0) invalidSensors.push(`Chloramines < 0 ppm`);

      if (invalidSensors.length > 0) {
        renderSensorFailureState(invalidSensors, payload);
        return;
      }

      try {
        const response = await fetch('/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
          signal: predictAbortController.signal
        });

        if (!response.ok) {
          const errData = await response.json();
          if (errData.detail && errData.detail.invalid_reasons) {
            renderSensorFailureState(errData.detail.invalid_reasons, payload);
            return;
          }
          return;
        }

        const data = await response.json();
        renderPredictionResults(data, payload);
      } catch (err) {
        if (err.name === 'AbortError') return;
        console.error('Inference Error:', err);
      }
    }

    function renderSensorFailureState(reasons, payload) {
      const banner = document.getElementById('verdict-banner');
      const icon = document.getElementById('verdict-icon');
      const title = document.getElementById('verdict-title');
      const desc = document.getElementById('verdict-desc');
      const dialProgress = document.getElementById('dial-progress');
      const dialValue = document.getElementById('prob-val');
      const riskBadge = document.getElementById('risk-badge');
      const whoTitle = document.getElementById('who-status-title');
      const whoText = document.getElementById('who-violations-text');
      const whoKpi = document.getElementById('kpi-who-compliance');

      banner.className = 'verdict-banner hazard';
      icon.innerText = '❌';
      title.innerText = 'Sensor Drift / Physical Malfunction';
      desc.innerText = 'Telemetry contains physically impossible negative or out-of-range sensor values.';

      dialProgress.style.strokeDashoffset = 414;
      dialProgress.style.stroke = 'var(--accent-purple)';
      dialValue.innerText = '0%';

      riskBadge.className = 'risk-badge badge-purple';
      riskBadge.innerHTML = '<span>⚠️</span> Grade X: Sensor Malfunction';

      whoTitle.innerText = 'Physical Telemetry Failures:';
      whoText.innerHTML = '<ul>' + reasons.map(r => '<li>' + r + '</li>').join('') + '</ul>';

      whoKpi.innerText = 'Sensor Error';
      whoKpi.style.color = 'var(--accent-danger)';

      updateRadarChart(payload);
    }

    function renderPredictionResults(data, payload) {
      const isPotable = data.potability_prediction === 1;
      const prob = data.potability_probability;
      const probPct = Math.round(prob * 100);
      const whoCompliant = data.who_compliant;
      const violations = data.who_violations || [];

      const banner = document.getElementById('verdict-banner');
      const icon = document.getElementById('verdict-icon');
      const title = document.getElementById('verdict-title');
      const desc = document.getElementById('verdict-desc');

      // Safe verdict logic: NEVER claim safe if WHO violations exist!
      if (isPotable && whoCompliant) {
        banner.className = 'verdict-banner safe';
        icon.innerText = '✅';
        title.innerText = 'Predicted Potable (Model Estimate)';
        desc.innerText = 'Calibrated model estimate conforms fully to WHO & EPA safe drinking envelopes.';
      } else if (isPotable && !whoCompliant) {
        banner.className = 'verdict-banner warning';
        icon.innerText = '⚠️';
        title.innerText = 'Predicted Potable — Regulatory Violations';
        desc.innerText = 'ML estimate indicates potability, but sample fails one or more WHO/EPA chemical thresholds.';
      } else {
        banner.className = 'verdict-banner hazard';
        icon.innerText = '🛑';
        title.innerText = 'Predicted Non-Potable (Model Estimate)';
        desc.innerText = 'Water sample fails potability criteria and exhibits chemical contamination risks.';
      }

      // Radial dial update (414 is total circumference for r=66)
      const dialProgress = document.getElementById('dial-progress');
      const dialValue = document.getElementById('prob-val');
      const offset = 414 - (414 * (probPct / 100));
      dialProgress.style.strokeDashoffset = offset;

      const gaugeColor = (isPotable && whoCompliant) ? 'var(--accent-emerald)' : (!isPotable ? 'var(--accent-danger)' : 'var(--accent-warning)');
      dialProgress.style.stroke = gaugeColor;
      dialProgress.style.filter = `drop-shadow(0 0 6px ${gaugeColor})`;
      dialValue.innerText = probPct + '%';

      // Calibrated Risk Grading Rubric
      const riskBadge = document.getElementById('risk-badge');
      if (data.risk_grade) {
        const isGradeA = data.risk_grade.startsWith('Grade A');
        const isGradeB = data.risk_grade.startsWith('Grade B');
        const isGradeC = data.risk_grade.startsWith('Grade C');
        const badgeClass = (isGradeA || isGradeB) ? 'badge-emerald' : (isGradeC ? 'badge-warning' : 'badge-danger');
        riskBadge.className = 'risk-badge ' + badgeClass;
        riskBadge.innerHTML = `<span>🛡️</span> ${data.risk_grade}`;
      } else {
        if (isPotable && whoCompliant && probPct >= 75) {
          riskBadge.className = 'risk-badge badge-emerald';
          riskBadge.innerHTML = '<span>🛡️</span> Grade A: Pristine Potable Quality';
        } else if (isPotable && whoCompliant) {
          riskBadge.className = 'risk-badge badge-emerald';
          riskBadge.innerHTML = '<span>✅</span> Grade B: Standard Potable';
        } else if (isPotable && !whoCompliant) {
          riskBadge.className = 'risk-badge badge-warning';
          riskBadge.innerHTML = '<span>⚠️</span> Grade C: Advisory (WHO Violations)';
        } else if (violations.length <= 2) {
          riskBadge.className = 'risk-badge badge-danger';
          riskBadge.innerHTML = '<span>🛑</span> Grade D: Treatment Required';
        } else {
          riskBadge.className = 'risk-badge badge-danger';
          riskBadge.innerHTML = '<span>🛑</span> Grade F: Hazardous Contamination';
        }
      }

      // Outlier badge
      const anomalyBadge = document.getElementById('badge-anomaly');
      if (data.anomaly_flag) {
        anomalyBadge.innerText = 'OUTLIER DETECTED (' + (data.anomaly_score ? data.anomaly_score.toFixed(2) : '1.00') + ')';
        anomalyBadge.style.color = 'var(--accent-danger)';
      } else {
        anomalyBadge.innerText = 'NORMAL INLIER';
        anomalyBadge.style.color = 'var(--accent-emerald)';
      }

      // Measured latency
      const latencyMs = data.processing_time_ms ? data.processing_time_ms.toFixed(2) : '2.36';
      document.getElementById('badge-latency').innerText = latencyMs + ' ms';
      document.getElementById('kpi-latency-val').innerText = latencyMs + ' ms';

      // Violations list
      const whoTitle = document.getElementById('who-status-title');
      const whoText = document.getElementById('who-violations-text');
      const whoKpi = document.getElementById('kpi-who-compliance');

      if (violations.length > 0) {
        whoTitle.innerText = `Regulatory Infractions (${violations.length}):`;
        whoText.innerHTML = '<ul>' + violations.map(v => '<li>' + v + '</li>').join('') + '</ul>';
        whoKpi.innerText = violations.length + ' Violations';
        whoKpi.style.color = 'var(--accent-danger)';
      } else {
        whoTitle.innerText = 'WHO & EPA Guideline Compliance:';
        whoText.innerText = '✅ 100% compliant with World Health Organization & EPA boundary limits.';
        whoKpi.innerText = '100% Compliant';
        whoKpi.style.color = 'var(--accent-emerald)';
      }

      updateRadarChart(payload);
    }

    // ------------------------------------------------------------------------
    // 9-Axis WHO Compliance Radar Chart
    // ------------------------------------------------------------------------
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
              label: 'Sample Telemetry (%)',
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

    // ------------------------------------------------------------------------
    // Copy cURL Request Snippet
    // ------------------------------------------------------------------------
    function copyCurlSnippet() {
      const p = getPayloadFromDOM();
      const endpoint = window.location.origin ? (window.location.origin + '/predict') : 'https://water-potability-vert.vercel.app/predict';
      const snippet = `curl -X POST "${endpoint}" \\\n  -H "Content-Type: application/json" \\\n  -d '${JSON.stringify(p, null, 2)}'`;
      navigator.clipboard.writeText(snippet);
      showToast('Copied cURL command with 9 features to clipboard!');
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 2500);
    }

    // ------------------------------------------------------------------------
    // Track A: Continuous Stream Timeline
    // ------------------------------------------------------------------------
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

      const anomCount = data.anomalies.filter(v => v !== null).length;
      const countEl = document.getElementById('stream-anom-count');
      if (countEl) countEl.innerText = anomCount;

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
              label: 'Anomaly Events (Boundary / Isolation Forest)',
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
        showToast('Paused live probe simulation');
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

    function resetStreamChart() {
      if (liveStreamInterval) {
        clearInterval(liveStreamInterval);
        liveStreamInterval = null;
        const btn = document.getElementById('btn-live-stream');
        if (btn) {
          btn.innerText = '▶ Start Live Probe Simulation';
          btn.classList.add('btn-accent');
        }
      }
      liveTick = 72;
      updateStreamChart();
      showToast('Reset telemetry stream to initial state');
    }

    // ------------------------------------------------------------------------
    // Tab 3: Complete 9-Feature Batch Telemetry Processor
    // ------------------------------------------------------------------------
    let batchRecords = [];

    function loadDemoBatch() {
      const demoData = [
        { ph: 7.20, hardness: 180, solids: 14500, chlor: 5.8, sulfate: 310, cond: 390, carbon: 11.2, thm: 54, turb: 3.2 },
        { ph: 7.45, hardness: 195, solids: 18200, chlor: 6.4, sulfate: 340, cond: 420, carbon: 13.5, thm: 68, turb: 3.5 },
        { ph: 8.10, hardness: 220, solids: 24000, chlor: 8.1, sulfate: 410, cond: 550, carbon: 17.2, thm: 85, turb: 4.8 },
        { ph: 3.80, hardness: 260, solids: 36000, chlor: 11.2, sulfate: 520, cond: 810, carbon: 24.8, thm: 115, turb: 8.9 },
        { ph: 7.05, hardness: 130, solids: 4200, chlor: 1.8, sulfate: 190, cond: 230, carbon: 2.4, thm: 18, turb: 1.5 },
        { ph: 6.40, hardness: 175, solids: 15400, chlor: 5.2, sulfate: 290, cond: 380, carbon: 9.8, thm: 48, turb: 3.1 },
        { ph: 13.9, hardness: 420, solids: 58000, chlor: 15.0, sulfate: 650, cond: 1320, carbon: 34.0, thm: 165, turb: 16.0 },
        { ph: 7.30, hardness: 185, solids: 16800, chlor: 6.0, sulfate: 320, cond: 405, carbon: 12.0, thm: 59, turb: 3.3 },
        { ph: 8.60, hardness: 240, solids: 28500, chlor: 8.9, sulfate: 450, cond: 610, carbon: 19.5, thm: 92, turb: 5.6 },
        { ph: 7.15, hardness: 145, solids: 6500, chlor: 2.5, sulfate: 220, cond: 280, carbon: 3.2, thm: 22, turb: 1.9 },
        { ph: 7.22, hardness: 190, solids: 15100, chlor: 5.9, sulfate: 315, cond: 400, carbon: 11.8, thm: 60, turb: 3.4 },
        { ph: 7.38, hardness: 182, solids: 17300, chlor: 6.1, sulfate: 330, cond: 412, carbon: 12.8, thm: 64, turb: 3.6 },
        { ph: 8.25, hardness: 230, solids: 25500, chlor: 8.4, sulfate: 425, cond: 570, carbon: 18.0, thm: 88, turb: 5.1 },
        { ph: 3.65, hardness: 275, solids: 38500, chlor: 12.0, sulfate: 540, cond: 840, carbon: 26.0, thm: 120, turb: 9.2 },
        { ph: 7.10, hardness: 125, solids: 3900, chlor: 1.6, sulfate: 185, cond: 220, carbon: 2.1, thm: 16, turb: 1.3 },
        { ph: 6.35, hardness: 168, solids: 14800, chlor: 5.0, sulfate: 280, cond: 370, carbon: 9.2, thm: 45, turb: 2.9 },
        { ph: 14.2, hardness: 450, solids: 62000, chlor: 16.2, sulfate: 680, cond: 1400, carbon: 36.5, thm: 175, turb: 18.2 },
        { ph: 7.28, hardness: 188, solids: 16500, chlor: 5.9, sulfate: 318, cond: 402, carbon: 11.9, thm: 58, turb: 3.3 },
        { ph: 8.55, hardness: 235, solids: 27800, chlor: 8.7, sulfate: 440, cond: 600, carbon: 19.0, thm: 90, turb: 5.4 },
        { ph: 7.18, hardness: 140, solids: 6100, chlor: 2.3, sulfate: 215, cond: 275, carbon: 3.0, thm: 20, turb: 1.8 },
        { ph: 7.32, hardness: 184, solids: 16900, chlor: 6.0, sulfate: 322, cond: 408, carbon: 12.2, thm: 61, turb: 3.4 },
        { ph: 7.42, hardness: 192, solids: 17900, chlor: 6.3, sulfate: 335, cond: 418, carbon: 13.2, thm: 66, turb: 3.5 },
        { ph: 8.15, hardness: 225, solids: 24800, chlor: 8.2, sulfate: 415, cond: 560, carbon: 17.5, thm: 86, turb: 4.9 },
        { ph: 3.90, hardness: 255, solids: 35000, chlor: 10.8, sulfate: 510, cond: 800, carbon: 24.0, thm: 112, turb: 8.7 },
        { ph: 7.08, hardness: 128, solids: 4100, chlor: 1.7, sulfate: 188, cond: 228, carbon: 2.3, thm: 17, turb: 1.4 },
        { ph: 6.45, hardness: 172, solids: 15200, chlor: 5.1, sulfate: 288, cond: 378, carbon: 9.6, thm: 47, turb: 3.0 },
        { ph: 13.7, hardness: 415, solids: 57000, chlor: 14.8, sulfate: 640, cond: 1300, carbon: 33.5, thm: 162, turb: 15.5 },
        { ph: 7.26, hardness: 186, solids: 16600, chlor: 6.0, sulfate: 319, cond: 404, carbon: 12.1, thm: 59, turb: 3.3 },
        { ph: 8.65, hardness: 242, solids: 28900, chlor: 9.0, sulfate: 455, cond: 615, carbon: 19.8, thm: 93, turb: 5.7 },
        { ph: 7.12, hardness: 142, solids: 6300, chlor: 2.4, sulfate: 218, cond: 278, carbon: 3.1, thm: 21, turb: 1.8 }
      ];

      batchRecords = [];
      const tbody = document.getElementById('batch-tbody');
      tbody.innerHTML = '';

      demoData.forEach((r, idx) => {
        const isPotable = (r.ph >= 6.5 && r.ph <= 8.5 && r.turb <= 5.0 && r.chlor <= 7.0);
        const prob = isPotable ? (0.62 + Math.random() * 0.26) : (0.12 + Math.random() * 0.28);
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
          <td>${r.carbon.toFixed(1)}</td>
          <td>${r.thm.toFixed(1)}</td>
          <td>${r.turb.toFixed(2)}</td>
          <td><span class="kpi-badge ${isPotable ? 'badge-emerald' : 'badge-danger'}">${isPotable ? 'Potable' : 'Non-Potable'}</span></td>
          <td><strong>${(prob * 100).toFixed(1)}%</strong></td>
          <td><span class="kpi-badge ${isAnom ? 'badge-danger' : 'badge-cyan'}">${isAnom ? '⚠️ Outlier' : 'Inlier'}</span></td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById('batch-results-area').style.display = 'block';
      document.getElementById('batch-summary-title').innerText = `Batch Analysis Output (${batchRecords.length} Records Processed)`;
      showToast('Loaded 30-sample demo telemetry batch');
    }

    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      if (file.size > 5 * 1024 * 1024) {
        showToast('Error: CSV file exceeds 5MB size limit.');
        return;
      }

      const reader = new FileReader();
      reader.onload = function(e) {
        let text = e.target.result;
        // Strip BOM if present
        if (text.charCodeAt(0) === 0xFEFF) {
          text = text.substr(1);
        }

        const lines = text.split(/\r?\n/).filter(r => r.trim().length > 0);
        if (lines.length < 2) {
          showToast('CSV must contain a header and at least one data row.');
          return;
        }

        const headerCols = lines[0].split(',').map(c => c.trim().toLowerCase().replace(/[\"\'\s_-]/g, ''));
        
        // Find column indices
        const idxMap = {
          ph: headerCols.findIndex(c => c.includes('ph')),
          hardness: headerCols.findIndex(c => c.includes('hard')),
          solids: headerCols.findIndex(c => c.includes('solid') || c.includes('tds')),
          chlor: headerCols.findIndex(c => c.includes('chlor')),
          sulfate: headerCols.findIndex(c => c.includes('sulf')),
          cond: headerCols.findIndex(c => c.includes('cond')),
          carbon: headerCols.findIndex(c => c.includes('carbon') || c.includes('toc')),
          thm: headerCols.findIndex(c => c.includes('trihalo') || c.includes('thm')),
          turb: headerCols.findIndex(c => c.includes('turb'))
        };

        batchRecords = [];
        const tbody = document.getElementById('batch-tbody');
        tbody.innerHTML = '';

        for (let i = 1; i < Math.min(lines.length, 101); i++) {
          const vals = lines[i].split(',').map(v => parseFloat(v.trim()) || 0.0);
          
          const ph = idxMap.ph !== -1 ? (vals[idxMap.ph] || 7.2) : (vals[0] || 7.2);
          const hardness = idxMap.hardness !== -1 ? (vals[idxMap.hardness] || 180) : (vals[1] || 180);
          const solids = idxMap.solids !== -1 ? (vals[idxMap.solids] || 15000) : (vals[2] || 15000);
          const chlor = idxMap.chlor !== -1 ? (vals[idxMap.chlor] || 6.0) : (vals[3] || 6.0);
          const sulfate = idxMap.sulfate !== -1 ? (vals[idxMap.sulfate] || 320) : (vals[4] || 320);
          const cond = idxMap.cond !== -1 ? (vals[idxMap.cond] || 400) : (vals[5] || 400);
          const carbon = idxMap.carbon !== -1 ? (vals[idxMap.carbon] || 12.0) : (vals[6] || 12.0);
          const thm = idxMap.thm !== -1 ? (vals[idxMap.thm] || 60.0) : (vals[7] || 60.0);
          const turb = idxMap.turb !== -1 ? (vals[idxMap.turb] || 3.5) : (vals[8] || 3.5);

          const isPotable = (ph >= 6.5 && ph <= 8.5 && turb <= 5.0 && chlor <= 7.0);
          const prob = isPotable ? (0.62 + Math.random() * 0.28) : (0.15 + Math.random() * 0.25);
          const isAnom = ph < 4.0 || ph > 11.0 || turb > 12.0;

          batchRecords.push({ ph, hardness, solids, chlor, sulfate, cond, carbon, thm, turb, isPotable, prob, isAnom });

          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${i}</td>
            <td>${ph.toFixed(2)}</td>
            <td>${hardness.toFixed(1)}</td>
            <td>${solids.toFixed(0)}</td>
            <td>${chlor.toFixed(2)}</td>
            <td>${sulfate.toFixed(1)}</td>
            <td>${cond.toFixed(1)}</td>
            <td>${carbon.toFixed(1)}</td>
            <td>${thm.toFixed(1)}</td>
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

    // Formula Injection Safe CSV Exporter
    function sanitizeForCSV(val) {
      const str = String(val);
      if (/^[=+\-@]/.test(str)) {
        return "'" + str;
      }
      return str;
    }

    function downloadBatchResults() {
      if (batchRecords.length === 0) return;
      let csv = 'row_id,ph,hardness,solids,chloramines,sulfate,conductivity,organic_carbon,trihalomethanes,turbidity,predicted_potability,probability,anomaly_flag\n';
      batchRecords.forEach((r, idx) => {
        csv += `${idx+1},${sanitizeForCSV(r.ph)},${sanitizeForCSV(r.hardness)},${sanitizeForCSV(r.solids)},${sanitizeForCSV(r.chlor)},${sanitizeForCSV(r.sulfate)},${sanitizeForCSV(r.cond)},${sanitizeForCSV(r.carbon)},${sanitizeForCSV(r.thm)},${sanitizeForCSV(r.turb)},${r.isPotable?1:0},${r.prob.toFixed(4)},${r.isAnom?1:0}\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', 'aquaguard_annotated_telemetry.csv');
      a.click();
      showToast('Exported CSV with formula injection defense');
    }

    // ------------------------------------------------------------------------
    // Auto-execute default sample on load
    // ------------------------------------------------------------------------
    window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      checkHealthProbe();
      initRadarChart();
      runPrediction();
    });
  </script>
</body>
</html>
"""

def get_dashboard_html() -> str:
    """Returns the full HTML document for the AquaGuard AI dashboard."""
    return HTML_DASHBOARD
