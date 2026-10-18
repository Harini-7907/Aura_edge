from resource_profile import create_execution_resources


print("Starting environment condition test...")

resources = create_execution_resources()

# Simulate a stressed local device
resources[0].battery_level = 25.0
resources[0].temperature = 75.0

print("\n==========================================")
print("ENVIRONMENT CONDITION TEST")
print("==========================================")

print(
    "Resource:",
    resources[0].name
)

print(
    "Battery level:",
    f"{resources[0].battery_level:.1f}%"
)

print(
    "Temperature:",
    f"{resources[0].temperature:.1f} C"
)

print("\n==========================================")
print("ENVIRONMENT CONDITION TEST COMPLETED")
print("==========================================")