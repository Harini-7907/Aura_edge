from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mecperf_adapter import get_network_profile
from resource_profile import ExecutionResource


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

print("AURA-Edge + MECPerf")
print("===================")
print(f"Resource: {edge.name}")
print(f"Latency: {edge.latency:.2f} ms")
print(f"Bandwidth: {edge.bandwidth:.4f} Mbps")
print(f"CPU available: {edge.cpu_available:.2f}%")
print(f"Memory available: {edge.memory_available:.2f}%")