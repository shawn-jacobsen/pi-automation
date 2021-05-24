import os
from flask import Flask, request
import json

from pyNotifications import (
  sendEmail
)

from notionAutomation.index import (
    updateClasses
    updateSleepHours
)

app = Flask(__name__)

@app.route('/api/')
def welcome():
    rval = f"Welcome to Shawn's personal API!"
    return rval

@app.route('/api/update/classes', methods=['POST'])
def updatePassedClasses():
    rval = updateClasses()
    return rval

@app.route('/api/update/sleep', methods=['POST'])
def updatePassedSleepHours():
    sleep_hrs = request.args.get('hours')
    rval = False
    if sleep_hrs and sleep_hrs is not -1:
        rval = updateSleepHours(sleep_hrs)
    return rval


@app.route('/api/sleep-data', methods=['POST'])
def uploadSleepToNotion():
    text = f"values:\r\n{request.values}\r\n\r\nForm:\r\n{request.form}\r\n\r\nJSON:\r\n{request.json}"
    rval = False
    sleep_hrs = -1
    if request.json is not None:

        metrics = request.json['data']['metrics']
        sleep_data_index = 0
        for metric in metrics:
            if metric['name'] == 'sleep_analysis':
                break
            sleep_data_index += 1

        sleep_data = metrics[sleep_data_index]
        sleep_hrs = sleep_data['data']['asleep']

        rval = request.post(f"/api/update/sleep?hours={sleep_hrs}")
    return f"{'Success!' if rval else 'something went wrong...'}"


@app.route('/api/wakeup-time', methods=['POST'])
def uploadWakeTimeToNotion():
    text = f"values:\r\n{request.values}\r\n\r\nForm:\r\n{request.form}\r\n\r\nJSON:\r\n{request.json}"
    print(text)
    rval = sendEmail(app, text)
    return f"{'Success!' if rval else 'something went wrong...'}"


if __name__ == "__main__":
    app.run(debug=True)
