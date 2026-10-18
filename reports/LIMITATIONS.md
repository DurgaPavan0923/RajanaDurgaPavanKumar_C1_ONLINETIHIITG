# Operational Limitations & Vulnerability Register

## 1. Microbiological & Biological Blindspot
The model relies entirely on bulk physicochemical sensors (pH, Conductivity, Turbidity, Sulfate, Chloramines). It does not measure microbiological pathogens (e.g., *Giardia lamblia*, *Cryptosporidium*, *Escherichia coli*, norovirus) or trace heavy metals (Lead, Arsenic, Cadmium). High clarity/neutral pH water can still harbor deadly biological pathogens. The model must always be paired with secondary disinfectant verification.

## 2. Cross-Sensor Synergistic Non-Linearities
Chemical equilibria are non-linear. For example, the toxicity of Chloramines and Trihalomethanes varies drastically as a function of temperature and pH. While gradient-boosted decision trees capture feature interactions better than linear models, extreme multivariate shifts outside training convex hulls will yield uncalibrated risk predictions.

## 3. Sensor Drift, Biofouling & Salinity Saturation
In continuous underwater marine/river environments (Track A):
- Biofouling on optical turbidity lenses causes artificial upward baseline drift over 2–4 weeks.
- Galvanic dissolved oxygen membranes experience chemical depletion.
- High salinity/conductive environments can saturate standard low-power conductivity probes.
The pipeline provides an Isolation Forest drift detector, but physical recalibration remains mandatory.

## 4. Single-Pass Lockbox Governance
To maintain scientific reproducibility and eliminate cognitive data leakage, the 20% test partition (`data/04_lockbox/`) was unblinded exactly once. The model weights and preprocessing rules cannot be tuned on the test set post-evaluation.
