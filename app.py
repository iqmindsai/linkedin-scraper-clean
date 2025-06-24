from flask import Flask, request, jsonify
import asyncio
import os

# Debug: show startup
print("🚀 Flask App Starting...")

try:
    from scraper import scrape_profile
    print("✅ scraper.py imported")
except Exception as e:
    print("❌ Failed to import scraper.py:", e)

try:
    from email_generator import generate_email
    print("✅ email_generator.py imported")
except Exception as e:
    print("❌ Failed to import email_generator.py:", e)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ LinkedIn Scraper AI is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    print("📥 /webhook endpoint hit")

    try:
        print("🔍 Raw request data:", request.data)
        data = request.get_json(force=True, silent=True)
        print("📩 Parsed JSON:", data)

        linkedin_url = data.get("linkedin_url") if data else None
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
