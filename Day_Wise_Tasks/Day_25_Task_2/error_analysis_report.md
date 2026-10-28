# AquaGuard AI — Error Analysis & Operational Limitations Report
- **Test Lockbox Evaluated:** 656 samples

## 1. Hazard Audit (False Negatives)
- **Total Critical False Negatives:** 31
- **Top Violation Culprit:** Sulfate and Chloramines levels exceeding WHO drinking guidelines while other 7 parameters remained within bounds.
- **Safety Mitigation:** The REST serving layer enforces deterministic WHO Rule baseline overriding. Any sample with a guideline violation is flagged with a warning regardless of model probability.

## 2. Operational Limitations
1. Static bulk measurements cannot replace microbial pathogen or coliform testing.
2. Rapid industrial chemical spills may exhibit parameters within physical bounds but abnormal multi-ion ratios.
3. Temperature sensor drift requires bi-weekly calibration in marine deployments.
