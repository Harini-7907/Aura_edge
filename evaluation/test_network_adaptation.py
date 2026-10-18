import sys
from pathlib import Path
import csv
from datetime import datetime

# ==========================================
# PROJECT ROOT
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================
# IMPORT AURA-EDGE COMPONENTS
# ==========================================

from orchestration.mecperf_adapter import get_network_profile
from orchestration.enact_adapter import load_enact_resources
from orchestration.prediction_adapter import get_real_prediction
from prediction.uncertainty import get_resource_uncertainty
from orchestration.resource_profile import ExecutionResource
from orchestration.decision_engine import select_resource
from orchestration.task_profiler import create_task


# ==========================================
# RESULT FILE
# ==========================================

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "network_adaptation_results.csv"
)

RESULTS_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# GET REAL PREDICTION
# ==========================================

prediction = get_real_prediction()

uncertainty = get_resource_uncertainty()


# ==========================================
# GET REAL ENACT TELEMETRY
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

    task_id="network_adaptation_task",

    cpu_requirement=10.0,

    memory_requirement=10.0,

    deadline=2.0,

    priority=1,

    estimated_execution_time=1.0,

    task_size=5.0
)


# ==========================================
# START RESULT FILE
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

        "latency_ms",

        "bandwidth_mbps",

        "selected_resource"

    ])


# ==========================================
# START EXPERIMENT
# ==========================================

print()

print(
    "AURA-Edge NETWORK ADAPTATION TEST"
)

print(
    "================================="
)

print()


# ==========================================
# TEST FIVE REAL NETWORK CONDITIONS
# ==========================================

for condition in range(5):

    # --------------------------------------
    # Get MECPerf network condition
    # --------------------------------------

    network = get_network_profile(
        condition
    )


    # ======================================
    # LOCAL RESOURCE
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

        predicted_cpu=prediction[
            "target_cpu"
        ],

        predicted_memory=prediction[
            "target_memory"
        ],

        prediction_uncertainty=uncertainty[
            "target_cpu"
        ],

        battery_level=100.0,

        temperature=35.0
    )


    # ======================================
    # REAL ENACT EDGE RESOURCE
    # ======================================

    edge = ExecutionResource(

        name="Edge-ENACT-rpi4",

        cpu_available=(
            100.0
            - rpi4["cpu_utilization"]
        ),

        memory_available=(
            100.0
            - rpi4["memory_utilization"]
        ),

        latency=network[
            "latency_ms"
        ],

        bandwidth=network[
            "bandwidth_mbps"
        ],

        energy_cost=0.5,

        reliability=0.98,

        risk="SAFE",

        predicted_cpu=(
            100.0
            - rpi4["cpu_utilization"]
        ),

        predicted_memory=(
            100.0
            - rpi4["memory_utilization"]
        ),

        prediction_uncertainty=uncertainty[
            "target_cpu"
        ],

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
    # CLOUD RESOURCE
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

        predicted_cpu=prediction[
            "target_cpu"
        ],

        predicted_memory=prediction[
            "target_memory"
        ],

        prediction_uncertainty=uncertainty[
            "target_cpu"
        ],

        battery_level=100.0,

        temperature=45.0
    )


    # ======================================
    # AURA-EDGE DECISION
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
    # DISPLAY RESULTS
    # ======================================

    print(
        f"Condition {condition + 1}"
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

            network[
                "latency_ms"
            ],

            network[
                "bandwidth_mbps"
            ],

            selected_name

        ])


    print(
        "-" * 45
    )


# ==========================================
# COMPLETION MESSAGE
# ==========================================

print()

print(
    "NETWORK ADAPTATION TEST COMPLETED"
)

print(
    f"Results saved to:"
)

print(
    RESULTS_FILE
)