import numpy as np
from pathlib import Path


MODEL_PATH = Path("models/resource_prediction_model.npz")
DATA_PATH = Path("data/processed/resource_prediction_dataset.csv")


def main():

    print("Starting real resource prediction...")

    # Load model
    model = np.load(
        MODEL_PATH,
        allow_pickle=True
    )

    weights = model["weights"]
    features = model["features"]
    targets = model["targets"]

    print("\nModel loaded.")
    print("Number of features:", len(features))
    print("Targets:", list(targets))

    # Load processed prediction dataset
    data = np.genfromtxt(
        DATA_PATH,
        delimiter=",",
        names=True
    )

    # Take one real row
    row = data[0]

    # Build feature vector
    x = np.array(
        [row[name] for name in features],
        dtype=float
    )

    # Add bias term
    x_with_bias = np.concatenate(
        ([1.0], x)
    )

    # Predict
    prediction = (
        x_with_bias @ weights
    )

    print("\n==========================================")
    print("REAL RESOURCE PREDICTION")
    print("==========================================")

    for target, value in zip(
        targets,
        prediction
    ):
        print(
            f"{target}: {value:.2f}"
        )

    print("\n==========================================")
    print("RESOURCE PREDICTION COMPLETED")
    print("==========================================")


if __name__ == "__main__":
    main()