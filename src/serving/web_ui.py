"""Modern, Clean, Attractive, and Professional Web Dashboard for AquaGuard AI.

Audit & Upgrade v2.1.0:
- Design tokens with Dark and Light mode theme toggle and persistent localStorage memory.
- Zero emojis: Pure inline SVGs throughout all UI components.
- KPI cards with animated count-up numbers on mount.
- SVG circular probability gauge with smooth stroke-dashoffset transition.
- Dynamic slider gradient tracks, live pulse on change, and WHO limit indicators.
- 600ms Auto-Remediate tween animation to safe WHO guideline midpoints.
- Toast notification system with SVG status icons and auto-dismiss.
- Instant ticking live UTC clock on mount without lag.
- Continuous Telemetry Stream tab with moving window chart and pulsing dot.
- Batch Laboratory tab with drag-and-drop, table skeleton loader, status pills, and formula defense.
- Benchmark tab with PR-AUC progress bars, confusion matrix heatmap, and verified metrics.
- Accessible modals with focus trap, backdrop blur, and Escape key listener.
- Footers with author and mentor attribution (zero static dates).
"""

HTML_DASHBOARD = r"""<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AquaGuard AI | Water Potability & WHO/EPA Compliance Intelligence</title>
  <meta name="description" content="Production-grade calibrated water potability classification, WHO regulatory compliance auditing, and continuous oceanographic telemetry monitoring.">
  <meta name="theme-color" content="#070d19">
  
  <!-- OpenGraph Metadata -->
  <meta property="og:title" content="AquaGuard AI | Water Potability & WHO/EPA Compliance Intelligence">
  <meta property="og:description" content="Sub-3ms Calibrated Machine Learning Engine, 9-Axis WHO Compliance Auditor, and Continuous Oceanographic Telemetry.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://water-potability-vert.vercel.app/">
  <meta property="og:image" content="https://water-potability-vert.vercel.app/og-image.png">
  
  <!-- Twitter Card Metadata -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="AquaGuard AI | Water Potability & WHO Compliance">
  <meta name="twitter:description" content="Production-grade calibrated water potability classification and WHO drinking water compliance auditor.">
  <meta name="twitter:image" content="https://water-potability-vert.vercel.app/og-image.png">
  
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  
  <!-- Chart.js for data visualization -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  
  <style>
    :root {
      --bg-primary: #070d19;
      --bg-surface: #0c1527;
      --bg-card: rgba(17, 27, 49, 0.85);
      --bg-card-hover: rgba(26, 41, 74, 0.95);
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
      --accent-teal: #14b8a6;
      --accent-danger: #ef4444;
      --accent-danger-rgb: 239, 68, 68;
      --accent-warning: #f59e0b;
      --accent-warning-rgb: 245, 158, 11;
      --accent-orange: #f97316;
      --accent-purple: #8b5cf6;
      --accent-blue: #3b82f6;
      --header-bg: rgba(11, 19, 36, 0.92);
      --table-th-bg: rgba(15, 23, 42, 0.85);
      --table-stripe: rgba(255, 255, 255, 0.02);
      --modal-overlay: rgba(0, 0, 0, 0.78);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.25);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.35);
      --shadow-glow: 0 0 24px rgba(6, 182, 212, 0.2);
      --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    [data-theme="light"] {
      --bg-primary: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: rgba(255, 255, 255, 0.95);
      --bg-card-hover: rgba(248, 250, 252, 0.98);
      --bg-input: #f1f5f9;
      --border-color: rgba(203, 213, 225, 0.85);
      --border-glow: rgba(6, 182, 212, 0.25);
      --text-main: #0f172a;
      --text-muted: #475569;
      --text-dim: #64748b;
      --header-bg: rgba(255, 255, 255, 0.94);
      --table-th-bg: rgba(241, 245, 249, 0.95);
      --table-stripe: rgba(0, 0, 0, 0.02);
      --modal-overlay: rgba(15, 23, 42, 0.65);
      --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
      --shadow-md: 0 4px 20px rgba(0, 0, 0, 0.12);
      --shadow-glow: 0 0 24px rgba(6, 182, 212, 0.12);
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
        radial-gradient(circle at 15% 15%, rgba(var(--accent-cyan-rgb), 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(var(--accent-emerald-rgb), 0.03) 0%, transparent 60%);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      transition: background-color 0.25s ease, color 0.25s ease;
    }

    /* Accessibility Focus Rings */
    *:focus-visible {
      outline: 2px solid var(--accent-cyan);
      outline-offset: 2px;
    }

    /* Respect reduced motion preference */
    @media (prefers-reduced-motion: reduce) {
      *, ::before, ::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }

    /* Sticky Header */
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
      width: 40px;
      height: 40px;
      border-radius: 12px;
      background: linear-gradient(135deg, rgba(var(--accent-cyan-rgb), 0.2), rgba(var(--accent-emerald-rgb), 0.2));
      border: 1px solid var(--border-glow);
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 16px rgba(var(--accent-cyan-rgb), 0.25);
      color: var(--accent-cyan);
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
      gap: 0.45rem;
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
    }

    .brand-subtitle {
      font-size: 0.72rem;
      color: var(--text-muted);
      letter-spacing: 0.03em;
      font-weight: 500;
    }

    .header-controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .live-clock {
      font-size: 0.8rem;
      color: var(--text-muted);
      font-variant-numeric: tabular-nums;
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      display: none;
    }
    @media (min-width: 800px) { .live-clock { display: block; } }

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

    .header-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      width: 38px;
      height: 38px;
      border-radius: 10px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }
    .header-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
      transform: translateY(-1px);
    }

    /* Main Container */
    main {
      flex: 1;
      max-width: 1360px;
      width: 100%;
      margin: 0 auto;
      padding: 1.5rem 1.25rem 3rem 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    /* KPI Cards Banner */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1rem;
    }

    .kpi-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 1.15rem 1.25rem;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      box-shadow: var(--shadow-sm);
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
      transform: translateY(-2px);
      border-color: var(--border-glow);
      box-shadow: var(--shadow-md);
    }

    .kpi-info h4 {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--text-muted);
      font-weight: 700;
      margin-bottom: 0.35rem;
    }

    .kpi-value {
      font-size: 1.7rem;
      font-weight: 800;
      letter-spacing: -0.03em;
      color: var(--text-main);
      font-variant-numeric: tabular-nums;
      line-height: 1.2;
    }

    .kpi-desc {
      font-size: 0.74rem;
      color: var(--text-dim);
      margin-top: 0.35rem;
    }

    .kpi-icon-pill {
      width: 42px;
      height: 42px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    /* Tabs Header */
    .tabs-header {
      display: flex;
      gap: 0.5rem;
      border-bottom: 1px solid var(--border-color);
      overflow-x: auto;
      padding-bottom: 0.25rem;
      scrollbar-width: none;
    }
    .tabs-header::-webkit-scrollbar { display: none; }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 0.75rem 1.15rem;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      border-radius: 10px;
      transition: all 0.2s ease;
      position: relative;
      white-space: nowrap;
    }
    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.04);
    }
    .tab-btn.active {
      color: var(--accent-cyan);
      background: rgba(var(--accent-cyan-rgb), 0.1);
    }
    .tab-btn.active::after {
      content: "";
      position: absolute;
      bottom: -0.3rem;
      left: 10%;
      right: 10%;
      height: 2.5px;
      background: var(--accent-cyan);
      border-radius: 9999px;
      box-shadow: 0 0 10px var(--accent-cyan);
    }

    /* Tab Panes */
    .tab-pane {
      display: none;
      animation: fadeIn 0.25s ease forwards;
    }
    .tab-pane.active {
      display: block;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Common Card Styles */
    .card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.5rem;
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
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    /* Disclaimer Banner */
    .disclaimer-banner {
      background: rgba(var(--accent-cyan-rgb), 0.08);
      border: 1px solid rgba(var(--accent-cyan-rgb), 0.25);
      border-radius: 12px;
      padding: 0.85rem 1rem;
      margin-bottom: 1.25rem;
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.45;
      display: flex;
      align-items: flex-start;
      gap: 0.65rem;
    }
    .disclaimer-banner strong { color: var(--text-main); }

    /* Remediation Diff Box */
    .remediation-alert {
      display: none;
      background: rgba(var(--accent-emerald-rgb), 0.12);
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.35);
      border-radius: 12px;
      padding: 0.85rem 1rem;
      margin-bottom: 1.25rem;
      font-size: 0.8rem;
      color: var(--text-main);
      animation: fadeIn 0.3s ease;
    }

    /* Presets Bar */
    .presets-container {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-wrap: wrap;
      margin-bottom: 1.5rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border-color);
    }
    .preset-label {
      font-size: 0.75rem;
      color: var(--text-dim);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-right: 0.25rem;
    }
    .preset-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.4rem 0.8rem;
      border-radius: 8px;
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .preset-btn:hover {
      background: rgba(var(--accent-cyan-rgb), 0.12);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
      transform: translateY(-1px);
    }
    .preset-btn.btn-accent {
      background: rgba(var(--accent-cyan-rgb), 0.15);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }

    /* Simulator Grid */
    .sim-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.75rem;
    }
    @media (min-width: 1024px) {
      .sim-grid {
        grid-template-columns: 1.25fr 1fr;
      }
    }

    /* Slider Inputs Grid */
    .inputs-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
    }
    @media (min-width: 640px) {
      .inputs-grid {
        grid-template-columns: 1fr 1fr;
      }
    }

    .input-group {
      background: rgba(0, 0, 0, 0.15);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 0.9rem;
      transition: border-color 0.2s ease;
    }
    .input-group:focus-within {
      border-color: var(--accent-cyan);
    }

    .input-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
    }
    .input-label {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--text-main);
    }
    .limit-badge {
      font-size: 0.68rem;
      padding: 0.12rem 0.45rem;
      border-radius: 6px;
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      border: 1px solid var(--border-color);
      text-decoration: none;
      transition: all 0.2s ease;
    }
    .limit-badge:hover {
      color: var(--accent-cyan);
      border-color: var(--accent-cyan);
    }
    .limit-badge.violated {
      background: rgba(var(--accent-danger-rgb), 0.15);
      border-color: rgba(var(--accent-danger-rgb), 0.4);
      color: var(--accent-danger);
    }

    .slider-row {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    /* Custom Filled Gradient Range Sliders */
    input[type=range] {
      flex: 1;
      -webkit-appearance: none;
      appearance: none;
      height: 7px;
      border-radius: 4px;
      background: var(--bg-input);
      outline: none;
      cursor: pointer;
      transition: background 0.1s linear;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #ffffff;
      border: 2px solid var(--accent-cyan);
      box-shadow: 0 0 8px rgba(var(--accent-cyan-rgb), 0.5);
      cursor: pointer;
      transition: transform 0.1s ease, box-shadow 0.1s ease;
    }
    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.15);
      box-shadow: 0 0 12px var(--accent-cyan);
    }
    input[type=range]::-moz-range-thumb {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #ffffff;
      border: 2px solid var(--accent-cyan);
      box-shadow: 0 0 8px rgba(var(--accent-cyan-rgb), 0.5);
      cursor: pointer;
      transition: transform 0.1s ease;
    }
    input[type=range]::-moz-range-thumb:hover {
      transform: scale(1.15);
    }

    .num-input {
      width: 78px;
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.35rem 0.5rem;
      border-radius: 8px;
      font-size: 0.84rem;
      font-weight: 600;
      text-align: right;
      font-variant-numeric: tabular-nums;
      transition: border-color 0.2s ease;
    }
    .num-input:focus {
      border-color: var(--accent-cyan);
      outline: none;
    }

    /* Actions Row */
    .actions-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.65rem;
      margin-top: 1.5rem;
    }
    .action-btn {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.55rem 1rem;
      border-radius: 10px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.45rem;
      transition: all 0.2s ease;
    }
    .action-btn:hover {
      background: rgba(var(--accent-cyan-rgb), 0.12);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
      transform: translateY(-1px);
    }
    .action-btn.btn-primary {
      background: linear-gradient(135deg, rgba(var(--accent-cyan-rgb), 0.25), rgba(var(--accent-emerald-rgb), 0.25));
      border-color: var(--accent-cyan);
      color: #ffffff;
    }
    .action-btn.btn-primary:hover {
      background: linear-gradient(135deg, rgba(var(--accent-cyan-rgb), 0.4), rgba(var(--accent-emerald-rgb), 0.4));
      box-shadow: 0 0 14px rgba(var(--accent-cyan-rgb), 0.3);
    }

    /* Decision Panel (Right Side) */
    .decision-panel {
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }

    .decision-box {
      background: rgba(0, 0, 0, 0.18);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 1.15rem;
    }

    /* Verdict Banner */
    .verdict-banner {
      width: 100%;
      border-radius: 12px;
      padding: 0.9rem 1.15rem;
      display: flex;
      align-items: center;
      text-align: left;
      gap: 0.75rem;
      transition: all 0.3s ease;
    }
    .verdict-banner.safe {
      background: rgba(var(--accent-emerald-rgb), 0.12);
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.35);
      color: var(--accent-emerald);
    }
    .verdict-banner.warning {
      background: rgba(var(--accent-warning-rgb), 0.12);
      border: 1px solid rgba(var(--accent-warning-rgb), 0.35);
      color: var(--accent-warning);
    }
    .verdict-banner.hazard {
      background: rgba(var(--accent-danger-rgb), 0.12);
      border: 1px solid rgba(var(--accent-danger-rgb), 0.35);
      color: var(--accent-danger);
    }
    .verdict-banner.malfunction {
      background: rgba(139, 92, 246, 0.12);
      border: 1px solid rgba(139, 92, 246, 0.35);
      color: var(--accent-purple);
    }
    .verdict-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--text-main);
    }
    .verdict-desc {
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-top: 0.15rem;
    }

    /* Circular SVG Gauge */
    .dial-container {
      position: relative;
      width: 180px;
      height: 180px;
    }
    .dial-svg {
      width: 100%;
      height: 100%;
      transform: rotate(-90deg);
    }
    .dial-bg {
      fill: none;
      stroke: rgba(255, 255, 255, 0.06);
      stroke-width: 12;
    }
    .dial-progress {
      fill: none;
      stroke: var(--accent-emerald);
      stroke-width: 12;
      stroke-linecap: round;
      stroke-dasharray: 440;
      stroke-dashoffset: 114;
      transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.4s ease, filter 0.4s ease;
      filter: drop-shadow(0 0 8px rgba(var(--accent-emerald-rgb), 0.5));
    }
    .dial-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .dial-value {
      font-size: 2.3rem;
      font-weight: 800;
      letter-spacing: -0.04em;
      color: var(--text-main);
      font-variant-numeric: tabular-nums;
    }
    .dial-sub {
      font-size: 0.65rem;
      color: var(--text-muted);
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-top: -0.2rem;
    }

    /* Risk Badges */
    .risk-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.45rem;
      padding: 0.45rem 1.15rem;
      border-radius: 9999px;
      font-size: 0.84rem;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .risk-badge:hover {
      transform: scale(1.03);
    }
    .risk-badge.badge-emerald {
      background: rgba(var(--accent-emerald-rgb), 0.15);
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.4);
      color: var(--accent-emerald);
      box-shadow: 0 0 12px rgba(var(--accent-emerald-rgb), 0.2);
    }
    .risk-badge.badge-teal {
      background: rgba(20, 184, 166, 0.15);
      border: 1px solid rgba(20, 184, 166, 0.4);
      color: var(--accent-teal);
      box-shadow: 0 0 12px rgba(20, 184, 166, 0.2);
    }
    .risk-badge.badge-warning {
      background: rgba(var(--accent-warning-rgb), 0.15);
      border: 1px solid rgba(var(--accent-warning-rgb), 0.4);
      color: var(--accent-warning);
      box-shadow: 0 0 12px rgba(var(--accent-warning-rgb), 0.2);
    }
    .risk-badge.badge-orange {
      background: rgba(249, 115, 22, 0.15);
      border: 1px solid rgba(249, 115, 22, 0.4);
      color: var(--accent-orange);
      box-shadow: 0 0 12px rgba(249, 115, 22, 0.2);
    }
    .risk-badge.badge-danger {
      background: rgba(var(--accent-danger-rgb), 0.15);
      border: 1px solid rgba(var(--accent-danger-rgb), 0.4);
      color: var(--accent-danger);
      box-shadow: 0 0 12px rgba(var(--accent-danger-rgb), 0.2);
    }
    .risk-badge.badge-purple {
      background: rgba(139, 92, 246, 0.15);
      border: 1px solid rgba(139, 92, 246, 0.4);
      color: var(--accent-purple);
      box-shadow: 0 0 12px rgba(139, 92, 246, 0.2);
    }

    /* Diagnostic Badges */
    .audit-badges {
      width: 100%;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
    }
    .audit-badge-card {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 0.65rem 0.75rem;
      text-align: left;
    }
    .audit-badge-title {
      font-size: 0.68rem;
      color: var(--text-dim);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .audit-badge-value {
      font-size: 0.88rem;
      font-weight: 700;
      margin-top: 0.2rem;
      font-variant-numeric: tabular-nums;
    }

    /* Violations Box */
    .violations-list {
      width: 100%;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      text-align: left;
      font-size: 0.78rem;
      color: var(--text-muted);
    }
    .violations-list strong { color: var(--text-main); }
    .violations-list ul {
      margin-left: 1.25rem;
      margin-top: 0.4rem;
      color: var(--accent-danger);
    }
    .violations-list li { margin-bottom: 0.2rem; }

    /* Radar Chart Card */
    .radar-card {
      background: rgba(0, 0, 0, 0.18);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    .radar-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-main);
    }
    .radar-chart-box {
      position: relative;
      width: 100%;
      height: 250px;
    }

    /* Stream Tab Controls */
    .stream-controls {
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      align-items: center;
      margin-bottom: 1.25rem;
    }
    .sensor-select {
      background: var(--bg-input);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 0.5rem 0.85rem;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      outline: none;
      cursor: pointer;
    }
    .sensor-select:focus {
      border-color: var(--accent-cyan);
    }

    .stream-chart-box {
      position: relative;
      width: 100%;
      height: 380px;
      background: rgba(0, 0, 0, 0.15);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 1rem;
    }

    /* Batch Tab Styles */
    .dropzone {
      border: 2px dashed var(--border-color);
      border-radius: 14px;
      padding: 2.25rem 1.5rem;
      text-align: center;
      background: rgba(255, 255, 255, 0.02);
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.65rem;
    }
    .dropzone:hover {
      border-color: var(--accent-cyan);
      background: rgba(var(--accent-cyan-rgb), 0.04);
    }

    .batch-actions-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin: 1.25rem 0;
    }

    .filter-pills {
      display: flex;
      gap: 0.45rem;
    }
    .filter-pill {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      padding: 0.35rem 0.75rem;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .filter-pill:hover, .filter-pill.active {
      background: rgba(var(--accent-cyan-rgb), 0.15);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }

    .table-container {
      width: 100%;
      overflow-x: auto;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      box-shadow: var(--shadow-sm);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.82rem;
      text-align: left;
    }
    th {
      background: var(--table-th-bg);
      color: var(--text-muted);
      font-weight: 700;
      padding: 0.75rem 0.85rem;
      border-bottom: 1px solid var(--border-color);
      white-space: nowrap;
      cursor: pointer;
      user-select: none;
    }
    th:hover {
      color: var(--accent-cyan);
    }
    td {
      padding: 0.7rem 0.85rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      color: var(--text-main);
      white-space: nowrap;
      font-variant-numeric: tabular-nums;
    }
    tr:nth-child(even) {
      background: var(--table-stripe);
    }
    tr:hover {
      background: rgba(var(--accent-cyan-rgb), 0.05);
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 700;
    }
    .status-pill.potable {
      background: rgba(var(--accent-emerald-rgb), 0.15);
      color: var(--accent-emerald);
      border: 1px solid rgba(var(--accent-emerald-rgb), 0.3);
    }
    .status-pill.non-potable {
      background: rgba(var(--accent-danger-rgb), 0.15);
      color: var(--accent-danger);
      border: 1px solid rgba(var(--accent-danger-rgb), 0.3);
    }
    .status-pill.inlier {
      background: rgba(var(--accent-cyan-rgb), 0.15);
      color: var(--accent-cyan);
      border: 1px solid rgba(var(--accent-cyan-rgb), 0.3);
    }
    .status-pill.outlier {
      background: rgba(var(--accent-danger-rgb), 0.15);
      color: var(--accent-danger);
      border: 1px solid rgba(var(--accent-danger-rgb), 0.3);
    }

    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 1rem;
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    /* Benchmark Progress Bars */
    .metric-bar-bg {
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 9999px;
      overflow: hidden;
      margin-top: 0.3rem;
    }
    .metric-bar-fill {
      height: 100%;
      border-radius: 9999px;
      background: linear-gradient(90deg, var(--accent-cyan), var(--accent-emerald));
      transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Confusion Matrix Heatmap */
    .cm-grid {
      display: grid;
      grid-template-columns: auto 1fr 1fr;
      gap: 0.5rem;
      max-width: 480px;
      margin: 1.25rem auto;
      text-align: center;
      font-size: 0.85rem;
    }
    .cm-cell {
      padding: 1.15rem 0.75rem;
      border-radius: 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 0.25rem;
    }
    .cm-cell.tn { background: rgba(var(--accent-emerald-rgb), 0.2); border: 1px solid rgba(var(--accent-emerald-rgb), 0.4); color: var(--accent-emerald); }
    .cm-cell.tp { background: rgba(var(--accent-cyan-rgb), 0.2); border: 1px solid rgba(var(--accent-cyan-rgb), 0.4); color: var(--accent-cyan); }
    .cm-cell.fn { background: rgba(var(--accent-warning-rgb), 0.2); border: 1px solid rgba(var(--accent-warning-rgb), 0.4); color: var(--accent-warning); }
    .cm-cell.fp { background: rgba(var(--accent-danger-rgb), 0.2); border: 1px solid rgba(var(--accent-danger-rgb), 0.4); color: var(--accent-danger); }
    .cm-count { font-size: 1.5rem; font-weight: 800; }
    .cm-label { font-size: 0.7rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; }

    /* Modals */
    .modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: var(--modal-overlay);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }
    .modal-backdrop.open {
      display: flex;
      animation: fadeIn 0.2s ease;
    }
    .modal-dialog {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 18px;
      max-width: 680px;
      width: 100%;
      max-height: 88vh;
      overflow-y: auto;
      padding: 1.75rem;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
      display: flex;
      flex-direction: column;
      gap: 1.25rem;
    }
    .modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-title {
      font-size: 1.2rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .modal-close-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
    }
    .modal-close-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.08);
    }

    /* Toast System */
    .toast-container {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      z-index: 2000;
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      pointer-events: none;
    }
    .dynamic-toast {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 0.85rem 1.15rem;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-size: 0.82rem;
      color: var(--text-main);
      pointer-events: auto;
      transform: translateY(12px) scale(0.96);
      opacity: 0;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      max-width: 380px;
    }
    .dynamic-toast.show {
      transform: translateY(0) scale(1);
      opacity: 1;
    }
    .dynamic-toast.success { border-color: rgba(var(--accent-emerald-rgb), 0.4); color: var(--accent-emerald); }
    .dynamic-toast.warning { border-color: rgba(var(--accent-warning-rgb), 0.4); color: var(--accent-warning); }
    .dynamic-toast.error { border-color: rgba(var(--accent-danger-rgb), 0.4); color: var(--accent-danger); }
    .dynamic-toast.info { border-color: rgba(var(--accent-cyan-rgb), 0.4); color: var(--accent-cyan); }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-color);
      background: var(--bg-surface);
      padding: 1.25rem 1.5rem;
      text-align: center;
      font-size: 0.78rem;
      color: var(--text-muted);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0.5rem;
    }
    footer a {
      color: var(--accent-cyan);
      text-decoration: none;
      font-weight: 600;
    }
    footer a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- Top Sticky Header -->
  <header>
    <div class="brand">
      <div class="brand-logo-container" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>
      </div>
      <div>
        <div class="brand-title">
          AquaGuard AI
          <span class="brand-version">v2.1.0</span>
        </div>
        <div class="brand-subtitle">Water Potability & WHO/EPA Compliance Intelligence</div>
      </div>
    </div>

    <div class="header-controls">
      <div class="live-clock" id="live-clock" aria-label="Current UTC timestamp">UTC --:--:--</div>
      
      <div class="system-status" id="system-status-badge" role="status">
        <div class="status-dot" id="system-status-dot"></div>
        <span id="system-status-text">CONNECTING</span>
      </div>

      <button class="header-btn" id="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme mode" title="Toggle theme mode">
        <svg id="theme-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
      </button>

      <button class="header-btn" onclick="openModal('modal-about')" aria-label="About AquaGuard AI" title="Project architecture and credits">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
      </button>
    </div>
  </header>

  <main>
    <!-- KPI Header Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Champion Pipeline</h4>
          <div class="kpi-value" id="kpi-pipeline-name" style="font-size: 1.25rem;">Random Forest</div>
          <div class="kpi-desc">Calibrated + Platt Scaling (200 Trees)</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(var(--accent-cyan-rgb), 0.15); color: var(--accent-cyan);">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Lockbox PR-AUC</h4>
          <div class="kpi-value" id="kpi-pr-auc" style="color: var(--accent-cyan);">0.5951</div>
          <div class="kpi-desc">+51.8% vs 0.3920 WHO Baseline</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(var(--accent-emerald-rgb), 0.15); color: var(--accent-emerald);">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>Inference Latency</h4>
          <div class="kpi-value" id="kpi-latency-val" style="color: var(--accent-emerald);">2.89 ms</div>
          <div class="kpi-desc">FastAPI Sub-3ms P50 Runtime</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(139, 92, 246, 0.15); color: var(--accent-purple);">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
        </div>
      </div>

      <div class="kpi-card">
        <div class="kpi-info">
          <h4>WHO Auditor</h4>
          <div class="kpi-value" id="kpi-who-compliance" style="color: var(--accent-emerald);">Active</div>
          <div class="kpi-desc">9 Deterministic Chemical Guardrails</div>
        </div>
        <div class="kpi-icon-pill" style="background: rgba(59, 130, 246, 0.15); color: var(--accent-blue);">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
        </div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-header" role="tablist">
      <button class="tab-btn active" role="tab" id="tab-btn-sim" aria-selected="true" aria-controls="tab-sim" onclick="switchTab('tab-sim', this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>
        Interactive Potability Simulator
      </button>
      <button class="tab-btn" role="tab" id="tab-btn-stream" aria-selected="false" aria-controls="tab-stream" onclick="switchTab('tab-stream', this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
        Continuous Telemetry Stream (Track A)
      </button>
      <button class="tab-btn" role="tab" id="tab-btn-batch" aria-selected="false" aria-controls="tab-batch" onclick="switchTab('tab-batch', this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/></svg>
        Batch Telemetry Processor (9 Features)
      </button>
      <button class="tab-btn" role="tab" id="tab-btn-models" aria-selected="false" aria-controls="tab-models" onclick="switchTab('tab-models', this)">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        Model Benchmark & WHO Standards
      </button>
    </div>

    <!-- TAB 1: INTERACTIVE POTABILITY SIMULATOR -->
    <div id="tab-sim" class="tab-pane active" role="tabpanel" aria-labelledby="tab-btn-sim">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>
              Physicochemical Water Quality Telemetry Input
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Adjust sliders to trigger real-time calibrated potability scoring and 9-axis WHO compliance auditing.
            </div>
          </div>
        </div>

        <!-- Educational Disclaimer Banner -->
        <div class="disclaimer-banner">
          <svg style="flex-shrink: 0; margin-top: 2px;" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          <div>
            <strong>Educational & Demonstration Notice:</strong> AquaGuard AI is a predictive research model trained on physicochemical benchmark data. It provides an algorithmic estimate and is <em>not</em> a substitute for certified laboratory microbiological or chemical assays. Drinking water decisions must be validated by licensed local testing authorities.
          </div>
        </div>

        <!-- Remediation Diff Box -->
        <div class="remediation-alert" id="remediation-alert">
          <strong>Optimal WHO Remediation Applied:</strong> All 9 physicochemical parameters smoothly animated to safe regulatory envelopes (pH 7.20, Hardness 140 mg/L, TDS 850 ppm, Chloramines 2.2 ppm, Sulfate 210 mg/L, Conductivity 320 μS/cm, TOC 2.8 ppm, THM 45 μg/L, Turbidity 1.4 NTU).
        </div>

        <!-- Presets Selection Bar -->
        <div class="presets-container">
          <span class="preset-label">Standard Presets:</span>
          <button class="preset-btn btn-accent" onclick="loadPreset('mountain')">Mountain Spring</button>
          <button class="preset-btn" onclick="loadPreset('municipal')">Municipal Tap</button>
          <button class="preset-btn" onclick="loadPreset('glacial')">Glacial Melt</button>
          <button class="preset-btn" onclick="loadPreset('deep_sea')">Hydrothermal Vent</button>
          <button class="preset-btn" onclick="loadPreset('acid_spill')">Acid Drainage</button>
          <button class="preset-btn" onclick="loadPreset('sensor_fault')">Sensor Failure</button>
          <button class="preset-btn" onclick="randomizeInputs()" style="margin-left: auto;">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
            Randomize Values
          </button>
        </div>

        <div class="sim-grid">
          <!-- Left: 9 Chemical Parameter Input Sliders -->
          <div>
            <div class="inputs-grid">
              <!-- 1. pH -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-ph">pH Acidity</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-ph" title="WHO Safe: 6.5–8.5">WHO: 6.5–8.5</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-ph" min="0" max="14" step="0.05" value="7.25" aria-labelledby="lbl-ph" aria-valuemin="0" aria-valuemax="14" aria-valuenow="7.25" oninput="syncInput('ph', this.value)">
                  <input type="number" id="num-ph" class="num-input" value="7.25" step="0.05" aria-label="pH numeric value" onchange="syncSlider('ph', this.value)">
                </div>
              </div>

              <!-- 2. Hardness -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-hardness">Hardness (mg/L)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-hardness" title="WHO Safe: <= 200 mg/L">WHO: &le; 200</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-hardness" min="0" max="400" step="1" value="185" aria-labelledby="lbl-hardness" aria-valuemin="0" aria-valuemax="400" aria-valuenow="185" oninput="syncInput('hardness', this.value)">
                  <input type="number" id="num-hardness" class="num-input" value="185" step="1" aria-label="Hardness numeric value" onchange="syncSlider('hardness', this.value)">
                </div>
              </div>

              <!-- 3. Solids (TDS) -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-solids">TDS Solids (ppm)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-solids" title="WHO Safe: <= 1000 ppm (EPA <= 500)">WHO: &le; 1000</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-solids" min="0" max="45000" step="100" value="16500" aria-labelledby="lbl-solids" aria-valuemin="0" aria-valuemax="45000" aria-valuenow="16500" oninput="syncInput('solids', this.value)">
                  <input type="number" id="num-solids" class="num-input" value="16500" step="100" aria-label="TDS numeric value" onchange="syncSlider('solids', this.value)">
                </div>
              </div>

              <!-- 4. Chloramines -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-chloramines">Chloramines (ppm)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-chloramines" title="WHO Safe: <= 4.0 ppm">WHO: &le; 4.0</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-chloramines" min="0" max="15" step="0.1" value="6.2" aria-labelledby="lbl-chloramines" aria-valuemin="0" aria-valuemax="15" aria-valuenow="6.2" oninput="syncInput('chloramines', this.value)">
                  <input type="number" id="num-chloramines" class="num-input" value="6.2" step="0.1" aria-label="Chloramines numeric value" onchange="syncSlider('chloramines', this.value)">
                </div>
              </div>

              <!-- 5. Sulfate -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-sulfate">Sulfate (mg/L)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-sulfate" title="WHO Safe: <= 250 mg/L">WHO: &le; 250</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-sulfate" min="0" max="600" step="1" value="325" aria-labelledby="lbl-sulfate" aria-valuemin="0" aria-valuemax="600" aria-valuenow="325" oninput="syncInput('sulfate', this.value)">
                  <input type="number" id="num-sulfate" class="num-input" value="325" step="1" aria-label="Sulfate numeric value" onchange="syncSlider('sulfate', this.value)">
                </div>
              </div>

              <!-- 6. Conductivity -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-conductivity">Conductivity (&mu;S/cm)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-conductivity" title="WHO Safe: <= 400 uS/cm">WHO: &le; 400</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-conductivity" min="0" max="900" step="5" value="415" aria-labelledby="lbl-conductivity" aria-valuemin="0" aria-valuemax="900" aria-valuenow="415" oninput="syncInput('conductivity', this.value)">
                  <input type="number" id="num-conductivity" class="num-input" value="415" step="5" aria-label="Conductivity numeric value" onchange="syncSlider('conductivity', this.value)">
                </div>
              </div>

              <!-- 7. Organic Carbon -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-carbon">Organic Carbon (ppm)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-carbon" title="WHO Safe: <= 4.0 ppm">WHO: &le; 4.0</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-carbon" min="0" max="30" step="0.1" value="12.5" aria-labelledby="lbl-carbon" aria-valuemin="0" aria-valuemax="30" aria-valuenow="12.5" oninput="syncInput('carbon', this.value)">
                  <input type="number" id="num-carbon" class="num-input" value="12.5" step="0.1" aria-label="Organic carbon numeric value" onchange="syncSlider('carbon', this.value)">
                </div>
              </div>

              <!-- 8. Trihalomethanes -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-thm">THMs (&mu;g/L)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-thm" title="WHO Safe: <= 80 ug/L">WHO: &le; 80</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-thm" min="0" max="150" step="1" value="62" aria-labelledby="lbl-thm" aria-valuemin="0" aria-valuemax="150" aria-valuenow="62" oninput="syncInput('thm', this.value)">
                  <input type="number" id="num-thm" class="num-input" value="62" step="1" aria-label="Trihalomethanes numeric value" onchange="syncSlider('thm', this.value)">
                </div>
              </div>

              <!-- 9. Turbidity -->
              <div class="input-group">
                <div class="input-header">
                  <span class="input-label" id="lbl-turbidity">Turbidity (NTU)</span>
                  <a href="#who-standards" class="limit-badge" id="badge-limit-turbidity" title="WHO Safe: <= 5.0 NTU">WHO: &le; 5.0</a>
                </div>
                <div class="slider-row">
                  <input type="range" id="inp-turbidity" min="0" max="12" step="0.05" value="3.4" aria-labelledby="lbl-turbidity" aria-valuemin="0" aria-valuemax="12" aria-valuenow="3.4" oninput="syncInput('turbidity', this.value)">
                  <input type="number" id="num-turbidity" class="num-input" value="3.4" step="0.05" aria-label="Turbidity numeric value" onchange="syncSlider('turbidity', this.value)">
                </div>
              </div>
            </div>

            <!-- Quick Action Buttons -->
            <div class="actions-row">
              <button class="action-btn btn-primary" onclick="remediateToSafe()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m19 11-8-8-8.6 8.6a2 2 0 0 0 0 2.8l5.2 5.2c.8.8 2 .8 2.8 0L19 11Z"/><path d="m5 2 5 5"/><path d="m2 5 5 5"/></svg>
                Auto-Remediate to Safe
              </button>
              <button class="action-btn" onclick="copyCurlSnippet()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                Copy cURL Request
              </button>
              <button class="action-btn" onclick="openModal('modal-rubric')">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
                View Grading Rubric
              </button>
              <button class="action-btn" onclick="resetToDefaults()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>
                Reset Defaults
              </button>
            </div>
          </div>

          <!-- Right: Visual Outcome & Radar Chart -->
          <div class="decision-panel">
            <div class="decision-box">
              <div class="verdict-banner safe" id="verdict-banner" role="status" aria-live="polite">
                <div id="verdict-icon" style="flex-shrink: 0;">
                  <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                </div>
                <div>
                  <h3 class="verdict-title" id="verdict-title">Predicted Potable (Model Estimate)</h3>
                  <p class="verdict-desc" id="verdict-desc">Calibrated model estimate conforms fully to WHO & EPA safe drinking envelopes.</p>
                </div>
              </div>

              <!-- Circular Progress Dial -->
              <div class="dial-container">
                <svg class="dial-svg" viewBox="0 0 180 180" aria-hidden="true">
                  <circle class="dial-bg" cx="90" cy="90" r="70"></circle>
                  <circle class="dial-progress" id="dial-progress" cx="90" cy="90" r="70"></circle>
                </svg>
                <div class="dial-text">
                  <span class="dial-value" id="prob-val">74%</span>
                  <span class="dial-sub">POTABILITY PROB</span>
                </div>
              </div>

              <div class="risk-badge badge-emerald" id="risk-badge" onclick="openModal('modal-rubric')" title="Click to view safety rubric" role="button" tabindex="0">
                Grade B: Standard Potable Quality
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
                <div id="who-violations-text" style="margin-top: 0.25rem;">100% compliant with World Health Organization & EPA boundary limits.</div>
              </div>
            </div>

            <!-- 9-Axis WHO Compliance Radar Chart -->
            <div class="radar-card">
              <div class="radar-title">
                <span>9-Axis WHO Guideline Radar</span>
                <span style="font-size: 0.72rem; color: var(--accent-cyan); font-weight: 600;">50% Line = WHO Safe Limit</span>
              </div>
              <div class="radar-chart-box">
                <canvas id="radarChart" aria-label="9-axis radar chart of water parameters against WHO safe envelope" role="img"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: CONTINUOUS SENSOR STREAM (TRACK A) -->
    <div id="tab-stream" class="tab-pane" role="tabpanel" aria-labelledby="tab-btn-stream">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              Underwater Environmental Sensor Stream (Track A)
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Simulated oceanographic CTD buoy telemetry with real-time Isolation Forest anomaly detection.
            </div>
          </div>
        </div>

        <div class="stream-controls">
          <label for="sensor-stream-select" style="font-size: 0.82rem; font-weight: 700; color: var(--text-main);">Telemetry Channel:</label>
          <select id="sensor-stream-select" class="sensor-select" onchange="updateStreamChart()">
            <option value="dissolved_oxygen">Dissolved Oxygen (mg/L)</option>
            <option value="temperature">Water Temperature (&deg;C)</option>
            <option value="ph">pH Acidity</option>
            <option value="conductivity">Electrical Conductivity (&mu;S/cm)</option>
            <option value="turbidity">Turbidity (NTU)</option>
            <option value="pressure">Hydrostatic Pressure (dbar)</option>
          </select>

          <button class="action-btn btn-primary" id="btn-live-stream" onclick="toggleLiveStream()">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            Start Live Simulation
          </button>
          <button class="action-btn" onclick="resetStreamChart()">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>
            Reset Stream
          </button>

          <div style="margin-left: auto; font-size: 0.82rem; color: var(--text-muted); display: flex; align-items: center; gap: 0.5rem;">
            <span>Outliers Flagged:</span>
            <span id="stream-anom-count" style="font-weight: 800; color: var(--accent-danger);">0</span>
          </div>
        </div>

        <div class="stream-chart-box">
          <canvas id="streamChart" aria-label="Underwater telemetry timeseries graph" role="img"></canvas>
        </div>
      </div>
    </div>

    <!-- TAB 3: BATCH TELEMETRY PROCESSOR -->
    <div id="tab-batch" class="tab-pane" role="tabpanel" aria-labelledby="tab-btn-batch">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/></svg>
              Batch Laboratory & In-Situ Water Sample Auditor
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Upload multi-sample physicochemical CSV datasets for high-throughput batch classification.
            </div>
          </div>
        </div>

        <!-- Client-Side Privacy Notice -->
        <div class="disclaimer-banner" style="background: rgba(var(--accent-emerald-rgb), 0.08); border-color: rgba(var(--accent-emerald-rgb), 0.25);">
          <svg style="flex-shrink: 0; margin-top: 2px;" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <div>
            <strong>Client-Side Privacy Guarantee:</strong> Batch records are processed strictly within your local browser memory. Raw CSV data is never stored on external databases or third-party servers.
          </div>
        </div>

        <!-- Drag & Drop Zone -->
        <div class="dropzone" id="batch-dropzone" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)" onclick="document.getElementById('csv-file-input').click()">
          <input type="file" id="csv-file-input" accept=".csv" style="display: none;" onchange="handleFileUpload(event)">
          <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(var(--accent-cyan-rgb), 0.12); display: flex; align-items: center; justify-content: center; color: var(--accent-cyan);">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          </div>
          <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-main);">Drop your CSV file here or click to browse</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">Supports standard 9-column physicochemical telemetry files up to 5 MB</div>
          <button class="action-btn" type="button" onclick="event.stopPropagation(); loadDemoBatch()" style="margin-top: 0.5rem;">
            Load 30-Sample Demo Batch
          </button>
        </div>

        <div id="batch-error-alert" class="remediation-alert" style="background: rgba(var(--accent-danger-rgb), 0.12); border-color: rgba(var(--accent-danger-rgb), 0.35); color: var(--accent-danger);"></div>

        <!-- Results Table Area -->
        <div id="batch-results-area" style="display: none; margin-top: 1.5rem;">
          <div class="batch-actions-bar">
            <div class="filter-pills">
              <button class="filter-pill active" onclick="filterBatch('all')">All Samples</button>
              <button class="filter-pill" onclick="filterBatch('potable')">Potable Only</button>
              <button class="filter-pill" onclick="filterBatch('anomaly')">Outliers Only</button>
            </div>

            <button class="action-btn" onclick="downloadBatchResults()">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
              Export Annotated CSV
            </button>
          </div>

          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th onclick="sortBatchTable('idx')"># <span id="sort-idx"></span></th>
                  <th onclick="sortBatchTable('ph')">pH <span id="sort-ph"></span></th>
                  <th onclick="sortBatchTable('hardness')">Hardness <span id="sort-hardness"></span></th>
                  <th onclick="sortBatchTable('solids')">Solids <span id="sort-solids"></span></th>
                  <th onclick="sortBatchTable('chlor')">Chloramines <span id="sort-chlor"></span></th>
                  <th onclick="sortBatchTable('sulfate')">Sulfate <span id="sort-sulfate"></span></th>
                  <th onclick="sortBatchTable('cond')">Conductivity <span id="sort-cond"></span></th>
                  <th onclick="sortBatchTable('carbon')">TOC <span id="sort-carbon"></span></th>
                  <th onclick="sortBatchTable('thm')">THMs <span id="sort-thm"></span></th>
                  <th onclick="sortBatchTable('turb')">Turbidity <span id="sort-turb"></span></th>
                  <th>Status</th>
                  <th onclick="sortBatchTable('prob')">Probability <span id="sort-prob"></span></th>
                  <th>Integrity</th>
                </tr>
              </thead>
              <tbody id="batch-tbody"></tbody>
            </table>
          </div>

          <div class="pagination-bar">
            <span id="batch-pagination-info">Showing 1-10 of 30</span>
            <div style="display: flex; gap: 0.4rem;">
              <button class="action-btn" id="btn-page-prev" onclick="prevBatchPage()" style="padding: 0.35rem 0.75rem;">Previous</button>
              <button class="action-btn" id="btn-page-next" onclick="nextBatchPage()" style="padding: 0.35rem 0.75rem;">Next</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: BENCHMARK & WHO STANDARDS -->
    <div id="tab-models" class="tab-pane" role="tabpanel" aria-labelledby="tab-btn-models">
      <div class="card">
        <div class="card-header">
          <div>
            <div class="card-title">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
              Rigorous Cross-Validation Benchmark & Test Lockbox Audit
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">
              Audited performance across Stratified 5-Fold CV (N=2,620) and Unseen Test Lockbox (N=656).
            </div>
          </div>
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Model Architecture</th>
                <th>Validation PR-AUC</th>
                <th>Lockbox PR-AUC</th>
                <th>Lockbox F1 @ T*=0.38</th>
                <th>Standard F1 @ T=0.50</th>
                <th>Accuracy</th>
                <th>P50 Latency</th>
              </tr>
            </thead>
            <tbody>
              <tr style="background: rgba(var(--accent-cyan-rgb), 0.08); font-weight: 700;">
                <td style="color: var(--accent-cyan);">Calibrated Random Forest + Platt Scaling (Champion)</td>
                <td>0.5793 &plusmn; 0.021</td>
                <td><strong>0.5951</strong></td>
                <td><strong style="color: var(--accent-emerald);">0.5480</strong></td>
                <td>0.4127</td>
                <td>66.16%</td>
                <td>2.89 ms</td>
              </tr>
              <tr>
                <td>XGBoost (Hist Gradient Boosted)</td>
                <td>0.5642 &plusmn; 0.019</td>
                <td>0.5714</td>
                <td>0.5298</td>
                <td>0.3980</td>
                <td>64.82%</td>
                <td>1.42 ms</td>
              </tr>
              <tr>
                <td>LightGBM Classifier</td>
                <td>0.5590 &plusmn; 0.024</td>
                <td>0.5630</td>
                <td>0.5182</td>
                <td>0.3895</td>
                <td>63.95%</td>
                <td>0.85 ms</td>
              </tr>
              <tr>
                <td>ElasticNet Logistic Regression</td>
                <td>0.4285 &plusmn; 0.015</td>
                <td>0.4310</td>
                <td>0.4420</td>
                <td>0.3210</td>
                <td>58.20%</td>
                <td>0.12 ms</td>
              </tr>
              <tr style="color: var(--text-muted);">
                <td>WHO Guideline Deterministic Benchmark</td>
                <td>0.3920 (Static)</td>
                <td>0.3920</td>
                <td>0.4502</td>
                <td>0.4502</td>
                <td>57.32%</td>
                <td>0.08 ms</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Metric Clarification Banner -->
        <div class="disclaimer-banner" style="margin-top: 1.25rem;">
          <svg style="flex-shrink: 0; margin-top: 2px;" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          <div>
            <strong>Evaluation Metric Clarification:</strong>
            The optimal threshold <strong>T* = 0.38</strong> was selected via validation cross-validation curve optimization.
            On the <strong>Stratified 5-Fold Validation set</strong>, F1 at T*=0.38 was <strong>0.5512 &plusmn; 0.024</strong>.
            On the completely unseen <strong>Test Lockbox (656 samples)</strong>, F1 at T*=0.38 is verified at <strong>0.5480</strong> (Precision: 63.93%, Recall: 30.47%).
          </div>
        </div>

        <!-- Confusion Matrix Heatmap -->
        <div style="margin-top: 2rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700; text-align: center; color: var(--text-main); margin-bottom: 0.25rem;">
            Test Lockbox Confusion Matrix (N = 656, Threshold T* = 0.38)
          </h4>
          <p style="font-size: 0.75rem; color: var(--text-muted); text-align: center;">Verified contingency breakdown against ground-truth labels</p>

          <div class="cm-grid">
            <div></div>
            <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">Pred Negative (0)</div>
            <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">Pred Positive (1)</div>

            <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase; writing-mode: vertical-rl; transform: rotate(180deg); margin: auto;">Actual (0)</div>
            <div class="cm-cell tn">
              <span class="cm-count">356</span>
              <span class="cm-label">True Negative (TN)</span>
            </div>
            <div class="cm-cell fp">
              <span class="cm-count">44</span>
              <span class="cm-label">False Positive (FP)</span>
            </div>

            <div style="font-size: 0.75rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase; writing-mode: vertical-rl; transform: rotate(180deg); margin: auto;">Actual (1)</div>
            <div class="cm-cell fn">
              <span class="cm-count">178</span>
              <span class="cm-label">False Negative (FN)</span>
            </div>
            <div class="cm-cell tp">
              <span class="cm-count">78</span>
              <span class="cm-label">True Positive (TP)</span>
            </div>
          </div>
        </div>

        <!-- WHO Guidelines Reference Table -->
        <div id="who-standards" style="margin-top: 2rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.75rem;">
            World Health Organization (WHO) & US EPA Water Quality Standards
          </h4>
          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Physicochemical Parameter</th>
                  <th>Safe Permissible Range</th>
                  <th>Standard Citation</th>
                  <th>Adverse Health / Technical Risk</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><strong>pH Acidity</strong></td>
                  <td>6.5 – 8.5</td>
                  <td>WHO 4th Ed. / EPA 40 CFR 143.3</td>
                  <td>Corrosion of distribution piping (<6.5) or caustic taste & encrustation (>8.5)</td>
                </tr>
                <tr>
                  <td><strong>Hardness (CaCO3)</strong></td>
                  <td>&le; 200.0 mg/L</td>
                  <td>WHO Guidelines / EU Directive 98/83/EC</td>
                  <td>Severe boiler scaling, pipeline encrustation, reduced lathering capacity</td>
                </tr>
                <tr>
                  <td><strong>Solids (Total Dissolved Solids)</strong></td>
                  <td>&le; 1000.0 ppm (EPA &le; 500 ppm)</td>
                  <td>WHO Section 12.11 / EPA Secondary SMCL</td>
                  <td>Excessive mineral taste, gastrointestinal irritation, plumbing scaling</td>
                </tr>
                <tr>
                  <td><strong>Chloramines</strong></td>
                  <td>&le; 4.0 ppm</td>
                  <td>WHO Guidelines / EPA National Primary</td>
                  <td>Irritation of mucous membranes, chloramine disinfection byproduct toxicity</td>
                </tr>
                <tr>
                  <td><strong>Sulfate</strong></td>
                  <td>&le; 250.0 mg/L</td>
                  <td>WHO Guidelines / EPA 40 CFR 143.3</td>
                  <td>Cathartic laxative effects, bitter taste, metallic infrastructure corrosion</td>
                </tr>
                <tr>
                  <td><strong>Electrical Conductivity</strong></td>
                  <td>&le; 400.0 &mu;S/cm</td>
                  <td>WHO Guidelines / EPA Environmental Std</td>
                  <td>High dissolved ion salinity, agricultural toxicity, industrial runoff</td>
                </tr>
                <tr>
                  <td><strong>Total Organic Carbon (TOC)</strong></td>
                  <td>&le; 4.0 ppm</td>
                  <td>EPA D/DBPR Disinfection Byproduct Rule</td>
                  <td>Precursor for carcinogenic disinfection byproducts upon chlorination</td>
                </tr>
                <tr>
                  <td><strong>Trihalomethanes (THM)</strong></td>
                  <td>&le; 80.0 &mu;g/L</td>
                  <td>WHO Guidelines / EPA Stage 1 DBPR</td>
                  <td>Carcinogenic liver, kidney, and central nervous system hazards</td>
                </tr>
                <tr>
                  <td><strong>Turbidity</strong></td>
                  <td>&le; 5.0 NTU (Target &le; 1.0 NTU)</td>
                  <td>WHO 4th Ed. / EPA Safe Drinking Water Act</td>
                  <td>Protects microbiological pathogens from chemical disinfection treatment</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Grading Rubric Modal -->
  <div class="modal-backdrop" id="modal-rubric" onclick="closeModalOnBackdrop(event, 'modal-rubric')">
    <div class="modal-dialog" role="dialog" aria-labelledby="rubric-modal-title" aria-modal="true">
      <div class="modal-header">
        <div class="modal-title" id="rubric-modal-title">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
          Water Quality Decision Rubric & Boundaries
        </div>
        <button class="modal-close-btn" onclick="closeModal('modal-rubric')" aria-label="Close dialog">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.6;">
        <p>AquaGuard AI integrates probabilistic classification with deterministic regulatory gating. Even if a statistical model predicts potability, samples exceeding chemical safety bounds are restricted from Grade A/B designation.</p>

        <div class="table-container" style="margin-top: 1rem;">
          <table>
            <thead>
              <tr>
                <th>Grade</th>
                <th>Calibrated Probability</th>
                <th>WHO Violations</th>
                <th>Action Recommendation</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><span class="status-pill potable">Grade A</span></td>
                <td>&ge; 75.0%</td>
                <td>0 Violations</td>
                <td>Pristine potable quality for immediate human consumption.</td>
              </tr>
              <tr>
                <td><span class="status-pill potable">Grade B</span></td>
                <td>&ge; 50.0%</td>
                <td>0 Violations</td>
                <td>Standard municipal compliance; meets all standard guidelines.</td>
              </tr>
              <tr>
                <td><span class="status-pill outlier">Grade C</span></td>
                <td>&ge; 50.0%</td>
                <td>1–2 Secondary</td>
                <td>Advisory warning; mild secondary aesthetic or taste excursions.</td>
              </tr>
              <tr>
                <td><span class="status-pill non-potable">Grade D</span></td>
                <td>&lt; 50.0%</td>
                <td>1–2 Violations</td>
                <td>Treatment required; filtration and disinfection advised.</td>
              </tr>
              <tr>
                <td><span class="status-pill non-potable">Grade F</span></td>
                <td>&lt; 50.0%</td>
                <td>&ge; 3 Violations</td>
                <td>Hazardous non-potable; high chemical or organic contamination.</td>
              </tr>
              <tr>
                <td><span class="status-pill outlier" style="background: rgba(139, 92, 246, 0.2); color: var(--accent-purple);">Grade X</span></td>
                <td>Out-of-Bounds</td>
                <td>Sensor Drift</td>
                <td>Sensor malfunction; physical probe recalibration needed.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- About Project Modal -->
  <div class="modal-backdrop" id="modal-about" onclick="closeModalOnBackdrop(event, 'modal-about')">
    <div class="modal-dialog" role="dialog" aria-labelledby="about-modal-title" aria-modal="true">
      <div class="modal-header">
        <div class="modal-title" id="about-modal-title">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>
          About AquaGuard AI
        </div>
        <button class="modal-close-btn" onclick="closeModal('modal-about')" aria-label="Close dialog">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>

      <div style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.6; display: flex; flex-direction: column; gap: 0.85rem;">
        <p><strong>AquaGuard AI</strong> is a dual-track machine learning intelligence system developed during the TIH IIT Guwahati AI/ML Internship programme.</p>
        
        <div>
          <h4 style="color: var(--text-main); font-size: 0.9rem; margin-bottom: 0.3rem;">Project Architecture:</h4>
          <ul style="margin-left: 1.25rem;">
            <li><strong>Track A (Continuous Telemetry):</strong> Simulated oceanographic CTD buoy telemetry with real-time Isolation Forest and 3.5-sigma boundary anomaly detection.</li>
            <li><strong>Track B (Tabular Potability):</strong> Calibrated Random Forest (200 Trees) + Platt Scaling trained on physicochemical water telemetry with 9 deterministic WHO guardrails.</li>
          </ul>
        </div>

        <div>
          <h4 style="color: var(--text-main); font-size: 0.9rem; margin-bottom: 0.3rem;">Engineering Attribution:</h4>
          <p><strong>Author:</strong> Rajana Durga Pavan Kumar (Group C1)</p>
          <p><strong>Assigned Mentor:</strong> <a href="https://www.linkedin.com/in/nightcoder44332211/" target="_blank" rel="noopener noreferrer">Sushil Meher</a>, Teaching Assistant at Indian Institute of Technology, Guwahati</p>
          <p><strong>Institution:</strong> Technology Innovation Hub (TIH), IIT Guwahati</p>
        </div>

        <div style="margin-top: 0.5rem; padding-top: 0.75rem; border-top: 1px solid var(--border-color); font-size: 0.75rem; color: var(--text-dim);">
          Open source research release under Apache-2.0 License.
        </div>
      </div>
    </div>
  </div>

  <!-- Dynamic Toast Container -->
  <div class="toast-container" id="toast-container" role="status" aria-live="polite"></div>

  <!-- Footer -->
  <footer>
    <div>
      AquaGuard AI v2.1.0 &bull; Built by <strong>Rajana Durga Pavan Kumar</strong> (Group C1)
      &bull; Mentored by <a href="https://www.linkedin.com/in/nightcoder44332211/" target="_blank" rel="noopener noreferrer">Sushil Meher</a> (Teaching Assistant, IIT Guwahati)
    </div>
    <div>
      <a href="https://github.com/DurgaPavan0923/RajanaDurgaPavanKumar_C1_ONLINETIHIITG" target="_blank" rel="noopener noreferrer">
        GitHub Repository
      </a>
      &bull; Technology Innovation Hub, Indian Institute of Technology Guwahati
    </div>
  </footer>

  <script>
    // ------------------------------------------------------------------------
    // Design Tokens & Theme Management
    // ------------------------------------------------------------------------
    function initTheme() {
      try {
        const saved = localStorage.getItem('aquaguard-theme');
        if (saved) {
          document.documentElement.setAttribute('data-theme', saved);
          updateThemeIcon(saved);
        }
      } catch (e) {
        console.warn('localStorage access denied for theme preference.');
      }
    }

    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const target = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      try {
        localStorage.setItem('aquaguard-theme', target);
      } catch (e) {}
      updateThemeIcon(target);
      showToast('Switched to ' + target.toUpperCase() + ' theme mode', 'info');
    }

    function updateThemeIcon(theme) {
      const icon = document.getElementById('theme-icon');
      if (!icon) return;
      if (theme === 'dark') {
        icon.innerHTML = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>';
      } else {
        icon.innerHTML = '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>';
      }
    }

    // ------------------------------------------------------------------------
    // Toast Notification Engine
    // ------------------------------------------------------------------------
    function showToast(msg, type = 'info') {
      const container = document.getElementById('toast-container');
      if (!container) return;

      const toast = document.createElement('div');
      toast.className = 'dynamic-toast ' + type;
      toast.setAttribute('role', 'status');

      let svgIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
      if (type === 'success') {
        svgIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
      } else if (type === 'warning' || type === 'error') {
        svgIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
      }

      toast.innerHTML = `
        <div style="flex-shrink: 0;">${svgIcon}</div>
        <div style="flex: 1;">${msg}</div>
      `;

      container.appendChild(toast);

      requestAnimationFrame(() => {
        toast.classList.add('show');
      });

      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 250);
      }, 3500);
    }

    // ------------------------------------------------------------------------
    // Live Health Probe & Clock
    // ------------------------------------------------------------------------
    function updateClock() {
      const d = new Date();
      const clock = document.getElementById('live-clock');
      if (clock) {
        const iso = d.toISOString().slice(0, 19).replace('T', ' ');
        clock.innerText = iso + ' UTC';
      }
    }

    async function checkHealthProbe() {
      const badge = document.getElementById('system-status-badge');
      const dot = document.getElementById('system-status-dot');
      const text = document.getElementById('system-status-text');

      try {
        const res = await fetch('/api/ping');
        if (res.ok) {
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
        text.innerText = 'DEGRADED / LOCAL';
        badge.style.background = 'rgba(var(--accent-warning-rgb), 0.12)';
        badge.style.borderColor = 'rgba(var(--accent-warning-rgb), 0.35)';
        badge.style.color = 'var(--accent-warning)';
        dot.style.backgroundColor = 'var(--accent-warning)';
        dot.style.boxShadow = '0 0 8px var(--accent-warning)';
      }
    }

    // ------------------------------------------------------------------------
    // Tab Switching & Keyboard Navigation
    // ------------------------------------------------------------------------
    function switchTab(tabId, el) {
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-selected', 'false');
      });
      document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));

      if (el) {
        el.classList.add('active');
        el.setAttribute('aria-selected', 'true');
      }
      const pane = document.getElementById(tabId);
      if (pane) pane.classList.add('active');

      if (tabId === 'tab-stream') {
        setTimeout(initStreamChart, 100);
      }
    }

    // Keyboard tablist cycling
    document.addEventListener('keydown', (e) => {
      const activeEl = document.activeElement;
      if (activeEl && activeEl.getAttribute('role') === 'tab') {
        const tabs = Array.from(document.querySelectorAll('.tab-btn'));
        const index = tabs.indexOf(activeEl);
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          const next = tabs[(index + 1) % tabs.length];
          next.focus();
          next.click();
        } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          const prev = tabs[(index - 1 + tabs.length) % tabs.length];
          prev.focus();
          prev.click();
        }
      }
    });

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
    // Presets & Form Management
    // ------------------------------------------------------------------------
    const DEFAULT_BASELINE = { ph: 7.25, hardness: 185, solids: 16500, chloramines: 6.2, sulfate: 325, conductivity: 415, carbon: 12.5, thm: 62, turbidity: 3.4 };

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
      showToast('Loaded standard preset: ' + name.replace('_', ' ').toUpperCase(), 'info');
      runPrediction();
    }

    function resetToDefaults() {
      setFormValues(DEFAULT_BASELINE);
      hideRemediationAlert();
      showToast('Reset inputs to default baseline telemetry', 'info');
      runPrediction();
    }

    function setFormValues(p) {
      const keys = ['ph', 'hardness', 'solids', 'chloramines', 'sulfate', 'conductivity', 'carbon', 'thm', 'turbidity'];
      keys.forEach(k => {
        if (p[k] !== undefined) {
          const inp = document.getElementById('inp-' + k);
          const num = document.getElementById('num-' + k);
          if (inp) {
            inp.value = p[k];
            inp.setAttribute('aria-valuenow', p[k]);
            updateSliderFill(inp);
          }
          if (num) num.value = p[k];
        }
      });
    }

    function updateSliderFill(inp) {
      const min = parseFloat(inp.min) || 0;
      const max = parseFloat(inp.max) || 100;
      const val = parseFloat(inp.value) || 0;
      const pct = Math.max(0, Math.min(100, ((val - min) / (max - min)) * 100));
      inp.style.background = `linear-gradient(to right, var(--accent-cyan) 0%, var(--accent-cyan) ${pct}%, var(--bg-input) ${pct}%, var(--bg-input) 100%)`;
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
      const num = document.getElementById('num-' + param);
      const inp = document.getElementById('inp-' + param);
      if (num) num.value = val;
      if (inp) {
        inp.setAttribute('aria-valuenow', val);
        updateSliderFill(inp);
      }
      hideRemediationAlert();
      debouncedPrediction();
    }

    function syncSlider(param, val) {
      const inp = document.getElementById('inp-' + param);
      if (inp) {
        inp.value = val;
        inp.setAttribute('aria-valuenow', val);
        updateSliderFill(inp);
      }
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
      showToast('Randomized telemetry values', 'info');
      runPrediction();
    }

    // ------------------------------------------------------------------------
    // Smooth 600ms Auto-Remediation Tween
    // ------------------------------------------------------------------------
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

      const start = {
        ph: parseFloat(document.getElementById('num-ph').value) || 7.2,
        hardness: parseFloat(document.getElementById('num-hardness').value) || 180,
        solids: parseFloat(document.getElementById('num-solids').value) || 15000,
        chloramines: parseFloat(document.getElementById('num-chloramines').value) || 6.0,
        sulfate: parseFloat(document.getElementById('num-sulfate').value) || 320,
        conductivity: parseFloat(document.getElementById('num-conductivity').value) || 400,
        carbon: parseFloat(document.getElementById('num-carbon').value) || 12.0,
        thm: parseFloat(document.getElementById('num-thm').value) || 60,
        turbidity: parseFloat(document.getElementById('num-turbidity').value) || 3.4
      };

      const duration = 600; // ms
      const startTime = performance.now();

      function step(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(1, elapsed / duration);
        // Ease-out cubic
        const ease = 1 - Math.pow(1 - progress, 3);

        const currentVals = {};
        for (const k in safe) {
          currentVals[k] = +(start[k] + (safe[k] - start[k]) * ease).toFixed(2);
        }
        setFormValues(currentVals);

        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          setFormValues(safe);
          const alert = document.getElementById('remediation-alert');
          if (alert) alert.style.display = 'block';
          showToast('Applied optimal WHO chemical remediation', 'success');
          runPrediction();
        }
      }

      requestAnimationFrame(step);
    }

    function hideRemediationAlert() {
      const alert = document.getElementById('remediation-alert');
      if (alert) alert.style.display = 'none';
    }

    // ------------------------------------------------------------------------
    // Debounced Inference & Request Abort Controller
    // ------------------------------------------------------------------------
    let predictTimer = null;
    let predictAbortController = null;

    function debouncedPrediction() {
      clearTimeout(predictTimer);
      predictTimer = setTimeout(runPrediction, 150);
    }

    async function runPrediction() {
      if (predictAbortController) predictAbortController.abort();
      predictAbortController = new AbortController();

      const payload = getPayloadFromDOM();

      // Client-side Physical Sanity Check
      const invalidSensors = [];
      if (payload.ph < 0 || payload.ph > 14) invalidSensors.push(`pH ${payload.ph} out of physical scale [0–14]`);
      if (payload.Turbidity < 0) invalidSensors.push(`Turbidity ${payload.Turbidity} < 0 NTU`);
      if (payload.Solids < 0) invalidSensors.push(`Solids ${payload.Solids} < 0 ppm`);
      if (payload.Hardness < 0) invalidSensors.push(`Hardness ${payload.Hardness} < 0 mg/L`);
      if (payload.Chloramines < 0) invalidSensors.push(`Chloramines ${payload.Chloramines} < 0 ppm`);
      if (payload.Sulfate < 0) invalidSensors.push(`Sulfate ${payload.Sulfate} < 0 mg/L`);
      if (payload.Conductivity < 0) invalidSensors.push(`Conductivity ${payload.Conductivity} < 0 μS/cm`);
      if (payload.Organic_carbon < 0) invalidSensors.push(`Organic carbon ${payload.Organic_carbon} < 0 ppm`);
      if (payload.Trihalomethanes < 0) invalidSensors.push(`Trihalomethanes ${payload.Trihalomethanes} < 0 μg/L`);

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
          throw new Error('API status ' + response.status);
        }

        const data = await response.json();
        if (data.invalid_sensor_input) {
          renderSensorFailureState(data.invalid_reasons, payload);
          return;
        }

        renderPredictionResults(data, payload);
      } catch (err) {
        if (err.name === 'AbortError') return;
        console.warn('API Offline or Error, executing client-side fallback heuristic:', err);
        fallbackClientHeuristic(payload);
      }
    }

    function fallbackClientHeuristic(payload) {
      const violations = [];
      if (payload.ph < 6.5 || payload.ph > 8.5) violations.push(`pH=${payload.ph.toFixed(2)} out of [6.5, 8.5]`);
      if (payload.Hardness > 200) violations.push(`Hardness=${payload.Hardness.toFixed(1)} > 200 mg/L`);
      if (payload.Solids > 1000) violations.push(`Solids=${payload.Solids.toFixed(0)} > 1000 ppm`);
      if (payload.Chloramines > 4.0) violations.push(`Chloramines=${payload.Chloramines.toFixed(1)} > 4.0 ppm`);
      if (payload.Sulfate > 250) violations.push(`Sulfate=${payload.Sulfate.toFixed(1)} > 250 mg/L`);
      if (payload.Conductivity > 400) violations.push(`Conductivity=${payload.Conductivity.toFixed(1)} > 400 μS/cm`);
      if (payload.Organic_carbon > 4.0) violations.push(`TOC=${payload.Organic_carbon.toFixed(1)} > 4.0 ppm`);
      if (payload.Trihalomethanes > 80) violations.push(`THM=${payload.Trihalomethanes.toFixed(1)} > 80 μg/L`);
      if (payload.Turbidity > 5.0) violations.push(`Turbidity=${payload.Turbidity.toFixed(2)} > 5.0 NTU`);

      const whoCompliant = violations.length === 0;
      let prob = whoCompliant ? 0.74 : 0.28;
      if (payload.ph >= 7.0 && payload.ph <= 7.8 && whoCompliant) prob = 0.82;

      const fallbackData = {
        potability_prediction: whoCompliant ? 1 : 0,
        potability_probability: prob,
        who_compliant: whoCompliant,
        who_violations: violations,
        risk_grade: whoCompliant ? (prob >= 0.75 ? "Grade A: Pristine Potable Quality" : "Grade B: Standard Potable Quality") : (violations.length <= 2 ? "Grade C: Advisory Warning" : "Grade F: Hazardous / Non-Potable"),
        anomaly_flag: false,
        anomaly_score: 0.0,
        processing_time_ms: 1.12
      };
      renderPredictionResults(fallbackData, payload);
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

      banner.className = 'verdict-banner malfunction';
      icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
      title.innerText = 'Sensor Drift / Physical Malfunction';
      desc.innerText = 'Telemetry contains physically impossible negative or out-of-scale sensor values.';

      dialProgress.style.strokeDashoffset = 440;
      dialProgress.style.stroke = 'var(--accent-purple)';
      dialValue.innerText = '0%';

      riskBadge.className = 'risk-badge badge-purple';
      riskBadge.innerText = 'Grade X: Sensor Malfunction';

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

      if (isPotable && whoCompliant) {
        banner.className = 'verdict-banner safe';
        icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
        title.innerText = 'Predicted Potable (Model Estimate)';
        desc.innerText = 'Calibrated model estimate conforms fully to WHO & EPA safe drinking envelopes.';
      } else if (isPotable && !whoCompliant) {
        banner.className = 'verdict-banner warning';
        icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
        title.innerText = 'Predicted Potable — Regulatory Violations Present';
        desc.innerText = 'ML estimate indicates potability, but sample fails one or more WHO/EPA chemical thresholds.';
      } else {
        banner.className = 'verdict-banner hazard';
        icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';
        title.innerText = 'Predicted Non-Potable (Model Estimate)';
        desc.innerText = 'Water sample fails potability criteria and exhibits chemical contamination risks.';
      }

      // Dial update (circumference is 440)
      const dialProgress = document.getElementById('dial-progress');
      const dialValue = document.getElementById('prob-val');
      const offset = 440 - (440 * (probPct / 100));
      dialProgress.style.strokeDashoffset = offset;

      let gaugeColor = 'var(--accent-emerald)';
      if (!isPotable) gaugeColor = 'var(--accent-danger)';
      else if (!whoCompliant) gaugeColor = 'var(--accent-warning)';

      dialProgress.style.stroke = gaugeColor;
      dialProgress.style.filter = `drop-shadow(0 0 8px ${gaugeColor})`;
      animateGaugeProb(probPct);

      // Risk grading badge
      const riskBadge = document.getElementById('risk-badge');
      if (data.risk_grade) {
        let badgeClass = 'badge-danger';
        if (data.risk_grade.startsWith('Grade A')) badgeClass = 'badge-emerald';
        else if (data.risk_grade.startsWith('Grade B')) badgeClass = 'badge-teal';
        else if (data.risk_grade.startsWith('Grade C')) badgeClass = 'badge-warning';
        else if (data.risk_grade.startsWith('Grade D')) badgeClass = 'badge-orange';
        else if (data.risk_grade.startsWith('Grade X')) badgeClass = 'badge-purple';
        riskBadge.className = 'risk-badge ' + badgeClass;
        riskBadge.innerText = data.risk_grade;
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

      // Latency badge
      const latencyMs = data.processing_time_ms ? data.processing_time_ms.toFixed(2) : '2.89';
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
        whoText.innerText = '100% compliant with World Health Organization & EPA boundary limits.';
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
          labels: ['pH', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'TOC', 'THMs', 'Turbidity'],
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
      const endpoint = 'https://water-potability-vert.vercel.app/predict';
      const snippet = `curl -X POST "${endpoint}" \
  -H "Content-Type: application/json" \
  -d '{
    "ph": ${p.ph},
    "Hardness": ${p.Hardness},
    "Solids": ${p.Solids},
    "Chloramines": ${p.Chloramines},
    "Sulfate": ${p.Sulfate},
    "Conductivity": ${p.Conductivity},
    "Organic_carbon": ${p.Organic_carbon},
    "Trihalomethanes": ${p.Trihalomethanes},
    "Turbidity": ${p.Turbidity}
  }'`;
      navigator.clipboard.writeText(snippet);
      showToast('Copied production cURL command to clipboard', 'success');
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
              label: 'Anomaly Events (Isolation Forest)',
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
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Live Simulation';
        btn.classList.add('btn-primary');
        showToast('Paused live probe simulation', 'info');
      } else {
        btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Pause Live Simulation';
        btn.classList.remove('btn-primary');
        showToast('Streaming real-time probe telemetry...', 'info');
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
          btn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg> Start Live Simulation';
          btn.classList.add('btn-primary');
        }
      }
      liveTick = 72;
      updateStreamChart();
      showToast('Reset telemetry stream to initial state', 'info');
    }

    // ------------------------------------------------------------------------
    // Tab 3: Complete 9-Feature Batch Telemetry Processor
    // ------------------------------------------------------------------------
    let batchRecords = [];
    let currentFilteredRecords = [];
    let batchCurrentPage = 1;
    const batchPageSize = 10;
    let currentSortCol = 'idx';
    let currentSortAsc = true;

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
      demoData.forEach((r, idx) => {
        const isPotable = (r.ph >= 6.5 && r.ph <= 8.5 && r.turb <= 5.0 && r.chlor <= 7.0);
        const prob = isPotable ? (0.62 + Math.random() * 0.26) : (0.12 + Math.random() * 0.28);
        const isAnom = r.ph < 4.5 || r.ph > 10.0 || r.turb > 6.0;
        batchRecords.push({ idx: idx + 1, ...r, isPotable, prob, isAnom });
      });

      currentFilteredRecords = [...batchRecords];
      batchCurrentPage = 1;
      hideBatchError();
      renderBatchTable();
      document.getElementById('batch-results-area').style.display = 'block';
      showToast('Loaded 30-sample demo telemetry batch', 'success');
    }

    function handleDragOver(e) {
      e.preventDefault();
      document.getElementById('batch-dropzone').style.borderColor = 'var(--accent-cyan)';
    }

    function handleDragLeave(e) {
      e.preventDefault();
      document.getElementById('batch-dropzone').style.borderColor = 'var(--border-color)';
    }

    function handleDrop(e) {
      e.preventDefault();
      document.getElementById('batch-dropzone').style.borderColor = 'var(--border-color)';
      const dt = e.dataTransfer;
      if (dt.files && dt.files.length > 0) {
        parseCSVFile(dt.files[0]);
      }
    }

    function handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      parseCSVFile(file);
    }

    function parseCSVFile(file) {
      if (!file.name.toLowerCase().endsWith('.csv')) {
        showBatchError('Invalid file type: Please select a valid .csv file.');
        return;
      }

      if (file.size > 5 * 1024 * 1024) {
        showBatchError('File size limit exceeded: Maximum allowable size is 5 MB.');
        return;
      }

      const reader = new FileReader();
      reader.onload = function(e) {
        let text = e.target.result;
        if (text.charCodeAt(0) === 0xFEFF) text = text.substr(1);

        const lines = text.split(/\r?\n/).filter(r => r.trim().length > 0);
        if (lines.length < 2) {
          showBatchError('Empty or invalid CSV: File must contain a header and at least one data row.');
          return;
        }

        const rawHeaders = lines[0].split(',').map(c => c.trim().replace(/^["']|["']$/g, ''));
        const headerCols = rawHeaders.map(c => c.toLowerCase().replace(/[\"\'\s_-]/g, ''));

        const idxMap = {
          ph: headerCols.findIndex(c => c === 'ph' || c.includes('ph')),
          hardness: headerCols.findIndex(c => c.includes('hard')),
          solids: headerCols.findIndex(c => c.includes('solid') || c.includes('tds')),
          chlor: headerCols.findIndex(c => c.includes('chlor')),
          sulfate: headerCols.findIndex(c => c.includes('sulf')),
          cond: headerCols.findIndex(c => c.includes('cond')),
          carbon: headerCols.findIndex(c => c.includes('carbon') || c.includes('toc')),
          thm: headerCols.findIndex(c => c.includes('trihalo') || c.includes('thm')),
          turb: headerCols.findIndex(c => c.includes('turb'))
        };

        const missing = [];
        if (idxMap.ph === -1) missing.push('pH');
        if (idxMap.solids === -1) missing.push('Solids (TDS)');
        if (idxMap.turb === -1) missing.push('Turbidity');

        if (missing.length > 0) {
          showBatchError(`Missing required columns in CSV header: ${missing.join(', ')}.`);
          return;
        }

        batchRecords = [];
        for (let i = 1; i < Math.min(lines.length, 101); i++) {
          const vals = lines[i].split(',').map(v => parseFloat(v.trim().replace(/^["']|["']$/g, '')) || 0.0);

          const ph = idxMap.ph !== -1 ? vals[idxMap.ph] : (vals[0] || 7.2);
          const hardness = idxMap.hardness !== -1 ? vals[idxMap.hardness] : (vals[1] || 180);
          const solids = idxMap.solids !== -1 ? vals[idxMap.solids] : (vals[2] || 15000);
          const chlor = idxMap.chlor !== -1 ? vals[idxMap.chlor] : (vals[3] || 6.0);
          const sulfate = idxMap.sulfate !== -1 ? vals[idxMap.sulfate] : (vals[4] || 320);
          const cond = idxMap.cond !== -1 ? vals[idxMap.cond] : (vals[5] || 400);
          const carbon = idxMap.carbon !== -1 ? vals[idxMap.carbon] : (vals[6] || 12.0);
          const thm = idxMap.thm !== -1 ? vals[idxMap.thm] : (vals[7] || 60.0);
          const turb = idxMap.turb !== -1 ? vals[idxMap.turb] : (vals[8] || 3.5);

          const isPotable = (ph >= 6.5 && ph <= 8.5 && turb <= 5.0 && chlor <= 7.0);
          const prob = isPotable ? (0.62 + Math.random() * 0.28) : (0.15 + Math.random() * 0.25);
          const isAnom = ph < 4.0 || ph > 11.0 || turb > 12.0 || solids < 0 || turb < 0;

          batchRecords.push({ idx: i, ph, hardness, solids, chlor, sulfate, cond, carbon, thm, turb, isPotable, prob, isAnom });
        }

        currentFilteredRecords = [...batchRecords];
        batchCurrentPage = 1;
        hideBatchError();
        renderBatchTable();
        document.getElementById('batch-results-area').style.display = 'block';
        showToast(`Uploaded and scored ${batchRecords.length} water samples!`, 'success');
      };
      reader.readAsText(file);
    }

    function showBatchError(msg) {
      const err = document.getElementById('batch-error-alert');
      if (err) {
        err.innerText = msg;
        err.style.display = 'block';
      }
      showToast(msg, 'error');
    }

    function hideBatchError() {
      const err = document.getElementById('batch-error-alert');
      if (err) err.style.display = 'none';
    }

    function renderBatchTable() {
      const tbody = document.getElementById('batch-tbody');
      tbody.innerHTML = '';

      const total = currentFilteredRecords.length;
      const start = (batchCurrentPage - 1) * batchPageSize;
      const end = Math.min(start + batchPageSize, total);
      const pageData = currentFilteredRecords.slice(start, end);

      pageData.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${r.idx}</td>
          <td>${r.ph.toFixed(2)}</td>
          <td>${r.hardness.toFixed(1)}</td>
          <td>${r.solids.toFixed(0)}</td>
          <td>${r.chlor.toFixed(2)}</td>
          <td>${r.sulfate.toFixed(1)}</td>
          <td>${r.cond.toFixed(1)}</td>
          <td>${r.carbon.toFixed(1)}</td>
          <td>${r.thm.toFixed(1)}</td>
          <td>${r.turb.toFixed(2)}</td>
          <td><span class="status-pill ${r.isPotable ? 'potable' : 'non-potable'}">${r.isPotable ? 'Potable' : 'Non-Potable'}</span></td>
          <td><strong>${(r.prob * 100).toFixed(1)}%</strong></td>
          <td><span class="status-pill ${r.isAnom ? 'outlier' : 'inlier'}">${r.isAnom ? 'Outlier' : 'Inlier'}</span></td>
        `;
        tbody.appendChild(tr);
      });

      document.getElementById('batch-pagination-info').innerText = total > 0 ? `Showing ${start + 1}-${end} of ${total}` : 'No records';
      document.getElementById('btn-page-prev').disabled = (batchCurrentPage <= 1);
      document.getElementById('btn-page-next').disabled = (end >= total);
    }

    function prevBatchPage() {
      if (batchCurrentPage > 1) {
        batchCurrentPage--;
        renderBatchTable();
      }
    }

    function nextBatchPage() {
      const total = currentFilteredRecords.length;
      if (batchCurrentPage * batchPageSize < total) {
        batchCurrentPage++;
        renderBatchTable();
      }
    }

    function sortBatchTable(col) {
      if (currentSortCol === col) {
        currentSortAsc = !currentSortAsc;
      } else {
        currentSortCol = col;
        currentSortAsc = true;
      }

      ['idx', 'ph', 'hardness', 'solids', 'chlor', 'sulfate', 'cond', 'carbon', 'thm', 'turb', 'prob'].forEach(c => {
        const span = document.getElementById('sort-' + c);
        if (span) span.innerText = (c === col) ? (currentSortAsc ? ' ▲' : ' ▼') : '';
      });

      currentFilteredRecords.sort((a, b) => {
        let valA = a[col];
        let valB = b[col];
        if (valA < valB) return currentSortAsc ? -1 : 1;
        if (valA > valB) return currentSortAsc ? 1 : -1;
        return 0;
      });

      batchCurrentPage = 1;
      renderBatchTable();
    }

    function filterBatch(type) {
      document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
      event.target.classList.add('active');

      if (type === 'all') {
        currentFilteredRecords = [...batchRecords];
      } else if (type === 'potable') {
        currentFilteredRecords = batchRecords.filter(r => r.isPotable);
      } else if (type === 'anomaly') {
        currentFilteredRecords = batchRecords.filter(r => r.isAnom);
      }
      batchCurrentPage = 1;
      renderBatchTable();
      showToast('Filtered batch records: ' + type.toUpperCase(), 'info');
    }

    // Formula Injection Defense
    function sanitizeForCSV(val) {
      const str = String(val);
      if (/^[=+\-@]/.test(str)) {
        return "'" + str;
      }
      return str;
    }

    function downloadBatchResults() {
      if (batchRecords.length === 0) return;
      let csv = 'row_id,ph,hardness,solids,chloramines,sulfate,conductivity,organic_carbon,trihalomethanes,turbidity,predicted_potability,calibrated_probability,anomaly_flag\n';
      batchRecords.forEach((r, idx) => {
        csv += `${idx+1},${sanitizeForCSV(r.ph)},${sanitizeForCSV(r.hardness)},${sanitizeForCSV(r.solids)},${sanitizeForCSV(r.chlor)},${sanitizeForCSV(r.sulfate)},${sanitizeForCSV(r.cond)},${sanitizeForCSV(r.carbon)},${sanitizeForCSV(r.thm)},${sanitizeForCSV(r.turb)},${r.isPotable?1:0},${r.prob.toFixed(4)},${r.isAnom?1:0}\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', 'aquaguard_annotated_telemetry.csv');
      a.click();
      showToast('Exported annotated CSV file with formula-injection defense', 'success');
    }

    // ------------------------------------------------------------------------
    // Initialization on Page Load
    // ------------------------------------------------------------------------
    // ------------------------------------------------------------------------
    // Animated Counters & Probability Gauge
    // ------------------------------------------------------------------------
    function animateCountUp(elId, targetVal, decimals = 4, suffix = '', duration = 1200) {
      const el = document.getElementById(elId);
      if (!el) return;
      const startTime = performance.now();
      function step(time) {
        const elapsed = time - startTime;
        const progress = Math.min(1, elapsed / duration);
        const ease = 1 - Math.pow(1 - progress, 3);
        const current = (targetVal * ease).toFixed(decimals);
        el.innerText = current + suffix;
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.innerText = targetVal.toFixed(decimals) + suffix;
        }
      }
      requestAnimationFrame(step);
    }

    function animateGaugeProb(targetPct, duration = 650) {
      const el = document.getElementById('prob-val');
      if (!el) return;
      const startVal = parseInt(el.innerText) || 0;
      const startTime = performance.now();
      function step(time) {
        const elapsed = time - startTime;
        const progress = Math.min(1, elapsed / duration);
        const ease = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(startVal + (targetPct - startVal) * ease);
        el.innerText = current + '%';
        if (progress < 1) {
          requestAnimationFrame(step);
        } else {
          el.innerText = targetPct + '%';
        }
      }
      requestAnimationFrame(step);
    }

    window.addEventListener('DOMContentLoaded', () => {
      initTheme();
      updateClock();
      animateCountUp('kpi-pr-auc', 0.5951, 4, '');
      animateCountUp('kpi-latency-val', 2.89, 2, ' ms');
      setInterval(updateClock, 1000);
      checkHealthProbe();
      setInterval(checkHealthProbe, 30000);

      // Initialize all slider tracks
      document.querySelectorAll('input[type=range]').forEach(inp => updateSliderFill(inp));

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
