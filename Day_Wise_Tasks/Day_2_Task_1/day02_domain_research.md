# Day 02: Domain Research, Sensor Specifications & WHO Standards
- **Phase:** Phase 1: Ingestion & Governance
- **Deliverable:** Physicochemical domain range catalog, sensor calibration standards, and WHO drinking water guideline envelopes.

---

## 1. Objectives & Context
Formulate physical and chemical boundary constraints governing aquatic sensors. Establish deterministic regulatory baselines for drinking water safety and continuous environmental telemetry monitoring.

## 2. Sensor Physical Boundary Specifications
| Parameter | Minimum Plausible | Maximum Plausible | Physical Units | Failure / Anomaly Mode |
| :--- | :---: | :---: | :--- | :--- |
| **Temperature** | -2.0 | 45.0 | °C | Thermal shock, ice freeze, hydrothermal vent |
| **Dissolved Oxygen (DO)** | 0.0 | 25.0 | mg/L | Anoxia (<2.0 mg/L), supersaturation (>14.0 mg/L) |
| **pH** | 0.0 | 14.0 | pH units | Acidic contamination (<6.5), extreme alkalosis (>8.5) |
| **Conductivity** | 10.0 | 2000.0 | µS/cm | Saline intrusion, heavy industrial ion dump |
| **Turbidity** | 0.0 | 100.0 | NTU | Sediment suspension, algal bloom, sensor fouling |
| **Pressure** | 0.0 | 500.0 | dbar | Depth gauge malfunction, sensor drift |

## 3. World Health Organization (WHO) Guideline Envelopes
Deterministic thresholds for potable human consumption:
- **pH:** $6.5 \le \text{pH} \le 8.5$
- **Solids (TDS):** $\le 1000.0 \text{ mg/L}$
- **Chloramines:** $\le 4.0 \text{ mg/L}$
- **Sulfate:** $\le 250.0 \text{ mg/L}$
- **Conductivity:** $\le 400.0 \text{ µS/cm}$
- **Organic Carbon:** $\le 4.0 \text{ mg/L}$
- **Trihalomethanes:** $\le 80.0 \text{ µg/L}$
- **Turbidity:** $\le 5.0 \text{ NTU}$

## 4. Handoff to Day 03
Carry forward the physical bounds and regulatory boundaries to formulate loss functions, evaluation metrics, and asymmetric risk penalties.
