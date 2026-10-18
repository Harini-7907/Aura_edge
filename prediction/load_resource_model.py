import numpy as np
from pathlib import Path


MODEL_PATH = Path("models/resource_prediction_model.npz")


def load_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found: {MODEL_PATH}"
        )

    model = np.load(
        MODEL_PATH,
        allow_pickle=True
    )

    print("==========================================")
    print("RESOURCE PREDICTION MODEL")
    print("==========================================")

    print(
        "Model loaded successfully"
    )

    print(
        "Features:",
        len(model["features"])
    )

    print(
        "Targets:",
        list(model["targets"])
    )

    print(
        "Weights shape:",
        model["weights"].shape
    )

    print("==========================================")

    return model


if __name__ == "__main__":

    load_model()