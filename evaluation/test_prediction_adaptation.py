import sys
from pathlib import Path
import csv
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from orchestration.mecperf_adapter import get_network_profile
from orchestration.enact_adapter import (
    load_enact_resources,
    get_enact_prediction
)
from orchestration.resource_profile import ExecutionResource
from orchestration.decision_engine import select_resource
from orchestration.task_profiler import create_task


# ==========================================
# RESULT FILE
# ==========================================

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "prediction_adaptation_results.csv"
)

RESULTS_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# REAL ENACT PREDICTION
# ==========================================

prediction = get_enact_prediction(
    "rpi4"
)

cpu_prediction = prediction[
    "predicted_cpu"
]

memory_prediction = prediction[
    "predicted_memory"
]

cpu_uncertainty = prediction[
    "cpu_uncertainty"
]

memory_uncertainty = prediction[
    "memory_uncertainty"
]


# ==========================================
# REAL ENACT TELEMETRY
# ==========================================

enact_nodes = load_enact_resources()

rpi4 = None

for node in enact_nodes:

    if node["node_name"] == "rpi4":

        rpi4 = node

        break


if rpi4 is None:

    raise RuntimeError(
        "rpi4 telemetry was not found."
    )


# ==========================================
# CREATE AI TASK
# ==========================================

task = create_task(

    task_id="prediction_adaptation_task",

    cpu_requirement=10.0,

    memory_requirement=10.0,

    deadline=2.0,

    priority=1,

    estimated_execution_time=1.0,

    task_size=5.0
)


# ==========================================
# INITIALIZE RESULT FILE
# ==========================================

with open(

    RESULTS_FILE,

    "w",

    newline="",

    encoding="utf-8"

) as file:

    writer = csv.writer(file)

    writer.writerow([

        "timestamp",

        "condition",

        "current_cpu_edge",

        "current_memory_edge",

        "predicted_cpu",

        "predicted_memory",

        "cpu_uncertainty",

        "memory_uncertainty",

        "latency_ms",

        "bandwidth_mbps",

        "selected_resource"

    ])


# ==========================================
# START EXPERIMENT
# ==========================================

print()

print(
    "AURA-Edge PREDICTION-AWARE ADAPTATION TEST"
)

print(
    "=========================================="
)

print()

print(
    "Using ENACT-specific rpi4 prediction"
)

print()


# ==========================================
# TEST FIVE CONDITIONS
# ==========================================

for condition in range(5):

    # --------------------------------------
    # MECPerf network condition
    # --------------------------------------

    network = get_network_profile(
        condition
    )


    # --------------------------------------
    # Current ENACT resources
    # --------------------------------------

    current_edge_cpu = (
        100.0
        - rpi4["cpu_utilization"]
    )

    current_edge_memory = (
        100.0
        - rpi4["memory_utilization"]
    )


    # ======================================
    # LOCAL
    # ======================================

    local = ExecutionResource(

        name="Local",

        cpu_available=60.0,

        memory_available=70.0,

        latency=5.0,

        bandwidth=50.0,

        energy_cost=0.8,

        reliability=0.95,

        risk="WARNING",

        predicted_cpu=65.0,

        predicted_memory=65.0,

        prediction_uncertainty=cpu_uncertainty,

        battery_level=100.0,

        temperature=35.0
    )


    # ======================================
    # EDGE WITH ENACT TELEMETRY + PREDICTION
    # ======================================

    edge = ExecutionResource(

        name="Edge-ENACT-rpi4",

        cpu_available=current_edge_cpu,

        memory_available=current_edge_memory,

        latency=network[
            "latency_ms"
        ],

        bandwidth=network[
            "bandwidth_mbps"
        ],

        energy_cost=0.5,

        reliability=0.98,

        risk="SAFE",

        predicted_cpu=cpu_prediction,

        predicted_memory=memory_prediction,

        prediction_uncertainty=cpu_uncertainty,

        battery_level=100.0,

        temperature=40.0,

        energy_watts=rpi4[
            "energy_watts"
        ],

        network_rx_bps=rpi4[
            "network_rx_bps"
        ],

        network_tx_bps=rpi4[
            "network_tx_bps"
        ]
    )


    # ======================================
    # CLOUD
    # ======================================

    cloud = ExecutionResource(

        name="Cloud",

        cpu_available=95.0,

        memory_available=95.0,

        latency=80.0,

        bandwidth=500.0,

        energy_cost=0.3,

        reliability=0.995,

        risk="SAFE",

        predicted_cpu=45.0,

        predicted_memory=50.0,

        prediction_uncertainty=cpu_uncertainty,

        battery_level=100.0,

        temperature=45.0
    )


    # ======================================
    # RUN DECISION
    # ======================================

    selected, results, rejected = (
        select_resource(

            task,

            [
                local,
                edge,
                cloud
            ]
        )
    )


    # ======================================
    # DISPLAY
    # ======================================

    print(
        f"Condition {condition + 1}"
    )

    print(
        f"Current Edge CPU: "
        f"{current_edge_cpu:.2f}%"
    )

    print(
        f"Current Edge Memory: "
        f"{current_edge_memory:.2f}%"
    )

    print(
        f"Predicted CPU: "
        f"{cpu_prediction:.2f}%"
    )

    print(
        f"Predicted Memory: "
        f"{memory_prediction:.2f}%"
    )

    print(
        f"CPU uncertainty: "
        f"{cpu_uncertainty:.4f}%"
    )

    print(
        f"Memory uncertainty: "
        f"{memory_uncertainty:.4f}%"
    )

    print(
        f"Latency: "
        f"{network['latency_ms']:.2f} ms"
    )

    print(
        f"Bandwidth: "
        f"{network['bandwidth_mbps']:.4f} Mbps"
    )


    print(
        "Scores:"
    )

    for resource, score in results:

        print(

            f"  {resource.name}: "
            f"{score:.2f}"

        )


    if selected:

        selected_name = selected.name

        print(
            f"Selected: "
            f"{selected_name}"
        )

    else:

        selected_name = "NONE"

        print(
            "Selected: NONE"
        )


    # ======================================
    # SAVE RESULT
    # ======================================

    with open(

        RESULTS_FILE,

        "a",

        newline="",

        encoding="utf-8"

    ) as file:

        writer = csv.writer(file)

        writer.writerow([

            datetime.now().isoformat(),

            condition + 1,

            current_edge_cpu,

            current_edge_memory,

            cpu_prediction,

            memory_prediction,

            cpu_uncertainty,

            memory_uncertainty,

            network[
                "latency_ms"
            ],

            network[
                "bandwidth_mbps"
            ],

            selected_name

        ])


    print(
        "-" * 50
    )


# ==========================================
# COMPLETION
# ==========================================

print()

print(
    "PREDICTION-AWARE ADAPTATION TEST COMPLETED"
)

print()

print(
    "Results saved to:"
)

print(
    RESULTS_FILE
)