import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_email(profile):
    prompt = f"""Write a short, personalized cold email to {profile['name']} who is a {profile['headline']}.
    Their LinkedIn summary is: {profile['summary']}.
    Keep the email under 100 words, professional, and relevant to their role."""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']
