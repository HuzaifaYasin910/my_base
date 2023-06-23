from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from django.template.loader import render_to_string



from django.contrib import messages
from django.shortcuts import redirect,render
from .filters import *
import os
from .forms import SubscribersForm

EMAIL_ADDRESS  = 'novelsnotions@gmail.com'
EMAIL_PASSWORD = 'tsojwmidjtrgnavv'







smtp_port = 587
smtp_server = 'smtp.gmail.com'
FROM = EMAIL_ADDRESS

def mail_test(TO, SUBJECT, newsletter, authentication, token):
    msg = MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = EMAIL_ADDRESS

    context = {'newsletter': newsletter, 'authentication': authentication, 'token': token}
    html_template = render_to_string('stores/mails.html', context)
    html_content = MIMEText(html_template, 'html')
    msg.attach(html_content)
    
    print('Sending email...')
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(FROM, TO, msg.as_string())
    print('Email sent!')









def is_admin(user):
    return user.is_authenticated and user.is_staff


def send_email(email,subject,message):
    
    subject = 'Thank you for joinig our NewsLetter'
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()