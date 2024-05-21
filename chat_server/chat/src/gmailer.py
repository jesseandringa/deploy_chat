import base64
import os
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

####
# class EmailService:
#     def __init__(self, my_email_address:str = 'jess.andringa@gmail.com'):
#         self.recieving_email_address = my_email_address
# API_Key = 'AIzaSyDdxScsVPNYaAfRFMfJ7dao9wh2RpHiKkg'
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


# send email to single email
def gmail_send_message(message_txt, name, email):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # creds, _ = google.auth.default()
    message_txt = "Email from: " + name + " " + email + "\n " + message_txt
    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(message_txt)

        message["To"] = "your.municipal.assistant@gmail.com"
        message["From"] = "bumpdog@gmail.com"
        message["Subject"] = "Chat Email from: " + name + " " + email

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    print("send_message", send_message)
    return send_message


if __name__ == "__main__":
    gmail_send_message("test1", "test2", "test3")
