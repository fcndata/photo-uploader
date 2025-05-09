from dotenv import load_dotenv
from pathlib import Path
from src.google_photos_client import GooglePhotosClient
from src.pipeline import UploadPipeline
import os

# Load env variables
load_dotenv(override=True)

FOLDER_PATH = Path(os.environ['FOLDER_PATH'].replace("\\", "/"))
GOOGLE_CLIENT_SECRET_JSON = Path(os.environ['GOOGLE_CLIENT_SECRET_JSON'])
TOKEN_JSON_PATH = Path(os.environ.get('TOKEN_JSON_PATH', './credentials/token.json'))

# Choose headless=True for servers or pipelines without browser, False for local testing
google_client = GooglePhotosClient(
    credentials_json_path=GOOGLE_CLIENT_SECRET_JSON,
    token_json_path=TOKEN_JSON_PATH,
    scopes=['https://www.googleapis.com/auth/photoslibrary.appendonly'],
    headless=True,
    dry_run=True  # Set to False to execute real uploads
)

pipeline = UploadPipeline(
    base_path=FOLDER_PATH,
    google_client=google_client
)

# Run in test mode with a limit of 3 files
pipeline.run(limit=2)
