"""Command Line Interface (CLI) for Water Potability & Monitoring Pipeline."""

import argparse
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml

from src.data.audit import DataQualityAuditor
from src.data.loader import DataLoader
from src.features.engineer import FeatureEngineer
from src.logger import get_logger
from src.pipeline.runner import ExperimentRunner

logger = get_logger("CLI")


def cmd_verify_data(args: argparse.Namespace) -> None:
    """Verifies cryptographic hashes of raw data."""
    config_path = Path(args.config)
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    checksums = cfg.get("data", {}).get("checksums", {})
    all_ok = True
    for _track_key, meta in checksums.items():
        fname = meta.get("filename")
        expected_sha = meta.get("sha256")
        fpath = Path(cfg.get("data", {}).get("raw_dir", "data/01_raw")) / fname
        if not fpath.exists():
            logger.error(f"Missing file: {fpath}")
            all_ok = False
            continue
        if not DataLoader.verify_checksum(fpath, expected_sha):
            all_ok = False

    if not all_ok:
        sys.exit(1)
    logger.info("All raw data checksums verified successfully.")


def cmd_audit(args: argparse.Namespace) -> None:
    """Runs data quality audit on specified dataset."""
    data_path = Path(args.data)
    out_path = Path(args.out)

    df, track, ts_col = DataLoader.load_dataset(data_path)
    auditor = DataQualityAuditor()

    if track == "A" and ts_col:
        res = auditor.audit_temporal(df, timestamp_col=ts_col)
    else:
        target = "Potability" if "Potability" in df.columns else None
        res = auditor.audit_tabular(df, target_col=target)

    csv_path, md_path = auditor.export_reports(res, out_path.with_suffix(""))
    print(f"Data audit complete.\nCSV Report: {csv_path}\nMarkdown Report: {md_path}")


def cmd_train(args: argparse.Namespace) -> None:
    """Executes config-driven experiment suite and saves production artifacts."""
    runner = ExperimentRunner(args.config)
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    track = cfg.get("track", "B")
    if track == "B":
        results = runner.run_track_b_experiments()
    else:
        results = runner.run_track_a_experiments()

    print("\n=== Experiment Execution Completed Successfully ===")
    print(f"Track: {track}")
    print(f"Best Candidate Model: {results.get('best_model') or results.get('best_forecaster')}")
    print(f"Lockbox Test Metrics: {results.get('lockbox_metrics')}")
    print(f"Production Artifact: {results.get('artifact_path')}")


def cmd_evaluate(args: argparse.Namespace) -> None:
    """Evaluates frozen production artifact against test set."""
    runner = ExperimentRunner(args.config)
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    track = cfg.get("track", "B")
    if track == "B":
        results = runner.run_track_b_experiments()
    else:
        results = runner.run_track_a_experiments()
    print(f"Evaluation Complete: {results['lockbox_metrics']}")


def cmd_predict(args: argparse.Namespace) -> None:
    """Executes batch inference using frozen production bundle."""
    input_path = Path(args.input).resolve()
    output_path = Path(args.out).resolve()
    model_path = Path(args.model).resolve()
    workspace_root = Path(".").resolve()

    # Security check: Prevent path traversal outside repository
    if not str(model_path).startswith(str(workspace_root)):
        logger.error(f"Security Violation: Model path traversal detected: {args.model}")
        sys.exit(1)

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)

    if not model_path.exists():
        logger.error(f"Model bundle not found: {model_path}. Train the model first.")
        sys.exit(1)

    df_in = pd.read_csv(input_path)
    bundle = joblib.load(model_path)
    pipeline = bundle["pipeline"]
    classifier = bundle["classifier"]
    anomaly_detector = bundle.get("anomaly_detector")

    # Feature engineering
    df_fe = FeatureEngineer.engineer_track_b_features(df_in)
    training_cols = bundle.get("feature_names", list(df_fe.columns))
    for c in training_cols:
        if c not in df_fe.columns:
            df_fe[c] = np.nan
    aligned = df_fe[training_cols]

    X_trans = pipeline.transform(aligned)
    probas = (
        classifier.predict_proba(X_trans)[:, 1]
        if hasattr(classifier, "predict_proba")
        else classifier.predict(X_trans)
    )
    preds = (probas >= 0.50).astype(int)

    df_out = df_in.copy()
    df_out["predicted_potability"] = preds
    df_out["potability_probability"] = np.round(probas, 4)

    if anomaly_detector is not None:
        df_out["anomaly_flag"] = anomaly_detector.predict(X_trans)
        df_out["anomaly_score"] = np.round(anomaly_detector.score_samples(X_trans), 4)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(output_path, index=False)
    logger.info(f"Batch prediction written to {output_path} ({len(df_out)} records)")


def main():
    parser = argparse.ArgumentParser(
        prog="water_monitor",
        description="Water Potability & Environmental Telemetry CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # verify-data
    p_verify = subparsers.add_parser("verify-data", help="Verify raw data SHA-256 hashes")
    p_verify.add_argument(
        "--config", default="configs/base_config.yaml", help="Path to base config"
    )

    # audit
    p_audit = subparsers.add_parser("audit", help="Run data quality audit")
    p_audit.add_argument("--data", required=True, help="Path to input data CSV")
    p_audit.add_argument(
        "--out", default="reports/audit_report.md", help="Output report prefix or path"
    )

    # train
    p_train = subparsers.add_parser("train", help="Train models per configuration")
    p_train.add_argument(
        "--config", default="configs/track_b_tabular.yaml", help="Config YAML path"
    )

    # evaluate
    p_eval = subparsers.add_parser("evaluate", help="Evaluate frozen model on test lockbox")
    p_eval.add_argument("--config", default="configs/track_b_tabular.yaml", help="Config YAML path")

    # predict
    p_pred = subparsers.add_parser("predict", help="Run batch predictions")
    p_pred.add_argument("--input", required=True, help="Input CSV path")
    p_pred.add_argument("--out", required=True, help="Output CSV path")
    p_pred.add_argument(
        "--model",
        default="models/production/water_potability_pipeline_v1.joblib",
        help="Model path",
    )

    args = parser.parse_args()

    if args.command == "verify-data":
        cmd_verify_data(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "train":
        cmd_train(args)
    elif args.command == "evaluate":
        cmd_evaluate(args)
    elif args.command == "predict":
        cmd_predict(args)


if __name__ == "__main__":
    main()
