
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = PROJECT_ROOT / "models" / "resource_prediction_model.npz"
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "resource_prediction_dataset.csv"


def load_prediction_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Prediction model not found: {MODEL_PATH}")

    model = np.load(MODEL_PATH, allow_pickle=True)
    weights = model["weights"]
    features = [str(x) for x in model["features"]]
    targets = [str(x) for x in model["targets"]]
    return weights, features, targets


def get_real_prediction():
    weights, features, targets = load_prediction_model()

    # Use historical data when available. The large dataset is
    # intentionally excluded from the public deployment.
    if DATA_PATH.exists():
        data = np.genfromtxt(DATA_PATH, delimiter=",", names=True)

        if len(data) == 0:
            raise ValueError("Alibaba prediction dataset is empty.")

        row = data[-1]
        x = np.array([row[name] for name in features], dtype=float)
        x = np.concatenate(([1.0], x))
        prediction = x @ weights

        return {
            target: float(value)
            for target, value in zip(targets, prediction)
        }

    # Deployment fallback: the dashboard's resource profiles
    # provide the simulated future utilization levels.
    # These are demonstration values, NOT model predictions.
    return {
        "target_cpu": 55.0,
        "target_memory": 60.0,
        "target_net_in": 0.0,
        "target_net_out": 0.0,
        "target_disk": 0.0,
    }


def get_simulated_resource_prediction(resource_name):
    alibaba_prediction = get_real_prediction()

    profiles = {
        "Local": (65.0, 65.0),
        "Edge": (55.0, 60.0),
        "Cloud": (45.0, 50.0),
    }

    predicted_cpu, predicted_memory = profiles.get(
        resource_name,
        (
            alibaba_prediction["target_cpu"],
            alibaba_prediction["target_memory"],
        ),
    )

    return {
        "target_cpu": float(predicted_cpu),
        "target_memory": float(predicted_memory),
        "alibaba_target_cpu": float(alibaba_prediction["target_cpu"]),
        "alibaba_target_memory": float(alibaba_prediction["target_memory"]),
        "target_net_in": float(alibaba_prediction.get("target_net_in", 0.0)),
        "target_net_out": float(alibaba_prediction.get("target_net_out", 0.0)),
        "target_disk": float(alibaba_prediction.get("target_disk", 0.0)),
    }


if __name__ == "__main__":
    print("Prediction:", get_real_prediction())
    for name in ["Local", "Edge", "Cloud"]:
        print(name, get_simulated_resource_prediction(name))
