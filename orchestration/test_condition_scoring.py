from task_profiler import create_task
from resource_profile import create_execution_resources
from decision_engine import calculate_score


print("Starting condition-aware scoring test...")

resources = create_execution_resources()

task = create_task(
    task_id="condition_test",
    cpu_requirement=40.0,
    memory_requirement=30.0,
    deadline=2.0,
    priority=2,
    estimated_execution_time=1.2,
    task_size=5.0
)

# ------------------------------------------
# NORMAL LOCAL CONDITION
# ------------------------------------------

normal_score = calculate_score(
    task,
    resources[0]
)

# ------------------------------------------
# STRESSED LOCAL CONDITION
# ------------------------------------------

resources[0].battery_level = 25.0
resources[0].temperature = 75.0

stressed_score = calculate_score(
    task,
    resources[0]
)

print("\n==========================================")
print("CONDITION-AWARE SCORING")
print("==========================================")

print(
    "Normal battery:",
    "100.0%"
)

print(
    "Normal temperature:",
    "35.0 C"
)

print(
    "Normal score:",
    f"{normal_score:.2f}"
)

print()

print(
    "Stressed battery:",
    f"{resources[0].battery_level:.1f}%"
)

print(
    "Stressed temperature:",
    f"{resources[0].temperature:.1f} C"
)

print(
    "Stressed score:",
    f"{stressed_score:.2f}"
)

print()

print(
    "Score reduction:",
    f"{normal_score - stressed_score:.2f}"
)

print("\n==========================================")
print("CONDITION-AWARE SCORING TEST COMPLETED")
print("==========================================")