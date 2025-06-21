import sqlite3
import json
from web3 import Web3

# === STEP 1: Connect to Ganache ===
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert w3.is_connected(), "❌ Ganache is not running"
account = w3.eth.accounts[0]

# === STEP 2: Load ABI and Contract Address ===
with open("abi.json") as f:
    abi = json.load(f)
with open("contract_address.txt") as f:
    contract_address = f.read().strip()

contract = w3.eth.contract(address=contract_address, abi=abi)

# === STEP 3: Connect to SQLite and Fetch Weights ===
conn = sqlite3.connect("journey_data.db")
cursor = conn.cursor()
cursor.execute("SELECT total_weight FROM driver_assignments")
rows = cursor.fetchall()
conn.close()

weights = [int(float(row[0])) for row in rows]
assert len(weights) >= 4, "❌ Need at least 4 weights (1 original + 3 checkpoints)"

# === STEP 4: Send Checkpoint Weights Immediately ===
print("\n🚚 Sending Checkpoint Weights:")
for i, weight in enumerate(weights[1:4]):
    print(f"📤 Submitting checkpoint {i+1}: {weight} kg")
    tx = contract.functions.submitCheckpointWeight(weight).transact({'from': account})
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"✅ Checkpoint {i+1} submitted")


# === STEP 5: Fetch and Print Events (compatible with web3.py v6+) ===
from web3._utils.events import get_event_data

print("\n📋 Blockchain Submission Results:")

event_abi = contract.events.WeightSubmitted._get_event_abi()
event_signature = "WeightSubmitted(uint8,uint256,bool)"
event_topic = "0x" + w3.keccak(text=event_signature).hex()  # ✅ fixed

logs = w3.eth.get_logs({
    "fromBlock": 0,
    "toBlock": "latest",
    "address": contract.address,
    "topics": [event_topic]
})

for log in logs:
    decoded_event = get_event_data(w3.codec, event_abi, log)
    args = decoded_event["args"]
    print(f"Checkpoint {args['checkpointNumber']}: {args['submittedWeight']} kg → {'✅ Match' if args['isMatching'] else '❌ Discrepancy'}")
