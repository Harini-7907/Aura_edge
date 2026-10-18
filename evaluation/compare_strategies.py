import sys
from pathlib import Path

# ==========================================
# ADD PROJECT ROOT TO PYTHON PATH
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from simulation.environment import (
    create_environments,
    apply_resource_change
)


# ==========================================
# EXPERIMENT PARAMETERS
# ==========================================

CPU_THRESHOLD = 40.0
MEMORY_THRESHOLD = 30.0


# ==========================================
# RUN REACTIVE STRATEGY
# ==========================================

def run_reactive():

    environments = create_environments()

    local = environments[0]
    edge = environments[1]

    # Resource degradation happens first
    apply_resource_change(
        local,
        cpu_change=-25.0,
        memory_change=-20.0,
        battery_change=-40.0,
        temperature_change=25.0
    )

    migration_occurred = False

    migration_trigger = "None"

    destination = "Local"

    # Reactive strategy checks AFTER degradation
    if (
        local.cpu_capacity < CPU_THRESHOLD
        or
        local.memory_capacity < 60.0
    ):

        migration_occurred = True

        migration_trigger = (
            "After degradation"
        )

        if edge.cpu_capacity >= CPU_THRESHOLD:

            destination = "Edge"

    return {
        "strategy": "Reactive",
        "migration": migration_occurred,
        "trigger": migration_trigger,
        "destination": destination
    }


# ==========================================
# RUN AURA-EDGE STRATEGY
# ==========================================

def run_aura_edge():

    environments = create_environments()

    local = environments[0]
    edge = environments[1]
    cloud = environments[2]

    # Future degradation is predicted
    future_cpu = (
        local.cpu_capacity - 25.0
    )

    future_memory = (
        local.memory_capacity - 20.0
    )

    migration_occurred = False

    migration_trigger = "None"

    destination = "Local"

    # AURA-Edge checks future state
    if (
        future_cpu < CPU_THRESHOLD
        or
        future_memory < 60.0
    ):

        migration_occurred = True

        migration_trigger = (
            "Before degradation"
        )

        # Choose destination
        if edge.cpu_capacity >= CPU_THRESHOLD:

            destination = "Edge"

        else:

            destination = "Cloud"

    return {
        "strategy": "AURA-Edge",
        "migration": migration_occurred,
        "trigger": migration_trigger,
        "destination": destination
    }


# ==========================================
# RUN EXPERIMENT
# ==========================================

print(
    "Starting strategy comparison..."
)


reactive_result = run_reactive()

aura_result = run_aura_edge()


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "\n=========================================="
)

print(
    "STRATEGY COMPARISON"
)

print(
    "=========================================="
)


for result in [
    reactive_result,
    aura_result
]:

    print(
        "\nStrategy:",
        result["strategy"]
    )

    print(
        "Migration occurred:",
        "YES"
        if result["migration"]
        else "NO"
    )

    print(
        "Migration trigger:",
        result["trigger"]
    )

    print(
        "Destination:",
        result["destination"]
    )


# ==========================================
# FINAL COMPARISON
# ==========================================

print(
    "\n=========================================="
)

print(
    "COMPARISON SUMMARY"
)

print(
    "=========================================="
)

print(
    "Reactive strategy waits for degradation."
)

print(
    "AURA-Edge predicts degradation beforehand."
)

print(
    "\nStrategy comparison completed."
)

print(
    "=========================================="
)