"""Config-Driven Experiment Runner with Cryptographic Seeds, Logging, and Lockbox Governance."""

import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

UTC = timezone.utc

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import StratifiedKFold

from src.data.loader import DataLoader
from src.data.preprocessing import DataPreprocessor
from src.eval.comparison import ModelComparisonEngine
from src.eval.metrics import EvaluationMetrics
from src.features.engineer import FeatureEngineer
from src.logger import get_logger
from src.models.anomaly import IsolationForestAnomalyDetector
from src.models.baselines import PersistenceForecaster, WHORuleClassifier
from src.models.classifier import WaterPotabilityClassifier
from src.models.forecaster import WaterQualityForecaster

logger = get_logger("ExperimentRunner")


class ExperimentRunner:
    """Orchestrates end-to-end model experiments, cross-validation, and lockbox unblinding."""

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = Path(config_path)
        with open(self.config_path, encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.seed = self.config.get("random_state", 42)
        self._set_deterministic_seeds(self.seed)
        self.comparison_engine = ModelComparisonEngine()

    @staticmethod
    def _set_deterministic_seeds(seed: int) -> None:
        random.seed(seed)
        np.random.seed(seed)
        logger.info(f"Deterministic seed pinned to {seed}")

    def log_experiment_entry(
        self,
        log_file: str | Path,
        run_data: dict[str, Any],
    ) -> None:
        """Appends experiment run metadata and metrics to persistent CSV log."""
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp_utc": datetime.now(UTC).isoformat(),
            **run_data,
        }
        df_entry = pd.DataFrame([entry])
        if not log_path.exists():
            df_entry.to_csv(log_path, index=False)
        else:
            df_entry.to_csv(log_path, mode="a", header=False, index=False)

    def run_track_b_experiments(self) -> dict[str, Any]:
        """Executes Track B tabular experiment suite: Stratified CV, Best Model Selection, and Lockbox Test."""
        data_path = self.config.get("raw_data_path", "data/01_raw/water_potability.csv")
        target_col = self.config.get("target_column", "Potability")

        df, track, _ = DataLoader.load_dataset(data_path, force_track="B")
        logger.info(f"Loaded Track B dataset: {df.shape}")

        # 1. Feature Engineering (Domain ratios, log1p, WHO distances)
        df_fe = FeatureEngineer.engineer_track_b_features(df)

        # 2. Split into 80% Dev and 20% Lockbox Test Set
        preprocessor = DataPreprocessor(
            imputation_strategy=self.config.get("preprocessing", {}).get(
                "imputation_strategy", "median"
            ),
            scaling_strategy=self.config.get("preprocessing", {}).get("scaling_strategy", "robust"),
            random_state=self.seed,
        )
        X_dev, X_lockbox, y_dev, y_lockbox = preprocessor.split_track_b(
            df_fe,
            target_col=target_col,
            test_size=self.config.get("split", {}).get("test_lockbox_ratio", 0.20),
        )

        # 4. Leakage-Proof Stratified 5-Fold Cross Validation on Dev Partition
        # Preprocessor MUST be fitted strictly within each fold on train_idx only
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.seed)
        models_to_test = [
            ("WHO_Baseline", WHORuleClassifier()),
            (
                "Logistic_Regression",
                WaterPotabilityClassifier(
                    "logistic_regression", calibrate=False, random_state=self.seed
                ),
            ),
            (
                "Random_Forest",
                WaterPotabilityClassifier("random_forest", calibrate=False, random_state=self.seed),
            ),
            (
                "XGBoost",
                WaterPotabilityClassifier("xgboost", calibrate=False, random_state=self.seed),
            ),
        ]

        leaderboard = []

        for name, model in models_to_test:
            logger.info(
                f"Evaluating {name} on 5-Fold Stratified CV (Dev Set with fold-internal fitting)..."
            )
            cv_praucs, cv_f1s, cv_briers = [], [], []

            for train_idx, val_idx in cv.split(X_dev, y_dev):
                X_tr_raw, X_val_raw = X_dev.iloc[train_idx], X_dev.iloc[val_idx]
                y_tr, y_val = y_dev.iloc[train_idx], y_dev.iloc[val_idx]

                if name == "WHO_Baseline":
                    y_pred = model.predict(X_val_raw)
                    y_prob = model.predict_proba(X_val_raw)[:, 1]
                else:
                    # Fit fold-isolated preprocessor strictly on training fold
                    fold_prep = DataPreprocessor(
                        imputation_strategy=self.config.get("preprocessing", {}).get(
                            "imputation_strategy", "median"
                        ),
                        scaling_strategy=self.config.get("preprocessing", {}).get(
                            "scaling_strategy", "robust"
                        ),
                        random_state=self.seed,
                    )
                    X_tr_trans, _ = fold_prep.fit_transform_train(X_tr_raw)
                    X_val_trans = fold_prep.transform_eval(X_val_raw, fold_prep.pipeline)

                    model.fit(X_tr_trans, y_tr)
                    y_pred = model.predict(X_val_trans)
                    y_prob = model.predict_proba(X_val_trans)[:, 1]

                fold_metrics = EvaluationMetrics.evaluate_classification(y_val, y_pred, y_prob)
                cv_praucs.append(fold_metrics.get("pr_auc", 0.0))
                cv_f1s.append(fold_metrics.get("f1_score", 0.0))
                cv_briers.append(fold_metrics.get("brier_score", 0.0))

            mean_prauc = round(float(np.mean(cv_praucs)), 4)
            mean_f1 = round(float(np.mean(cv_f1s)), 4)
            mean_brier = round(float(np.mean(cv_briers)), 4)

            leaderboard.append(
                {
                    "model_name": name,
                    "cv_pr_auc_mean": mean_prauc,
                    "cv_f1_mean": mean_f1,
                    "cv_brier_mean": mean_brier,
                }
            )

            # Record in comparison engine
            sample_eval = X_val_trans[:100] if name != "WHO_Baseline" else X_val_raw.iloc[:100]
            self.comparison_engine.add_model_evaluation(
                model_name=name,
                track="Track B",
                task="Classification",
                metrics={"cv_pr_auc": mean_prauc, "cv_f1": mean_f1, "cv_brier": mean_brier},
                model_object=model,
                X_sample=sample_eval,
            )

        # 5. Best Candidate Selection based strictly on Validation PR-AUC
        sorted_candidates = sorted(leaderboard, key=lambda x: x["cv_pr_auc_mean"], reverse=True)
        best_candidate_name = sorted_candidates[0]["model_name"]
        logger.info(
            f"Best model candidate selected based on Validation PR-AUC: {best_candidate_name}"
        )

        # Fit production preprocessor on entire Dev set ONLY for the winning model
        prod_preprocessor = DataPreprocessor(
            imputation_strategy=self.config.get("preprocessing", {}).get(
                "imputation_strategy", "median"
            ),
            scaling_strategy=self.config.get("preprocessing", {}).get("scaling_strategy", "robust"),
            random_state=self.seed,
        )
        X_dev_trans, pipeline = prod_preprocessor.fit_transform_train(X_dev)
        X_lockbox_trans = prod_preprocessor.transform_eval(X_lockbox, pipeline)

        if best_candidate_name == "WHO_Baseline":
            best_candidate_model = WHORuleClassifier()
        elif best_candidate_name == "Logistic_Regression":
            best_candidate_model = WaterPotabilityClassifier(
                "logistic_regression", calibrate=True, random_state=self.seed
            )
            best_candidate_model.fit(X_dev_trans, y_dev)
        elif best_candidate_name == "Random_Forest":
            best_candidate_model = WaterPotabilityClassifier(
                "random_forest", calibrate=True, random_state=self.seed
            )
            best_candidate_model.fit(X_dev_trans, y_dev)
        else:  # XGBoost
            best_candidate_model = WaterPotabilityClassifier(
                "xgboost", calibrate=True, random_state=self.seed
            )
            best_candidate_model.fit(X_dev_trans, y_dev)

        # 6. Single-Pass Unblinding of Test-Set Lockbox
        logger.info("Unblinding Test-Set Lockbox for SINGLE-PASS evaluation...")
        if best_candidate_name == "WHO_Baseline":
            y_test_pred = best_candidate_model.predict(X_lockbox)
            y_test_prob = best_candidate_model.predict_proba(X_lockbox)[:, 1]
        else:
            y_test_pred = best_candidate_model.predict(X_lockbox_trans)
            y_test_prob = best_candidate_model.predict_proba(X_lockbox_trans)[:, 1]

        lockbox_metrics = EvaluationMetrics.evaluate_classification(
            y_lockbox, y_test_pred, y_test_prob
        )
        logger.info(f"Lockbox Test Metrics ({best_candidate_name}): {lockbox_metrics}")

        # 7. Unsupervised Anomaly Model on Dev Set
        logger.info("Fitting Unsupervised Isolation Forest Anomaly Detector...")
        iso_forest = IsolationForestAnomalyDetector(contamination=0.05, random_state=self.seed)
        iso_forest.fit(X_dev_trans)
        iso_preds = iso_forest.predict(X_lockbox_trans)
        logger.info(
            f"Anomalies detected in Lockbox Test set: {int(np.sum(iso_preds))} / {len(iso_preds)}"
        )

        # 8. Packaging: Save frozen pipeline + best model bundle
        artifact_dir = Path("models/production")
        artifact_dir.mkdir(parents=True, exist_ok=True)
        production_bundle_path = artifact_dir / "water_potability_pipeline_v1.joblib"

        package = {
            "track": "B",
            "model_name": best_candidate_name,
            "pipeline": pipeline,
            "classifier": best_candidate_model,
            "anomaly_detector": iso_forest,
            "feature_names": list(X_dev.columns),
            "lockbox_test_metrics": lockbox_metrics,
            "timestamp": datetime.now(UTC).isoformat(),
        }
        joblib.dump(package, production_bundle_path)
        logger.info(f"Production pipeline artifact packaged and saved to {production_bundle_path}")

        # 9. Log experiment
        self.log_experiment_entry(
            "reports/experiments_log.csv",
            {
                "track": "B",
                "best_model": best_candidate_name,
                "cv_pr_auc": sorted_candidates[0]["cv_pr_auc_mean"],
                "lockbox_pr_auc": lockbox_metrics.get("pr_auc"),
                "lockbox_f1": lockbox_metrics.get("f1_score"),
                "artifact_path": str(production_bundle_path),
            },
        )

        return {
            "leaderboard": pd.DataFrame(leaderboard),
            "best_model": best_candidate_name,
            "lockbox_metrics": lockbox_metrics,
            "lockbox_test_metrics": lockbox_metrics,
            "artifact_path": str(production_bundle_path),
        }

    def run_track_a_experiments(self) -> dict[str, Any]:
        """Executes Track A temporal stream experiments: Chronological split, forecasting and anomaly detection."""
        data_path = self.config.get("raw_data_path", "data/01_raw/underwater_sensor_stream.csv")
        ts_col = self.config.get("timestamp_column", "timestamp")

        df, track, _ = DataLoader.load_dataset(data_path, force_track="A")
        logger.info(f"Loaded Track A stream: {df.shape}")

        # 1. Feature Engineering: Lags, rolling statistics, cross-sensor ratios
        df_fe = FeatureEngineer.engineer_track_a_features(df, timestamp_col=ts_col)

        # 2. Split chronologically (70/15/15)
        preprocessor = DataPreprocessor(random_state=self.seed)
        train_df, val_df, test_df = preprocessor.split_track_a(df_fe, timestamp_col=ts_col)

        # 3. Target setup: 6-hour ahead forecasting of dissolved_oxygen
        target_sensor = "dissolved_oxygen"
        horizon = 6

        feature_cols = [c for c in train_df.columns if c != ts_col]
        X_train, y_train = WaterQualityForecaster.prepare_forecasting_targets(
            train_df[feature_cols], target_sensor, horizon
        )
        X_val, y_val = WaterQualityForecaster.prepare_forecasting_targets(
            val_df[feature_cols], target_sensor, horizon
        )
        X_test, y_test = WaterQualityForecaster.prepare_forecasting_targets(
            test_df[feature_cols], target_sensor, horizon
        )

        # Preprocessing: Impute and Scale
        X_train_trans, pipeline = preprocessor.fit_transform_train(X_train)
        X_val_trans = preprocessor.transform_eval(X_val, pipeline)
        X_test_trans = preprocessor.transform_eval(X_test, pipeline)

        forecasters = [
            ("Persistence", PersistenceForecaster()),
            (
                "Ridge_Regression",
                WaterQualityForecaster("ridge", {"alpha": 1.0}, random_state=self.seed),
            ),
            (
                "Random_Forest_Regressor",
                WaterQualityForecaster(
                    "random_forest", {"n_estimators": 100}, random_state=self.seed
                ),
            ),
            (
                "XGBoost_Regressor",
                WaterQualityForecaster(
                    "xgboost", {"n_estimators": 150, "learning_rate": 0.05}, random_state=self.seed
                ),
            ),
        ]

        results = []
        for name, model in forecasters:
            if name == "Persistence":
                # Persistence predicts last known value of target_sensor
                last_idx = (
                    list(X_train.columns).index(target_sensor)
                    if target_sensor in X_train.columns
                    else 0
                )
                val_preds = pd.Series(X_val.iloc[:, last_idx]).ffill().bfill().values
            else:
                model.fit(X_train_trans, y_train)
                val_preds = model.predict(X_val_trans)

            m = EvaluationMetrics.evaluate_forecasting(y_val, val_preds)
            results.append({"model_name": name, **m})

            self.comparison_engine.add_model_evaluation(
                model_name=name,
                track="Track A",
                task="Forecasting",
                metrics=m,
                model_object=model,
                X_sample=X_val_trans[:50] if name != "Persistence" else X_val.iloc[:50],
            )

        # Best forecaster selection on Validation MAE
        best_fc = sorted(results, key=lambda x: x["mae"])[0]
        logger.info(
            f"Best Forecaster on Validation set: {best_fc['model_name']} (MAE: {best_fc['mae']})"
        )

        # Test set lockbox evaluation
        best_model_name = best_fc["model_name"]
        if best_model_name != "Persistence":
            best_model_obj = [m for n, m in forecasters if n == best_model_name][0]
            test_preds = best_model_obj.predict(X_test_trans)
        else:
            last_idx = list(X_test.columns).index(target_sensor)
            test_preds = pd.Series(X_test.iloc[:, last_idx]).ffill().bfill().values

        lockbox_fc_metrics = EvaluationMetrics.evaluate_forecasting(y_test, test_preds)
        logger.info(f"Lockbox Test Forecasting Metrics: {lockbox_fc_metrics}")

        # Anomaly detection on stream
        iso = IsolationForestAnomalyDetector(contamination=0.02, random_state=self.seed)
        iso.fit(X_train_trans)
        test_anomalies = iso.predict(X_test_trans)
        logger.info(
            f"Detected anomalies in Test Stream: {int(np.sum(test_anomalies))} / {len(test_anomalies)}"
        )

        # Save Track A artifact
        artifact_path = Path("models/production/underwater_forecaster_v1.joblib")
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(
            {
                "track": "A",
                "model_name": best_model_name,
                "pipeline": pipeline,
                "forecaster": best_model_obj if best_model_name != "Persistence" else None,
                "anomaly_detector": iso,
                "target_sensor": target_sensor,
                "horizon": horizon,
                "lockbox_metrics": lockbox_fc_metrics,
            },
            artifact_path,
        )

        return {
            "leaderboard": pd.DataFrame(results),
            "best_forecaster": best_model_name,
            "lockbox_metrics": lockbox_fc_metrics,
            "artifact_path": str(artifact_path),
        }


if __name__ == "__main__":
    runner = ExperimentRunner("configs/config.yaml")
    print("Running Track B (Tabular Potability Classification)...")
    res_b = runner.run_track_b_experiments()
    print("Track B Best Model:", res_b["best_model"])
    print("Track B Metrics:", res_b["lockbox_test_metrics"])
    print("Running Track A (Temporal Anomaly & Forecasting)...")
    res_a = runner.run_track_a_experiments()
    print("Track A Best Forecaster:", res_a["best_forecaster"])
    print("Track A Metrics:", res_a["lockbox_metrics"])

