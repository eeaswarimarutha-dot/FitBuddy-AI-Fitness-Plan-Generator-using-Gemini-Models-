async function generatePlan() {

    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const goal = document.getElementById("goal").value;
    const fitnessLevel = document.getElementById("fitness_level").value;

    // Check whether all fields are filled
    if (!age || !gender || !height || !weight || !goal || !fitnessLevel) {
        alert("⚠️ Please fill in all the fields.");
        return;
    }

    // Show loading message
    document.getElementById("loading").style.display = "block";

    const result = document.getElementById("result");
    result.style.display = "none";
    result.innerHTML = "";

    try {

        const response = await fetch("/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                age: age,
                gender: gender,
                height: height,
                weight: weight,
                goal: goal,
                fitness_level: fitnessLevel

            })

        });

        const data = await response.json();

        if (data.success) {

            result.style.display = "block";

            // Convert Gemini Markdown into simple HTML
            let plan = data.plan;

            plan = plan
                .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                .replace(/^### (.*)$/gm, "<h3>$1</h3>")
                .replace(/^## (.*)$/gm, "<h2>$1</h2>")
                .replace(/^# (.*)$/gm, "<h1>$1</h1>")
                .replace(/\n/g, "<br>");

            result.innerHTML = plan;

        } else {

            result.style.display = "block";

            result.innerHTML =
                "<strong>❌ Error:</strong> " + data.error;
        }

    } catch (error) {

        result.style.display = "block";

        result.innerHTML =
            "<strong>❌ Error:</strong> Unable to connect to the server.";

        console.error(error);
    }

    // Hide loading message
    document.getElementById("loading").style.display = "none";
}