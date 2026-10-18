import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "mecperf_network_conditions.csv"
)


def load_mecperf_data():
    """Load processed MECPerf network measurements."""
    return pd.read_csv(DATA_FILE)


def get_network_profile(row_index=0):
    """
    Get one real network condition from MECPerf.

    RTT measurements provide latency.
    Bandwidth measurements provide bandwidth.
    """

    df = load_mecperf_data()

    rtt = df[
        df["command"].isin(["TCPRTT", "UDPRTT"])
    ][["test_id", "timestamp", "direction", "command", "latency_ms"]].dropna(
        subset=["latency_ms"]
    )

    bandwidth = df[
        df["command"].isin(["TCPBandwidth", "UDPBandwidth"])
    ][["test_id", "timestamp", "direction", "command", "bandwidth_mbps"]].dropna(
        subset=["bandwidth_mbps"]
    )

    if rtt.empty:
        latency_ms = 0.0
        rtt_info = {}
    else:
        row = rtt.iloc[row_index % len(rtt)]

        latency_ms = float(row["latency_ms"])

        rtt_info = {
            "rtt_test_id": int(row["test_id"]),
            "rtt_timestamp": row["timestamp"],
            "rtt_direction": row["direction"],
            "rtt_command": row["command"],
        }

    if bandwidth.empty:
        bandwidth_mbps = 0.0
        bandwidth_info = {}
    else:
        row = bandwidth.iloc[row_index % len(bandwidth)]

        bandwidth_mbps = float(row["bandwidth_mbps"])

        bandwidth_info = {
            "bandwidth_test_id": int(row["test_id"]),
            "bandwidth_timestamp": row["timestamp"],
            "bandwidth_direction": row["direction"],
            "bandwidth_command": row["command"],
        }

    return {
        "latency_ms": latency_ms,
        "bandwidth_mbps": bandwidth_mbps,
        **rtt_info,
        **bandwidth_info,
    }


if __name__ == "__main__":
    print("MECPerf Network Conditions")
    print("==========================")

    for index in range(5):
        profile = get_network_profile(index)

        print()
        print(f"Condition {index + 1}")
        print(f"Latency: {profile['latency_ms']:.2f} ms")
        print(f"Bandwidth: {profile['bandwidth_mbps']:.4f} Mbps")
        print(f"RTT test ID: {profile.get('rtt_test_id')}")
        print(f"Bandwidth test ID: {profile.get('bandwidth_test_id')}")