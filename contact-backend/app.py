from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import smtplib, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

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

    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response, 200

    try:
        data = request.form

        full_message = f"""Subject: {data.get('subject')}

Name: {data.get('name')}
Email: {data.get('email')}

{data.get('message')}
"""

        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.sendmail(EMAIL, EMAIL, full_message)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
