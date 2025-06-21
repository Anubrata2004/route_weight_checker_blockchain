import sqlite3
from pymongo import MongoClient
from bson import ObjectId

# ✅ MongoDB setup
mongo_url = "mongodb+srv://debarghasamanta2004:DipenSamanta2000@disasterreleif.amshhkz.mongodb.net"
client = MongoClient(mongo_url)
db = client['distaterrelief']  # use correct spelling

driver_assignments_col = db['driverassignments']
predictaids_col = db['predictedaids']

# ✅ Find a driver with at least one assignment
driver_doc = driver_assignments_col.find_one({"assignments.0": {"$exists": True}})

if not driver_doc:
    print("❌ No driver assignment found.")
    exit()

# ✅ Try each assignment until one has a valid predictedAid in predictedaids
matched_assignment = None
matched_predicted_doc = None

for assignment in driver_doc.get('assignments', []):
    predicted_aid_id = assignment.get('predictedAid')
    predicted_doc = predictaids_col.find_one({"_id": predicted_aid_id})

    if predicted_doc:
        matched_assignment = assignment
        matched_predicted_doc = predicted_doc
        break  # ✅ Stop at the first valid match

# ✅ Check if a valid assignment-predictedAid pair was found
if not matched_assignment or not matched_predicted_doc:
    print("❌ No valid predictedAid match found in any assignment.")
    exit()

# ✅ Extract data
driver_id = str(driver_doc.get('driverId'))
source = matched_assignment.get('source')
destination = matched_assignment.get('destination')
predicted_aid_id = matched_assignment.get('predictedAid')
total_weight = matched_predicted_doc.get('total_weight', 0)

# ✅ Create SQLite DB
conn = sqlite3.connect("driver_data.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS driver_assignments (
        driverId TEXT,
        source TEXT,
        destination TEXT,
        predictedAid TEXT,
        total_weight REAL
    )
""")

cursor.execute("""
    INSERT INTO driver_assignments (
        driverId, source, destination, predictedAid, total_weight
    ) VALUES (?, ?, ?, ?, ?)
""", (
    driver_id,
    source,
    destination,
    str(predicted_aid_id),
    total_weight
))

conn.commit()
conn.close()

print("✅ Data inserted from first matching predictedAid.")

