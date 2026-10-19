"""Preprocessing, Leakage-Proof Splitting, and Sklearn Pipeline Composition."""

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, StandardScaler

from src.exceptions import DataLeakageError
from src.logger import get_logger

logger = get_logger("DataPreprocessor")


class MissingIndicatorAppender(BaseEstimator, TransformerMixin):
    """Custom transformer to append binary missingness indicators (*_is_missing)."""

    def __init__(self, columns_to_track: list[str] | None = None) -> None:
        self.columns_to_track = columns_to_track
        self.feature_names_out_: list[str] = []

    def fit(self, X: pd.DataFrame | np.ndarray, y: Any = None) -> "MissingIndicatorAppender":
        if isinstance(X, pd.DataFrame):
            self.cols_ = self.columns_to_track or list(X.columns)
        else:
            self.cols_ = [f"feat_{i}" for i in range(X.shape[1])]
        return self

    def transform(self, X: pd.DataFrame | np.ndarray) -> pd.DataFrame:
        if isinstance(X, np.ndarray):
            X_df = pd.DataFrame(X, columns=self.cols_)
        else:
            X_df = X.copy()

        for col in self.cols_:
            if col in X_df.columns:
                X_df[f"{col}_is_missing"] = X_df[col].isna().astype(float)
        return X_df


class DomainBoundsClipper(BaseEstimator, TransformerMixin):
    """Clips features to physically plausible water sensor limits."""

    def __init__(self, bounds: dict[str, tuple[float, float]] | None = None) -> None:
        self.bounds = bounds or {
            "ph": (0.0, 14.0),
            "Hardness": (10.0, 500.0),
            "Solids": (100.0, 100000.0),
            "Chloramines": (0.0, 25.0),
            "Sulfate": (10.0, 800.0),
            "Conductivity": (10.0, 2000.0),
            "Organic_carbon": (0.0, 50.0),
            "Trihalomethanes": (0.0, 250.0),
            "Turbidity": (0.0, 25.0),
            "temperature": (-5.0, 50.0),
            "dissolved_oxygen": (0.0, 25.0),
            "pressure": (0.0, 600.0),
        }

    def fit(self, X: Any, y: Any = None) -> "DomainBoundsClipper":
        return self

    def transform(self, X: pd.DataFrame | np.ndarray) -> pd.DataFrame:
        if isinstance(X, np.ndarray):
            return X
        X_df = X.copy()
        for col, (lower, upper) in self.bounds.items():
            if col in X_df.columns:
                X_df[col] = X_df[col].clip(lower=lower, upper=upper)
        return X_df


