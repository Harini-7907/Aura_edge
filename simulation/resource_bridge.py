import sys
from pathlib import Path

# Add AURA-Edge project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from environment import create_environments
from orchestration.resource_profile import ExecutionResource


# ==========================================
# CONVERT SIMULATION ENVIRONMENTS
# ==========================================

def create_execution_resources_from_simulation():

    environments = create_environments()

    resources = []

    for environment in environments:

        resource = ExecutionResource(

            name=environment.name,

            cpu_available=environment.cpu_capacity,

            memory_available=environment.memory_capacity,

            latency=environment.latency,

            bandwidth=environment.bandwidth,

            energy_cost=environment.energy_cost,

            reliability=environment.reliability,

            risk="SAFE",

            predicted_cpu=environment.cpu_capacity,

            predicted_memory=environment.memory_capacity,

            prediction_uncertainty=0.0,

            battery_level=environment.battery_level,

            temperature=environment.temperature
        )

        resources.append(resource)

    return resources


# ==========================================
# TEST BRIDGE
# ==========================================

if __name__ == "__main__":

    print(
        "Starting simulation resource bridge..."
    )

    resources = (
        create_execution_resources_from_simulation()
    )

    print(
        "\n=========================================="
    )

    print(
        "SIMULATION RESOURCE BRIDGE"
    )

    print(
        "=========================================="
    )

    for resource in resources:

        print(
            f"\nResource: {resource.name}"
        )

        print(
            "CPU:",
            f"{resource.cpu_available:.1f}%"
        )

        print(
            "Memory:",
            f"{resource.memory_available:.1f}%"
        )

        print(
            "Latency:",
            f"{resource.latency:.1f} ms"
        )

        print(
            "Bandwidth:",
            f"{resource.bandwidth:.1f} Mbps"
        )

    print(
        "\n=========================================="
    )

    print(
        "SIMULATION RESOURCE BRIDGE COMPLETED"
    )

    print(
        "=========================================="
    )