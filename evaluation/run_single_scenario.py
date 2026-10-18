import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simulation.environment import create_environments, apply_resource_change
from evaluation.scenario_generator import generate_scenario
from evaluation.experiment_results import record_result


def run_single_scenario():

    print("Starting single scenario simulation...")

    environments = create_environments()

    local = environments[0]
    edge = environments[1]

    scenario = generate_scenario()

    print("\n==========================================")
    print("GENERATED SCENARIO")
    print("==========================================")

    print("CPU degradation:",
          f"{scenario['cpu_degradation']:.2f}%")

    print("Memory degradation:",
          f"{scenario['memory_degradation']:.2f}%")

    print("Battery drop:",
          f"{scenario['battery_drop']:.2f}%")

    print("Temperature increase:",
          f"{scenario['temperature_increase']:.2f} C")

    print("\n==========================================")
    print("CURRENT LOCAL STATE")
    print("==========================================")

    print("CPU:", local.cpu_capacity, "%")
    print("Memory:", local.memory_capacity, "%")
    print("Battery:", local.battery_level, "%")
    print("Temperature:", local.temperature, "C")

    future_cpu = local.cpu_capacity - scenario["cpu_degradation"]
    future_memory = local.memory_capacity - scenario["memory_degradation"]
    future_battery = local.battery_level - scenario["battery_drop"]
    future_temperature = local.temperature + scenario["temperature_increase"]

    print("\n==========================================")
    print("PREDICTED FUTURE LOCAL STATE")
    print("==========================================")

    print("Future CPU:", f"{future_cpu:.2f}%")
    print("Future Memory:", f"{future_memory:.2f}%")
    print("Future Battery:", f"{future_battery:.2f}%")
    print("Future Temperature:", f"{future_temperature:.2f} C")

    degradation_detected = (
        future_cpu < 40.0
        or future_memory < 60.0
        or future_battery < 50.0
        or future_temperature >= 60.0
    )

    print("\n==========================================")
    print("AURA-EDGE PROACTIVE DECISION")
    print("==========================================")

    if degradation_detected:

        print("Future degradation detected: YES")
        print("Migration decision: YES")
        print("Selected destination:", edge.name)

    else:

        print("Future degradation detected: NO")
        print("Migration decision: NO")
        print("Task remains on:", local.name)

    record_result(
        scenario_id="scenario_001",
        strategy="AURA-Edge",
        migration=degradation_detected,
        migration_time=0.0,
        deadline_feasible=True,
        cpu_at_migration=local.cpu_capacity,
        memory_at_migration=local.memory_capacity,
        battery_at_migration=local.battery_level,
        temperature_at_migration=local.temperature,
        destination=edge.name if degradation_detected else local.name
    )
        
    apply_resource_change(
        local,
        cpu_change=-scenario["cpu_degradation"],
        memory_change=-scenario["memory_degradation"],
        battery_change=-scenario["battery_drop"],
        temperature_change=scenario["temperature_increase"]
    )

    print("\n==========================================")
    print("ACTUAL STATE AFTER DEGRADATION")
    print("==========================================")

    print("CPU:", f"{local.cpu_capacity:.2f}%")
    print("Memory:", f"{local.memory_capacity:.2f}%")
    print("Battery:", f"{local.battery_level:.2f}%")
    print("Temperature:", f"{local.temperature:.2f} C")

    print("\n==========================================")
    print("SCENARIO COMPLETED")
    print("==========================================")


if __name__ == "__main__":
    run_single_scenario()