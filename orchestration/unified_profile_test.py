import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from orchestration.mecperf_adapter import get_network_profile
from orchestration.prediction_adapter import get_real_prediction
from prediction.uncertainty import get_resource_uncertainty
from orchestration.resource_profile import ExecutionResource


# -----------------------------------------
# 1. Get predicted future resources
# -----------------------------------------

prediction = get_real_prediction()
uncertainty = get_resource_uncertainty()

predicted_cpu = prediction["target_cpu"]
predicted_memory = prediction["target_memory"]
cpu_uncertainty = uncertainty["target_cpu"]


# -----------------------------------------
# 2. Get real MECPerf network condition
# -----------------------------------------

network = get_network_profile(0)


# -----------------------------------------
# 3. Build unified Edge resource
# -----------------------------------------

edge = ExecutionResource(
    name="Edge-AURA",
    cpu_available=80.0,
    memory_available=85.0,

    # Real MECPerf values
    latency=network["latency_ms"],
    bandwidth=network["bandwidth_mbps"],

    energy_cost=0.5,
    reliability=0.98,
    risk="SAFE",

    # Real prediction values
    predicted_cpu=predicted_cpu,
    predicted_memory=predicted_memory,
    prediction_uncertainty=cpu_uncertainty,

    battery_level=100.0,
    temperature=40.0,

    energy_watts=0.0,
    network_rx_bps=0.0,
    network_tx_bps=0.0,
)


# -----------------------------------------
# 4. Display unified profile
# -----------------------------------------

print("AURA-Edge Unified Resource Profile")
print("===================================")

print()
print("CURRENT RESOURCES")
print(f"CPU available: {edge.cpu_available:.2f}%")
print(f"Memory available: {edge.memory_available:.2f}%")

print()
print("PREDICTED FUTURE RESOURCES")
print(f"Predicted CPU: {edge.predicted_cpu:.2f}%")
print(f"Predicted Memory: {edge.predicted_memory:.2f}%")
print(f"Prediction uncertainty: {edge.prediction_uncertainty:.4f}")

print()
print("REAL NETWORK CONDITIONS")
print(f"Latency: {edge.latency:.2f} ms")
print(f"Bandwidth: {edge.bandwidth:.4f} Mbps")

print()
print("OTHER CONDITIONS")
print(f"Battery: {edge.battery_level:.2f}%")
print(f"Temperature: {edge.temperature:.2f} C")
print(f"Reliability: {edge.reliability:.3f}")