from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

def run_script(script_name, description):
    if not os.path.exists(script_name):
        return {
            "success": False,
            "error": f" Required file '{script_name}' not found during {description} step.",
            "stage": description
        }

    try:
        result = subprocess.run(
            ['python', script_name],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "success": True,
            "output": result.stdout,
            "stage": description
        }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f" Error during {description} step:\n{e.stderr.strip()}",
            "output": e.stdout,
            "stage": description
        }


@app.route('/run_all', methods=['GET'])
def run_all_steps():
    logs = []

    # Step 1: Compile contract
    step = run_script('compile_contract.py', 'contract compilation')
    logs.append(step)
    if not step["success"]:
        return jsonify({"status": "error", "steps": logs})

    # Step 2: Deploy contract
    step = run_script('deploy_contract.py', 'contract deployment')
    logs.append(step)
    if not step["success"]:
        return jsonify({"status": "error", "steps": logs})

    # Step 3: Read contract address
    try:
        with open("contract_address.txt", "r") as f:
            address = f.read().strip()
    except FileNotFoundError:
        logs.append({
            "success": False,
            "error": " Could not find 'contract_address.txt' after deployment.",
            "stage": "read contract address"
        })
        return jsonify({"status": "error", "steps": logs})

    # Step 4: Send weight data to contract
    step = run_script('send_weights_from_db.py', 'send weights from DB to blockchain')
    logs.append(step)
    if not step["success"]:
        return jsonify({"status": "error", "contract_address": address, "steps": logs})

    return jsonify({
        "status": "success",
        "contract_address": address,
        "steps": logs
    })


if __name__ == '__main__':
    app.run(debug=True)


