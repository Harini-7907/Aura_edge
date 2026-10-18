import csv
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(
    exist_ok=True
)

LOG_FILE = RESULTS_DIR / "migration_log.csv"


def log_migration(
    task_id,
    previous_resource,
    new_resource,
    migration_time,
    deadline_feasible,
    score,
    reason
):

    file_exists = LOG_FILE.exists()

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "timestamp",
                "task_id",
                "previous_resource",
                "new_resource",
                "migration_time",
                "deadline_feasible",
                "score",
                "reason"
            ])

        writer.writerow([

            datetime.now().isoformat(
                timespec="seconds"
            ),

            task_id,

            previous_resource,

            new_resource,

            round(
                migration_time,
                3
            ),

            deadline_feasible,

            round(
                score,
                2
            ),

            reason
        ])


if __name__ == "__main__":

    print(
        "Starting migration logger test..."
    )

    log_migration(

        task_id="test_task",

        previous_resource="Local",

        new_resource="Edge",

        migration_time=0.415,

        deadline_feasible=True,

        score=116.75,

        reason="Future resource degradation predicted"
    )

    print("\n==========================================")

    print(
        "MIGRATION LOG CREATED"
    )

    print(
        "Log file:",
        LOG_FILE
    )

    print("==========================================")

    print(
        "Migration logger test completed."
    )