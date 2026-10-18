import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "network_adaptation_results.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "network_adaptation_decisions.png"
)


# ==========================================
# LOAD RESULTS
# ==========================================

df = pd.read_csv(INPUT_FILE)


# ==========================================
# PREPARE DECISION VALUES
# ==========================================

decision_map = {
    "Local": 0,
    "Edge-ENACT-rpi4": 1,
    "Cloud": 2
}

df["decision_value"] = (
    df["selected_resource"]
    .map(decision_map)
)


# ==========================================
# CREATE GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    df["condition"],
    df["decision_value"],
    marker="o",
    linewidth=2
)


# ==========================================
# LABELS
# ==========================================

plt.yticks(
    [0, 1, 2],
    [
        "Local",
        "Edge-ENACT-rpi4",
        "Cloud"
    ]
)

plt.xlabel(
    "MECPerf Network Condition"
)

plt.ylabel(
    "Selected Execution Resource"
)

plt.title(
    "AURA-Edge Adaptive Resource Selection"
)

plt.xticks(
    df["condition"]
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()


# ==========================================
# SAVE GRAPH
# ==========================================

plt.savefig(
    OUTPUT_FILE,
    dpi=300
)

plt.close()


print()
print(
    "NETWORK ADAPTATION GRAPH CREATED"
)

print(
    f"Saved to:"
)

print(
    OUTPUT_FILE
)