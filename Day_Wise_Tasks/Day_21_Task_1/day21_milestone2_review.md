# Day 21: Milestone 2 Review — Modeling, Ablation & Architecture Selection
- **Date:** 09 Sep 2026
- **Phase:** Phase 3: Modeling & Validation Review
- **Deliverable:** Formal model selection decision log, validation benchmark review, and champion architecture freeze sign-off.

---

## 1. Candidate Architecture Review
| Architecture | Track | Primary Metric | Validation Performance | Inferred Latency | Status |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Persistence Forecaster** | Track A | MAE (DO) | Baseline | 0.05 ms | Baseline |
| **Multi-Step Ridge** | Track A | MAE (DO) | 0.312 mg/L | 0.12 ms | Linear Benchmark |
| **Random Forest Forecaster** | Track A | MAE (DO) | **0.248 mg/L** | 1.84 ms | **Champion Forecaster** |
| **WHO Rule Classifier** | Track B | PR-AUC | 0.3902 | 0.10 ms | Regulatory Baseline |
| **Logistic Regression** | Track B | PR-AUC | 0.4674 | 0.15 ms | Linear Benchmark |
| **Calibrated Random Forest** | Track B | PR-AUC | **0.5788** | 1.95 ms | **Champion Classifier** |

## 2. Robustness & Ablation Sign-Off
- LOFO ablation on Day 20 confirmed highest positive impact from dissolved oxygen lags (1h, 3h) and temperature-DO coupling.
- Elimination of high-collinearity noise features validated.

## 3. Decision Log & Sign-Off
- **Status:** APPROVED for Final Model Freezing (Day 22) and Single-Pass Lockbox Unblinding (Day 23).
