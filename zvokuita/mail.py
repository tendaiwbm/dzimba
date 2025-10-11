import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()


def prepare_data(listings,source_domain_url,path_column_name):
    listings[path_column_name] = source_domain_url + listings[path_column_name]
    listingEndpoints = listings[path_column_name].tolist()
    listingsAsString = "\n".join(listingEndpoints)
    return listingsAsString

def send_email(source,data):
    message = f"""Subject: Apartments from {source} matching your criteria
Hello,

Please see the listings below.

{data}

Ciao
    """

    atumira = os.getenv("sender_email_address")
    password = os.getenv("sender_email_password")
    atumirwa = os.getenv("recipient_email_address") 
    smtpServer = os.getenv("smtp_server")
    smtpPort = os.getenv("smtp_port")

    server = smtplib.SMTP(smtpServer,smtpPort)
    statusCode, response = server.ehlo()
    print(statusCode,response)
    statusCode, response = server.starttls()
    print(statusCode,response)
    statusCode, response = server.login(atumira,password)
    print(statusCode,response)
    server.sendmail(atumira,atumirwa,message)
    server.quit()
