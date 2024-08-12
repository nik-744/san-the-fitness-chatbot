import google.generativeai as genai
import os
import requests

# Configure the API with the provided API key
genai.configure(api_key=os.environ["GEMINI_AI"])

# Define generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Define safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_ONLY_HIGH",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH",
    },
]

# Initialize the model with the correct name and configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="Hello! I am SAN,your personalized fitness assistant that offers tailored guidance and expert insights to help individuals achieve their health and fitness goals."
)

# Custom exception for GenAI errors
class GeniAIException(Exception):
    pass

# ChatBot class
class ChatBot:
    CHATBOT_NAME = 'SAN'

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = model  # Use the globally initialized model
        self.conversation = None
        self._conversation_history = []

    def send_prompt(self, prompt, temperature=0.1):
        if temperature < 0 or temperature > 1:
            raise GeniAIException('Temperature can be between 0 and 1')
        if not prompt:
            raise GeniAIException('Prompt cannot be empty')

        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature),
            )
            response.resolve()
            return response.text
        except Exception as e:
            raise GeniAIException(str(e))

    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)

    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }

    def preload_conversation(self, conversation_history):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._construct_message(
                    'From now on, return the output as JSON object that can be loaded in Python with the key as \'text\'. For example, {"text": "<output goes here"}'),
                self._construct_message(
                    '{"text": "Sure, I can return the output as a regular JSON object with the key as `text`. Here is the example: {"text": "Your Output"}.',
                    'model')
            ]
    def format_response(self, response_text):
        """
        Format the response text into a structured format.
        """
        formatted_response = {
            "response": response_text,
            # Add more structured fields if needed
        }
        return formatted_response

class FitnessAgent:
    def __init__(self, openai_api_key: str, nut_api_key: str):
        self.openai_api_key = openai_api_key
        self.nut_api_key = nut_api_key

    def get_nutritional_info(self, query: str) -> dict:
        """Fetch the nutritional information for a specific food item."""
        api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
        response = requests.get(api_url, timeout=100, headers={'X-Api-Key': self.nut_api_key})

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            return {"Error": response.status_code, "Message": response.text}

    def calculate_bmi(self, weight: float, height: float) -> float:
        """Calculate the Body Mass Index (BMI) for a person."""
        height_meters = height / 100
        bmi = weight / (height_meters ** 2)
        return round(bmi, 2)

    def calculate_calories_to_lose_weight(self, desired_weight_loss_kg: float) -> float:
        """Calculate the number of calories required to lose a certain amount of weight."""
        calories_per_kg_fat = 7700
        return desired_weight_loss_kg * calories_per_kg_fat

    def calculate_bmr(self, weight: float, height: float, age: int, gender: str,
                      equation: str = 'mifflin_st_jeor') -> float:
        """Calculate the Basal Metabolic Rate (BMR) for a person."""
        if equation.lower() == 'mifflin_st_jeor':
            if gender.lower() == 'male':
                return (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                return (10 * weight) + (6.25 * height) - (5 * age) - 161
        else:
            if gender.lower() == 'male':
                return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    def calculate_tdee(self, bmr: float, activity_level: str) -> float:
        """Calculate the Total Daily Energy Expenditure (TDEE) for a person."""
        activity_factors = {
            '1': 1.2,    # Sedentary
            '2': 1.375,  # Lightly active
            '3': 1.55,   # Moderately active
            '4': 1.725,  # Very active
            '5': 1.9,    # Super active
        }
        return bmr * activity_factors.get(activity_level, 1)

    def calculate_ibw(self, height: float, gender: str) -> float:
        """Calculate the Ideal Body Weight (IBW)."""
        if gender.lower() == 'male':
            if height <= 60:
                return 50
            else:
                return 50 + 2.3 * (height - 60)
        elif gender.lower() == 'female':
            if height <= 60:
                return 45.5
            else:
                return 45.5 + 2.3 * (height - 60)
        else:
            raise ValueError("Invalid gender. Expected 'male' or 'female'.")

# Create an instance of ChatBot and FitnessAgent

