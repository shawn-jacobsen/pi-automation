from flask import Flask, request
import json

from pyNotifications import (
  sendEmail
)

# read in email json data
with open('email_secret.json') as f:
    EMAIL_DATA = json.load(f)

# Notification data for sending text message
PORT = 587  # For starttls
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = EMAIL_DATA['email']
SENDER_PSW = EMAIL_DATA['password']
# RECEIVER_EMAIL = "6143701557@messaging.sprintpcs.com"
RECEIVER_EMAIL = "shawn.jacobsen0@gmail.com"

# sendEmail(PORT, SMTP_SERVER, SENDER_EMAIL, SENDER_PSW, RECEIVER_EMAIL, text)

app = Flask(__name__)

@app.route('/api/')
def welcome():
    return "Welcome to Shawn's personal API!"

@app.route('/api/sleep-data', methods=['POST'])
def print_data():
    text = f"values:\r\n{request.values}\r\n\r\nForm:\r\n{request.form}\r\n\r\nJSON:\r\n{request.json}"
    print(text)
    sendEmail(PORT, SMTP_SERVER, SENDER_EMAIL, SENDER_PSW, RECEIVER_EMAIL, text)
    return "Received!"

if __name__ == "__main__":
    app.run(debug=True)
