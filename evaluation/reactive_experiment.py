import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from simulation.environment import create_environments, apply_resource_change
from evaluation.experiment_results import record_result


SCENARIO_FILE = (
    PROJECT_ROOT
    / "results"
    / "scenarios.json"
)


def load_scenarios():

    with open(
        SCENARIO_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def run_reactive_scenario(scenario, scenario_id):

    environments = create_environments()

    local = environments[0]
    edge = environments[1]

    # Reactive strategy waits until degradation occurs.
    apply_resource_change(
        local,
        cpu_change=-scenario["cpu_degradation"],
        memory_change=-scenario["memory_degradation"],
        battery_change=-scenario["battery_drop"],
        temperature_change=scenario["temperature_increase"]
    )

    degradation_detected = (
        local.cpu_capacity < 40.0
        or local.memory_capacity < 60.0
        or local.battery_level < 50.0
        or local.temperature >= 60.0
    )

    if degradation_detected:

        destination = edge.name
        migration = True

    else:

        destination = local.name
        migration = False

    record_result(
        scenario_id=scenario_id,
        strategy="Reactive",
        migration=migration,
        migration_time=0.0,
        deadline_feasible=True,
        cpu_at_migration=local.cpu_capacity,
        memory_at_migration=local.memory_capacity,
        battery_at_migration=local.battery_level,
        temperature_at_migration=local.temperature,
        destination=destination
    )

    return migration, destination


def run_reactive_experiments():

    print("Starting Reactive baseline experiment...")

    scenarios = load_scenarios()

    migration_count = 0

    for index, scenario in enumerate(
        scenarios,
        start=1
    ):

        scenario_id = f"scenario_{index:03d}"

        migration, destination = (
            run_reactive_scenario(
                scenario,
                scenario_id
            )
        )

        if migration:
            migration_count += 1

        print(
            f"Scenario {index:02d}: "
            f"Migration={migration} | "
            f"Destination={destination}"
        )

    print("\n==========================================")
    print("REACTIVE EXPERIMENT COMPLETED")
    print("==========================================")

    print("Total scenarios:", len(scenarios))
    print("Migrations:", migration_count)

    print(
        "Migration rate:",
        f"{(migration_count / len(scenarios)) * 100:.2f}%"
    )


if __name__ == "__main__":
    run_reactive_experiments()