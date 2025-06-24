from flask import Flask, request, jsonify
import asyncio
from scraper import scrape_profile
from email_generator import generate_email

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return jsonify({"message": "✅ LinkedIn Scraper API is live!"})

# Test endpoint to verify the webhook is reachable via GET
@app.route('/webhook', methods=['GET'])
def test_webhook():
    return jsonify({"message": "🧪 Webhook GET is working!"})

# Main endpoint: receives LinkedIn URL and returns email
@app.route('/webhook', methods=['POST'])
def webhook():
    print("📥 POST /webhook hit")
    print("Headers:", request.headers)
    print("Raw data:", request.data)

    try:
        data = request.get_json(force=True)
        print("✅ Parsed JSON:", data)

        linkedin_url = data.get("linkedin_url")
        if not linkedin_url:
            print("❌ No LinkedIn URL in payload")
            return jsonify({"error": "Missing LinkedIn URL"}), 400

        print(f"🔗 Scraping LinkedIn URL: {linkedin_url}")
        profile = asyncio.run(scrape_profile(linkedin_url))
        print("✅ Scraped profile:", profile)

        email = generate_email(profile)
        print("✉️ Generated email:", email)

        return jsonify({"email": email})

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Flask App Starting...")

    try:
        from scraper import scrape_profile
        print("✅ scraper.py imported")
    except Exception as e:
        print("❌ scraper.py import failed:", e)

    try:
        from email_generator import generate_email
        print("✅ email_generator.py imported")
    except Exception as e:
        print("❌ email_generator.py import failed:", e)

    app.run(debug=True, host='0.0.0.0', port=10000)
