import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------
# AURA-Edge: CPU Prediction Baseline
# NumPy-based Auto-Regressive Model
# ---------------------------------------

INPUT_FILE = Path(
    "data/processed/prediction_dataset.csv"
)

MODEL_FILE = Path(
    "models/cpu_prediction_model.npz"
)

print("Loading prediction dataset...")

df = pd.read_csv(INPUT_FILE)

print("Rows:", len(df))

FEATURES = [
    "cpu_lag_1",
    "cpu_lag_2",
    "cpu_lag_3",
    "cpu_lag_4",
    "cpu_lag_5"
]

TARGET = "target_cpu"

X = df[FEATURES].values.astype(float)
y = df[TARGET].values.astype(float)

# ---------------------------------------
# Time-based train/test split
# ---------------------------------------

split_index = int(len(df) * 0.8)

X_train = X[:split_index]
X_test = X[split_index:]

y_train = y[:split_index]
y_test = y[split_index:]

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

# ---------------------------------------
# Add intercept column
# ---------------------------------------

X_train_with_bias = np.column_stack(
    [np.ones(len(X_train)), X_train]
)

X_test_with_bias = np.column_stack(
    [np.ones(len(X_test)), X_test]
)

# ---------------------------------------
# Train Linear Regression using NumPy
# ---------------------------------------

print("\nTraining prediction model...")

weights = np.linalg.lstsq(
    X_train_with_bias,
    y_train,
    rcond=None
)[0]

print("Training completed!")

# ---------------------------------------
# Predict
# ---------------------------------------

predictions = X_test_with_bias @ weights

# ---------------------------------------
# Evaluation
# ---------------------------------------

errors = y_test - predictions

mae = np.mean(np.abs(errors))

rmse = np.sqrt(
    np.mean(errors ** 2)
)

print("\n--- MODEL PERFORMANCE ---")
print(f"MAE:  {mae:.4f}")
print(f"RMSE: {rmse:.4f}")

# ---------------------------------------
# Prediction uncertainty baseline
# ---------------------------------------

uncertainty = np.std(errors)

print(f"Prediction uncertainty (std): {uncertainty:.4f}")

# ---------------------------------------
# Save model
# ---------------------------------------

MODEL_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

np.savez(
    MODEL_FILE,
    weights=weights,
    uncertainty=uncertainty
)

print("\nModel saved to:")
print(MODEL_FILE)