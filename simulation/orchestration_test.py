import sys
from pathlib import Path

# Add AURA-Edge project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from environment import create_environments
from orchestration.resource_profile import ExecutionResource
from orchestration.task_profiler import create_task
from orchestration.decision_engine import select_resource


# ==========================================
# CONVERT ENVIRONMENTS TO RESOURCES
# ==========================================

def create_simulation_resources():

    environments = create_environments()

    resources = []

    for environment in environments:

        resource = ExecutionResource(

            name=environment.name,

            cpu_available=environment.cpu_capacity,

            memory_available=environment.memory_capacity,

            latency=environment.latency,

            bandwidth=environment.bandwidth,

            energy_cost=environment.energy_cost,

            reliability=environment.reliability,

            risk="SAFE",

            predicted_cpu=environment.cpu_capacity,

            predicted_memory=environment.memory_capacity,

            prediction_uncertainty=0.0,

            battery_level=environment.battery_level,

            temperature=environment.temperature
        )

        resources.append(resource)

    return resources


# ==========================================
# MAIN TEST
# ==========================================

if __name__ == "__main__":

    print(
        "Starting simulation + orchestration test..."
    )

    resources = create_simulation_resources()

    task = create_task(

        task_id="simulation_task",

        cpu_requirement=40.0,

        memory_requirement=30.0,

        deadline=2.0,

        priority=1,

        estimated_execution_time=1.2,

        task_size=5.0
    )

    selected, results, rejected = select_resource(
        task,
        resources
    )

    print(
        "\n=========================================="
    )

    print(
        "SIMULATION ORCHESTRATION RESULT"
    )

    print(
        "=========================================="
    )

    print(
        "\nTask:",
        task.task_id
    )

    print(
        "CPU requirement:",
        f"{task.cpu_requirement:.1f}%"
    )

    print(
        "Memory requirement:",
        f"{task.memory_requirement:.1f}%"
    )

    print(
        "Deadline:",
        f"{task.deadline:.2f}s"
    )

    print(
        "\nCandidate resources:"
    )

    for resource, score in results:

        print(
            f"{resource.name}: "
            f"Score = {score:.2f}"
        )

    if rejected:

        print(
            "\nRejected resources:"
        )

        for resource, reasons in rejected:

            print(
                f"\n{resource.name}:"
            )

            for reason in reasons:

                print(
                    f"  - {reason}"
                )

    if selected is not None:

        print(
            "\nSelected resource:",
            selected[0].name
        )

        print(
            "Selected score:",
            f"{selected[1]:.2f}"
        )

    else:

        print(
            "\nSelected resource: NONE"
        )

    print(
        "\n=========================================="
    )

    print(
        "SIMULATION ORCHESTRATION TEST COMPLETED"
    )

    print(
        "=========================================="
    )