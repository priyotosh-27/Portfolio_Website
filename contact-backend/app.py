from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

@app.route("/")
def home():
    return "Backend is running"

@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.form

        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = data.get("subject")

        body = f"""
Name: {data.get('name')}
Email: {data.get('email')}

Message:
{data.get('message')}
"""
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
