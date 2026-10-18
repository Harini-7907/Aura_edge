import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def calculate_migration_time(task_size_mb, bandwidth_mbps):
    """
    Estimate task migration time in seconds.
    """

    if bandwidth_mbps <= 0:
        return float("inf")

    task_size_megabits = task_size_mb * 8

    migration_time = (
        task_size_megabits / bandwidth_mbps
    )

    return migration_time


def calculate_total_migration_time(
    task,
    destination_resource
):
    """
    Migration time + destination network latency.
    """

    migration_time = calculate_migration_time(
        task.task_size,
        destination_resource.bandwidth
    )

    latency_seconds = (
        destination_resource.latency / 1000
    )

    total_time = (
        migration_time
        + latency_seconds
    )

    return total_time


def can_migrate_before_deadline(
    task,
    destination_resource
):
    """
    Check whether migration can complete
    before the task deadline.
    """

    migration_time = calculate_total_migration_time(
        task,
        destination_resource
    )

    remaining_time = (
        task.deadline
        - task.estimated_execution_time
    )

    return migration_time <= remaining_time


if __name__ == "__main__":

    from orchestration.task_profiler import create_task
    from orchestration.resource_profile import ExecutionResource


    print(
        "Starting deadline-aware migration test..."
    )


    # ======================================
    # CREATE TEST TASK
    # ======================================

    task = create_task(
        task_id="migration_deadline_task",
        cpu_requirement=40.0,
        memory_requirement=30.0,
        deadline=2.0,
        priority=2,
        estimated_execution_time=1.2,
        task_size=5.0
    )


    # ======================================
    # CREATE TEST DESTINATION
    # ======================================

    edge = ExecutionResource(
        name="Edge",
        cpu_available=80.0,
        memory_available=85.0,
        latency=15.0,
        bandwidth=100.0,
        energy_cost=0.5,
        reliability=0.98,
        risk="SAFE",
        predicted_cpu=80.0,
        predicted_memory=85.0,
        prediction_uncertainty=0.0,
        battery_level=100.0,
        temperature=40.0
    )


    # ======================================
    # CALCULATE MIGRATION
    # ======================================

    migration_time = calculate_total_migration_time(
        task,
        edge
    )

    deadline_feasible = can_migrate_before_deadline(
        task,
        edge
    )


    # ======================================
    # DISPLAY RESULT
    # ======================================

    print("\n==========================================")
    print("DEADLINE-AWARE MIGRATION")
    print("==========================================")

    print(
        "Task:",
        task.task_id
    )

    print(
        "Task deadline:",
        task.deadline,
        "seconds"
    )

    print(
        "Estimated execution time:",
        task.estimated_execution_time,
        "seconds"
    )

    print(
        "Task size:",
        task.task_size,
        "MB"
    )

    print(
        "Destination:",
        edge.name
    )

    print(
        "Migration + latency time:",
        f"{migration_time:.3f}",
        "seconds"
    )

    print(
        "Migration deadline feasible:",
        "YES" if deadline_feasible else "NO"
    )


    print("\n==========================================")
    print(
        "DEADLINE-AWARE MIGRATION TEST COMPLETED"
    )
    print("==========================================")