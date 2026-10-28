"""Smoke and accessibility regression tests for AquaGuard AI Web UI Dashboard."""

import re

from src.serving.api import serve_dashboard
from src.serving.web_ui import HTML_DASHBOARD


def test_ui_serves_html():
    response = serve_dashboard()
    assert response.status_code == 200
    html = response.body.decode("utf-8")
    assert "<!DOCTYPE html>" in html
    assert "AquaGuard AI" in html


def test_ui_design_tokens_and_theme():
    assert "--bg-primary: #070d19" in HTML_DASHBOARD
    assert "--accent-cyan: #06b6d4" in HTML_DASHBOARD
    assert "--accent-emerald: #10b981" in HTML_DASHBOARD
    assert 'data-theme="dark"' in HTML_DASHBOARD
    assert '[data-theme="light"]' in HTML_DASHBOARD


def test_ui_all_four_tabs_present():
    tabs = ["tab-btn-sim", "tab-btn-stream", "tab-btn-batch", "tab-btn-models"]
    for tab in tabs:
        assert f'id="{tab}"' in HTML_DASHBOARD

    panes = ["tab-sim", "tab-stream", "tab-batch", "tab-models"]
    for pane in panes:
        assert f'id="{pane}"' in HTML_DASHBOARD


def test_ui_nine_sliders_present():
    params = [
        "ph", "hardness", "solids", "chloramines", "sulfate",
        "conductivity", "carbon", "thm", "turbidity"
    ]
    for p in params:
        assert f'id="inp-{p}"' in HTML_DASHBOARD
        assert f'id="num-{p}"' in HTML_DASHBOARD


def test_ui_circular_svg_gauge():
    assert "dial-container" in HTML_DASHBOARD
    assert "dial-svg" in HTML_DASHBOARD
    assert 'id="dial-progress"' in HTML_DASHBOARD
    assert 'id="prob-val"' in HTML_DASHBOARD


def test_ui_accessibility_attributes():
    assert 'role="tablist"' in HTML_DASHBOARD
    assert 'role="tab"' in HTML_DASHBOARD
    assert 'role="tabpanel"' in HTML_DASHBOARD
    assert 'aria-live="polite"' in HTML_DASHBOARD
    assert 'prefers-reduced-motion: reduce' in HTML_DASHBOARD


def test_ui_zero_emojis():
    # Regex matching emoji unicode planes and symbols
    emoji_pattern = re.compile(
        r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50]|[\u3030]|'
        r'[\u00a9]|[\u00ae]|[\u203c]|[\u2049]|[\u2122]|[\u2139]|[\u2194-\u21aa]|'
        r'[\u25aa-\u25ab]|[\u25b6]|[\u25c0]|[\u25fb-\u25fe]'
    )
    matches = emoji_pattern.findall(HTML_DASHBOARD)
    assert len(matches) == 0, f"Found {len(matches)} emojis in HTML_DASHBOARD: {matches}"


def test_ui_zero_static_review_dates():
    # Ensure no hardcoded project/review dates exist in the web UI
    pattern = re.compile(r'\b(202[0-9]|october|august|september)\b', re.IGNORECASE)
    matches = pattern.findall(HTML_DASHBOARD)
    assert len(matches) == 0, f"Found static dates in HTML_DASHBOARD: {matches}"


def test_ui_author_and_mentor_attribution():
    assert "Rajana Durga Pavan Kumar" in HTML_DASHBOARD
    assert "Sushil Meher" in HTML_DASHBOARD
    assert "Teaching Assistant" in HTML_DASHBOARD
    assert "Indian Institute of Technology" in HTML_DASHBOARD


def test_ui_live_clock_ist_attributes_and_epoch_zero():
    from datetime import datetime, timezone, timedelta
    import shutil
    import subprocess

    # 1. Accessible attributes and no static placeholder
    assert 'id="live-clock"' in HTML_DASHBOARD
    assert 'aria-label="Current time in Indian Standard Time"' in HTML_DASHBOARD
    assert 'aria-live="off"' in HTML_DASHBOARD
    assert "UTC --:--:--" not in HTML_DASHBOARD
    assert "Asia/Kolkata" in HTML_DASHBOARD
    assert "formatIST" in HTML_DASHBOARD
    assert "IST" in HTML_DASHBOARD

    # 2. Python reference calculation for Epoch 0 in Asia/Kolkata (UTC+05:30)
    ist_tz = timezone(timedelta(hours=5, minutes=30))
    epoch_0_dt = datetime.fromtimestamp(0, tz=timezone.utc).astimezone(ist_tz)
    expected_epoch_0 = epoch_0_dt.strftime("%Y-%m-%d %H:%M:%S IST")
    assert expected_epoch_0 == "1970-01-01 05:30:00 IST"

    # 3. If node is available, execute the exact JS formatIST implementation on epoch 0
    node = shutil.which("node")
    if node:
        js_code = """
        function formatIST(date = new Date()) {
          const parts = new Intl.DateTimeFormat('en-IN', {
            timeZone: 'Asia/Kolkata',
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false,
            hourCycle: 'h23'
          }).formatToParts(date);
          const m = {};
          parts.forEach(p => m[p.type] = p.value);
          return `${m.year}-${m.month}-${m.day} ${m.hour}:${m.minute}:${m.second} IST`;
        }
        console.log(formatIST(new Date(0)));
        """
        out = subprocess.check_output([node, "-e", js_code], text=True).strip()
        assert out == "1970-01-01 05:30:00 IST"

