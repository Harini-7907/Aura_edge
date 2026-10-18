import bz2

path = r".\data\raw\mecperf_active_measurements_db_dump_20200417.sql.bz2"

targets = [
    "CREATE TABLE `Test`",
    "CREATE TABLE `RttMeasure`",
    "CREATE TABLE `BandwidthMeasure`",
]

with bz2.open(path, "rt", encoding="utf-8", errors="replace") as f:
    active = False
    remaining = 0

    for line in f:
        if any(target in line for target in targets):
            print("\n" + "=" * 60)
            print(line, end="")
            active = True
            remaining = 30
            continue

        if active:
            print(line, end="")
            remaining -= 1

            if line.strip().startswith(")"):
                active = False
                print("=" * 60)

            elif remaining <= 0:
                active = False