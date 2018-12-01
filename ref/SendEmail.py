# allow less secure apps to access your Gmail at: https://support.google.com/accounts/answer/6010255?hl=en
# guide for setting up PiCamera at: https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/
# guide for connecting PIR sensor to Pi at: https://www.raspberrypi.org/learning/parent-detector/worksheet/
# requires your email password to run (line 56), obviously a security hazard so be careful.

from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import email.encoders
import smtplib
import email
import sys


def send(textToSend, imgLink = ""):
    '''Send Email with content textToSend, imgLink state the image path
    '''

    sender = "something@gmail.com"
    receiver = "otherthing@gmail.com"
    print('Preparing to send the email')
    msg = MIMEMultipart()
    msg["Subject"] = "Info From Pi 3"
    msg["From"] = sender
    msg["To"] = receiver
    text = MIMEText(textToSend)
    msg.attach(text)

    # attach img to email
    try:
        with open(imgLink, 'rb') as fp:
            img = MIMEImage(fp.read())
            msg.attach(img)
    except Exception as e:
        err = "Error in attaching the image to email\n"
        print(err + str(e))
        return sendError(err)

    # access Gmail account and send email
    try:
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(sender,"asdfjkl;0-21")
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        print("Email Sent")
        return True
    except Exception as e:
        err = "Error in sending the email\n"
        print(err + str(e))
        return sendError(err)

def sendError(textToSend):
    try:
	sender = "something@gmail.com"
	receiver = "otherthing@gmail.com"
        msg = MIMEMultipart()
        msg["Subject"] = "Error From Pi 3"
        msg["From"] = sender
        msg["To"] = receiver
        text = MIMEText(textToSend)
        msg.attach(text)
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(sender,"asdfjkl;0-21")
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        return False
    except Exception as e:
        print(str(e))
        return False
