from task_profiler import create_task
from resource_profile import create_execution_resources
from decision_engine import select_resource


print("Starting stress-aware resource selection test...")

resources = create_execution_resources()

# ------------------------------------------
# Make Local competitive for this test
# ------------------------------------------

resources[0].bandwidth = 10.0
resources[0].energy_cost = 0.3
resources[0].reliability = 0.99
resources[0].risk = "SAFE"

# ------------------------------------------
# Create AI task
# ------------------------------------------

task = create_task(
    task_id="stress_test",
    cpu_requirement=40.0,
    memory_requirement=30.0,
    deadline=2.0,
    priority=1,
    estimated_execution_time=1.2,
    task_size=5.0
)

# ------------------------------------------
# NORMAL ENVIRONMENT
# ------------------------------------------

normal_selected, normal_results, normal_rejected = (
    select_resource(
        task,
        resources
    )
)

# ------------------------------------------
# STRESSED LOCAL ENVIRONMENT
# ------------------------------------------

resources[0].battery_level = 25.0
resources[0].temperature = 75.0

stressed_selected, stressed_results, stressed_rejected = (
    select_resource(
        task,
        resources
    )
)

# ------------------------------------------
# DISPLAY RESULTS
# ------------------------------------------

print("\n==========================================")
print("STRESS-AWARE RESOURCE SELECTION")
print("==========================================")

print("\nNormal Local Conditions:")

print(
    "Battery:",
    "100.0%"
)

print(
    "Temperature:",
    "35.0 C"
)

if normal_selected is not None:

    print(
        "Selected resource:",
        normal_selected[0].name
    )

    print(
        "Score:",
        f"{normal_selected[1]:.2f}"
    )

else:

    print(
        "Selected resource: NONE"
    )

print("\nStressed Local Conditions:")

print(
    "Battery:",
    f"{resources[0].battery_level:.1f}%"
)

print(
    "Temperature:",
    f"{resources[0].temperature:.1f} C"
)

if stressed_selected is not None:

    print(
        "Selected resource:",
        stressed_selected[0].name
    )

    print(
        "Score:",
        f"{stressed_selected[1]:.2f}"
    )

else:

    print(
        "Selected resource: NONE"
    )

print("\n==========================================")
print("STRESS-AWARE SELECTION TEST COMPLETED")
print("==========================================")