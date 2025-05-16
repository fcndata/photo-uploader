from logs.logger import logger
from src.image_handler import ImageHandler
from src.google_photos_client import GooglePhotosClient
from pathlib import Path
from src.utils import load_config, save_failed_uploads


class UploadPipeline:
    def __init__(self, base_path: Path, google_client: GooglePhotosClient, log_path: Path = Path("./logs/failed_uploads.csv")):
        """
        Initialize the UploadPipeline with a base path and Google Photos client.
        Args:
            base_path (Path): The base path where images are stored in local .
            google_client (GooglePhotosClient): Instance of GooglePhotosClient for uploading images.
        
        """
        self.image_handler = ImageHandler(base_path)
        self.google_client = google_client
        self.log_path = log_path

    def run(self):
        """
        Run the upload pipeline.

        Args:
            limit (int): The maximum number of images to upload (test). If None, process all files.
        """

        logger.info("Starting the upload pipeline.")
        metadata_dict = self.image_handler.scan_folder()

        failed_uploads = []

        for img_name, metadata in metadata_dict.items():

            logger.info(f"Preparing image: {metadata.filename}")

            if metadata.file_suffix.lower() == '.png':
                metadata = self.image_handler.convert_png_to_jpg(metadata)

            self.image_handler.set_exif_timestamp(metadata)

            try:
                upload_token = self.google_client.upload_image(metadata.img_url)
                if not upload_token:
                    raise Exception("Upload token is None")

                description = f"File date: {metadata.timestamp}" if metadata.timestamp else "No timestamp available"
                self.google_client.create_media_item(upload_token, description)

            except Exception as e:
                logger.error(f"Error uploading {metadata.filename}: {e}")
                failed_uploads.append((metadata.filename, str(e)))

        # Save failed uploads 
        if failed_uploads:
            save_failed_uploads(failed_uploads, self.log_path)

        logger.info("Upload pipeline completed.")
