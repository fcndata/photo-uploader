from logs.logger import logger
from src.image_handler import ImageHandler
from src.google_photos_client import GooglePhotosClient
from pathlib import Path

class UploadPipeline:
    def __init__(self, base_path: Path, google_client: GooglePhotosClient):
        self.image_handler = ImageHandler(base_path)
        self.google_client = google_client

    def run(self, limit: int = None):
        logger.info("Starting the upload pipeline.")
        metadata_dict = self.image_handler.scan_folder()

        count = 0
        for img_name, metadata in metadata_dict.items():
            if limit and count >= limit:
                logger.info(f"Reached test limit of {limit} files. Stopping.")
                break

            logger.info(f"Preparing image: {metadata.filename}")

            if metadata.file_suffix.lower() == '.png':
                metadata = self.image_handler.convert_png_to_jpg(metadata)

            self.image_handler.set_exif_timestamp(metadata)

            upload_token = self.google_client.upload_image(metadata.img_url)
            if not upload_token:
                logger.error(f"Skipping {metadata.filename} due to upload failure.")
                continue

            description = f"File date: {metadata.timestamp}" if metadata.timestamp else "No timestamp available"
            self.google_client.create_media_item(upload_token, description)

            count += 1

        logger.info("Upload pipeline completed.")
