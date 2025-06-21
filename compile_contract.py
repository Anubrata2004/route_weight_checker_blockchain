from solcx import compile_standard, install_solc
import json

# Install specific compiler version
install_solc("0.8.17")

with open("TruckWeightVerifier.sol", "r") as file:
    contract_code = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"TruckWeightVerifier.sol": {"content": contract_code}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "evm.bytecode"]}
        }
    }
}, solc_version="0.8.17")

contract_data = compiled_sol['contracts']['TruckWeightVerifier.sol']['TruckWeightVerifier']
abi = contract_data['abi']
bytecode = contract_data['evm']['bytecode']['object']

with open("abi.json", "w") as f:
    json.dump(abi, f)
with open("bytecode.txt", "w") as f:
    f.write(bytecode)

print("✅ Contract compiled. ABI and Bytecode saved.")
