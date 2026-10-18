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

sample = machine_data.iloc[-1]


# ==========================================
# PREPARE INPUT
# ==========================================

X = sample[features].astype(float).values

X = np.insert(
    X,
    0,
    1.0
)


# ==========================================
# PREDICT FUTURE RESOURCE STATE
# ==========================================

prediction = X @ weights


# ==========================================
# RESOURCE VALUES
# ==========================================

cpu = np.clip(prediction[0], 0, 100)
memory = np.clip(prediction[1], 0, 100)
network_in = max(prediction[2], 0)
network_out = max(prediction[3], 0)
disk = np.clip(prediction[4], 0, 100)


# ==========================================
# RISK CLASSIFICATION
# ==========================================

def classify_utilization(value):

    if value < 70:
        return "SAFE"

    elif value < 85:
        return "WARNING"

    else:
        return "CRITICAL"


cpu_status = classify_utilization(cpu)

memory_status = classify_utilization(memory)

disk_status = classify_utilization(disk)


# ==========================================
# DISPLAY RESOURCE FORECAST
# ==========================================

print("\n==========================================")
print("AURA-EDGE RESOURCE RISK ANALYSIS")
print("==========================================")

print("\nMachine:", machine_id)

print("Timestamp:", sample["timestamp"])


print("\nPredicted Future Resource State:")

print(
    f"CPU:         {cpu:.2f}%"
)

print(
    f"Memory:      {memory:.2f}%"
)

print(
    f"Network In:  {network_in:.4f}"
)

print(
    f"Network Out: {network_out:.4f}"
)

print(
    f"Disk I/O:    {disk:.2f}%"
)


# ==========================================
# RESOURCE STATUS
# ==========================================

print("\nResource Status:")

print(
    f"CPU:         {cpu_status}"
)

print(
    f"Memory:      {memory_status}"
)

print(
    f"Disk I/O:    {disk_status}"
)


# ==========================================
# OVERALL MACHINE RISK
# ==========================================

statuses = [
    cpu_status,
    memory_status,
    disk_status
]


if "CRITICAL" in statuses:

    overall_status = "CRITICAL"

elif "WARNING" in statuses:

    overall_status = "WARNING"

else:

    overall_status = "SAFE"


print("\n==========================================")

print(
    "OVERALL MACHINE STATUS:",
    overall_status
)

print("==========================================")