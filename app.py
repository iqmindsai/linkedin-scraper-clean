from flask import Flask, request, jsonify
import asyncio
from scraper import scrape_profile
from email_generator import generate_email
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    linkedin_url = data.get("linkedin_url")
    if not linkedin_url:
        return jsonify({"error": "Missing LinkedIn URL"}), 400

    profile = asyncio.run(scrape_profile(linkedin_url))
    email = generate_email(profile)

    return jsonify({
        "linkedin_url": linkedin_url,
        "name": profile.get("name"),
        "headline": profile.get("headline"),
        "summary": profile.get("summary"),
        "email": email
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
