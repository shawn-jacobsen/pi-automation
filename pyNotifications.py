import os
import json
from flask import Flask
from flask_mail import Mail, Message

RECEIVER_EMAIL = "6143701557@messaging.sprintpcs.com"
# get env vars
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PSW = os.environ.get('SENDER_PSW')

def sendEmail(app, text):
  rval = True # true if success, false if not

  # setup app for email send
  app.config.update(dict(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = SENDER_EMAIL,
    MAIL_PASSWORD = SENDER_PSW,
  ))

  mail = Mail(app)
  msg = Message(
    '',
    sender = SENDER_EMAIL,
    recipients = [RECEIVER_EMAIL]
  )
  msg.body = text

  try:   
    with app.app_context():
      mail.send(msg)
  except Exception as err:
    print("ERROR: Cannot send email")
    print(err)
    rval = f"{err}"

  return rval
  