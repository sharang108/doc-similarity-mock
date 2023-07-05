import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


class DriveAuthException(Exception):
    pass


class GdriveUtils:
    def __init__(self) -> None:
        cwd = os.getcwd()
        self.token_file = os.path.join(cwd, os.getenv("TOKEN_FILE"))
        self.creds_file = os.path.join(cwd, os.getenv("CREDS_FILE"))
        # self.scopes = os.getenv("SCOPES")
        self.scopes = [
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        self.creds = self.authenticate()
        self.service = build("drive", "v3", credentials=self.creds)

    def authenticate(self) -> Credentials:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds_file, self.scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        return creds

    def read_files(self, file_id: str = None):
        if file_id:
            request = self.service.files().get_media(fileId=file_id)
            file_data = request.execute().decode("utf-8")
            return file_data
        else:
            results = self.service.files().list(pageSize=1000).execute()
            files = results.get("files", [])
            for file in files:
                print(f"{file['id']}: {file['name']}")
