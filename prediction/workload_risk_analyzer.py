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

print("\nLoading workload data...")

df = pd.read_csv(
    DATA_FILE
)

# Use one real observation
sample = df.iloc[-1]

X = sample[
    features
].values.astype(float)

X_with_bias = np.concatenate(
    [
        [1.0],
        X
    ]
)

prediction = (
    X_with_bias @ weights
)


def classify(value):

    if value >= 85:
        return "CRITICAL"

    elif value >= 70:
        return "WARNING"

    else:
        return "SAFE"


print("\n==========================================")
print("PREDICTED WORKLOAD RISK")
print("==========================================")


resources = {
    "CPU": prediction[0],
    "Memory": prediction[1],
    "Disk": prediction[2]
}


for resource, value in resources.items():

    status = classify(value)

    print(
        f"{resource}: "
        f"{value:.2f}% -> {status}"
    )


# Overall workload status
statuses = [
    classify(value)
    for value in resources.values()
]


if "CRITICAL" in statuses:

    overall = "CRITICAL"

elif "WARNING" in statuses:

    overall = "WARNING"

else:

    overall = "SAFE"


print("\n------------------------------------------")

print(
    "Overall predicted workload:",
    overall
)

print("------------------------------------------")

print("\nObservation timestamp:")

print(
    int(sample["timestamp"])
)

print("\nInstance:")

print(
    sample["instance_id"]
)

print("\n==========================================")
print("RISK ANALYSIS COMPLETED")
print("==========================================")