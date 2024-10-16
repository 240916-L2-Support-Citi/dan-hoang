#!/usr/bin/env python3

import os
import psycopg

# Initialize variables.

POSTGRES_DBNAME = os.environ["POSTGRES_DBNAME"]
POSTGRES_USER = os.environ["POSTGRES_USER"]

ERROR_TOLERANCE = 5
FATAL_TOLERANCE = 1

with open("alert_system_last_time.txt", "r") as f:
    error_count = int(f.readline().strip())
    fatal_count = int(f.readline().strip())
    last_time = f.readline().strip()

# Process new log entries.

with psycopg.connect(f"dbname={POSTGRES_DBNAME} user={POSTGRES_USER}") as conn:
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM log_entry" + ("" if not last_time else f" WHERE log_entry_timestamp > '{last_time}'"))

        for record in cur:
            last_time = record[1].isoformat(sep=" ", timespec="seconds")
            level = record[2]

            match level:
                case "ERROR":
                    error_count += 1

                    if error_count == ERROR_TOLERANCE:
                        os.system('notify-send "Errors are piling up, go check your logs"')
                        error_count = 0

                case "FATAL":
                    fatal_count += 1

                    if fatal_count == FATAL_TOLERANCE:
                        os.system('notify-send "Something really bad happened, go check your logs"')
                        fatal_count = 0

# Save variables.

with open("alert_system_last_time.txt", "w") as f:
    f.write(f"{error_count}\n")
    f.write(f"{fatal_count}\n")
    f.write(last_time)
