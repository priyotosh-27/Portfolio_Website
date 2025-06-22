from flask import Flask, request, jsonify
from flask_cors import CORS 
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app) 

EMAIL = os.getenv("EMAIL_USER")
PASSWORD = os.getenv("EMAIL_PASS")

@app.route('/send', methods=['POST'])
def send_email():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    try:
        full_message = f"Subject: {subject}\n\nName: {name}\nEmail: {email}\n\n{message}"
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL, PASSWORD)
            smtp.sendmail(EMAIL, EMAIL, full_message)

        return jsonify({'status': 'success', 'message': 'Email sent!'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
