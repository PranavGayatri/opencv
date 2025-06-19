import os
import base64
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def fetch_resumes_from_gmail(credentials_file):
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", q="has:attachment filename:(pdf OR docx)").execute()
    messages = results.get("messages", [])
    files = []

    for msg in messages[:10]:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        for part in msg_data["payload"].get("parts", []):
            filename = part.get("filename")
            if filename:
                att_id = part["body"]["attachmentId"]
                att = service.users().messages().attachments().get(userId="me", messageId=msg["id"], id=att_id).execute()
                data = base64.urlsafe_b64decode(att["data"].encode("UTF-8"))
                with open(os.path.join("uploads", filename), "wb") as f:
                    f.write(data)
                files.append(open(os.path.join("uploads", filename), "rb"))
    return files