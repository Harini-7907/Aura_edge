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

print("\nFeatures:", len(features))

print("Targets:", targets)


print("\nLoading workload dataset...")

df = pd.read_csv(
    DATA_FILE
)

# Select one real observation
sample = df.iloc[100].copy()


X = sample[
    features
].values.astype(float)


# Add bias
X_with_bias = np.concatenate(
    [
        [1.0],
        X
    ]
)


# Predict
prediction = (
    X_with_bias @ weights
)


actual = sample[
    targets
].values.astype(float
)


print("\n==========================================")
print("WORKLOAD PREDICTION TEST")
print("==========================================")


for i, target in enumerate(targets):

    print(
        f"\n{target}"
    )

    print(
        f"Predicted: {prediction[i]:.4f}"
    )

    print(
        f"Actual:    {actual[i]:.4f}"
    )

    print(
        f"Error:     {abs(prediction[i] - actual[i]):.4f}"
    )


print("\n==========================================")
print("TEST COMPLETED")
print("==========================================")