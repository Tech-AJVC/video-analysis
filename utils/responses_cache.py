from utils.audio_transcribe import ensure_cache_folders
import os
import json

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
    