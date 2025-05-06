import os
import requests
from msal import ConfidentialClientApplication
import logs
from dotenv import load_dotenv


load_dotenv() # using env to avoid hardcoding (git related)

# environment variables for API calls
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# global variables for API calls
AZURE_API_URL = f"https://login.microsoftonline.com/{tenant_id}"
PERMISSIONS = ["https://graph.microsoft.com/.default"]
GRAPH_API_URL = "https://graph.microsoft.com/v1.0/users/{user_id}/sendMail" # user_id is defined in graph request

# ---------------- Functions
    
def get_access_token(interface:object) -> str | None:
    """
    Requests an access token from Azure API

    Args:
        interface (object): object of ui.UserInterface class

    Returns:
        str | any: access token if request was succesful, None if unsuccesful
    """


    app = ConfidentialClientApplication(client_id, client_secret, AZURE_API_URL) # object of MSAL library
    
    try: 
        token_data = app.acquire_token_for_client(scopes=PERMISSIONS) # makes an API call to MS Entra and returns a json dict containing the token

        if "access_token" in token_data: # looks for "access_token" in the dict
            return token_data["access_token"] # returns the value for "access_token"
        else:
            raise LookupError # if the token is not found, an error is raised
        
    except Exception as e:  
        interface.update_status("Access Token konnte nicht abgerufen werden...")
        logs.new_error(f"Error obtaining token: {e} + {token_data.get("error_description")}")
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
    
    if not access_token: # additional bug prevention
        logs.new_error(f"Access Token was empty...")
        return False

    headers = { # headers of http request
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
        response = requests.post(GRAPH_API_URL.format(user_id=user_address), headers=headers, json=email_data) # the Graph API call that tries to send the mail
        
        if response.status_code == 202: # if the request was successful
            interface.update_status(f"Mail gesendet an: {recipient_address}")
            logs.new_info(f"Mail send to: {recipient_address}")
            return True # for possible further checking
        else:
            raise Exception("post error") # leading to except block even though no specific "code error" was encountered
        
    except Exception as e:
        interface.update_status(f"Error bei Mail an: {recipient_address}")
        logs.new_error(f"Error {e} + {response.status_code} sending mail to: {recipient_address}")
        return False # for possible further checking

def placeholder(): # temporarily in order for ui to function
    pass