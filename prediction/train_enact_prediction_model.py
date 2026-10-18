import numpy as np
import pandas as pd
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "enact_prediction_dataset.csv"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "enact_prediction_model.npz"
)


# ==========================================
# LOAD DATA
# ==========================================

print("Loading ENACT prediction dataset...")

df = pd.read_csv(INPUT_FILE)


# ==========================================
# INPUT FEATURES
# ==========================================

feature_columns = []

for lag in range(1, 6):

    feature_columns.append(
        f"cpu_lag_{lag}"
    )

    feature_columns.append(
        f"memory_lag_{lag}"
    )


target_columns = [
    "target_cpu",
    "target_memory"
]


X = df[
    feature_columns
].to_numpy(
    dtype=float
)

y = df[
    target_columns
].to_numpy(
    dtype=float
)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

split_index = int(
    len(X) * 0.8
)

X_train = X[
    :split_index
]

X_test = X[
    split_index:
]

y_train = y[
    :split_index
]

y_test = y[
    split_index:
]


# ==========================================
# ADD INTERCEPT
# ==========================================

X_train_bias = np.column_stack(
    [
        np.ones(
            len(X_train)
        ),
        X_train
    ]
)

X_test_bias = np.column_stack(
    [
        np.ones(
            len(X_test)
        ),
        X_test
    ]
)


# ==========================================
# LINEAR AUTOREGRESSIVE MODEL
# ==========================================

weights = np.linalg.lstsq(
    X_train_bias,
    y_train,
    rcond=None
)[0]


# ==========================================
# PREDICTIONS
# ==========================================

predictions = (
    X_test_bias @ weights
)


# ==========================================
# CALCULATE METRICS
# ==========================================

errors = (
    predictions
    - y_test
)

absolute_errors = np.abs(
    errors
)

squared_errors = (
    errors ** 2
)


cpu_mae = (
    absolute_errors[:, 0]
    .mean()
)

cpu_rmse = np.sqrt(
    squared_errors[:, 0]
    .mean()
)

memory_mae = (
    absolute_errors[:, 1]
    .mean()
)

memory_rmse = np.sqrt(
    squared_errors[:, 1]
    .mean()
)


# ==========================================
# UNCERTAINTY ESTIMATE
# ==========================================

cpu_uncertainty = (
    errors[:, 0]
    .std()
)

memory_uncertainty = (
    errors[:, 1]
    .std()
)


# ==========================================
# SAVE MODEL
# ==========================================

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

np.savez(

    MODEL_FILE,

    weights=weights,

    features=np.array(
        feature_columns
    ),

    targets=np.array(
        target_columns
    ),

    cpu_mae=cpu_mae,

    cpu_rmse=cpu_rmse,

    memory_mae=memory_mae,

    memory_rmse=memory_rmse,

    cpu_uncertainty=cpu_uncertainty,

    memory_uncertainty=memory_uncertainty
)


# ==========================================
# RESULTS
# ==========================================

print()

print(
    "ENACT PREDICTION MODEL TRAINED"
)

print()

print(
    f"Training rows: "
    f"{len(X_train)}"
)

print(
    f"Testing rows: "
    f"{len(X_test)}"
)

print()

print(
    "CPU prediction:"
)

print(
    f"  MAE: "
    f"{cpu_mae:.4f}%"
)

print(
    f"  RMSE: "
    f"{cpu_rmse:.4f}%"
)

print(
    f"  Uncertainty: "
    f"{cpu_uncertainty:.4f}%"
)

print()

print(
    "Memory prediction:"
)

print(
    f"  MAE: "
    f"{memory_mae:.4f}%"
)

print(
    f"  RMSE: "
    f"{memory_rmse:.4f}%"
)

print(
    f"  Uncertainty: "
    f"{memory_uncertainty:.4f}%"
)

print()

print(
    f"Model saved to:"
)

print(
    MODEL_FILE
)