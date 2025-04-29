import os
import requests
from msal import ConfidentialClientApplication
import logs
from dotenv import load_dotenv


load_dotenv() # using env to avoid hardcoding (git related)

tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

AZURE_API_URL = f"https://login.microsoftonline.com/{tenant_id}"
PERMISSIONS = ["https://graph.microsoft.com/.default"]
GRAPH_API_URL = "https://graph.microsoft.com/v1.0/users/{user_id}/sendMail" # user_id is defined in graph request

    
def get_access_token(interface:object) -> str | None:
    """
    Requests an access token from MS Azure API

    Args:
        interface (object): object of ui.UserInterface class in ui

    Returns:
        str | any: access token if request was succesful, None if unsuccesful
    """


    app = ConfidentialClientApplication(client_id, client_secret, AZURE_API_URL)
    token_data = app.acquire_token_for_client(scopes=PERMISSIONS)
    
    try:
        if "access_token" in token_data:
            return token_data["access_token"]
        
    except:
        interface.update_status("Access Token konnte nicht abgerufen werden...")
        logs.new_error(f"Error obtaining token: {token_data.get("error_description")}")
        return None


def send_mail(interface:object, token:str, user_address:str, subject:str, body:str, recipient_address:str) -> bool:
    """
    Function that defines an email based on the arguments given and posts the sending request to MS Graph API
    
    Args:
        interface (object): object of UserInterface class in ui
        token (str): already filtered access token
        user_address (str): mail address of user
        subject (str): subject of mail
        body (str): body of mail
        recipient_address (str): mail address of recipient

    Raises:
        Exception: raising no specific exception for debuging purposes and further protection from crashes

    Returns:
        bool: True if mail was sent successfully, False if unsuccessful
    """

    access_token = token
    
    if not access_token:
        logs.new_error(f"Access Token was empty...")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    email_data = { # json format specified by Graph API
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "from": {
                "emailAddress": {
                    "address": user_address
                }
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_address
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }
    
    try:
        response = requests.post(GRAPH_API_URL.format(user_id=user_address), headers=headers, json=email_data)
        
        if response.status_code == 202:
            interface.update_status(f"Mail gesendet an: {recipient_address}")
            logs.new_info(f"Mail send to: {recipient_address}")
            return True
        else:
            raise Exception
        
    except Exception:
        interface.update_status(f"Error bei Mail an: {recipient_address}")
        logs.new_error(f"Error {response.status_code} sending mail to: {recipient_address}")
        return False

def placeholder(): # temporarily in order for ui to function
    pass