from pathlib import Path
import sys


# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------
from orchestration.task_profiler import create_task
from orchestration.resource_profile import ExecutionResource
from orchestration.decision_engine import select_resource
from orchestration.mecperf_adapter import get_network_profile
from orchestration.enact_adapter import get_enact_resource_profile


# ---------------------------------------------------------
# Create AI task
# ---------------------------------------------------------
task = create_task(
    task_id="unified_ai_task",
    cpu_requirement=10,
    memory_requirement=10,
    deadline=2,
    priority=1,
    estimated_execution_time=1,
    task_size=5,
)


# ---------------------------------------------------------
# Get REAL ENACT edge telemetry + prediction
# ---------------------------------------------------------
enact = get_enact_resource_profile("rpi4")


# ---------------------------------------------------------
# Get REAL MECPerf network condition
# ---------------------------------------------------------
network = get_network_profile(0)


# ---------------------------------------------------------
# Build Local resource
# ---------------------------------------------------------
local = ExecutionResource(
    name="Local",

    cpu_available=70,
    memory_available=60,

    latency=2,
    bandwidth=10,

    energy_cost=2,
    reliability=0.95,
    risk="SAFE",

    predicted_cpu=70,
    predicted_memory=60,
    prediction_uncertainty=3.0,

    battery_level=80,
    temperature=40,
)


# ---------------------------------------------------------
# Build REAL ENACT Edge resource
# ---------------------------------------------------------
edge = ExecutionResource(
    name=f"Edge-ENACT-{enact['node_name']}",

    # Current available resources
    cpu_available=100 - enact["cpu_utilization"],
    memory_available=100 - enact["memory_utilization"],

    # REAL MECPerf network condition
    latency=network["latency_ms"],
    bandwidth=network["bandwidth_mbps"],

    # REAL ENACT power
    energy_cost=enact["energy_watts"],

    reliability=0.95,
    risk="SAFE",

    # ENACT-specific future prediction
    predicted_cpu=enact["predicted_cpu"],
    predicted_memory=enact["predicted_memory"],

    # ENACT-specific uncertainty
    prediction_uncertainty=enact[
        "cpu_prediction_uncertainty"
    ],

    battery_level=100,
    temperature=35,

    # Real ENACT telemetry
    energy_watts=enact["energy_watts"],
    network_rx_bps=enact["network_rx_bps"],
    network_tx_bps=enact["network_tx_bps"],
)


# ---------------------------------------------------------
# Build Cloud resource
# ---------------------------------------------------------
cloud = ExecutionResource(
    name="Cloud",

    cpu_available=90,
    memory_available=90,

    latency=80,
    bandwidth=20,

    energy_cost=3,
    reliability=0.99,
    risk="SAFE",

    predicted_cpu=50,
    predicted_memory=50,
    prediction_uncertainty=2.0,

    battery_level=100,
    temperature=30,
)


# ---------------------------------------------------------
# Run AURA-Edge decision engine
# ---------------------------------------------------------
best, results, rejected = select_resource(
    task,
    [local, edge, cloud]
)


# ---------------------------------------------------------
# Display task information
# ---------------------------------------------------------
print("\nAURA-EDGE REAL TELEMETRY + PREDICTION")
print("=" * 50)

print("\nAI TASK")
print(f"Task ID: {task.task_id}")
print(
    f"CPU requirement: "
    f"{task.cpu_requirement}%"
)
print(
    f"Memory requirement: "
    f"{task.memory_requirement}%"
)
print(
    f"Deadline: "
    f"{task.deadline:.2f} seconds"
)
print(
    f"Execution time: "
    f"{task.estimated_execution_time:.2f} seconds"
)


# ---------------------------------------------------------
# Display REAL ENACT telemetry
# ---------------------------------------------------------
print("\nREAL ENACT EDGE")
print(
    f"Node: "
    f"{enact['node_name']}"
)

print(
    f"Current CPU utilization: "
    f"{enact['cpu_utilization']:.2f}%"
)

print(
    f"Current memory utilization: "
    f"{enact['memory_utilization']:.2f}%"
)

print(
    f"Available CPU: "
    f"{edge.cpu_available:.2f}%"
)

print(
    f"Available memory: "
    f"{edge.memory_available:.2f}%"
)

print(
    f"Energy: "
    f"{enact['energy_watts']:.2f} W"
)

print(
    f"Network RX: "
    f"{enact['network_rx_bps']:.2f} B/s"
)

print(
    f"Network TX: "
    f"{enact['network_tx_bps']:.2f} B/s"
)


# ---------------------------------------------------------
# Display ENACT-specific prediction
# ---------------------------------------------------------
print("\nENACT-SPECIFIC PREDICTION")

print(
    f"Predicted CPU: "
    f"{enact['predicted_cpu']:.2f}%"
)

print(
    f"Predicted memory: "
    f"{enact['predicted_memory']:.2f}%"
)

print(
    f"CPU uncertainty: "
    f"{enact['cpu_prediction_uncertainty']:.4f}%"
)

print(
    f"Memory uncertainty: "
    f"{enact['memory_prediction_uncertainty']:.4f}%"
)


# ---------------------------------------------------------
# Display REAL MECPerf network condition
# ---------------------------------------------------------
print("\nREAL MECPerf NETWORK")

print(
    f"Latency: "
    f"{network['latency_ms']:.2f} ms"
)

print(
    f"Bandwidth: "
    f"{network['bandwidth_mbps']:.4f} Mbps"
)


# ---------------------------------------------------------
# Display resource scores
# ---------------------------------------------------------
print("\nRESOURCE SCORES")

for result in results:

    # decision_engine returns:
    # (ExecutionResource, score)
    resource, score = result

    print(
        f"{resource.name}: "
        f"{score:.2f}"
    )


# ---------------------------------------------------------
# Display rejected resources
# ---------------------------------------------------------
if rejected:

    print("\nREJECTED RESOURCES")

    for item in rejected:

        # decision_engine returns:
        # (ExecutionResource, reasons)
        resource, reasons = item

        print(
            f"{resource.name}: "
            f"{', '.join(reasons)}"
        )


# ---------------------------------------------------------
# Final decision
# ---------------------------------------------------------
print(
    f"\nFINAL SELECTED RESOURCE: "
    f"{best.name if best else 'NONE'}"
)

print("=" * 50)