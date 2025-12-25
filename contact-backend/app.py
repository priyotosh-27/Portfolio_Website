from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import smtplib, os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

# Debug check (safe — does not expose password)
print("EMAIL ENV:", EMAIL)
print("PASS ENV:", "SET" if PASSWORD else "NOT SET")

@app.before_request
def log_request():
    print("INCOMING:", request.method, request.path)

@app.route("/")
def home():
    return "Backend is running"

@app.route("/send", methods=["POST", "OPTIONS"])
def send_email():

    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response, 200

    try:
        data = request.form

        if not EMAIL or not PASSWORD:
            raise Exception("Email credentials are not configured in environment variables")

        msg = EmailMessage()
        msg["From"] = EMAIL
        msg["To"] = EMAIL
        msg["Subject"] = data.get("subject", "New Contact Form Message")

        body = f"""
Name: {data.get('name')}
Email: {data.get('email')}

Message:
{data.get('message')}
"""
        msg.set_content(body)

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print("EMAIL SENT SUCCESSFULLY")
        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
