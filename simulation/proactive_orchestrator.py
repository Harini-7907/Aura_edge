import sys
from pathlib import Path

# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================
# IMPORT PROJECT MODULES
# ==========================================

from simulation.environment import (
    create_environments,
    apply_resource_change
)

from orchestration.task_profiler import (
    create_task
)

from orchestration.decision_engine import (
    select_resource
)

from orchestration.resource_profile import (
    ExecutionResource
)

from simulation.migration_cost import (
    calculate_total_migration_time,
    can_migrate_before_deadline
)

from simulation.migration_logger import (
    log_migration
)


# ==========================================
# START
# ==========================================

print(
    "Starting proactive orchestrator..."
)


# ==========================================
# CREATE ENVIRONMENTS
# ==========================================

environments = create_environments()

local = environments[0]
edge = environments[1]
cloud = environments[2]


# ==========================================
# CREATE AI TASK
# ==========================================

task = create_task(

    task_id="proactive_task",

    cpu_requirement=40.0,

    memory_requirement=30.0,

    deadline=2.0,

    priority=2,

    estimated_execution_time=1.2,

    task_size=5.0
)


# ==========================================
# INITIAL RESOURCE STATE
# ==========================================

print(
    "\n=========================================="
)

print(
    "INITIAL RESOURCE STATE"
)

print(
    "=========================================="
)

print(
    "Local CPU:",
    f"{local.cpu_capacity:.1f}%"
)

print(
    "Local Memory:",
    f"{local.memory_capacity:.1f}%"
)

print(
    "Local Battery:",
    f"{local.battery_level:.1f}%"
)

print(
    "Local Temperature:",
    f"{local.temperature:.1f} C"
)


# ==========================================
# SIMULATE FUTURE LOCAL DEGRADATION
# ==========================================

apply_resource_change(

    local,

    cpu_change=-25.0,

    memory_change=-20.0,

    battery_change=-40.0,

    temperature_change=25.0
)


print(
    "\n=========================================="
)

print(
    "PREDICTED FUTURE LOCAL STATE"
)

print(
    "=========================================="
)

print(
    "Future Local CPU:",
    f"{local.cpu_capacity:.1f}%"
)

print(
    "Future Local Memory:",
    f"{local.memory_capacity:.1f}%"
)

print(
    "Future Local Battery:",
    f"{local.battery_level:.1f}%"
)

print(
    "Future Local Temperature:",
    f"{local.temperature:.1f} C"
)


# ==========================================
# CREATE RESOURCES FOR DECISION ENGINE
# ==========================================

resources = []


for environment in environments:

    risk = "SAFE"


    # --------------------------------------
    # CPU risk
    # --------------------------------------

    if environment.cpu_capacity < 50:

        risk = "WARNING"


    # --------------------------------------
    # Memory risk
    # --------------------------------------

    if environment.memory_capacity < 60:

        risk = "WARNING"


    # --------------------------------------
    # Battery risk
    # --------------------------------------

    if environment.battery_level < 50:

        risk = "WARNING"


    # --------------------------------------
    # Temperature risk
    # --------------------------------------

    if environment.temperature >= 60:

        risk = "WARNING"


    # --------------------------------------
    # Create execution resource
    # --------------------------------------

    resource = ExecutionResource(

        name=environment.name,

        cpu_available=environment.cpu_capacity,

        memory_available=environment.memory_capacity,

        latency=environment.latency,

        bandwidth=environment.bandwidth,

        energy_cost=environment.energy_cost,

        reliability=environment.reliability,

        risk=risk,

        # The degraded state is used as the
        # future state for this simulation.
        predicted_cpu=100.0 - environment.cpu_capacity,

        predicted_memory=100.0 - environment.memory_capacity,

        prediction_uncertainty=0.0,

        battery_level=environment.battery_level,

        temperature=environment.temperature
    )


    resources.append(resource)


# ==========================================
# PROACTIVE ORCHESTRATION
# ==========================================

print(
    "\n=========================================="
)

print(
    "PROACTIVE ORCHESTRATION"
)

print(
    "=========================================="
)


# ==========================================
# DECISION ENGINE
# ==========================================

selected, results, rejected = select_resource(

    task,

    resources
)


# ==========================================
# INITIALIZE MIGRATION VARIABLES
# ==========================================

migration_feasible = False

migration_time = 0.0

selected_score = None


# ==========================================
# MIGRATION DECISION
# ==========================================

if selected is None:

    print(
        "Migration decision: NO"
    )

    print(
        "No feasible resource found."
    )


else:

    # --------------------------------------
    # Calculate migration overhead
    # --------------------------------------

    migration_time = calculate_total_migration_time(

        task,

        selected
    )


    # --------------------------------------
    # Check deadline feasibility
    # --------------------------------------

    migration_feasible = can_migrate_before_deadline(

        task,

        selected
    )


    # --------------------------------------
    # Find selected resource score
    # --------------------------------------

    for resource, score in results:

        if resource.name == selected.name:

            selected_score = score

            break


    # --------------------------------------
    # Display decision
    # --------------------------------------

    print(
        "Migration decision: YES"
    )

    print(
        "Previous resource: Local"
    )

    print(
        "Selected resource:",
        selected.name
    )


    if selected_score is not None:

        print(
            "Selected score:",
            f"{selected_score:.2f}"
        )


    print(
        "Migration + latency time:",
        f"{migration_time:.3f}",
        "seconds"
    )


    print(
        "Migration deadline feasible:",
        "YES"
        if migration_feasible
        else "NO"
    )


# ==========================================
# FINAL MIGRATION DECISION
# ==========================================

if selected is not None:

    if migration_feasible:

        print(
            "Migration approved:"
            " task can meet its deadline"
        )

        log_migration(

            task_id=task.task_id,

            previous_resource="Local",

            new_resource=selected.name,

            migration_time=migration_time,

            deadline_feasible=True,

            score=selected_score,

            reason="Future resource degradation predicted"
        )

        print(
            "Migration decision logged successfully."
        )

    else:

        print(
            "Migration rejected:"
            " migration overhead is too high"
        )

        log_migration(

            task_id=task.task_id,

            previous_resource="Local",

            new_resource=selected.name,

            migration_time=migration_time,

            deadline_feasible=False,

            score=selected_score,

            reason="Migration overhead exceeds deadline constraint"
        )

        print(
            "Rejected migration decision logged."
        )

else:

    print(
        "Migration cannot be performed:"
        " no feasible destination resource."
    )


# ==========================================
# RESOURCE EVALUATION
# ==========================================

print(
    "\n=========================================="
)

print(
    "RESOURCE EVALUATION"
)

print(
    "=========================================="
)


if results:

    print(
        "Candidate resources:"
    )


    for resource, score in results:

        print(
            f"{resource.name}: "
            f"Score = {score:.2f}"
        )


else:

    print(
        "No feasible candidate resources."
    )


# ==========================================
# REJECTED RESOURCES
# ==========================================

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


# ==========================================
# FINAL STATUS
# ==========================================

print(
    "\n=========================================="
)

if selected is not None and migration_feasible:

    print(
        "FINAL STATUS: MIGRATION APPROVED"
    )

elif selected is not None:

    print(
        "FINAL STATUS: MIGRATION REJECTED"
    )

else:

    print(
        "FINAL STATUS: NO FEASIBLE DESTINATION"
    )

print(
    "=========================================="
)

print(
    "PROACTIVE ORCHESTRATOR COMPLETED"
)

print(
    "=========================================="
)