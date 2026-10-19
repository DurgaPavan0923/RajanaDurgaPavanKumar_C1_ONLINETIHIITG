"""Sensor and Feature Ablation Study Engine."""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold

from src.eval.metrics import EvaluationMetrics
from src.logger import get_logger
from src.models.classifier import WaterPotabilityClassifier

logger = get_logger("FeatureAblationEngine")


class FeatureAblationEngine:
    """Executes systematic leave-one-feature-out (LOFO) and sensor ablation on validation folds."""

    def __init__(self, random_state: int = 42) -> None:
        self.random_state = random_state

    def run_tabular_ablation(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        base_features: list[str],
    ) -> pd.DataFrame:
        """Evaluates model performance degradation when each individual feature is removed."""
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)

        # Baseline with all features
        def eval_feature_subset(feat_cols: list[str]) -> float:
            praucs = []
            for tr_idx, val_idx in cv.split(X[feat_cols], y):
                X_tr, X_v = X[feat_cols].iloc[tr_idx], X[feat_cols].iloc[val_idx]
                y_tr, y_v = y.iloc[tr_idx], y.iloc[val_idx]

                # Impute missing values with median for quick ablation comparison
                imputed_tr = X_tr.fillna(X_tr.median())
                imputed_v = X_v.fillna(X_tr.median())

                clf = WaterPotabilityClassifier(
                    "xgboost", random_state=self.random_state, calibrate=False
                )
                clf.fit(imputed_tr, y_tr)
                preds = clf.predict_proba(imputed_v)[:, 1]

                m = EvaluationMetrics.evaluate_classification(
                    y_v, (preds >= 0.5).astype(int), preds
                )
                praucs.append(m.get("pr_auc", 0.0))
            return float(np.mean(praucs))

        base_prauc = eval_feature_subset(base_features)
        logger.info(f"Baseline PR-AUC with all {len(base_features)} features: {base_prauc:.4f}")

        ablation_results = [
            {"ablated_feature": "NONE (Full Baseline)", "pr_auc": base_prauc, "delta_pr_auc": 0.0}
        ]

        for feat in base_features:
            reduced = [c for c in base_features if c != feat]
            score = eval_feature_subset(reduced)
            delta = round(score - base_prauc, 4)
            ablation_results.append(
                {
                    "ablated_feature": feat,
                    "pr_auc": round(score, 4),
                    "delta_pr_auc": delta,
                }
            )
            logger.info(f"Ablation [-{feat}]: PR-AUC={score:.4f} (Delta={delta:+.4f})")

        df_ablation = pd.DataFrame(ablation_results).sort_values(by="delta_pr_auc")
        return df_ablation


if __name__ == "__main__":
    from src.data.loader import DataLoader
    from src.features.engineer import FeatureEngineer

    df, _, _ = DataLoader.load_dataset("data/01_raw/water_potability.csv", force_track="B")
    df_fe = FeatureEngineer.engineer_track_b_features(df)
    X = df_fe.drop(columns=["Potability"])
    y = df_fe["Potability"]
    engine = FeatureAblationEngine(random_state=42)
    res = engine.run_tabular_ablation(X, y, list(X.columns)[:6])
    print(res)

