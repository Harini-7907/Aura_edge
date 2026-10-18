import csv
from pathlib import Path
from datetime import datetime


RESULTS_FILE = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "experiment_results.csv"
)


def initialize_results_file():

    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not RESULTS_FILE.exists():

        with open(
            RESULTS_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "timestamp",
                "scenario_id",
                "strategy",
                "migration",
                "migration_time",
                "deadline_feasible",
                "cpu_at_migration",
                "memory_at_migration",
                "battery_at_migration",
                "temperature_at_migration",
                "destination"
            ])


def record_result(
    scenario_id,
    strategy,
    migration,
    migration_time,
    deadline_feasible,
    cpu_at_migration,
    memory_at_migration,
    battery_at_migration,
    temperature_at_migration,
    destination
):

    initialize_results_file()

    with open(
        RESULTS_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            scenario_id,
            strategy,
            migration,
            migration_time,
            deadline_feasible,
            cpu_at_migration,
            memory_at_migration,
            battery_at_migration,
            temperature_at_migration,
            destination
        ])


if __name__ == "__main__":

    initialize_results_file()

    print("==========================================")
    print("EXPERIMENT RESULT STORAGE READY")
    print("==========================================")

    print("Results file:")
    print(RESULTS_FILE)

    print("\nExperiment result structure initialized.")