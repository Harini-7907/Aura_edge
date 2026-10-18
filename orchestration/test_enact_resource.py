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


# ---------------------------------------------------------
# Convert ENACT node to AURA-Edge resource
# ---------------------------------------------------------

def create_enact_resource(node):

    cpu_utilization = node["cpu_utilization"]

    memory_utilization = node["memory_utilization"]

    # Convert utilization to available capacity
    cpu_available = max(
        0.0,
        100.0 - cpu_utilization
    )

    memory_available = max(
        0.0,
        100.0 - memory_utilization
    )

    resource = ExecutionResource(

        name=f"ENACT-{node['node_name']}",

        cpu_available=cpu_available,

        memory_available=memory_available,

        # These remain placeholders for now.
        # MECPerf will later provide network
        # latency/bandwidth measurements.
        latency=0.0,

        bandwidth=0.0,

        # Energy cost is represented by real
        # ENACT power telemetry for this test.
        energy_cost=node["energy_watts"],

        reliability=0.95,

        risk="SAFE",

        predicted_cpu=0.0,

        predicted_memory=0.0,

        prediction_uncertainty=0.0,

        battery_level=100.0,

        temperature=35.0,

        energy_watts=node["energy_watts"],

        network_rx_bps=node["network_rx_bps"],

        network_tx_bps=node["network_tx_bps"]
    )

    return resource


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("ENACT → AURA-EDGE RESOURCE TEST")
    print("=" * 70)

    nodes = load_enact_resources()

    # Select Raspberry Pi
    rpi_node = next(
        node
        for node in nodes
        if node["node_name"] == "rpi4"
    )

    resource = create_enact_resource(
        rpi_node
    )

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
        f"Energy: "
        f"{resource.energy_watts:.2f} W"
    )

    print(
        f"Network RX: "
        f"{resource.network_rx_bps:.2f} B/sec"
    )

    print(
        f"Network TX: "
        f"{resource.network_tx_bps:.2f} B/sec"
    )

    print()

    print(
        "ENACT → AURA-Edge resource conversion successful."
    )