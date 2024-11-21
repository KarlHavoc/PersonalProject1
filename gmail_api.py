import os

# for encoding/decoding messages in base64
# from base64 import urlsafe_b64decode
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for dealing with attachement MIME types
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.image import MIMEImage
# from email.mime.audio import MIMEAudio
# from email.mime.base import MIMEBase
# from mimetypes import guess_type as guess_mime_type

SCOPES = ["https://mail.google.com/"]


def gmail_authenticate():
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
    try:
        service = build("gmail", "v1", credentials=creds)
    except HttpError as error:
        print(f"An error ocurred: {error}")
    return service


def get_unread_tips_emails_ids(service, query):
    result = service.users().messages().list(userId="me", q=query)
    message_ids = []

    if result:
        for message in result:
            message_ids.extend(result[message]["id"])