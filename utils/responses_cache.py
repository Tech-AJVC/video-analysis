from utils.audio_transcribe import ensure_cache_folders
import os
import json
import logging

TRACKING_FILE = "tracking/last_processed_id.json"

def get_cached_response(id: str, type: str):
    ensure_cache_folders()
    response_path = f"responses/{id}_responses_{type}.json"
    if os.path.exists(response_path):
        try:
            with open(response_path, 'r') as response_file:
                response_data = json.load(response_file)
            print(f"Using cached response for ID {id}")
            return response_data
        except Exception as e:
            print(f"Error reading cached response: {str(e)}")
            return None
    return None

def store_response(id: str, response: dict, type: str):
    ensure_cache_folders()
    
    response_path = f"responses/{id}_responses_{type}.json"
    
    try:
        with open(response_path, 'w') as response_file:
            json.dump(response, response_file, indent=4)
        print(f"Cached response for ID {id}")
    except Exception as e:
        print(f"Error writing cached response: {str(e)}")
        logging.error(f"Error writing cached response: {str(e)}")


def ensure_tracking_folder():
    """Ensure the tracking folder exists"""
    os.makedirs("tracking", exist_ok=True)


def store_last_processed_id(id):
    """Store the last processed application ID in the tracking file
    
    Args:
        id: The application ID that was last processed
    """
    ensure_tracking_folder()
    
    try:
        # Create tracking data with the last processed ID and timestamp
        tracking_data = {
            "last_processed_id": id,
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
        
        with open(TRACKING_FILE, 'w') as tracking_file:
            json.dump(tracking_data, tracking_file, indent=4)
            
        logging.info(f"Updated last processed ID to {id}")
    except Exception as e:
        logging.error(f"Error updating last processed ID: {str(e)}")


def get_last_processed_id():
    """Get the last processed application ID from the tracking file
    
    Returns:
        The last processed application ID or None if not found
    """
    ensure_tracking_folder()
    
    if os.path.exists(TRACKING_FILE):
        try:
            with open(TRACKING_FILE, 'r') as tracking_file:
                tracking_data = json.load(tracking_file)
                return tracking_data.get("last_processed_id")
        except Exception as e:
            logging.error(f"Error reading last processed ID: {str(e)}")
            return None
    else:
        logging.info("No tracking file found, creating one")
        store_last_processed_id(0)  # Initialize with 0 if no tracking file exists
        return 0


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
    