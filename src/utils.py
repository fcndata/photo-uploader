import yaml
import csv
from pathlib import Path
from typing import List, Tuple
from logs.logger import logger
import json

def load_config(config_path="env_config.yaml"):
    """
    Loads the configuration from a YAML file.
    Args:
        config_path (str): Path to the YAML configuration file.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        
        return yaml.safe_load(f)

def save_failed_uploads(failed_uploads: List[Tuple[str, str]], output_path: Path) -> None:
    """
    Saves a list of failed uploads as a CSV file.

    Args:
        failed_uploads (List[Tuple[str, str]]): List of tuples with (filename, error_message)
        output_path (Path): Path to the output CSV file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "error_message"])
        writer.writerows(failed_uploads)

    logger.warning(f"{len(failed_uploads)} uploads failed. Details saved in {output_path}")


def generate_devcontainer(output_dir=".devcontainer"):

    config = load_config()    
    source_path = config["mount"]["host_path"]
    target_path = config["mount"]["container_mount_path"]

    devcontainer = {
        "name": "Photo Uploader Dev",
        "context": "..",
        "dockerFile": "Dockerfile",
        "settings": {
            "terminal.integrated.defaultProfile.linux": "bash"
        },
        "extensions": [
            "ms-python.python"
        ],
        "mounts": [
            f"source={source_path},target={target_path},type=readonly" 
        ],
        "remoteUser": "root"
    }

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    devcontainer_file = output_path / "devcontainer.json"

    if devcontainer_file.exists():
        devcontainer_file.unlink()
        logger.info("Previous devcontainer.json found and deleted.")

    with devcontainer_file.open("w", encoding="utf-8") as f:
        json.dump(devcontainer, f, indent=4)

    logger.info(f" DevContainer file generated at {devcontainer_file.resolve()}")
