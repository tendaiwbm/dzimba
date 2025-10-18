import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()


def prepare_data(listings,source_domain_url,path_column_name):
    listings[path_column_name] = source_domain_url + listings[path_column_name]
    listingEndpoints = listings[path_column_name].tolist()
    listingsAsString = "\n".join(listingEndpoints)
    return listingsAsString

def send_email(pipeline_result):
    data = prepare_data(*pipeline_result.values())
    
    subject = f"NEW - {list(pipeline_result.keys())[0]}"
    body = f"""
Hello,

Please see the listings below.

{data}

Ciao
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
