from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

def get_response_from_groq(user_input):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": user_input}],
        model="mixtral-8x7b-32768"
    )
    return response.choices[0].message.content
