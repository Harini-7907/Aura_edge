import random


def generate_scenario():

    scenario_type = random.choice([
        "stable",
        "mild",
        "moderate",
        "severe"
    ])

    if scenario_type == "stable":

        cpu_degradation = random.uniform(2.0, 8.0)
        memory_degradation = random.uniform(2.0, 8.0)
        battery_drop = random.uniform(2.0, 10.0)
        temperature_increase = random.uniform(1.0, 5.0)

    elif scenario_type == "mild":

        cpu_degradation = random.uniform(8.0, 15.0)
        memory_degradation = random.uniform(8.0, 15.0)
        battery_drop = random.uniform(10.0, 20.0)
        temperature_increase = random.uniform(5.0, 12.0)

    elif scenario_type == "moderate":

        cpu_degradation = random.uniform(15.0, 25.0)
        memory_degradation = random.uniform(15.0, 25.0)
        battery_drop = random.uniform(20.0, 35.0)
        temperature_increase = random.uniform(12.0, 25.0)

    else:

        cpu_degradation = random.uniform(25.0, 35.0)
        memory_degradation = random.uniform(25.0, 35.0)
        battery_drop = random.uniform(35.0, 50.0)
        temperature_increase = random.uniform(25.0, 35.0)

    return {
        "scenario_type": scenario_type,
        "cpu_degradation": cpu_degradation,
        "memory_degradation": memory_degradation,
        "battery_drop": battery_drop,
        "temperature_increase": temperature_increase
    }


def generate_scenarios(number_of_scenarios):

    scenarios = []

    for _ in range(number_of_scenarios):

        scenario = generate_scenario()

        scenarios.append(scenario)

    return scenarios


if __name__ == "__main__":

    random.seed(42)

    print("Starting balanced scenario generator...")

    scenarios = generate_scenarios(20)

    print("\n==========================================")
    print("GENERATED SCENARIOS")
    print("==========================================")

    for index, scenario in enumerate(
        scenarios,
        start=1
    ):

        print(f"\nScenario {index}")
        print("Type:", scenario["scenario_type"])
        print(
            "CPU degradation:",
            f"{scenario['cpu_degradation']:.2f}%"
        )
        print(
            "Memory degradation:",
            f"{scenario['memory_degradation']:.2f}%"
        )
        print(
            "Battery drop:",
            f"{scenario['battery_drop']:.2f}%"
        )
        print(
            "Temperature increase:",
            f"{scenario['temperature_increase']:.2f} C"
        )

    print("\n==========================================")
    print("BALANCED SCENARIO GENERATION COMPLETED")
    print("==========================================")