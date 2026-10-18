import pandas as pd
import numpy as np
from pathlib import Path


# ==========================================
# FILE LOCATIONS
# ==========================================

DATA_FILE = Path(
    "data/processed/resource_prediction_dataset.csv"
)

MODEL_FILE = Path(
    "models/resource_prediction_model.npz"
)


# ==========================================
# LOAD MODEL
# ==========================================

print("Loading resource prediction model...")

model = np.load(MODEL_FILE)

weights = model["weights"]

features = model["features"]

targets = model["targets"]

print("Model loaded successfully!")


# ==========================================
# LOAD DATA
# ==========================================

print("\nLoading resource prediction dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset rows:", len(df))


# ==========================================
# SELECT ONE REAL OBSERVATION
# ==========================================

sample = df.iloc[0]

X = sample[features].astype(float).values

X = np.insert(
    X,
    0,
    1.0
)


# ==========================================
# MAKE PREDICTION
# ==========================================

prediction = X @ weights


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("\n==========================================")
print("RESOURCE PREDICTION TEST")
print("==========================================")

print("\nMachine:", sample["machine_id"])

print("Timestamp:", sample["timestamp"])

print("\nPredicted next resource state:")

for target, value in zip(targets, prediction):

    print(
        f"{target}: {value:.4f}"
    )


# ==========================================
# ACTUAL VALUES
# ==========================================

print("\nActual next resource state:")

for target in targets:

    print(
        f"{target}: {sample[target]:.4f}"
    )


# ==========================================
# ERROR
# ==========================================

print("\nPrediction error:")

for target, value in zip(targets, prediction):

    actual = sample[target]

    error = abs(actual - value)

    print(
        f"{target}: {error:.4f}"
    )