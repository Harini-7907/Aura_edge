import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from orchestration.mecperf_adapter import get_network_profile
from orchestration.resource_profile import ExecutionResource
from orchestration.decision_engine import select_resource
from orchestration.task_profiler import create_task


task = create_task(
    task_id="network_test_task",
    cpu_requirement=20.0,
    memory_requirement=20.0,
    deadline=2.0,
    priority=1,
    estimated_execution_time=1.0,
    task_size=5.0,
)


for index in range(5):

    profile = get_network_profile(index)

    edge = ExecutionResource(
        name="Edge-MECPerf",
        cpu_available=80.0,
        memory_available=85.0,
        latency=profile["latency_ms"],
        bandwidth=profile["bandwidth_mbps"],
        energy_cost=0.5,
        reliability=0.98,
        risk="SAFE",
        predicted_cpu=50.0,
        predicted_memory=50.0,
        prediction_uncertainty=0.0,
        battery_level=100.0,
        temperature=40.0,
    )

    selected, results, rejected = select_resource(
        task,
        [edge]
    )

    print(
        f"Condition {index + 1}: "
        f"Latency={profile['latency_ms']:.2f} ms | "
        f"Bandwidth={profile['bandwidth_mbps']:.4f} Mbps | "
        f"Score={results[0][1]:.2f} | "
        f"Selected={selected.name}"
    )