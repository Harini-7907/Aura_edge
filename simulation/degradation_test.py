from environment import create_environments, apply_resource_change


print("Starting resource degradation test...")


# ==========================================
# CREATE ENVIRONMENTS
# ==========================================

environments = create_environments()

local = environments[0]


# ==========================================
# INITIAL STATE
# ==========================================

print("\n==========================================")
print("INITIAL LOCAL STATE")
print("==========================================")

print(
    "CPU:",
    f"{local.cpu_capacity:.1f}%"
)

print(
    "Memory:",
    f"{local.memory_capacity:.1f}%"
)

print(
    "Battery:",
    f"{local.battery_level:.1f}%"
)

print(
    "Temperature:",
    f"{local.temperature:.1f} C"
)


# ==========================================
# SIMULATE FUTURE DEGRADATION
# ==========================================

apply_resource_change(

    local,

    cpu_change=-25.0,

    memory_change=-20.0,

    battery_change=-40.0,

    temperature_change=25.0
)


# ==========================================
# FUTURE STATE
# ==========================================

print("\n==========================================")
print("FUTURE DEGRADED STATE")
print("==========================================")

print(
    "CPU:",
    f"{local.cpu_capacity:.1f}%"
)

print(
    "Memory:",
    f"{local.memory_capacity:.1f}%"
)

print(
    "Battery:",
    f"{local.battery_level:.1f}%"
)

print(
    "Temperature:",
    f"{local.temperature:.1f} C"
)


# ==========================================
# SIMPLE DEGRADATION DETECTION
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
print("DEGRADATION ANALYSIS")
print("==========================================")

if degradation_detected:

    print(
        "Future degradation detected: YES"
    )

else:

    print(
        "Future degradation detected: NO"
    )


print("\n==========================================")
print("DEGRADATION TEST COMPLETED")
print("==========================================")