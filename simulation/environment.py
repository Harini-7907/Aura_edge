from dataclasses import dataclass


# ==========================================
# EXECUTION ENVIRONMENT
# ==========================================

@dataclass
class Environment:

    name: str

    cpu_capacity: float
    memory_capacity: float

    latency: float
    bandwidth: float

    energy_cost: float
    reliability: float

    battery_level: float
    temperature: float


# ==========================================
# CREATE ENVIRONMENTS
# ==========================================

def create_environments():

    # ------------------------------------------
    # LOCAL DEVICE
    # ------------------------------------------

    local = Environment(

        name="Local",

        cpu_capacity=60.0,

        memory_capacity=70.0,

        latency=5.0,

        bandwidth=50.0,

        energy_cost=0.8,

        reliability=0.95,

        battery_level=100.0,

        temperature=35.0
    )

    # ------------------------------------------
    # EDGE SERVER
    # ------------------------------------------

    edge = Environment(

        name="Edge",

        cpu_capacity=80.0,

        memory_capacity=85.0,

        latency=15.0,

        bandwidth=100.0,

        energy_cost=0.5,

        reliability=0.98,

        battery_level=100.0,

        temperature=40.0
    )

    # ------------------------------------------
    # CLOUD
    # ------------------------------------------

    cloud = Environment(

        name="Cloud",

        cpu_capacity=95.0,

        memory_capacity=95.0,

        latency=80.0,

        bandwidth=500.0,

        energy_cost=0.3,

        reliability=0.995,

        battery_level=100.0,

        temperature=45.0
    )

    return [
        local,
        edge,
        cloud
    ]


# ==========================================
# APPLY RESOURCE CHANGE
# ==========================================

def apply_resource_change(
    environment,
    cpu_change=0.0,
    memory_change=0.0,
    battery_change=0.0,
    temperature_change=0.0
):

    environment.cpu_capacity += cpu_change

    environment.memory_capacity += memory_change

    environment.battery_level += battery_change

    environment.temperature += temperature_change

    # Keep values within realistic limits

    environment.cpu_capacity = max(
        0.0,
        min(100.0, environment.cpu_capacity)
    )

    environment.memory_capacity = max(
        0.0,
        min(100.0, environment.memory_capacity)
    )

    environment.battery_level = max(
        0.0,
        min(100.0, environment.battery_level)
    )

    environment.temperature = max(
        20.0,
        min(100.0, environment.temperature)
    )


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(
        "Starting AURA-Edge environment simulator..."
    )

    environments = create_environments()

    local = environments[0]

    print(
        "\n=========================================="
    )

    print(
        "BEFORE RESOURCE CHANGE"
    )

    print(
        "=========================================="
    )

    print(
        "Local CPU:",
        f"{local.cpu_capacity:.1f}%"
    )

    print(
        "Local memory:",
        f"{local.memory_capacity:.1f}%"
    )

    print(
        "Local battery:",
        f"{local.battery_level:.1f}%"
    )

    print(
        "Local temperature:",
        f"{local.temperature:.1f} C"
    )

    # Simulate device degradation

    apply_resource_change(

        local,

        cpu_change=-20.0,

        memory_change=-15.0,

        battery_change=-30.0,

        temperature_change=30.0
    )

    print(
        "\n=========================================="
    )

    print(
        "AFTER RESOURCE CHANGE"
    )

    print(
        "=========================================="
    )

    print(
        "Local CPU:",
        f"{local.cpu_capacity:.1f}%"
    )

    print(
        "Local memory:",
        f"{local.memory_capacity:.1f}%"
    )

    print(
        "Local battery:",
        f"{local.battery_level:.1f}%"
    )

    print(
        "Local temperature:",
        f"{local.temperature:.1f} C"
    )

    print(
        "\n=========================================="
    )

    print(
        "RESOURCE CHANGE TEST COMPLETED"
    )

    print(
        "=========================================="
    )