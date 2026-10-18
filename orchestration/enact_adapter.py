from pathlib import Path
import sys
import numpy as np
import pandas as pd


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
ENACT_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "node_telemetry_pods_on_clean.csv"
)

ENACT_PREDICTION_DATA = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "enact_prediction_dataset.csv"
)

ENACT_MODEL = (
    PROJECT_ROOT
    / "models"
    / "enact_prediction_model.npz"
)


# ---------------------------------------------------------
# Load latest ENACT telemetry
# ---------------------------------------------------------
def load_enact_resources(
    filename="node_telemetry_pods_on_clean.csv"
):
    """
    Load the latest telemetry observation for every ENACT node.
    """

    data_path = PROJECT_ROOT / "data" / "processed" / filename

    df = pd.read_csv(data_path)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Latest observation for every node
    latest = (
        df.sort_values("timestamp")
        .groupby("node_name")
        .tail(1)
        .reset_index(drop=True)
    )

    resources = []

    for _, row in latest.iterrows():

        resources.append(
            {
                "node_name": row["node_name"],
                "timestamp": row["timestamp"],

                # ENACT stores CPU/MEM as fractions
                "cpu_utilization": float(row["CPU (%)"]) * 100.0,
                "memory_utilization": float(row["MEM (%)"]) * 100.0,
                "filesystem_utilization": float(row["fs (%)"]) * 100.0,

                "energy_watts": float(row["Energy (watts)"]),

                "network_rx_bps": float(row["rx (B/sec)"]),
                "network_tx_bps": float(row["tx (B/sec)"]),
            }
        )

    return resources


# ---------------------------------------------------------
# Load ENACT prediction model
# ---------------------------------------------------------
def load_enact_prediction_model():
    """
    Load the NumPy-based ENACT prediction model.
    """

    if not ENACT_MODEL.exists():
        raise FileNotFoundError(
            f"ENACT prediction model not found:\n{ENACT_MODEL}"
        )

    model = np.load(ENACT_MODEL, allow_pickle=True)

    weights = model["weights"]

    feature_names = [
        str(x)
        for x in model["features"]
    ]

    target_names = [
        str(x)
        for x in model["targets"]
    ]

    return weights, feature_names, target_names


# ---------------------------------------------------------
# Get latest ENACT prediction
# ---------------------------------------------------------
def get_enact_prediction(node_name="rpi4"):
    """
    Predict the next ENACT CPU and memory utilization.

    Uses the most recent 5 CPU and memory observations
    from the ENACT prediction dataset.
    """

    df = pd.read_csv(ENACT_PREDICTION_DATA)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # The prediction dataset currently contains rpi4 data.
    node_df = df.sort_values("timestamp")

    if len(node_df) < 1:
        raise ValueError("No ENACT prediction data available.")

    latest = node_df.iloc[-1]

    weights, feature_names, target_names = (
        load_enact_prediction_model()
    )

    features = np.array(
        [
            float(latest[name])
            for name in feature_names
        ],
        dtype=float
    )

    # Add intercept
    x = np.concatenate(
        [
            [1.0],
            features
        ]
    )

    prediction = x @ weights

    # Model stores residual-based uncertainty
    model = np.load(
        ENACT_MODEL,
        allow_pickle=True
    )

    cpu_uncertainty = float(
        model["cpu_uncertainty"]
    )

    memory_uncertainty = float(
        model["memory_uncertainty"]
    )

    result = {
        "node_name": node_name,
        "timestamp": latest["timestamp"],

        "predicted_cpu": float(prediction[0]),
        "predicted_memory": float(prediction[1]),

        "cpu_uncertainty": cpu_uncertainty,
        "memory_uncertainty": memory_uncertainty,
    }

    return result


# ---------------------------------------------------------
# Combined current + predicted ENACT profile
# ---------------------------------------------------------
def get_enact_resource_profile(node_name="rpi4"):
    """
    Return current ENACT telemetry together with
    next-step CPU/memory prediction and uncertainty.
    """

    resources = load_enact_resources()

    resource = None

    for item in resources:
        if item["node_name"] == node_name:
            resource = item
            break

    if resource is None:
        raise ValueError(
            f"ENACT node '{node_name}' not found."
        )

    prediction = get_enact_prediction(node_name)

    resource["predicted_cpu"] = prediction[
        "predicted_cpu"
    ]

    resource["predicted_memory"] = prediction[
        "predicted_memory"
    ]

    # Use CPU uncertainty as the primary orchestration
    # uncertainty, while retaining both values.
    resource["prediction_uncertainty"] = (
        prediction["cpu_uncertainty"]
    )

    resource["cpu_prediction_uncertainty"] = (
        prediction["cpu_uncertainty"]
    )

    resource["memory_prediction_uncertainty"] = (
        prediction["memory_uncertainty"]
    )

    return resource


# ---------------------------------------------------------
# Simple test
# ---------------------------------------------------------
if __name__ == "__main__":

    print("\nENACT RESOURCE + PREDICTION TEST")
    print("=" * 45)

    profile = get_enact_resource_profile("rpi4")

    print(f"Node: {profile['node_name']}")
    print(f"Timestamp: {profile['timestamp']}")

    print("\nCURRENT TELEMETRY")
    print(
        f"CPU utilization: "
        f"{profile['cpu_utilization']:.2f}%"
    )

    print(
        f"Memory utilization: "
        f"{profile['memory_utilization']:.2f}%"
    )

    print(
        f"Energy: "
        f"{profile['energy_watts']:.2f} W"
    )

    print(
        f"Network RX: "
        f"{profile['network_rx_bps']:.2f} B/s"
    )

    print(
        f"Network TX: "
        f"{profile['network_tx_bps']:.2f} B/s"
    )

    print("\nNEXT-STEP PREDICTION")

    print(
        f"Predicted CPU: "
        f"{profile['predicted_cpu']:.2f}%"
    )

    print(
        f"Predicted memory: "
        f"{profile['predicted_memory']:.2f}%"
    )

    print(
        f"CPU uncertainty: "
        f"{profile['cpu_prediction_uncertainty']:.4f}%"
    )

    print(
        f"Memory uncertainty: "
        f"{profile['memory_prediction_uncertainty']:.4f}%"
    )