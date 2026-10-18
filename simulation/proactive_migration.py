import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from environment import create_environments, apply_resource_change
from orchestration.task_profiler import create_task


print("Starting proactive migration test...")


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
    task_id="migration_task",
    cpu_requirement=40.0,
    memory_requirement=30.0,
    deadline=2.0,
    priority=2,
    estimated_execution_time=1.2,
    task_size=5.0
)


# ==========================================
# INITIAL DECISION
# ==========================================

print("\n==========================================")
print("INITIAL TASK PLACEMENT")
print("==========================================")

print("Task:", task.task_id)
print("Initial placement: Local")


# ==========================================
# PREDICT FUTURE LOCAL DEGRADATION
# ==========================================

apply_resource_change(
    local,
    cpu_change=-25.0,
    memory_change=-20.0,
    battery_change=-40.0,
    temperature_change=25.0
)


# ==========================================
# CHECK FUTURE DEGRADATION
# ==========================================

degradation_detected = False

if local.cpu_capacity < 50:
    degradation_detected = True

if local.memory_capacity < 60:
    degradation_detected = True

if local.battery_level < 50:
    degradation_detected = True

if local.temperature >= 60:
    degradation_detected = True


print("\n==========================================")
print("FUTURE RESOURCE ANALYSIS")
print("==========================================")

print("Future Local CPU:", f"{local.cpu_capacity:.1f}%")
print("Future Local Memory:", f"{local.memory_capacity:.1f}%")
print("Future Local Battery:", f"{local.battery_level:.1f}%")
print("Future Local Temperature:", f"{local.temperature:.1f} C")

print(
    "Future degradation detected:",
    "YES" if degradation_detected else "NO"
)


# ==========================================
# PROACTIVE MIGRATION DECISION
# ==========================================

print("\n==========================================")
print("PROACTIVE MIGRATION DECISION")
print("==========================================")


if degradation_detected:

    if edge.cpu_capacity >= task.cpu_requirement:

        selected_resource = edge

    else:

        selected_resource = cloud

    print("Migration required: YES")
    print("Current resource: Local")
    print("New resource:", selected_resource.name)
    print("Reason: Future resource degradation predicted")

else:

    selected_resource = local

    print("Migration required: NO")
    print("Task remains on Local")


# ==========================================
# FINAL RESULT
# ==========================================

print("\n==========================================")
print("PROACTIVE MIGRATION TEST COMPLETED")
print("==========================================")

print(
    "Final task placement:",
    selected_resource.name
)