from flask import Flask, request, jsonify
from scraper import scrape_profile  # Async function
from email_generator import generate_email  # Uses OpenAI
import asyncio
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ LinkedIn Scraper AI is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("📩 Incoming data:", data)

        linkedin_url = data.get("linkedin_url")
        if not linkedin_url:
            print("❌ No LinkedIn URL found.")
            return jsonify({"error": "Missing LinkedIn URL"}), 400

        print(f"🔗 Scraping LinkedIn URL: {linkedin_url}")
        profile = asyncio.run(scrape_profile(linkedin_url))
        print("✅ Scraped profile:", profile)

        email = generate_email(profile)
        print("✉️ Generated email:", email)

        return jsonify({"email": email})

    except Exception as e:
        print("🔥 ERROR during webhook processing:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
