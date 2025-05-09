from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
from typing import Optional

class ImageMetadata(BaseModel):
    img_url: Path
    filename: str
    folderpath: Path
    file_suffix: str
    timestamp: Optional[datetime]

    class Config: # Allow arbitrary types for the fields
        arbitrary_types_allowed = True