# Day 03: Metric Strategy & Evaluation Formulation
- **Phase:** Phase 1: Ingestion & Governance
- **Deliverable:** Mathematical formulation of evaluation metrics, imbalance penalties, and temporal forecasting loss functions.

---

## 1. Objectives & Context
Design evaluation criteria that align with public health hazards (False Negatives = toxic water classified as safe) and environmental operational forecasting.

## 2. Classification Metrics (Track B)
1. **Precision-Recall AUC (PR-AUC):**
   $$\text{PR-AUC} = \int_{0}^{1} P(R) \, dR$$
   Primary metric for model selection due to class imbalance (~39% potable). Avoids inflated ROC-AUC scores driven by true negatives.
2. **Brier Score (Probability Calibration):**
   $$\text{BS} = \frac{1}{N} \sum_{i=1}^{N} (f_i - y_i)^2$$
   Measures calibrated reliability of predicted probabilities ($0 \le \text{BS} \le 1$). Lower is better.
3. **$F_2$ Score (Recall-Biased Hazard Mitigation):**
   $$F_2 = (1 + 2^2) \frac{\text{Precision} \cdot \text{Recall}}{2^2 \cdot \text{Precision} + \text{Recall}}$$
   Weights recall twice as heavily as precision to penalize critical False Negatives.

## 3. Time-Series Forecasting Metrics (Track A)
1. **Mean Absolute Error (MAE):** $\text{MAE} = \frac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|$ (Robust against heavy sensor outliers).
2. **Root Mean Squared Error (RMSE):** $\text{RMSE} = \sqrt{\frac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2}$ (Penalizes large sudden sensor deviations).
3. **Mean Directional Accuracy (MDA):** Verifies whether the model predicts the correct direction of sensor shift ($\Delta y$).

## 4. Handoff to Day 04
Integrate metric definitions into system architecture design and component API interfaces.
