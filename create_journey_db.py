import sqlite3
import os
import shutil

# Source database
source_db = "driver_data.db"
target_db = "journey_data.db"

# Copy the original DB to a new one
if os.path.exists(target_db):
    os.remove(target_db)  # remove old one if re-running
shutil.copy(source_db, target_db)

# Connect to new journey database
conn = sqlite3.connect(target_db)
cursor = conn.cursor()

# Fetch original row from driver_data
cursor.execute("SELECT * FROM driver_assignments LIMIT 1")
original = cursor.fetchone()

if not original:
    print("❌ No original data found in driver_data.db.")
    exit()

print("✅ Original data loaded.")

# Prepare 3 more entries
entries = [
    original,         # ✅ Original
    original,         # ✅ Same as original (simulated checkpoint 1)
    original,         # ✅ Same as original (simulated checkpoint 2)
    (
        original[0],  # driverId
        original[1],  # source
        original[2],  # destination
        original[3],  # predictedAid
        original[4] - 900.0  # ❌ Tampered weight (900 kg lost)
    )
]

# Insert into journey table (same table as before)
cursor.execute("DELETE FROM driver_assignments")  # clear table
cursor.executemany("""
    INSERT INTO driver_assignments (
        driverId, source, destination, predictedAid, total_weight
    ) VALUES (?, ?, ?, ?, ?)
""", entries)

conn.commit()
conn.close()

print("✅ journey_data.db populated with 4 entries (3 valid + 1 tampered).")
