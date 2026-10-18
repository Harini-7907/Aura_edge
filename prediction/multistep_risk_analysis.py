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

print("Model loaded successfully!")


# ==========================================
# LOAD DATA
# ==========================================

print("\nLoading resource prediction dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset rows:", len(df))


# ==========================================
# SELECT MACHINES
# ==========================================

machines = [
    "m_1973"
]


# ==========================================
# RISK FUNCTION
# ==========================================

def classify_utilization(value):

    if value < 70:
        return "SAFE"

    elif value < 85:
        return "WARNING"

    else:
        return "CRITICAL"


# ==========================================
# ANALYZE EACH MACHINE
# ==========================================

for machine_id in machines:

    machine_data = df[
        df["machine_id"] == machine_id
    ].copy()

    machine_data = machine_data.sort_values(
        "timestamp"
    ).reset_index(drop=True)

    if len(machine_data) == 0:

        print(
            f"\nMachine {machine_id} not found."
        )

        continue

    # Use the latest available observation
    sample = machine_data.iloc[-1]

    current_features = (
        sample[features]
        .astype(float)
        .values
    )

    print("\n==========================================")
    print("MACHINE:", machine_id)
    print("==========================================")

    for step in range(1, 6):

        X = np.insert(
            current_features,
            0,
            1.0
        )

        prediction = X @ weights

        # Keep percentage resources realistic
        cpu = np.clip(
            prediction[0],
            0,
            100
        )

        memory = np.clip(
            prediction[1],
            0,
            100
        )

        network_in = max(
            prediction[2],
            0
        )

        network_out = max(
            prediction[3],
            0
        )

        disk = np.clip(
            prediction[4],
            0,
            100
        )

        cpu_status = classify_utilization(
            cpu
        )

        memory_status = classify_utilization(
            memory
        )

        disk_status = classify_utilization(
            disk
        )

        print(
            f"\nFuture Step {step}"
        )

        print(
            f"CPU: {cpu:.2f}% [{cpu_status}]"
        )

        print(
            f"Memory: {memory:.2f}% [{memory_status}]"
        )

        print(
            f"Network In: {network_in:.4f}"
        )

        print(
            f"Network Out: {network_out:.4f}"
        )

        print(
            f"Disk I/O: {disk:.2f}% [{disk_status}]"
        )

        # --------------------------------------
        # UPDATE RESOURCE HISTORY
        # --------------------------------------

        new_features = current_features.copy()

        # CPU
        new_features[0:5] = np.roll(
            new_features[0:5],
            1
        )

        new_features[0] = cpu

        # Memory
        new_features[5:10] = np.roll(
            new_features[5:10],
            1
        )

        new_features[5] = memory

        # Network In
        new_features[10:15] = np.roll(
            new_features[10:15],
            1
        )

        new_features[10] = network_in

        # Network Out
        new_features[15:20] = np.roll(
            new_features[15:20],
            1
        )

        new_features[15] = network_out

        # Disk
        new_features[20:25] = np.roll(
            new_features[20:25],
            1
        )

        new_features[20] = disk

        current_features = new_features


print("\n==========================================")
print("MULTI-STEP RISK ANALYSIS COMPLETED")
print("==========================================")