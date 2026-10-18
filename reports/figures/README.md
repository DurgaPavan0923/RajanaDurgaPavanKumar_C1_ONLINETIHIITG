# 📊 AquaGuard AI: Reports & Deliverables Figure Catalog

All figures generated across the 28-day internship schedule are consolidated below with direct links, associated intern schedule days, and technical descriptions.

---

## 1. Catalog of Technical Figures

| Figure File | Schedule Day | Phase | Description & Technical Insights |
|---|:---:|:---:|---|
| [`sensor_streams.png`](sensor_streams.png) | **Day 10** | Phase 1 | Multi-sensor continuous time series trajectories across training partition showing diurnal rhythms and sensor dynamics. |
| [`eda_correlation_matrix.png`](eda_correlation_matrix.png) | **Day 10** | Phase 1 | Cross-sensor Pearson correlation heatmap highlighting physical inverse coupling between Temperature and Dissolved Oxygen. |
| [`eda_sensor_distributions.png`](eda_sensor_distributions.png) | **Day 10** | Phase 1 | Empirical probability density distributions and operating envelopes across all 6 environmental telemetry sensors. |
| [`anomaly_overlay_plot.png`](anomaly_overlay_plot.png) | **Day 15** | Phase 3 | Telemetry time series overlay with unsupervised Isolation Forest multi-sensor anomaly detection flags. |
| [`forecast_vs_actual.png`](forecast_vs_actual.png) | **Day 16** | Phase 3 | Multi-step forecasting benchmark comparing lead step T+1 predictions against actual observed sensor trajectories. |
| [`training_validation_curves.png`](training_validation_curves.png) | **Day 17** | Phase 3 | Advanced XGBoost forecaster training vs. validation MAE convergence curves across tree complexity increments. |
| [`leaderboard_comparison.png`](leaderboard_comparison.png) | **Day 18** | Phase 3 | Cross-method leaderboard comparing Persistence, Ridge, Random Forest, and XGBoost validation error. |
| [`ablation_tornado.png`](ablation_tornado.png) | **Day 20** | Phase 3 | Leave-One-Feature-Out (LOFO) ablation tornado diagram ranking predictive sensitivity across feature groups. |
| [`test_pr_and_calibration.png`](test_pr_and_calibration.png) | **Day 23** | Phase 4 | Precision-Recall curve (PR-AUC = 0.5943) and Platt reliability calibration diagram evaluated on held-out test lockbox. |
| [`feature_importances.png`](feature_importances.png) | **Day 25** | Phase 4 | Mean Gini impurity decrease feature importance ranking across the calibrated tree ensemble. |
| [`stream_simulation.png`](stream_simulation.png) | **Day 26** | Phase 4 | Simulated continuous 48-hour streaming telemetry inference showing real-time threshold and anomaly triggers. |

---

## 2. Reproduction Command

To re-generate all figures from scratch:
```bash
python run_all.py
```
Or via Makefile:
```bash
make run-all
```
