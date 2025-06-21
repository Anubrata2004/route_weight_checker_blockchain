import sqlite3
import os

DB_NAME = "journey_data.db"

# ✅ Check if database exists
if not os.path.exists(DB_NAME):
    print(f" Database file '{DB_NAME}' not found.")
    exit()

# ✅ Connect to the journey database
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM driver_assignments")
    rows = cursor.fetchall()

    if not rows:
        print(" No journey records found in 'driver_assignments' table.")
    else:
        print("\n Truck Journey Records:\n" + "-" * 70)

        for i, row in enumerate(rows, start=1):
            print(f" Checkpoint {i}")
            print(f"🔹 Driver ID     : {row[0]}")
            print(f"🔹 Source        : {row[1]}")
            print(f"🔹 Destination   : {row[2]}")
            print(f"🔹 PredictedAid  : {row[3]}")
            print(f"🔹 Total Weight  : {row[4]} kg")
            print("-" * 70)

except sqlite3.Error as e:
    print(f" SQLite error: {e}")
finally:
    conn.close()