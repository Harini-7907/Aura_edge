import csv
from pathlib import Path


RESULTS_FILE = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "experiment_results.csv"
)


def analyze_results():

    aura_cpu = []
    aura_memory = []
    aura_temperature = []
    aura_battery = []

    reactive_cpu = []
    reactive_memory = []
    reactive_temperature = []
    reactive_battery = []

    with open(
        RESULTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["strategy"] == "AURA-Edge":

                aura_cpu.append(
                    float(row["cpu_at_migration"])
                )

                aura_memory.append(
                    float(row["memory_at_migration"])
                )

                aura_temperature.append(
                    float(row["temperature_at_migration"])
                )

                aura_battery.append(
                    float(row["battery_at_migration"])
                )

            elif row["strategy"] == "Reactive":

                reactive_cpu.append(
                    float(row["cpu_at_migration"])
                )

                reactive_memory.append(
                    float(row["memory_at_migration"])
                )

                reactive_temperature.append(
                    float(row["temperature_at_migration"])
                )

                reactive_battery.append(
                    float(row["battery_at_migration"])
                )

    aura_avg_cpu = sum(aura_cpu) / len(aura_cpu)
    aura_avg_memory = sum(aura_memory) / len(aura_memory)
    aura_avg_temperature = (
        sum(aura_temperature)
        / len(aura_temperature)
    )
    aura_avg_battery = (
        sum(aura_battery)
        / len(aura_battery)
    )

    reactive_avg_cpu = (
        sum(reactive_cpu)
        / len(reactive_cpu)
    )

    reactive_avg_memory = (
        sum(reactive_memory)
        / len(reactive_memory)
    )

    reactive_avg_temperature = (
        sum(reactive_temperature)
        / len(reactive_temperature)
    )

    reactive_avg_battery = (
        sum(reactive_battery)
        / len(reactive_battery)
    )

    print("==========================================")
    print("EXPERIMENT RESULT ANALYSIS")
    print("==========================================")

    print("\nAURA-Edge")

    print(
        "Average CPU at migration:",
        f"{aura_avg_cpu:.2f}%"
    )

    print(
        "Average Memory at migration:",
        f"{aura_avg_memory:.2f}%"
    )

    print(
        "Average Temperature at migration:",
        f"{aura_avg_temperature:.2f} C"
    )

    print(
        "Average Battery at migration:",
        f"{aura_avg_battery:.2f}%"
    )

    print("\nReactive")

    print(
        "Average CPU at migration:",
        f"{reactive_avg_cpu:.2f}%"
    )

    print(
        "Average Memory at migration:",
        f"{reactive_avg_memory:.2f}%"
    )

    print(
        "Average Temperature at migration:",
        f"{reactive_avg_temperature:.2f} C"
    )

    print(
        "Average Battery at migration:",
        f"{reactive_avg_battery:.2f}%"
    )

    print("\n==========================================")
    print("PROACTIVE ADVANTAGE")
    print("==========================================")

    print(
        "CPU advantage:",
        f"{aura_avg_cpu - reactive_avg_cpu:.2f}",
        "percentage points"
    )

    print(
        "Memory advantage:",
        f"{aura_avg_memory - reactive_avg_memory:.2f}",
        "percentage points"
    )

    print(
        "Temperature advantage:",
        f"{reactive_avg_temperature - aura_avg_temperature:.2f}",
        "C"
    )

    print(
        "Battery advantage:",
        f"{aura_avg_battery - reactive_avg_battery:.2f}",
        "percentage points"
    )


if __name__ == "__main__":
    analyze_results()