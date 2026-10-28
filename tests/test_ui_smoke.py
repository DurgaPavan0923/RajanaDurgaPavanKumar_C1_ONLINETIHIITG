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
