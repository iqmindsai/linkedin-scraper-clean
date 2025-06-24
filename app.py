from flask import Flask, request, jsonify
from scraper import scrape_profile  # Async function using Playwright
from email_generator import generate_email  # Function that takes profile dict and returns personalized email
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return "LinkedIn Scraper AI is running 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received request:", data)

    linkedin_url = data.get("linkedin_url")
    if not linkedin_url:
        return jsonify({"error": "Missing LinkedIn URL"}), 400

    try:
        profile = asyncio.run(scrape_profile(linkedin_url))
        print("Scraped profile:", profile)

        email = generate_email(profile)
        print("Generated email:", email)

        return jsonify({"email": email})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
