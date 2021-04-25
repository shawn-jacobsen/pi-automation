import smtplib, ssl

def sendEmail(port, smtp_server, sender_email, sender_psw, receiver_email, text):

  rval = True # true if success, false if not
  try:
    assembled_message = f"From: {sender_email}\r\nTo: {receiver_email}\r\nSubject: {''}\r\n\r\n{text}"
    server = smtplib.SMTP(smtp_server,port)
    server.starttls()
    server.login(sender_email, sender_psw)
    server.sendmail(sender_email, receiver_email, assembled_message)
  except Exception as err:
    print("ERROR: Cannot send email")
    print(err)
    rval = False

  return rval
  