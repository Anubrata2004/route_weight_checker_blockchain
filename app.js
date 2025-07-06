document.getElementById("connectBtn").addEventListener("click", async () => {
    const outputBox = document.getElementById("logOutput");
    const addressBox = document.getElementById("contractAddress");

    addressBox.textContent = "🔄 Starting process...";
    outputBox.textContent = "";

    try {
        const response = await fetch("http://127.0.0.1:5000/run_all");
        const data = await response.json();

        if (data.status === "success") {
            addressBox.textContent = "✅ Contract deployed at: " + data.contract_address;

            data.steps.forEach((step, index) => {
                outputBox.textContent += `\n[${index + 1}] ✅ ${step.stage}\n`;
                if (step.output) outputBox.textContent += step.output + "\n";
            });

        } else {
            addressBox.textContent = "❌ Process failed.";
            data.steps.forEach((step, index) => {
                outputBox.textContent += `\n[${index + 1}] ❌ ${step.stage}\n`;
                if (step.error) outputBox.textContent += step.error + "\n";
                if (step.output) outputBox.textContent += step.output + "\n";
            });
        }

    } catch (error) {
        addressBox.textContent = "❌ Could not connect to backend.";
        outputBox.textContent = error.toString();
    }
});




