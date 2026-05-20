import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
print('Key loaded:', api_key[:10] if api_key else 'None')
genai.configure(api_key=api_key)
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content('Say hi')
    print('Response:', response.text)
except Exception as e:
    print('Error:', str(e))
