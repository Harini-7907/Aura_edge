import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# FILE LOCATIONS
# ==========================================

INPUT_FILE = Path(
    "data/processed/resource_prediction_dataset.csv"
)

MODEL_FILE = Path(
    "models/resource_prediction_model.npz"
)


# ==========================================
# LOAD DATA
# ==========================================

print("Loading resource prediction dataset...")

df = pd.read_csv(INPUT_FILE)

print("Rows:", len(df))


# ==========================================
# DEFINE FEATURES
# ==========================================

FEATURES = [
    "cpu_lag_1",
    "cpu_lag_2",
    "cpu_lag_3",
    "cpu_lag_4",
    "cpu_lag_5",

    "memory_lag_1",
    "memory_lag_2",
    "memory_lag_3",
    "memory_lag_4",
    "memory_lag_5",

    "net_in_lag_1",
    "net_in_lag_2",
    "net_in_lag_3",
    "net_in_lag_4",
    "net_in_lag_5",

    "net_out_lag_1",
    "net_out_lag_2",
    "net_out_lag_3",
    "net_out_lag_4",
    "net_out_lag_5",

    "disk_lag_1",
    "disk_lag_2",
    "disk_lag_3",
    "disk_lag_4",
    "disk_lag_5"
]


# ==========================================
# DEFINE TARGETS
# ==========================================

TARGETS = [
    "target_cpu",
    "target_memory",
    "target_net_in",
    "target_net_out",
    "target_disk"
]


# ==========================================
# CONVERT TO NUMPY
# ==========================================

X = df[FEATURES].values.astype(float)

y = df[TARGETS].values.astype(float)

print("Input features:", X.shape)
print("Prediction targets:", y.shape)


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==========================================
# ADD BIAS TERM
# ==========================================

X_train_with_bias = np.column_stack(
    [np.ones(len(X_train)), X_train]
)

X_test_with_bias = np.column_stack(
    [np.ones(len(X_test)), X_test]
)


# ==========================================
# TRAIN MULTI-RESOURCE MODEL
# ==========================================

print("\nTraining multi-resource prediction model...")

weights = np.linalg.lstsq(
    X_train_with_bias,
    y_train,
    rcond=None
)[0]

print("Training completed!")


# ==========================================
# MAKE PREDICTIONS
# ==========================================

predictions = (
    X_test_with_bias @ weights
)


# ==========================================
# CALCULATE ERRORS
# ==========================================

errors = y_test - predictions


# ==========================================
# RESOURCE-WISE METRICS
# ==========================================

print("\n==========================================")
print("RESOURCE PREDICTION PERFORMANCE")
print("==========================================")

for i, target in enumerate(TARGETS):

    mae = np.mean(
        np.abs(errors[:, i])
    )

    rmse = np.sqrt(
        np.mean(errors[:, i] ** 2)
    )

    uncertainty = np.std(
        errors[:, i]
    )

    print(f"\n{target}")

    print(f"MAE: {mae:.4f}")

    print(f"RMSE: {rmse:.4f}")

    print(
        f"Uncertainty: {uncertainty:.4f}"
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
    features=np.array(FEATURES),
    targets=np.array(TARGETS)
)


print("\n==========================================")
print("MODEL SAVED")
print("==========================================")

print(MODEL_FILE)