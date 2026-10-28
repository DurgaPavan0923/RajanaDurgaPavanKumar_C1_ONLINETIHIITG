# Day 04: System Architecture & Pipeline Design
- **Date:** 23 Aug 2026
- **Phase:** Phase 1: Ingestion & Governance
- **Deliverable:** Dual-track pipeline architecture, DAG contracts, and component interface definitions.

---

## 1. System Architecture Overview
The system provides dual-track processing based on data provenance:
- **Track A (Temporal Telemetry Stream):** Continuous sensor readings $\to$ causal lag/rolling feature engineering $\to$ multi-step forecasting + streaming anomaly detection.
- **Track B (Static Physicochemical Benchmark):** 9 bulk water quality features $\to$ domain ratio engineering $\to$ Platt-calibrated classification + WHO compliance audit.

## 2. Ingestion & Pipeline Contracts
1. **Immutable Ingestion:** Raw CSVs in `data/raw/` are cryptographically verified against SHA-256 digests.
2. **Strict Chronology (Track A):** Partitioning preserves chronological order ($T_{train} < T_{val} < T_{test}$). Shuffling is strictly prohibited.
3. **Quarantined Test Set:** 15% (Track A) or 20% (Track B) test partitions are isolated on Day 09 and never touched during model exploration or tuning.
4. **Thin Notebooks:** All heavy algorithmic logic resides in `src/`. Notebooks invoke modular functions and persist outputs in `artifacts/dayXX/`.

## 3. Handoff to Day 05
Define experiment tracking schemas and cryptographic seed protocols to ensure reproducible execution.
