import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()


def send_email(source,data):
    
    subject = f"NEW - {source}"
    body = f"""
Hello,

Please see the listings below.

{data}

Kind regards
    """
    
    message = MIMEMultipart()
    message["From"] = os.getenv("sender_email_address")
    message["To"] = os.getenv("recipient_email_address") 
    message["Subject"] = subject
    message.attach(MIMEText(body,"plain"))

    smtpServer = os.getenv("smtp_server")
    smtpPort = os.getenv("smtp_port")
    server = smtplib.SMTP(smtpServer,smtpPort)

    statusCode, response = server.ehlo()
    print(statusCode,response)
    
    statusCode, response = server.starttls()
    print(statusCode,response)
    
    statusCode, response = server.login(os.getenv("sender_email_address"),os.getenv("sender_email_password"))
    print(statusCode,response)
    
    try:
        server.send_message(message)
        server.quit()
    except:
        return
