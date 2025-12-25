from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/send": {"origins": "*"}})

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

@app.before_request
def log_request():
    print("INCOMING:", request.method, request.path)

@app.route("/")
def home():
    return "Backend is running"

@app.route("/send", methods=["POST", "OPTIONS"])
def send_email():
    data = request.form

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject")
    message = data.get("message")

    try:
        full_message = f"""Subject: {subject}

Name: {name}
Email: {email}

{message}
"""

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.sendmail(EMAIL, EMAIL, full_message)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