class DataPreprocessor:
    """Manages train/test splits, pipeline fitting, and processed dataset persistence."""

    def __init__(
        self,
        imputation_strategy: str = "median",
        scaling_strategy: str = "robust",
        knn_neighbors: int = 5,
        random_state: int = 42,
    ) -> None:
        self.imputation_strategy = imputation_strategy
        self.scaling_strategy = scaling_strategy
        self.knn_neighbors = knn_neighbors
        self.random_state = random_state
        self.pipeline: Pipeline | None = None

    def split_track_b(
        self,
        df: pd.DataFrame,
        target_col: str = "Potability",
        test_size: float = 0.20,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Performs stratified train/test split on Track B tabular data.

        Guarantees zero overlap and strict separation of the Lockbox test set.
        """
        if target_col not in df.columns:
            raise KeyError(f"Target column '{target_col}' not found in dataframe.")

        X = df.drop(columns=[target_col])
        y = df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            stratify=y,
            random_state=self.random_state,
        )

        # Leakage guard verification
        overlap = set(X_train.index).intersection(set(X_test.index))
        if overlap:
            raise DataLeakageError(
                f"Data leakage detected! {len(overlap)} rows overlap between train and test."
            )

        logger.info(
            f"Track B Split complete: Train={len(X_train)} (Positive={y_train.mean():.2%}), "
            f"Test Lockbox={len(X_test)} (Positive={y_test.mean():.2%})"
        )
        return X_train, X_test, y_train, y_test

    def split_track_a(
        self,
        df: pd.DataFrame,
        timestamp_col: str = "timestamp",
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
    ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Performs strict chronological walk-forward split (e.g. 70% Train, 15% Val, 15% Test).

        Shuffling is strictly prohibited to prevent temporal leakage.
        """
        df_sorted = df.sort_values(by=timestamp_col).reset_index(drop=True)
        n = len(df_sorted)
        train_end = int(n * train_ratio)
        val_end = int(n * (train_ratio + val_ratio))

        train_df = df_sorted.iloc[:train_end].copy()
        val_df = df_sorted.iloc[train_end:val_end].copy()
        test_df = df_sorted.iloc[val_end:].copy()

        # Leakage check: verify timestamps are non-overlapping and strictly increasing
        t_train_max = train_df[timestamp_col].max()
        t_val_min = val_df[timestamp_col].min()
        t_val_max = val_df[timestamp_col].max()
        t_test_min = test_df[timestamp_col].min()

        if t_train_max >= t_val_min or t_val_max >= t_test_min:
            raise DataLeakageError(
                "Temporal leakage! Chronological partition boundaries violate causality."
            )

        logger.info(
            f"Track A Chronological Split: Train={len(train_df)} ({train_df[timestamp_col].min()} to {t_train_max}), "
            f"Val={len(val_df)}, Test Lockbox={len(test_df)} ({t_test_min} to {test_df[timestamp_col].max()})"
        )
        return train_df, val_df, test_df

    def build_sklearn_pipeline(self, feature_names: list[str]) -> Pipeline:
        """Constructs an end-to-end scikit-learn Pipeline with train-only fitted imputation and scaling."""
        if self.imputation_strategy == "median":
            imputer = SimpleImputer(strategy="median")
        elif self.imputation_strategy == "knn":
            imputer = KNNImputer(n_neighbors=self.knn_neighbors)
        else:
            imputer = SimpleImputer(strategy="mean")

        if self.scaling_strategy == "robust":
            scaler = RobustScaler()
        elif self.scaling_strategy == "standard":
            scaler = StandardScaler()
        else:
            scaler = RobustScaler()

        numeric_pipeline = Pipeline(
            [
                ("imputer", imputer),
                ("scaler", scaler),
            ]
        )

        full_pipeline = Pipeline(
            [
                ("clipper", DomainBoundsClipper()),
                (
                    "column_transform",
                    ColumnTransformer(
                        [("numeric", numeric_pipeline, feature_names)], remainder="passthrough"
                    ),
                ),
            ]
        )

        self.pipeline = full_pipeline
        return full_pipeline

    def fit_transform_train(self, X_train: pd.DataFrame) -> tuple[np.ndarray, Pipeline]:
        """Fits preprocessing pipeline strictly on training data."""
        feature_names = list(X_train.columns)
        pipeline = self.build_sklearn_pipeline(feature_names)
        X_train_trans = pipeline.fit_transform(X_train)
        return X_train_trans, pipeline

    def transform_eval(self, X_eval: pd.DataFrame, pipeline: Pipeline) -> np.ndarray:
        """Transforms validation or test set using frozen train statistics only."""
        return pipeline.transform(X_eval)

    @staticmethod
    def save_processed(
        df_train: pd.DataFrame,
        df_test: pd.DataFrame,
        output_dir: str | Path,
        version: str = "v1",
    ) -> tuple[Path, Path]:
        """Saves clean processed datasets alongside raw data."""
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        train_path = out_path / f"processed_{version}_train.parquet"
        test_path = out_path / f"processed_{version}_test.parquet"

        df_train.to_parquet(train_path, index=False)
        df_test.to_parquet(test_path, index=False)
        logger.info(f"Saved processed datasets to {train_path} and {test_path}")
        return train_path, test_path
