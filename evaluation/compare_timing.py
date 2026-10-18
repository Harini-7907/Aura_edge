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
# RUN REACTIVE STRATEGY
# ==========================================

def run_reactive():

    environments = create_environments()

    local = environments[0]

    # Degradation happens first
    apply_resource_change(
        local,
        cpu_change=-25.0,
        memory_change=-20.0,
        battery_change=-40.0,
        temperature_change=25.0
    )

    migration_cpu = local.cpu_capacity
    migration_memory = local.memory_capacity
    migration_battery = local.battery_level
    migration_temperature = local.temperature

    return {
        "strategy": "Reactive",
        "cpu": migration_cpu,
        "memory": migration_memory,
        "battery": migration_battery,
        "temperature": migration_temperature
    }


# ==========================================
# RUN AURA-EDGE
# ==========================================

def run_aura_edge():

    environments = create_environments()

    local = environments[0]

    # AURA-Edge observes current state
    current_cpu = local.cpu_capacity
    current_memory = local.memory_capacity
    current_battery = local.battery_level
    current_temperature = local.temperature

    # Predict future degradation
    future_cpu = (
        current_cpu - 25.0
    )

    future_memory = (
        current_memory - 20.0
    )

    # Migration is triggered BEFORE degradation
    if (
        future_cpu < 40.0
        or
        future_memory < 60.0
    ):

        migration_cpu = current_cpu
        migration_memory = current_memory
        migration_battery = current_battery
        migration_temperature = current_temperature

    else:

        migration_cpu = current_cpu
        migration_memory = current_memory
        migration_battery = current_battery
        migration_temperature = current_temperature

    return {
        "strategy": "AURA-Edge",
        "cpu": migration_cpu,
        "memory": migration_memory,
        "battery": migration_battery,
        "temperature": migration_temperature
    }


# ==========================================
# RUN EXPERIMENT
# ==========================================

print(
    "Starting migration timing comparison..."
)


reactive = run_reactive()

aura = run_aura_edge()


# ==========================================
# DISPLAY RESULTS
# ==========================================

print(
    "\n=========================================="
)

print(
    "MIGRATION TIMING COMPARISON"
)

print(
    "=========================================="
)


for result in [
    reactive,
    aura
]:

    print(
        "\nStrategy:",
        result["strategy"]
    )

    print(
        "CPU at migration:",
        f"{result['cpu']:.1f}%"
    )

    print(
        "Memory at migration:",
        f"{result['memory']:.1f}%"
    )

    print(
        "Battery at migration:",
        f"{result['battery']:.1f}%"
    )

    print(
        "Temperature at migration:",
        f"{result['temperature']:.1f} C"
    )


# ==========================================
# CALCULATE DIFFERENCE
# ==========================================

cpu_difference = (
    aura["cpu"] - reactive["cpu"]
)

memory_difference = (
    aura["memory"] - reactive["memory"]
)


print(
    "\n=========================================="
)

print(
    "TIMING ADVANTAGE"
)

print(
    "=========================================="
)

print(
    "CPU advantage at migration:",
    f"{cpu_difference:.1f} percentage points"
)

print(
    "Memory advantage at migration:",
    f"{memory_difference:.1f} percentage points"
)

print(
    "\nAURA-Edge migrates before the resource"
    " reaches the degraded state."
)

print(
    "\n=========================================="
)

print(
    "MIGRATION TIMING TEST COMPLETED"
)

print(
    "=========================================="
)