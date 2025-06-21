from web3 import Web3
import json

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
assert w3.is_connected(), "❌ Ganache not connected"

account = w3.eth.accounts[0]

# Load ABI and Bytecode
with open("abi.json", "r") as f:
    abi = json.load(f)
with open("bytecode.txt", "r") as f:
    bytecode = f.read().strip()

# Deploy Contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor(10687).transact({'from': account})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ Contract deployed at: {tx_receipt.contractAddress}")

# Save address for next script
with open("contract_address.txt", "w") as f:
    f.write(tx_receipt.contractAddress)
