import os
from flask import Flask, request
import json

from pyNotifications import (
  sendEmail
)

SENDER_EMAIL = ""
SENDER_PSW = ""
# get env vars
if os.environ.get('IS_PROD', None):
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
    SENDER_PSW = os.environ.get('SENDER_PSW')
else:
    print("\nWelcome to DEVELOPMENT MODE....")
    # read in email json data
    with open('email_secret.json') as f:
        EMAIL_DATA = json.load(f)
    SENDER_EMAIL = EMAIL_DATA['email']
    SENDER_PSW = EMAIL_DATA['password']

# Notification data for sending text message
PORT = 587  # For starttls
SMTP_SERVER = "smtp.gmail.com"
# RECEIVER_EMAIL = "6143701557@messaging.sprintpcs.com"
RECEIVER_EMAIL = "shawn.jacobsen0@gmail.com"

# sendEmail(PORT, SMTP_SERVER, SENDER_EMAIL, SENDER_PSW, RECEIVER_EMAIL, text)

app = Flask(__name__)

@app.route('/api/')
def welcome():
    rval = f"Welcome to Shawn's personal API!\r\nSENDER_EMAIL: {SENDER_EMAIL}\r\nSENDER_PSW: {SENDER_PSW}"
    return rval

@app.route('/api/sleep-data', methods=['POST'])
def print_data():
    text = f"values:\r\n{request.values}\r\n\r\nForm:\r\n{request.form}\r\n\r\nJSON:\r\n{request.json}"
    print(text)
    rval = sendEmail(PORT, SMTP_SERVER, SENDER_EMAIL, SENDER_PSW, RECEIVER_EMAIL, text)
    return f"{'Success!' if rval else 'something went wrong...'}"

if __name__ == "__main__":
    app.run(debug=True)
