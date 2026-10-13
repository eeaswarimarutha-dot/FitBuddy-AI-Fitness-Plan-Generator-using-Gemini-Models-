from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_plan():
    print("Generate button clicked!")

    data = request.json

    age = data.get("age")
    gender = data.get("gender")
    height = data.get("height")
    weight = data.get("weight")
    goal = data.get("goal")
    fitness_level = data.get("fitness_level")
    bmi = data.get("bmi")
    bmi_category = data.get("bmi_category")

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe and simple personalized fitness plan.

User Details:

Age: {age}
Gender: {gender}
Height: {height} cm
Weight: {weight} kg
BMI: {bmi}
BMI Category: {bmi_category}
Fitness Goal: {goal}
Fitness Level: {fitness_level}

Give the response in this format:

## Fitness Summary

Explain the user's current fitness situation briefly.

## 7-Day Workout Plan

Give a simple workout plan for Day 1 to Day 7.

## Daily Diet Suggestions

Give healthy and practical food suggestions.

## Water Intake Tips

Give simple hydration suggestions.

## Healthy Lifestyle Tips

Give sleep, activity and lifestyle suggestions.

## Important Safety Note

Mention that this is general fitness guidance and that the user should consult a qualified healthcare professional when necessary.

Rules:
- Keep the plan beginner-friendly and practical.
- Do not recommend extreme diets.
- Do not recommend dangerous exercises.
- Do not give medical diagnosis.
- Keep the language simple and easy to understand.
"""


    try:

        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=prompt
        )

        return jsonify({
            "success": True,
            "plan": interaction.output_text
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)