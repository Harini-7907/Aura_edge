import bz2
import csv
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "mecperf_active_measurements_db_dump_20200417.sql.bz2"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mecperf_network_conditions.csv"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

test_data = {}
rtt_data = {}
bandwidth_data = {}


def parse_values(text):
    """Extract tuples from an SQL INSERT VALUES section."""
    return re.findall(r"\(([^()]*)\)", text)


def split_sql_values(row):
    """Split one SQL tuple while respecting quoted strings."""
    values = []
    current = ""
    in_quotes = False

    for char in row:
        if char == "'":
            in_quotes = not in_quotes
        elif char == "," and not in_quotes:
            values.append(current.strip())
            current = ""
        else:
            current += char

    values.append(current.strip())
    return values


print("Reading MECPerf active dump...")
print("This may take a little while.")

with bz2.open(
    INPUT_FILE,
    "rt",
    encoding="utf-8",
    errors="replace"
) as file:

    for line in file:

        # -----------------------------
        # Test table
        # -----------------------------
        if line.startswith("INSERT INTO `Test` VALUES"):
            section = line.split("VALUES", 1)[1]

            for row in parse_values(section):
                values = split_sql_values(row)

                if len(values) >= 12:
                    test_id = int(values[1])

                    test_data[test_id] = {
                        "timestamp": values[2].strip("'"),
                        "direction": values[3].strip("'"),
                        "command": values[4].strip("'"),
                        "sender": values[5].strip("'"),
                        "receiver": values[6].strip("'"),
                        "keyword": values[9].strip("'"),
                    }

        # -----------------------------
        # RTT table
        # -----------------------------
        elif line.startswith("INSERT INTO `RttMeasure` VALUES"):
            section = line.split("VALUES", 1)[1]

            for row in parse_values(section):
                values = split_sql_values(row)

                if len(values) >= 3:
                    test_id = int(values[0])

                    try:
                        latency = float(values[1])
                    except ValueError:
                        continue

                    rtt_data.setdefault(test_id, []).append(latency)

        # -----------------------------
        # Bandwidth table
        # -----------------------------
        elif line.startswith("INSERT INTO `BandwidthMeasure` VALUES"):
            section = line.split("VALUES", 1)[1]

            for row in parse_values(section):
                values = split_sql_values(row)

                if len(values) >= 4:
                    test_id = int(values[0])

                    try:
                        nano_times = float(values[2])
                        kbytes = float(values[3])
                    except ValueError:
                        continue

                    if nano_times > 0:
                        # kBytes / nanoseconds → Mbps
                        bandwidth_mbps = (
                            kbytes / nano_times
                        ) * 8000.0

                        bandwidth_data.setdefault(
                            test_id, []
                        ).append(bandwidth_mbps)


print("Combining measurements...")

rows = []

for test_id, test in test_data.items():

    # RTT measurements
    if test_id in rtt_data:

        latency_values = rtt_data[test_id]

        if latency_values:
            latency_ms = sum(latency_values) / len(latency_values)

            rows.append({
                "test_id": test_id,
                "timestamp": test["timestamp"],
                "direction": test["direction"],
                "command": test["command"],
                "sender": test["sender"],
                "receiver": test["receiver"],
                "keyword": test["keyword"],
                "latency_ms": latency_ms,
                "bandwidth_mbps": "",
            })

    # Bandwidth measurements
    if test_id in bandwidth_data:

        bandwidth_values = bandwidth_data[test_id]

        if bandwidth_values:
            bandwidth_mbps = (
                sum(bandwidth_values)
                / len(bandwidth_values)
            )

            rows.append({
                "test_id": test_id,
                "timestamp": test["timestamp"],
                "direction": test["direction"],
                "command": test["command"],
                "sender": test["sender"],
                "receiver": test["receiver"],
                "keyword": test["keyword"],
                "latency_ms": "",
                "bandwidth_mbps": bandwidth_mbps,
            })


with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "test_id",
            "timestamp",
            "direction",
            "command",
            "sender",
            "receiver",
            "keyword",
            "latency_ms",
            "bandwidth_mbps",
        ],
    )

    writer.writeheader()
    writer.writerows(rows)


print()
print("MECPerf preprocessing completed.")
print(f"Test records: {len(test_data)}")
print(f"RTT test IDs: {len(rtt_data)}")
print(f"Bandwidth test IDs: {len(bandwidth_data)}")
priDONEnt(f"Processed rows: {len(rows)}")
print(f"Output: {OUTPUT_FILE}")