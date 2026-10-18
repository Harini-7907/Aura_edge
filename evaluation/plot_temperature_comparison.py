import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    PROJECT_ROOT
    / "results"
    / "final_comparison.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "results"
    / "aura_vs_reactive_temperature.png"
)


# ---------------------------------------------------------
# Load results
# ---------------------------------------------------------

df = pd.read_csv(RESULTS_FILE)


# ---------------------------------------------------------
# Get temperature values
# ---------------------------------------------------------

aura_temperature = float(
    df.loc[
        df["Metric"] == "Average Temperature at Migration (C)",
        "AURA-Edge"
    ].iloc[0]
)

reactive_temperature = float(
    df.loc[
        df["Metric"] == "Average Temperature at Migration (C)",
        "Reactive"
    ].iloc[0]
)


# ---------------------------------------------------------
# Graph data
# ---------------------------------------------------------

strategies = [
    "AURA-Edge",
    "Reactive"
]

temperature_values = [
    aura_temperature,
    reactive_temperature
]


# ---------------------------------------------------------
# Create graph
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

bars = plt.bar(
    strategies,
    temperature_values
)

plt.ylabel(
    "Average Temperature at Migration (°C)"
)

plt.xlabel(
    "Scheduling Strategy"
)

plt.title(
    "AURA-Edge vs Reactive: Temperature at Migration"
)

plt.ylim(
    0,
    60
)


# ---------------------------------------------------------
# Add values
# ---------------------------------------------------------

for bar, value in zip(
    bars,
    temperature_values
):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        value + 1,
        f"{value:.2f}°C",
        ha="center"
    )


# ---------------------------------------------------------
# Save graph
# ---------------------------------------------------------

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ---------------------------------------------------------
# Confirmation
# ---------------------------------------------------------

print("=" * 50)
print("TEMPERATURE COMPARISON GRAPH CREATED")
print("=" * 50)

print(
    f"AURA-Edge Temperature: {aura_temperature:.2f} C"
)

print(
    f"Reactive Temperature: {reactive_temperature:.2f} C"
)

print(
    f"Graph saved to: {OUTPUT_FILE}"
)