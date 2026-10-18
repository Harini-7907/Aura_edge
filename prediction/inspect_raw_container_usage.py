from pathlib import Path

INPUT_FILE = Path(
    "data/raw/alibaba_clusterdata_v2018/container_usage.csv"
)

print("Reading raw Alibaba container usage data...")

with open(INPUT_FILE, "r", encoding="utf-8") as f:

    for i in range(10):

        line = f.readline().strip()

        print(f"\nRAW ROW {i + 1}:")
        print(line)