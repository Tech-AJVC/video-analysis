from utils.audio_transcribe import ensure_cache_folders
import os
import json
import logging
from utils.hf_utils import upload_file_to_hf_dataset, download_file_from_hf_dataset, DATASET_REPO_ID

TRACKING_DATA_REPO_ID = "tech-ajvc/last_processed_data"
TRACKING_FILE_PATH_IN_REPO = "last_processed_id.json"
LOCAL_TEMP_TRACKING_DIR = "tracking" # Local directory for temporary tracking files
RESPONSES_DIR = "responses" # Local temporary directory

# Ensure the local temporary directory for responses exists
os.makedirs(RESPONSES_DIR, exist_ok=True)

# Ensure the local temporary directory for tracking files exists
os.makedirs(LOCAL_TEMP_TRACKING_DIR, exist_ok=True)


def get_cached_response(id: str, type: str):
    """Fetches a cached response from Hugging Face Datasets."""
    hf_path_in_repo = f"responses/{id}_responses_{type}.json"
    local_temp_download_path = os.path.join(RESPONSES_DIR, f"{id}_responses_{type}_temp_dl.json")
    response_data = None

    logging.info(f"Attempting to download cached response from HF: {DATASET_REPO_ID}/{hf_path_in_repo}")
    downloaded_file = download_file_from_hf_dataset(
        path_in_repo=hf_path_in_repo,
        local_destination_path=local_temp_download_path,
        repo_id=DATASET_REPO_ID
    )

    if downloaded_file and os.path.exists(downloaded_file):
        try:
            with open(downloaded_file, 'r') as f:
                response_data = json.load(f)
            logging.info(f"Successfully loaded response for ID {id} from HF via temp file {downloaded_file}")
        except Exception as e:
            logging.error(f"Error reading downloaded cached response for ID {id}: {e}")
            response_data = None # Ensure None if loading fails
        finally:
            try:
                os.remove(downloaded_file)
                logging.debug(f"Cleaned up temporary downloaded file: {downloaded_file}")
            except OSError as e:
                logging.error(f"Error removing temporary downloaded file {downloaded_file}: {e}")
    else:
        logging.info(f"Cached response not found on HF for ID {id}, type {type}.")

    return response_data

def store_response(id: str, response: dict, type: str):
    """Stores a response to Hugging Face Datasets via a temporary local file."""
    local_temp_upload_path = os.path.join(RESPONSES_DIR, f"{id}_responses_{type}_temp_ul.json")
    hf_path_in_repo = f"responses/{id}_responses_{type}.json"

    try:
        with open(local_temp_upload_path, 'w') as f:
            json.dump(response, f, indent=4)
        logging.debug(f"Temporary response file created at {local_temp_upload_path} for ID {id}")

        logging.info(f"Uploading response for ID {id} to HF: {DATASET_REPO_ID}/{hf_path_in_repo}")
        upload_url = upload_file_to_hf_dataset(
            local_file_path=local_temp_upload_path,
            path_in_repo=hf_path_in_repo,
            repo_id=DATASET_REPO_ID
        )
        if upload_url:
            logging.info(f"Successfully cached response for ID {id} to HF: {upload_url}")
        else:
            logging.error(f"Failed to cache response for ID {id} to HF.")

    except Exception as e:
        logging.error(f"Error preparing or uploading cached response for ID {id}: {e}")
    finally:
        if os.path.exists(local_temp_upload_path):
            try:
                os.remove(local_temp_upload_path)
                logging.debug(f"Cleaned up temporary upload file: {local_temp_upload_path}")
            except OSError as e:
                logging.error(f"Error removing temporary upload file {local_temp_upload_path}: {e}")


def ensure_tracking_folder(): # This function now ensures the local *temporary* tracking folder
    """Ensure the local temporary tracking folder exists."""
    os.makedirs(LOCAL_TEMP_TRACKING_DIR, exist_ok=True)


def store_last_processed_id(id):
    """Store the last processed application ID to Hugging Face Dataset."""
    ensure_tracking_folder() # Ensures local temp dir exists
    
    local_temp_tracking_file = os.path.join(LOCAL_TEMP_TRACKING_DIR, "last_processed_id_temp.json")
    tracking_data = {
        "last_processed_id": id,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }
    
    try:
        with open(local_temp_tracking_file, 'w') as f:
            json.dump(tracking_data, f, indent=4)
        
        logging.info(f"Uploading tracking data for ID {id} to HF: {TRACKING_DATA_REPO_ID}/{TRACKING_FILE_PATH_IN_REPO}")
        upload_url = upload_file_to_hf_dataset(
            local_file_path=local_temp_tracking_file,
            path_in_repo=TRACKING_FILE_PATH_IN_REPO,
            repo_id=TRACKING_DATA_REPO_ID
        )
        if upload_url:
            logging.info(f"Successfully updated last processed ID to {id} on HF: {upload_url}")
        else:
            logging.error(f"Failed to update last processed ID {id} on HF.")
            
    except Exception as e:
        logging.error(f"Error storing last processed ID {id} to HF: {e}")


def get_last_processed_id():
    """Get the last processed application ID from Hugging Face Dataset."""
    ensure_tracking_folder() # Ensures local temp dir exists for download

    local_temp_tracking_file = os.path.join(LOCAL_TEMP_TRACKING_DIR, "last_processed_id_temp_dl.json")
    downloaded_file = None
    last_id = None

    logging.info(f"Attempting to download last_processed_id from HF: {TRACKING_DATA_REPO_ID}/{TRACKING_FILE_PATH_IN_REPO}")
    downloaded_file = download_file_from_hf_dataset(
        path_in_repo=TRACKING_FILE_PATH_IN_REPO,
        local_destination_path=local_temp_tracking_file,
        repo_id=TRACKING_DATA_REPO_ID
    )

    if downloaded_file and os.path.exists(downloaded_file):
        try:
            with open(downloaded_file, 'r') as f:
                tracking_data = json.load(f)
            last_id = tracking_data.get("last_processed_id")
            logging.info(f"Successfully retrieved last_processed_id: {last_id} from HF.")
        except Exception as e:
            logging.error(f"Error reading downloaded tracking file: {e}")

    if last_id is None: # If not found on HF or error reading it
        logging.info("No valid tracking data found on HF or error during processing, initializing with ID 0.")
        store_last_processed_id(0)  # Initialize on HF
        return 0
    
    return last_id


def get_all_processed_ids():
    """Get a list of all processed application IDs based on the files in the responses folder
    
    Returns:
        A set of application IDs that have been processed
    """
    ensure_cache_folders()
    processed_ids = set()
    
    try:
        # Look for response files in the responses directory
        if os.path.exists("responses"):
            for filename in os.listdir("responses"):
                # Parse IDs from filenames like '123_responses_behavior.json'
                if filename.endswith("_responses_behavior.json"):
                    try:
                        id_str = filename.split("_")[0]
                        processed_ids.add(int(id_str))
                    except (ValueError, IndexError):
                        continue
    except Exception as e:
        logging.error(f"Error getting processed IDs: {str(e)}")
    
    return processed_ids