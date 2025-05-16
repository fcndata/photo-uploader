import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path(__file__).parent
LOG_DIR.mkdir(parents=True, exist_ok=True)

today = datetime.now().strftime('%Y%m%d')
log_filename = LOG_DIR / f'upload_log_{today}.txt'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)