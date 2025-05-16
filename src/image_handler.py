from pathlib import Path
from datetime import datetime
import piexif
from PIL import Image
from typing import Dict
from src.models import ImageMetadata
from logs.logger import logger

class ImageHandler:
    def __init__(self, base_path: Path):
        """
        Initialize the ImageHandler with a base path.
        
        Args:
            base_path (Path): The base path where images are stored in local.
        """
        self.base_path = base_path
        
    def scan_folder(self) -> Dict[str, ImageMetadata]:
        """
        Scan recursively the folder for images and create a metadata dictionary.
        
        Returns:
            Dict[str, ImageMetadata]: A dictionary with filenames as keys and ImageMetadata objects as values.
        """
        image_metadata_dict = {}
        for folder in self.base_path.iterdir():
            if folder.is_dir():
                image_metadata_dict.update(self._create_image_metadata_dict(folder))
        logger.info(f"Found {len(image_metadata_dict)} media files.")
        return image_metadata_dict

    def _create_image_metadata_dict(self, folder: Path) -> Dict[str, ImageMetadata]:
        """
        Recursively create a dictionary with the metadada of each image.
        Returns:
            Dict[str, ImageMetadata]: A dictionary with filenames as keys and ImageMetadata objects as values.
        """        
        logger.info(f"Scanning folder: {folder}")

        image_metadata_dict = {}
        for file in folder.iterdir():
            if file.is_dir():
                nested = self._create_image_metadata_dict(file)
                image_metadata_dict.update(nested)
            else:
                if file.suffix.lower() in ('.png', '.jpg', '.mov', '.mp4'):
                    try:
                        parsed_time = datetime.strptime(file.stem, "%Y-%m-%d %H.%M.%S")
                    except ValueError:
                        parsed_time = None

                    metadata = ImageMetadata(
                        img_url=file,
                        filename=file.name,
                        folderpath=file.parent,
                        file_suffix=file.suffix,
                        timestamp=parsed_time
                    )
                    image_metadata_dict[file.name] = metadata
                    logger.info(f"Processed metadata for: {file.name}")
        return image_metadata_dict

    def convert_png_to_jpg(self, metadata: ImageMetadata) -> ImageMetadata:
        """
        Transform .png files into .jpg to modify the metadata with Exif.

        Returns:
            Dict[str, ImageMetadata]: A dictionary with filenames as keys and ImageMetadata objects as values.        
        """
        logger.info(f"Converting {metadata.filename} to JPG.")
        im = Image.open(metadata.img_url)
        rgb_im = im.convert('RGB')
        new_path = metadata.img_url.with_suffix('.jpg')
        rgb_im.save(new_path)

        updated_metadata = metadata.copy(update={
            'img_url': new_path,
            'file_suffix': '.jpg',
            'filename': new_path.name
        })
        logger.info(f"Conversion complete: {new_path.name}")
        return updated_metadata

    def set_exif_timestamp(self, metadata: ImageMetadata):
        """
        Update the EXIF timestamp of the image with the parsed time from the filename.
        
        Args:
            metadata (ImageMetadata): The metadata object containing the image information.

        """
        if not metadata.timestamp:
            logger.warning(f"No timestamp found for {metadata.filename}. Skipping EXIF writing.")
            return

        formatted_time = metadata.timestamp.strftime("%Y:%m:%d %H:%M:%S")
        try:
            exif_dict = piexif.load(str(metadata.img_url))
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = formatted_time.encode()
            exif_dict['0th'][piexif.ImageIFD.DateTime] = formatted_time.encode()

            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, str(metadata.img_url))
            logger.info(f"EXIF timestamp set for {metadata.filename}")
        except Exception as e:
            logger.error(f"Failed to set EXIF timestamp for {metadata.filename}: {e}")
