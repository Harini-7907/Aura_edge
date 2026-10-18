import sys
from pathlib import Path
import json

# ---------------------------------------------------------
# Add project root to Python path
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

from simulation.environment import (
    create_environments,
    apply_resource_change
)

from simulation.migration_cost import (
    calculate_total_migration_time
)

from evaluation.experiment_results import (
    initialize_results_file,
    record_result
)


# ---------------------------------------------------------
# File locations
# ---------------------------------------------------------

SCENARIO_FILE = (
    PROJECT_ROOT
    / "results"
    / "scenarios.json"
)


# ---------------------------------------------------------
# Load scenarios
# ---------------------------------------------------------

def load_scenarios():

    with open(
        SCENARIO_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ---------------------------------------------------------
# Run one AURA-Edge scenario
# ---------------------------------------------------------

def run_aura_edge_scenario(
    scenario,
    scenario_id
):

    # -----------------------------------------------------
    # Create initial environments
    # -----------------------------------------------------

    environments = create_environments()

    local = environments[0]
    edge = environments[1]

    # -----------------------------------------------------
    # Store initial resource state
    # -----------------------------------------------------

    initial_cpu = local.cpu_capacity
    initial_memory = local.memory_capacity
    initial_battery = local.battery_level
    initial_temperature = local.temperature

    # -----------------------------------------------------
    # Predict future local resource state
    # -----------------------------------------------------

    future_cpu = (
        initial_cpu
        - scenario["cpu_degradation"]
    )

    future_memory = (
        initial_memory
        - scenario["memory_degradation"]
    )

    future_battery = (
        initial_battery
        - scenario["battery_drop"]
    )

    future_temperature = (
        initial_temperature
        + scenario["temperature_increase"]
    )

    # -----------------------------------------------------
    # AURA-Edge proactive degradation detection
    # -----------------------------------------------------

    degradation_detected = (

        future_cpu < 40

        or future_memory < 60

        or future_battery < 50

        or future_temperature >= 60
    )

    # -----------------------------------------------------
    # Select destination
    # -----------------------------------------------------

    if degradation_detected:

        migration = True
        destination = "Edge"

        # Calculate actual migration time
        # Task size = 5 MB
        migration_task = type(
            "MigrationTask",
            (),
            {
                "task_size": 5.0
            }
        )()

        migration_time = (
            calculate_total_migration_time(
                task=migration_task,
                destination_resource=edge
            )
        )

        deadline_feasible = (
            migration_time <= 0.8
        )

    else:

        migration = False
        destination = "Local"
        migration_time = 0.0
        deadline_feasible = True

    # -----------------------------------------------------
    # Record state BEFORE degradation
    # -----------------------------------------------------

    record_result(
        scenario_id=scenario_id,
        strategy="AURA-Edge",
        migration=migration,
        migration_time=migration_time,
        deadline_feasible=deadline_feasible,
        cpu_at_migration=initial_cpu,
        memory_at_migration=initial_memory,
        battery_at_migration=initial_battery,
        temperature_at_migration=initial_temperature,
        destination=destination
    )

    # -----------------------------------------------------
    # Apply degradation to environment
    # -----------------------------------------------------

    apply_resource_change(
        local,
        cpu_change=-scenario["cpu_degradation"],
        memory_change=-scenario["memory_degradation"],
        battery_change=-scenario["battery_drop"],
        temperature_change=scenario["temperature_increase"]
    )

    # -----------------------------------------------------
    # Print scenario result
    # -----------------------------------------------------

    print(
        f"Scenario {scenario_id:02d}: "
        f"Migration={migration} | "
        f"Destination={destination}"
    )


# ---------------------------------------------------------
# Main experiment
# ---------------------------------------------------------

def run_experiments():

    print("Starting AURA-Edge experiment...")

    # -----------------------------------------------------
    # Initialize results CSV
    # -----------------------------------------------------

    initialize_results_file()

    # -----------------------------------------------------
    # Load scenarios
    # -----------------------------------------------------

    scenarios = load_scenarios()

    # -----------------------------------------------------
    # Run every scenario
    # -----------------------------------------------------

    migration_count = 0

    for index, scenario in enumerate(
        scenarios,
        start=1
    ):

        run_aura_edge_scenario(
            scenario,
            index
        )

        # Count migration
        if (
            scenario["cpu_degradation"] > 0
        ):
            pass

    # -----------------------------------------------------
    # Read experiment results to calculate migration rate
    # -----------------------------------------------------

    results_file = (
        PROJECT_ROOT
        / "results"
        / "experiment_results.csv"
    )

    import csv

    with open(
        results_file,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)

    aura_rows = [
        row
        for row in rows
        if row["strategy"] == "AURA-Edge"
    ]

    migration_count = sum(
        row["migration"] == "True"
        for row in aura_rows
    )

    total_scenarios = len(aura_rows)

    if total_scenarios > 0:

        migration_rate = (
            migration_count
            / total_scenarios
            * 100
        )

    else:

        migration_rate = 0.0

    # -----------------------------------------------------
    # Final summary
    # -----------------------------------------------------

    print()
    print("AURA-Edge experiment completed.")
    print(
        f"Total scenarios: {total_scenarios}"
    )
    print(
        f"Migration count: {migration_count}"
    )
    print(
        f"Migration rate: {migration_rate:.2f}%"
    )


# ---------------------------------------------------------
# Run program
# ---------------------------------------------------------

if __name__ == "__main__":

    run_experiments()