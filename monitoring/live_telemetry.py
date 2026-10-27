
def get_live_telemetry():
    """
    Collect resource information from the computer running AURA-Edge.
    Battery information may not be available on hosted servers.
    """
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent

    # Battery sensors may be unavailable on cloud servers.
    try:
        battery_info = psutil.sensors_battery()
        battery = battery_info.percent if battery_info is not None else None
    except (OSError, FileNotFoundError):
        battery = None

    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_percent": cpu,
        "memory_percent": memory,
        "battery_percent": battery,
    }
