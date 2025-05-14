from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from typing import Optional

class ImageMetadata(BaseModel):
    """
    Class to hold metadata for images.
    
    """
    img_url: Path
    filename: str
    folderpath: Path
    file_suffix: str
    timestamp: Optional[datetime]

    class Config: # Allow arbitrary types for the fields
        """
        Configuration for Pydantic models.
        This allows arbitrary types for the fields in the model, in this particular case, it's Path and Datetime as base only support native types from Python.
        """
        arbitrary_types_allowed = True