import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "experiment_results.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "final_comparison.csv"
)


# ---------------------------------------------------------
# Create comparison
# ---------------------------------------------------------

def create_final_comparison():

    # Load experiment results
    df = pd.read_csv(RESULTS_FILE)

    # Separate strategies
    aura = df[df["strategy"] == "AURA-Edge"]
    reactive = df[df["strategy"] == "Reactive"]

    # Calculate averages
    aura_cpu = aura["cpu_at_migration"].mean()
    reactive_cpu = reactive["cpu_at_migration"].mean()

    aura_memory = aura["memory_at_migration"].mean()
    reactive_memory = reactive["memory_at_migration"].mean()

    aura_temperature = aura["temperature_at_migration"].mean()
    reactive_temperature = reactive["temperature_at_migration"].mean()

    aura_battery = aura["battery_at_migration"].mean()
    reactive_battery = reactive["battery_at_migration"].mean()

    # Calculate migration statistics
    aura_migrations = aura["migration"].sum()
    reactive_migrations = reactive["migration"].sum()

    aura_migration_rate = (
        aura_migrations / len(aura) * 100
    )

    reactive_migration_rate = (
        reactive_migrations / len(reactive) * 100
    )

    # Calculate proactive advantages
    cpu_advantage = (
        aura_cpu - reactive_cpu
    )

    memory_advantage = (
        aura_memory - reactive_memory
    )

    temperature_advantage = (
        reactive_temperature - aura_temperature
    )

    battery_advantage = (
        aura_battery - reactive_battery
    )

    # Create final summary table
    comparison = pd.DataFrame({

        "Metric": [
            "Average CPU at Migration (%)",
            "Average Memory at Migration (%)",
            "Average Temperature at Migration (C)",
            "Average Battery at Migration (%)",
            "Migration Count",
            "Migration Rate (%)",
            "CPU Advantage (percentage points)",
            "Memory Advantage (percentage points)",
            "Temperature Advantage (C)",
            "Battery Advantage (percentage points)"
        ],

        "AURA-Edge": [
            aura_cpu,
            aura_memory,
            aura_temperature,
            aura_battery,
            aura_migrations,
            aura_migration_rate,
            "",
            "",
            "",
            ""
        ],

        "Reactive": [
            reactive_cpu,
            reactive_memory,
            reactive_temperature,
            reactive_battery,
            reactive_migrations,
            reactive_migration_rate,
            "",
            "",
            "",
            ""
        ],

        "AURA-Edge Advantage": [
            cpu_advantage,
            memory_advantage,
            temperature_advantage,
            battery_advantage,
            "",
            "",
            cpu_advantage,
            memory_advantage,
            temperature_advantage,
            battery_advantage
        ]
    })

    # Create results directory if needed
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save
    comparison.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # Display results
    print("=" * 50)
    print("FINAL COMPARISON RESULTS")
    print("=" * 50)

    print()
    print(comparison.to_string(index=False))

    print()
    print("=" * 50)
    print("RESULT SAVED")
    print("=" * 50)

    print(
        f"File: {OUTPUT_FILE}"
    )


# ---------------------------------------------------------
# Run
# ---------------------------------------------------------

if __name__ == "__main__":

    create_final_comparison()