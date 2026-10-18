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
# SELECT ONE MACHINE
# ==========================================

machine_id = df["machine_id"].iloc[0]

machine_data = df[
    df["machine_id"] == machine_id
].copy()

machine_data = machine_data.sort_values(
    "timestamp"
).reset_index(drop=True)

print("Testing machine:", machine_id)


# ==========================================
# SELECT A STARTING POINT
# ==========================================

start_index = 100

sample = machine_data.iloc[start_index].copy()


# ==========================================
# INITIAL HISTORY
# ==========================================

history = []

for feature in features:

    history.append(
        float(sample[feature])
    )

history = np.array(history)


# ==========================================
# RESOURCE INDEXES
# ==========================================

resource_names = [
    "CPU",
    "Memory",
    "Network In",
    "Network Out",
    "Disk"
]


# ==========================================
# MULTI-STEP PREDICTION
# ==========================================

print("\n==========================================")
print("MULTI-STEP RESOURCE PREDICTION")
print("==========================================")

current_features = history.copy()

for step in range(1, 6):

    X = np.insert(
        current_features,
        0,
        1.0
    )

    prediction = X @ weights

    print(f"\nFuture Step {step}")

    for name, value in zip(
        resource_names,
        prediction
    ):

        print(
            f"{name}: {value:.4f}"
        )

    # Keep predictions within realistic ranges
    prediction[0] = np.clip(
        prediction[0],
        0,
        100
    )

    prediction[1] = np.clip(
        prediction[1],
        0,
        100
    )

    prediction[4] = np.clip(
        prediction[4],
        0,
        100
    )

    # --------------------------------------
    # Update history for next prediction
    # --------------------------------------

    new_features = current_features.copy()

    # CPU lags
    new_features[0:5] = np.roll(
        new_features[0:5],
        1
    )

    new_features[0] = prediction[0]

    # Memory lags
    new_features[5:10] = np.roll(
        new_features[5:10],
        1
    )

    new_features[5] = prediction[1]

    # Network In lags
    new_features[10:15] = np.roll(
        new_features[10:15],
        1
    )

    new_features[10] = prediction[2]

    # Network Out lags
    new_features[15:20] = np.roll(
        new_features[15:20],
        1
    )

    new_features[15] = prediction[3]

    # Disk lags
    new_features[20:25] = np.roll(
        new_features[20:25],
        1
    )

    new_features[20] = prediction[4]

    current_features = new_features


print("\n==========================================")
print("MULTI-STEP TEST COMPLETED")
print("==========================================")