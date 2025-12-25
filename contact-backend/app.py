from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import resend

load_dotenv()

app = Flask(__name__)
CORS(app)

resend.api_key = os.getenv("RESEND_API_KEY")

@app.route("/")
def home():
    return "Backend is running"

@app.route("/send", methods=["POST"])
def send_email():
    try:
        data = request.form

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        html_content = f"""
        <h2>New Contact Message</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Subject:</strong> {subject}</p>
        <p><strong>Message:</strong><br>{message}</p>
        """

        resend.Emails.send({
            "from": "Contact Form <onboarding@resend.dev>",
            "to": ["priyotoshroy269@gmail.com"],
            "subject": subject,
            "html": html_content
        })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
