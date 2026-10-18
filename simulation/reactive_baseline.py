import sys
from pathlib import Path

# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from environment import (
    create_environments,
    apply_resource_change
)

from orchestration.task_profiler import (
    create_task
)


print(
    "Starting reactive scheduling baseline..."
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

    task_id="reactive_task",

    cpu_requirement=40.0,

    memory_requirement=30.0,

    deadline=2.0,

    priority=2,

    estimated_execution_time=1.2,

    task_size=5.0
)


# ==========================================
# INITIAL PLACEMENT
# ==========================================

current_resource = local


print(
    "\n=========================================="
)

print(
    "INITIAL PLACEMENT"
)

print(
    "=========================================="
)

print(
    "Task:",
    task.task_id
)

print(
    "Current resource:",
    current_resource.name
)


# ==========================================
# SIMULATE DEGRADATION
# ==========================================

apply_resource_change(

    local,

    cpu_change=-25.0,

    memory_change=-20.0,

    battery_change=-40.0,

    temperature_change=25.0
)


# ==========================================
# CHECK CURRENT STATE
# ==========================================

print(
    "\n=========================================="
)

print(
    "CURRENT RESOURCE STATE"
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
# REACTIVE DECISION
# ==========================================

print(
    "\n=========================================="
)

print(
    "REACTIVE DECISION"
)

print(
    "=========================================="
)


if local.cpu_capacity < task.cpu_requirement:

    print(
        "Current degradation detected: YES"
    )

    print(
        "Reactive migration triggered."
    )

    # Choose Edge if it can satisfy task
    if edge.cpu_capacity >= task.cpu_requirement:

        current_resource = edge

    else:

        current_resource = cloud

else:

    print(
        "Current degradation detected: NO"
    )

    print(
        "Task remains on Local."
    )


# ==========================================
# FINAL RESULT
# ==========================================

print(
    "\n=========================================="
)

print(
    "REACTIVE BASELINE RESULT"
)

print(
    "=========================================="
)

print(
    "Final resource:",
    current_resource.name
)

print(
    "Migration occurred:",
    "YES"
    if current_resource.name != "Local"
    else "NO"
)


print(
    "\n=========================================="
)

print(
    "REACTIVE BASELINE COMPLETED"
)

print(
    "=========================================="
)