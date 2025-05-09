from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import requests
from logs.logger import logger

class GooglePhotosClient:
    def __init__(self, credentials_json_path: Path, token_json_path: Path, scopes, headless: bool = True, dry_run: bool = False):
        self.credentials_json_path = credentials_json_path
        self.token_json_path = token_json_path
        self.scopes = scopes
        self.creds = None
        self.service = None
        self.headless = headless
        self.dry_run = dry_run
        self.authenticate()

    def authenticate(self):
        if self.token_json_path.exists():
            self.creds = Credentials.from_authorized_user_file(str(self.token_json_path), self.scopes)
            logger.info("Loaded credentials from token file.")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(self.credentials_json_path), self.scopes)
            if self.headless:
                self.creds = flow.run_console()
                logger.info("Authentication via console (headless mode).")
            else:
                self.creds = flow.run_local_server()
                logger.info("Authentication via local server (browser mode).")
            with open(self.token_json_path, 'w') as token_file:
                token_file.write(self.creds.to_json())
            logger.info("Authentication complete. Token saved.")

        self.service = build('photoslibrary', 'v1', credentials=self.creds)

    def upload_image(self, image_path: Path):
        if self.dry_run:
            logger.info(f"[Dry Run] Would upload: {image_path}")
            return "dry_run_token"

        if self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
            logger.info(f"Refreshed access token.")

        headers = {
            'Authorization': f'Bearer {self.creds.token}',
            'Content-type': 'application/octet-stream',
            'X-Goog-Upload-File-Name': image_path.name,
            'X-Goog-Upload-Protocol': 'raw',
        }

        with open(image_path, 'rb') as f:
            response = requests.post(
                url='https://photoslibrary.googleapis.com/v1/uploads',
                data=f,
                headers=headers
            )

        if response.status_code == 200:
            upload_token = response.text
            logger.info(f"Uploaded {image_path} - received uploadToken.")
            return upload_token
        else:
            logger.error(f"Failed to upload {image_path}: {response.text}")
            return None

    def create_media_item(self, upload_token, description):
        if self.dry_run:
            logger.info(f"[Dry Run] Would create media item with token: {upload_token} and description: {description}")
            return {"status": "dry_run"}

        body = {
            "newMediaItems": [
                {
                    "description": description,
                    "simpleMediaItem": {
                        "uploadToken": upload_token
                    }
                }
            ]
        }

        response = self.service.mediaItems().batchCreate(body=body).execute()
        logger.info(f"Media item created with response: {response}")
        return response