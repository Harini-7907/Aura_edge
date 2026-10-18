import sys
from pathlib import Path


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from orchestration.enact_adapter import (
    load_enact_resources
)

from orchestration.resource_profile import (
    ExecutionResource
)

from orchestration.task_profiler import (
    create_task
)

from orchestration.decision_engine import (
    select_resource
)


# ---------------------------------------------------------
# Convert ENACT node into AURA-Edge resource
# ---------------------------------------------------------

def convert_enact_node(node):

    cpu_available = max(
        0.0,
        100.0 - node["cpu_utilization"]
    )

    memory_available = max(
        0.0,
        100.0 - node["memory_utilization"]
    )

    return ExecutionResource(

        name=f"ENACT-{node['node_name']}",

        cpu_available=cpu_available,

        memory_available=memory_available,

        latency=15.0,

        bandwidth=100.0,

        energy_cost=node["energy_watts"],

        reliability=0.95,

        risk="SAFE",

        predicted_cpu=cpu_available,

        predicted_memory=memory_available,

        prediction_uncertainty=0.0,

        battery_level=100.0,

        temperature=35.0,

        energy_watts=node["energy_watts"],

        network_rx_bps=node["network_rx_bps"],

        network_tx_bps=node["network_tx_bps"]
    )


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("ENACT + AURA-EDGE DECISION ENGINE TEST")
    print("=" * 70)

    # -----------------------------------------------------
    # Load ENACT telemetry
    # -----------------------------------------------------

    nodes = load_enact_resources()

    # Select Raspberry Pi
    rpi_node = next(
        node
        for node in nodes
        if node["node_name"] == "rpi4"
    )

    enact_resource = convert_enact_node(
        rpi_node
    )

    # -----------------------------------------------------
    # Create AI task
    # -----------------------------------------------------

    task = create_task(
        task_id="enact_task_001",
        cpu_requirement=10.0,
        memory_requirement=10.0,
        deadline=2.0,
        priority=1,
        estimated_execution_time=1.0,
        task_size=5.0
    )

    # -----------------------------------------------------
    # Add ENACT resource
    # -----------------------------------------------------

    resources = [
        enact_resource
    ]

    # -----------------------------------------------------
    # Run decision engine
    # -----------------------------------------------------

    best_resource, results, rejected = (
        select_resource(
            task,
            resources
        )
    )

    # -----------------------------------------------------
    # Display result
    # -----------------------------------------------------

    print()

    print(
        f"Task: {task.task_id}"
    )

    print(
        f"CPU requirement: "
        f"{task.cpu_requirement:.2f}%"
    )

    print(
        f"Memory requirement: "
        f"{task.memory_requirement:.2f}%"
    )

    print()

    print(
        f"Selected resource: "
        f"{best_resource.name}"
    )

    print()

    for resource, score in results:

        print(
            f"{resource.name}: "
            f"Score={score:.2f}"
        )

    print()

    if rejected:

        print("Rejected resources:")

        for resource, reasons in rejected:

            print(
                f"{resource.name}: "
                f"{reasons}"
            )

    print()

    print(
        "ENACT + AURA-Edge decision test completed."
    )