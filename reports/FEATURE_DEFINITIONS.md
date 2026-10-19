# Feature Definitions & Predictive Lineage Documentation

## 1. Track B: Static Physicochemical Water Features

| Feature Name | Origin | Physical Unit | Domain Range | Formulation / Rationale | Available at Inference? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `ph` | Raw | Dimensionless | 0.0 - 14.0 | Acid-base equilibrium. | Yes |
| `Hardness` | Raw | mg/L CaCO3 | 40 - 450 | Polyvalent cations (Ca2+, Mg2+). | Yes |
| `Solids` | Raw | ppm | 100 - 60000 | Total dissolved mineral content. | Yes |
| `Chloramines` | Raw | ppm | 0.0 - 15.0 | Disinfection byproducts. | Yes |
| `Sulfate` | Raw | mg/L | 20 - 600 | Dissolved sulfate minerals. | Yes |
| `Conductivity` | Raw | uS/cm | 50 - 1000 | Ionic mobility index. | Yes |
| `Organic_carbon` | Raw | ppm | 1.0 - 35.0 | Total dissolved organic matter. | Yes |
| `Trihalomethanes` | Raw | ug/L | 0.0 - 150.0 | Volatile halogenated byproducts. | Yes |
| `Turbidity` | Raw | NTU | 0.0 - 10.0 | Light scattering suspended matter. | Yes |
| `solids_log1p` | Engineered | log(ppm) | 4.6 - 11.0 | `log1p(Solids)` to stabilize heavy right tail. | Yes |
| `sulfate_to_conductivity` | Engineered | Ratio | 0.0 - 5.0 | `Sulfate / Conductivity` proxy for sulfate mineral fraction. | Yes |
| `organic_to_solids` | Engineered | Ratio | 0.0 - 0.01 | Dissolved carbon proportion of total solids. | Yes |
| `hardness_to_solids` | Engineered | Ratio | 0.0 - 0.5 | Hardness cation fraction. | Yes |
| `chloramines_x_turbidity`| Engineered | Interaction | 0.0 - 100.0 | Disinfectant shielding interaction. | Yes |
| `ph_dev_neutral` | Engineered | Absolute delta| 0.0 - 7.0 | `abs(ph - 7.0)` measures deviation from neutral. | Yes |
| `ph_who_out_of_bounds` | Engineered | Binary | {0, 1} | 1 if pH < 6.5 or pH > 8.5 (WHO violation). | Yes |
| `turbidity_who_excess` | Engineered | Binary | {0, 1} | 1 if Turbidity > 5.0 NTU. | Yes |
| `chloramines_who_excess`| Engineered | Binary | {0, 1} | 1 if Chloramines > 4.0 ppm. | Yes |

---

## 2. Track A: Underwater Environmental Stream Features

| Feature Name | Origin | Physical Unit | Description | Available at Inference? |
| :--- | :--- | :--- | :--- | :--- |
| `temperature` | Raw | deg C | Water sensor temperature. | Yes |
| `dissolved_oxygen` | Raw | mg/L | Dissolved oxygen concentration. | Yes |
| `pressure` | Raw | dbar | Hydrostatic water column pressure. | Yes |
| `hour_sin`, `hour_cos` | Engineered | Periodic | Diurnal Fourier encoding of timestamp hour. | Yes |
| `*_lag_k` | Engineered | Sensor units | Past observation at $t-k$ hours. | Yes |
| `*_roll_mean_w` | Engineered | Sensor units | Past rolling average over window $w$ (closed='left'). | Yes |
| `*_roll_std_w` | Engineered | Sensor units | Past rolling volatility over window $w$ (closed='left'). | Yes |
| `do_to_temp_ratio` | Engineered | Ratio | Solubility equilibrium proxy ($DO / (T + 20)$). | Yes |
