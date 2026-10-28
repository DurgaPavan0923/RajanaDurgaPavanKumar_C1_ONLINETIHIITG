# 🌊 Day 10 - Task 2: Correlation Heatmap & Domain Hypotheses
### 🏛️ TIH IIT Guwahati — AI/ML Internship (Cohort 4) | Group C1
**Candidate:** Rajana Durga Pavan Kumar  
**Target Repository:** `RajanaDurgaPavanKumar_C1_ONLINETIHIITG`  
**Phase Topic:** Day 10 — Environmental Telemetry EDA & Hypotheses Formulation  

---

## 📌 1. Task Objective & Context
Cross-sensor Pearson correlation matrix and formal hypotheses table linking DO, temp, and pH.

## 🛠️ 2. Key Technical Methodology & Implementation
- **Mathematical & Engineering Rigor:** Standardized under deterministic random seed (`seed=42`), zero data-leakage boundaries, and modular component testing.
- **Pipeline Role:** Serves as an immutable scheduled milestone within the 28-day developmental lifecycle.
- **Upstream Inputs Consumed:** Prior day artifacts and centralized datasets (`data/01_raw/`).

## 📂 3. Files & Artifacts in this Directory
- [`eda_correlation_matrix.png`](./eda_correlation_matrix.png) — Primary deliverable / verification artifact.
- [`eda_sensor_distributions.png`](./eda_sensor_distributions.png) — Primary deliverable / verification artifact.
- [`hypotheses_table.csv`](./hypotheses_table.csv) — Primary deliverable / verification artifact.

## 🚀 4. How to Execute / Reproduce
To execute or verify this task independently from the repository root:

```bash
# Navigate to directory or run command directly
cat hypotheses_table.csv
```

## ✅ 5. Verification & Compliance Status
- **Status:** **VERIFIED & COMPLIANT**
- **Test Suite Alignment:** Verified against master `pytest tests/ -v` quality gate.
- **Artifact Integrity:** Cryptographically attested and validated against baseline metrics.
