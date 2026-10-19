# 🌊 Day 06: Data Governance, Immutability & Lockbox Protocol
- **Date:** 25 Aug 2026
- **Phase:** Phase 1: Ingestion & Governance
- **Deliverable:** Data provenance attestations, cryptographic raw checksum seals, and Lockbox quarantine protocol.

---

## 1. Raw Dataset Provenance
1. **`data/raw/water_potability.csv`**:
   - Source: Kaggle Water Quality Benchmark.
   - Record Count: 3,276 samples across 9 physicochemical attributes.
   - SHA-256 Checksum: `904004BDE729BFE3D2E195F46343BCEEAD09E32A0EB95BB8184E7E20E029B2BF`.
2. **`data/raw/underwater_sensor_stream.csv`**:
   - Source: Oceanographic sensor telemetry node.
   - Record Count: 720 continuous hourly steps.
   - SHA-256 Checksum: `E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855` (Verified).

## 2. Lockbox Quarantine Rules
- **No Early Peeking:** Lockbox partitions (`data/processed/dataset_v1_test_lockbox.parquet`) must never be inspected, visualized, or used for model selection.
- **Single-Pass Unblinding:** The Lockbox is accessed exactly once on Day 23 after final model freeze on Day 22.

## 3. Handoff to Day 07
Commence notebook execution with Day 07 initial inspection and cryptographic attestation.
