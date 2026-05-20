import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv('C:/Desktop/Gymai/Fitness_Tracker_V4/.env')
key = os.environ.get('GEMINI_API_KEY')
print(f'Key loaded: {bool(key)}')
genai.configure(api_key=key)

try:
    model = genai.GenerativeModel('gemini-1.5-pro')
    generation_config = genai.GenerationConfig(response_mime_type='application/json')
    response = model.generate_content('Reply with JSON {"test": "success"}', generation_config=generation_config)
    print("Success:", response.text)
except Exception as e:
    print(f'Error: {str(e)}')
