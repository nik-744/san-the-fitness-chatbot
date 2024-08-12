from flask import Flask, request, jsonify, render_template
from bot import FitnessAgent, ChatBot
import os
import markdown 
 
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    user_input = request.json.get('msg')
    try:
        if any(keyword in user_input.lower() for keyword in ["diet plan", "muscle gain", "weight loss", "bmi", "tdee", "ibw"]):
            # Extract relevant details from the user's input
            # Note: You may want to further parse user_input to extract specific details
            height = 170  # Example values, you should parse these from the user's input
            weight = 70
            age = 25
            gender = "male"
            activity_level = "3"  # Moderately active

            bmi = fitness_agent.calculate_bmi(weight, height)
            bmr = fitness_agent.calculate_bmr(weight, height, age, gender)
            tdee = fitness_agent.calculate_tdee(bmr, activity_level)

            fitness_response = f"BMI: {bmi}, BMR: {bmr}, TDEE: {tdee}"
            return jsonify({'message': fitness_response})

        response = chatbot.send_prompt(user_input)

        # concerting markdown to html for rendering
        response_html = markdown.markdown(response)
        return jsonify({'message': response_html})
    except Exception as e:
        return jsonify({'error': str(e)})

chatbot = ChatBot(api_key=os.environ["GEMINI_AI"])
chatbot.start_conversation()
fitness_agent = FitnessAgent(openai_api_key=os.environ["GEMINI_AI"], nut_api_key=os.environ["NUT_API_KEY"])


if __name__ == "__main__":
    app.run(debug=True)
