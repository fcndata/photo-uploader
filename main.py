from pathlib import Path
from logs.logger import logger
from src.google_photos_client import GooglePhotosClient
from src.pipeline import UploadPipeline
from src.utils import load_config


def main():
    config = load_config()

    # Access values from the config
    FOLDER_PATH = Path(config["mount"].get("FOLDER_PATH")).resolve()
    GOOGLE_CLIENT_SECRET_JSON = Path(config["creds"].get("GOOGLE_CLIENT_SECRET_JSON")).resolve()
    TOKEN_JSON_PATH = Path(config["creds"].get("TOKEN_JSON_PATH", "./credentials/token.json")).resolve()
    HEADLESS = config["execute"].get("headless", True)
    DRY_RUN = config["execute"].get("dry_run", False)
    LOG_FILE = Path(config["mount"].get("log_file", "logs/failed_uploads.csv")).resolve()


    # Choose headless=True for servers or pipelines without browser, False for local testing
    google_client = GooglePhotosClient(
        credentials_json_path = GOOGLE_CLIENT_SECRET_JSON,
        token_json_path = TOKEN_JSON_PATH,
        scopes = ['https://www.googleapis.com/auth/photoslibrary.appendonly'],
        headless = HEADLESS,
        dry_run = DRY_RUN  
    )

    pipeline = UploadPipeline(
        base_path = FOLDER_PATH,
        google_client = google_client,
        log_path = LOG_FILE
        
    )

    logger.info("Pipeline started")

    pipeline.run()

if __name__ == "__main__":
    main()