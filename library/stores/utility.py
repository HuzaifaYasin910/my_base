from email.mime.text import MIMEText
import smtplib

EMAIL_ADDRESS  = 'novelsnotions@gmail.com'
EMAIL_PASSWORD = 'tsojwmidjtrgnavv'


























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