import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from dataclasses import dataclass


@dataclass
class ExecutionResource:

    name: str

    cpu_available: float
    memory_available: float

    latency: float
    bandwidth: float

    energy_cost: float
    reliability: float

    risk: str

    predicted_cpu: float = 0.0
    predicted_memory: float = 0.0

    prediction_uncertainty: float = 0.0

    battery_level: float = 100.0
    temperature: float = 35.0

    # Real ENACT telemetry
    energy_watts: float = 0.0

    network_rx_bps: float = 0.0
    network_tx_bps: float = 0.0


# ---------------------------------------------------------
# Create simulated execution resources
# ---------------------------------------------------------

def create_execution_resources():

    from orchestration.prediction_adapter import (
        get_simulated_resource_prediction
    )

    from prediction.uncertainty import (
        get_resource_uncertainty
    )

    uncertainty = get_resource_uncertainty()

    cpu_uncertainty = uncertainty[
        "target_cpu"
    ]

    # -----------------------------------------------------
    # Get resource-specific future predictions
    # -----------------------------------------------------

    local_prediction = (
        get_simulated_resource_prediction(
            "Local"
        )
    )

    edge_prediction = (
        get_simulated_resource_prediction(
            "Edge"
        )
    )

    cloud_prediction = (
        get_simulated_resource_prediction(
            "Cloud"
        )
    )


    # -----------------------------------------------------
    # Local
    # -----------------------------------------------------

    local = ExecutionResource(

        name="Local",

        cpu_available=60.0,

        memory_available=70.0,

        latency=5.0,

        bandwidth=50.0,

        energy_cost=0.8,

        reliability=0.95,

        risk="WARNING",

        predicted_cpu=local_prediction[
            "target_cpu"
        ],

        predicted_memory=local_prediction[
            "target_memory"
        ],

        prediction_uncertainty=cpu_uncertainty,

        battery_level=100.0,

        temperature=35.0,

        energy_watts=0.0,

        network_rx_bps=0.0,

        network_tx_bps=0.0
    )


    # -----------------------------------------------------
    # Edge
    # -----------------------------------------------------

    edge = ExecutionResource(

        name="Edge",

        cpu_available=80.0,

        memory_available=85.0,

        latency=15.0,

        bandwidth=100.0,

        energy_cost=0.5,

        reliability=0.98,

        risk="SAFE",

        predicted_cpu=edge_prediction[
            "target_cpu"
        ],

        predicted_memory=edge_prediction[
            "target_memory"
        ],

        prediction_uncertainty=cpu_uncertainty,

        battery_level=100.0,

        temperature=40.0,

        energy_watts=0.0,

        network_rx_bps=0.0,

        network_tx_bps=0.0
    )


    # -----------------------------------------------------
    # Cloud
    # -----------------------------------------------------

    cloud = ExecutionResource(

        name="Cloud",

        cpu_available=95.0,

        memory_available=95.0,

        latency=80.0,

        bandwidth=500.0,

        energy_cost=0.3,

        reliability=0.995,

        risk="SAFE",

        predicted_cpu=cloud_prediction[
            "target_cpu"
        ],

        predicted_memory=cloud_prediction[
            "target_memory"
        ],

        prediction_uncertainty=cpu_uncertainty,

        battery_level=100.0,

        temperature=45.0,

        energy_watts=0.0,

        network_rx_bps=0.0,

        network_tx_bps=0.0
    )


    return [
        local,
        edge,
        cloud
    ]


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    resources = create_execution_resources()

    print("=" * 60)
    print("EXECUTION RESOURCE PROFILE")
    print("=" * 60)

    for resource in resources:

        print()

        print(
            f"Resource: {resource.name}"
        )

        print(
            f"CPU available: "
            f"{resource.cpu_available:.2f}%"
        )

        print(
            f"Memory available: "
            f"{resource.memory_available:.2f}%"
        )

        print(
            f"Predicted CPU: "
            f"{resource.predicted_cpu:.2f}%"
        )

        print(
            f"Predicted memory: "
            f"{resource.predicted_memory:.2f}%"
        )

        print(
            f"Prediction uncertainty: "
            f"{resource.prediction_uncertainty:.4f}%"
        )

        print(
            f"Latency: "
            f"{resource.latency:.2f} ms"
        )

        print(
            f"Bandwidth: "
            f"{resource.bandwidth:.2f} Mbps"
        )

        print(
            f"Energy cost: "
            f"{resource.energy_cost:.2f}"
        )

        print(
            f"Energy telemetry: "
            f"{resource.energy_watts:.2f} W"
        )

        print(
            f"Battery: "
            f"{resource.battery_level:.2f}%"
        )

        print(
            f"Temperature: "
            f"{resource.temperature:.2f} C"
        )

    print()
    print("RESOURCE PROFILE TEST COMPLETED")