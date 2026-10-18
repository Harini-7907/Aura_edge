import json
from pathlib import Path
import random

from scenario_generator import generate_scenarios


OUTPUT_FILE = (
    Path(__file__).resolve().parent.parent
    / "results"
    / "scenarios.json"
)


def save_scenarios(number_of_scenarios=20):

    random.seed(42)

    scenarios = generate_scenarios(number_of_scenarios)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            scenarios,
            file,
            indent=4
        )

    print("==========================================")
    print("SCENARIOS SAVED")
    print("==========================================")

    print("Number of scenarios:", number_of_scenarios)
    print("File:", OUTPUT_FILE)


if __name__ == "__main__":
    save_scenarios(20)