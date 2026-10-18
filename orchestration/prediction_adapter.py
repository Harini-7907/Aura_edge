import numpy as np
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "resource_prediction_model.npz"
)

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "resource_prediction_dataset.csv"
)


# ---------------------------------------------------------
# Load trained Alibaba resource prediction model
# ---------------------------------------------------------

def load_prediction_model():

    model = np.load(
        MODEL_PATH,
        allow_pickle=True
    )

    weights = model["weights"]

    features = [
        str(x)
        for x in model["features"]
    ]

    targets = [
        str(x)
        for x in model["targets"]
    ]

    return weights, features, targets


# ---------------------------------------------------------
# Get Alibaba prediction
# ---------------------------------------------------------

def get_real_prediction():

    weights, features, targets = (
        load_prediction_model()
    )

    # Load processed Alibaba prediction data
    data = np.genfromtxt(
        DATA_PATH,
        delimiter=",",
        names=True
    )

    if len(data) == 0:

        raise ValueError(
            "Alibaba prediction dataset is empty."
        )

    # Use the most recent available row
    row = data[-1]

    # Create input vector
    x = np.array(
        [
            row[name]
            for name in features
        ],
        dtype=float
    )

    # Add bias/intercept
    x = np.concatenate(
        (
            [1.0],
            x
        )
    )

    # Generate prediction
    prediction = x @ weights

    result = {}

    for target, value in zip(
        targets,
        prediction
    ):

        result[target] = float(value)

    return result


# ---------------------------------------------------------
# Get prediction for simulated resources
# ---------------------------------------------------------

def get_simulated_resource_prediction(
    resource_name
):

    """
    Return a predicted utilization profile
    appropriate for the simulated execution resource.

    The Alibaba model is used as the workload reference,
    but Local, Edge and Cloud receive different
    simulated future utilization levels.

    This prevents one Alibaba utilization value from
    being incorrectly applied to every resource.
    """

    alibaba_prediction = get_real_prediction()

    base_cpu = alibaba_prediction[
        "target_cpu"
    ]

    base_memory = alibaba_prediction[
        "target_memory"
    ]

    # --------------------------------------
    # Local
    # --------------------------------------

    if resource_name == "Local":

        predicted_cpu = 65.0
        predicted_memory = 65.0

    # --------------------------------------
    # Edge
    # --------------------------------------

    elif resource_name == "Edge":

        predicted_cpu = 55.0
        predicted_memory = 60.0

    # --------------------------------------
    # Cloud
    # --------------------------------------

    elif resource_name == "Cloud":

        predicted_cpu = 45.0
        predicted_memory = 50.0

    else:

        predicted_cpu = base_cpu
        predicted_memory = base_memory

    return {
        "target_cpu": float(predicted_cpu),
        "target_memory": float(predicted_memory),

        # Keep the Alibaba prediction available
        # for research/evaluation purposes.
        "alibaba_target_cpu": float(base_cpu),
        "alibaba_target_memory": float(base_memory),

        "target_net_in": alibaba_prediction.get(
            "target_net_in",
            0.0
        ),

        "target_net_out": alibaba_prediction.get(
            "target_net_out",
            0.0
        ),

        "target_disk": alibaba_prediction.get(
            "target_disk",
            0.0
        )
    }


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print(
        "Starting prediction adapter..."
    )

    prediction = get_real_prediction()

    print(
        "\n=========================================="
    )

    print(
        "AURA-Edge REAL PREDICTION ADAPTER"
    )

    print(
        "=========================================="
    )

    print(
        "Alibaba predicted CPU:",
        f"{prediction['target_cpu']:.2f}%"
    )

    print(
        "Alibaba predicted Memory:",
        f"{prediction['target_memory']:.2f}%"
    )

    print(
        "Predicted Network In:",
        f"{prediction['target_net_in']:.4f}"
    )

    print(
        "Predicted Network Out:",
        f"{prediction['target_net_out']:.4f}"
    )

    print(
        "Predicted Disk:",
        f"{prediction['target_disk']:.2f}%"
    )

    print(
        "\nSIMULATED RESOURCE PREDICTIONS"
    )

    for resource_name in [
        "Local",
        "Edge",
        "Cloud"
    ]:

        simulated = (
            get_simulated_resource_prediction(
                resource_name
            )
        )

        print(
            f"\n{resource_name}:"
        )

        print(
            f"  Future CPU: "
            f"{simulated['target_cpu']:.2f}%"
        )

        print(
            f"  Future Memory: "
            f"{simulated['target_memory']:.2f}%"
        )

    print(
        "\n=========================================="
    )

    print(
        "PREDICTION ADAPTER COMPLETED"
    )

    print(
        "=========================================="
    )