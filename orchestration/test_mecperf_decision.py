import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mecperf_adapter import get_network_profile
from resource_profile import ExecutionResource
from decision_engine import select_resource
from task_profiler import create_task


profile = get_network_profile(0)

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

task = create_task(
    task_id="mecperf_task_001",
    cpu_requirement=20.0,
    memory_requirement=20.0,
    deadline=2.0,
    priority=1,
    estimated_execution_time=1.0,
    task_size=5.0,
)

selected, results, rejected = select_resource(
    task,
    [edge]
)

print("AURA-Edge MECPerf Decision")
print("==========================")
print(f"Network latency: {profile['latency_ms']:.2f} ms")
print(f"Network bandwidth: {profile['bandwidth_mbps']:.4f} Mbps")
print(f"Selected resource: {selected.name}")
print()

for resource, score in results:
    print(f"{resource.name}: score={score:.2f}")

if rejected:
    print()
    print("Rejected resources:")
    for resource, reasons in rejected:
        print(resource.name, reasons)
        