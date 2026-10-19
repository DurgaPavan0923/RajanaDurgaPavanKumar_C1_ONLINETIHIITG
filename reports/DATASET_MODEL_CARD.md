# Dataset & Model Card: Water Potability & Environmental Telemetry

## 1. Dataset Card

### Summary
The dataset encompasses two operational telemetry tracks:
- **Track B (Tabular Static Snapshot):** The Kaggle Water Potability dataset consisting of 3,276 water samples collected across distinct geographical monitoring stations. Evaluates 9 continuous physicochemical parameters with binary potability target labels (0 = Not Potable, 1 = Potable).
- **Track A (Temporal Sensor Stream):** A continuous multivariate underwater environmental telemetry stream recording water temperature, dissolved oxygen (DO), pH, conductivity, turbidity, and hydrostatic water column pressure at regular hourly intervals.

### Missing Data & Imbalance Profile
- **Missingness:** Missing values are concentrated in `ph` (~14.99%), `Sulfate` (~23.84%), and `Trihalomethanes` (~4.95%). These are imputed using median and iterative chained regression (MICE) fitted strictly on training partitions to prevent data leakage. Missingness indicator flags (`*_is_missing`) are appended to capture non-random missingness signals.
- **Class Imbalance:** In Track B, 61.0% of records are Non-Potable ($Y=0$) and 39.0% are Potable ($Y=1$). Addressed using algorithmic loss reweighting (`scale_pos_weight = 1.56` in XGBoost, `class_weight='balanced'` in Random Forest/Logistic Regression). SMOTE is avoided to prevent synthetic generation of chemically unphysical equilibria.

---

## 2. Model Card

### Intended Use
- **Primary:** Early warning environmental anomaly screening, industrial/municipal water quality compliance audits, and multi-hour sensor trend forecasting.
- **Safety Criticality:** High. False negatives (classifying toxic water as potable) carry severe human health risks. The model threshold is optimized to prioritize recall ($F_2$-score).
- **Out of Scope:** Replacing certified laboratory microbiological/pathogenic assays (e.g., E. coli, viral cultures, heavy metal ICP-MS).

### Model Architecture & Calibration
- **Model Family:** Calibrated Gradient Boosted Decision Trees (XGBoost) and Random Forests.
- **Probability Calibration:** Platt Scaling (Sigmoidal calibration via `CalibratedClassifierCV`) to ensure that predicted output probabilities represent empirical contamination risks.
- **Anomaly Detection:** Unsupervised Isolation Forest isolating anomalous ionic/sensor telemetry profiles without relying on ground-truth potability labels.
- **Baseline Comparator:** Deterministic World Health Organization (WHO) Drinking-water Guidelines rule engine.

### Metrics on Unblinded Lockbox (Single-Pass Evaluation)
- **PR-AUC:** Superiority over random baseline ($0.39$) and WHO rule baseline.
- **Latency:** Mean per-sample inference latency $< 5.0\text{ ms}$ on standard $x86\_64$ CPU.
- **Artifact Size:** Serialized end-to-end pipeline $< 25\text{ MB}$.
