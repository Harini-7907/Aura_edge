import pandas as pd
import numpy as np
from pathlib import Path

DATA_FILE = Path(
    "data/processed/workload_prediction_dataset.csv"
)

MODEL_FILE = Path(
    "models/workload_prediction_model.npz"
)

print("Loading workload prediction model...")

model = np.load(
    MODEL_FILE,
    allow_pickle=True
)

weights = model["weights"]

features = model["features"].tolist()

targets = model["targets"].tolist()

print("Model loaded successfully.")

print("\nLoading workload dataset...")

df = pd.read_csv(DATA_FILE)

# Select one real container observation
sample = df.iloc[-1]

instance_id = sample["instance_id"]

print("\nTesting instance:", instance_id)

print(
    "Starting timestamp:",
    int(sample["timestamp"])
)


# Create initial history
history = {}

for column in [
    "cpu_util",
    "mem_util",
    "disk_util",
    "load1",
    "load5",
    "load15"
]:

    history[column] = []

    for i in range(5, 0, -1):

        history[column].append(
            float(
                sample[
                    f"{column}_lag_{i}"
                ]
            )
        )


def classify(value):

    if value >= 85:
        return "CRITICAL"

    elif value >= 70:
        return "WARNING"

    else:
        return "SAFE"


print("\n==========================================")
print("5-STEP FUTURE WORKLOAD RISK")
print("==========================================")


for step in range(1, 6):

    feature_values = []

    for column in [
        "cpu_util",
        "mem_util",
        "disk_util",
        "load1",
        "load5",
        "load15"
    ]:

        feature_values.extend(
            history[column]
        )


    X = np.array(
        feature_values,
        dtype=float
    )


    X_with_bias = np.concatenate(
        [
            [1.0],
            X
        ]
    )


    prediction = (
        X_with_bias @ weights
    )


    cpu = prediction[0]

    memory = prediction[1]

    disk = prediction[2]


    print(
        f"\nStep {step}"
    )

    print(
        f"CPU:    {cpu:.2f}% -> {classify(cpu)}"
    )

    print(
        f"Memory: {memory:.2f}% -> {classify(memory)}"
    )

    print(
        f"Disk:   {disk:.2f}% -> {classify(disk)}"
    )


    statuses = [
        classify(cpu),
        classify(memory),
        classify(disk)
    ]


    if "CRITICAL" in statuses:

        overall = "CRITICAL"

    elif "WARNING" in statuses:

        overall = "WARNING"

    else:

        overall = "SAFE"


    print(
        f"Overall: {overall}"
    )


    # Update history with predictions
    predicted_values = {
        "cpu_util": cpu,
        "mem_util": memory,
        "disk_util": disk,
        "load1": prediction[3],
        "load5": prediction[4],
        "load15": prediction[5]
    }


    for column in predicted_values:

        history[column].append(
            predicted_values[column]
        )

        history[column] = (
            history[column][-5:]
        )


print("\n==========================================")
print("MULTI-STEP ANALYSIS COMPLETED")
print("==========================================")