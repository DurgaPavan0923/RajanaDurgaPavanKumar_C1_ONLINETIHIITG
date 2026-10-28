"""Generates a high-resolution 1200x630 Open Graph preview image for AquaGuard AI."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_og_image(output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 1200x630 px at 100 dpi
    fig = plt.figure(figsize=(12, 6.3), dpi=100)
    fig.patch.set_facecolor("#070d19")
    
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#070d19")
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 630)
    ax.axis("off")
    
    # Subtle background accent glows
    circ1 = patches.Circle((150, 500), 280, color="#06b6d4", alpha=0.08)
    circ2 = patches.Circle((1050, 120), 320, color="#8b5cf6", alpha=0.07)
    circ3 = patches.Circle((950, 480), 220, color="#10b981", alpha=0.06)
    ax.add_patch(circ1)
    ax.add_patch(circ2)
    ax.add_patch(circ3)
    
    # Border card outline
    card = patches.FancyBboxPatch(
        (40, 40), 1120, 550,
        boxstyle="round,pad=10,rounding_size=24",
        facecolor="#0c1527", edgecolor="#1e293b",
        linewidth=2, alpha=0.95
    )
    ax.add_patch(card)
    
    # Header badge
    badge = patches.FancyBboxPatch(
        (80, 490), 210, 42,
        boxstyle="round,pad=5,rounding_size=12",
        facecolor="#06b6d4", alpha=0.15,
        edgecolor="#06b6d4", linewidth=1.5
    )
    ax.add_patch(badge)
    ax.text(185, 511, "AQUAGUARD AI v2.1.0", color="#06b6d4", fontsize=12,
            fontweight="bold", ha="center", va="center", family="sans-serif")
    
    # Title
    ax.text(80, 420, "AquaGuard AI", color="#f8fafc", fontsize=44,
            fontweight="heavy", ha="left", va="center", family="sans-serif")
    ax.text(80, 360, "Calibrated Water Potability & WHO/EPA Compliance Intelligence",
            color="#94a3b8", fontsize=19, fontweight="normal", ha="left", va="center", family="sans-serif")
    
    # Metric KPI Cards
    kpis = [
        {"title": "LOCKBOX PR-AUC", "val": "0.5951", "sub": "vs 0.3920 WHO baseline", "color": "#06b6d4"},
        {"title": "OPTIMAL F1 SCORE", "val": "0.5480", "sub": "Threshold T* = 0.38", "color": "#10b981"},
        {"title": "INFERENCE LATENCY", "val": "2.89 ms", "sub": "Sub-3ms FastAPI engine", "color": "#38bdf8"},
        {"title": "WHO GUARDRAILS", "val": "9 / 9", "sub": "Deterministic auditor", "color": "#a855f7"},
    ]
    
    card_w, card_h = 245, 135
    start_x = 80
    y_pos = 175
    
    for i, k in enumerate(kpis):
        x = start_x + i * (card_w + 22)
        k_card = patches.FancyBboxPatch(
            (x, y_pos), card_w, card_h,
            boxstyle="round,pad=6,rounding_size=14",
            facecolor="#111c34", edgecolor="#263b61",
            linewidth=1.2, alpha=0.9
        )
        ax.add_patch(k_card)
        ax.text(x + 20, y_pos + 102, k["title"], color="#94a3b8", fontsize=10,
                fontweight="bold", ha="left", va="center", family="sans-serif")
        ax.text(x + 20, y_pos + 60, k["val"], color=k["color"], fontsize=26,
                fontweight="bold", ha="left", va="center", family="sans-serif")
        ax.text(x + 20, y_pos + 25, k["sub"], color="#64748b", fontsize=9.5,
                fontweight="normal", ha="left", va="center", family="sans-serif")
    
    # Footer attribution
    ax.text(80, 85, "Author: Rajana Durga Pavan Kumar (Group C1)  |  Mentor: Sushil Meher (Teaching Assistant, IIT Guwahati)",
            color="#94a3b8", fontsize=12, fontweight="medium", ha="left", va="center", family="sans-serif")
    ax.text(1120, 85, "TIH IIT Guwahati AI/ML Internship",
            color="#06b6d4", fontsize=12, fontweight="bold", ha="right", va="center", family="sans-serif")
    
    plt.savefig(output_path, dpi=100, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated OG image at {output_path}")

if __name__ == "__main__":
    create_og_image(Path("public/og-image.png"))
