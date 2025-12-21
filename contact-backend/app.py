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
    # Accept JSON or form-encoded bodies
    data = request.get_json(silent=True) or request.form or request.values
    name = data.get('name') if data else None
    email = data.get('email') if data else None
    subject = data.get('subject') if data else None
    message = data.get('message') if data else None

    # Basic validation
    if not EMAIL or not PASSWORD:
        return jsonify({'status': 'error', 'message': 'Server email credentials are not configured.'}), 500

    if not subject:
        subject = 'No subject'

    try:
        from email.message import EmailMessage

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = EMAIL
        # Send to the site owner; you can change this to send to the visitor's email if desired
        msg['To'] = EMAIL
        body = f"Name: {name}\nEmail: {email}\n\n{message or ''}"
        msg.set_content(body)

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        return jsonify({'status': 'success', 'message': 'Email sent!'}), 200
    except Exception as e:
        # Log the traceback to server logs for debugging
        app.logger.exception('Failed to send email')
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  
    app.run(host='0.0.0.0', port=port, debug=True)

