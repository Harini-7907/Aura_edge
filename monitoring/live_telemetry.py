import psutil
import time


def get_live_telemetry():
    """
    Collect real-time resource information
    from the computer running AURA-Edge.
    """

    cpu = psutil.cpu_percent(interval=1)

    memory = psutil.virtual_memory().percent

    battery_info = psutil.sensors_battery()

    if battery_info is not None:
        battery = battery_info.percent
    else:
        battery = None

    telemetry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": cpu,
        "memory_percent": memory,
        "battery_percent": battery,
    }

    return telemetry


if __name__ == "__main__":

    data = get_live_telemetry()

    print("\n===== AURA-Edge LIVE TELEMETRY =====")
    print(f"Time     : {data['timestamp']}")
    print(f"CPU      : {data['cpu_percent']:.2f}%")
    print(f"Memory   : {data['memory_percent']:.2f}%")

    if data["battery_percent"] is not None:
        print(f"Battery  : {data['battery_percent']:.2f}%")
    else:
        print("Battery  : Not available")