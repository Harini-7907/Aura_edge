import pandas as pd
import numpy as np
from pathlib import Path

INPUT_FILE = Path(
    "data/processed/workload_prediction_dataset.csv"
)

MODEL_FILE = Path(
    "models/workload_prediction_model.npz"
)

print("Loading workload prediction dataset...")

df = pd.read_csv(INPUT_FILE)

print("Rows:", len(df))

FEATURES = []

# Historical workload features
for column in [
    "cpu_util",
    "mem_util",
    "disk_util",
    "load1",
    "load5",
    "load15"
]:

    for i in range(1, 6):

        FEATURES.append(
            f"{column}_lag_{i}"
        )


TARGETS = [
    "target_cpu_util",
    "target_mem_util",
    "target_disk_util",
    "target_load1",
    "target_load5",
    "target_load15"
]


X = df[FEATURES].values.astype(float)

y = df[TARGETS].values.astype(float)

print("Input features:", X.shape)

print("Prediction targets:", y.shape)


# Time-based split
split_index = int(
    len(df) * 0.8
)

X_train = X[:split_index]

X_test = X[split_index:]

y_train = y[:split_index]

y_test = y[split_index:]


print("\nTraining rows:", len(X_train))

print("Testing rows:", len(X_test))


# Add bias/intercept
X_train_with_bias = np.column_stack(
    [
        np.ones(len(X_train)),
        X_train
    ]
)

X_test_with_bias = np.column_stack(
    [
        np.ones(len(X_test)),
        X_test
    ]
)


print("\nTraining workload prediction model...")

weights = np.linalg.lstsq(
    X_train_with_bias,
    y_train,
    rcond=None
)[0]


print("Training completed!")


# Predictions
predictions = (
    X_test_with_bias @ weights
)


# Errors
errors = (
    y_test - predictions
)


print("\n==========================================")
print("WORKLOAD PREDICTION PERFORMANCE")
print("==========================================")


for i, target in enumerate(TARGETS):

    mae = np.mean(
        np.abs(
            errors[:, i]
        )
    )

    rmse = np.sqrt(
        np.mean(
            errors[:, i] ** 2
        )
    )

    uncertainty = np.std(
        errors[:, i]
    )

    print(f"\n{target}")

    print(
        f"MAE: {mae:.4f}"
    )

    print(
        f"RMSE: {rmse:.4f}"
    )

    print(
        f"Uncertainty: {uncertainty:.4f}"
    )


# Save model
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