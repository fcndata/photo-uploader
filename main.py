from pathlib import Path
from logs.logger import logger
from src.google_photos_client import GooglePhotosClient
from src.pipeline import UploadPipeline
from src.utils import load_config


def main():
    config = load_config()

    # Load paths and runtime parameters from the YAML config
    container_photos_path = Path(config["mount"]["container_mount_path"]).resolve()
    google_client_secret_file = Path(config["creds"]["google_client_secret_file"]).resolve()
    token_file = Path(config["creds"].get("token_file", "./credentials/token.json")).resolve()
    output_log_file = Path(config["mount"].get("output_log_file", "logs/failed_uploads.csv")).resolve()

    headless = config["execute"].get("headless", True)
    dry_run = config["execute"].get("dry_run", False)

    # Initialize Google Photos client
    google_client = GooglePhotosClient(
        credentials_json_path=google_client_secret_file,
        token_json_path=token_file,
        scopes=['https://www.googleapis.com/auth/photoslibrary.appendonly'],
        headless=headless,
        dry_run=dry_run
    )

    # Initialize and run the upload pipeline
    pipeline = UploadPipeline(
        base_path=container_photos_path,
        google_client=google_client,
        log_path=output_log_file
    )

    logger.info("Pipeline started")
    pipeline.run()


if __name__ == "__main__":
    main()
