import os
from flask import Flask, request
import json

from pyNotifications import (
  sendEmail
)

app = Flask(__name__)

@app.route('/api/')
def welcome():
    rval = f"Welcome to Shawn's personal API!"
    return rval

@app.route('/api/sleep-data', methods=['POST'])
def print_data():
    text = f"values:\r\n{request.values}\r\n\r\nForm:\r\n{request.form}\r\n\r\nJSON:\r\n{request.json}"
    print(text)
    rval = sendEmail(app, text)
    return f"{'Success!' if rval else 'something went wrong...'}"

if __name__ == "__main__":
    app.run(debug=True)
