import os
import json
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
import subprocess
import shutil

load_dotenv(find_dotenv())

# Create necessary folders for caching
def ensure_cache_folders():
    folders = ["transcriptions", "responses"]
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created {folder} directory for caching")

def get_video_transcription(local_directory: str, id: str):
    ensure_cache_folders()
    client = OpenAI()
    transcript_dict = {}
    
    # Process all MP3 files in the directory
    file_id = id
    transcription_cache_path = f"transcriptions/{file_id}.json"
        
    # Check if transcription cache exists
    if os.path.exists(transcription_cache_path):
        print(f"Using cached transcription for {file_id}")
        with open(transcription_cache_path, 'r') as cache_file:
                transcription = json.load(cache_file)
                transcript_dict[file_id] = transcription
    else:
        print(f"Transcribing {file}...")
        with open(f"{local_directory}/{file}", 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe", 
                file=audio_file, 
                response_format="text",
                prompt=file_id
            )
            transcript_dict[file_id] = transcription
                
            # Cache the transcription
            with open(transcription_cache_path, 'w') as cache_file:
                json.dump(transcript_dict, cache_file)
            print(f"Cached transcription for {file_id}")
            os.remove(f"{local_directory}/{file}")
    return transcript_dict

def convert_file_mp3(local_directory:str, id:str):
    # Check if MP3 already exists for this ID
    mp3_path = os.path.join(local_directory, f"{id}.mp3")
    if os.path.exists(mp3_path) or os.path.exists(f"transcriptions/{id}.json"):
        print(f"MP3 file for ID {id} or its transcription already exists. Skipping conversion.")
        return True
        
    # Check if ffmpeg is installed
    if shutil.which('ffmpeg') is None:
        print("Error: ffmpeg is not installed or not in PATH. Please install ffmpeg first.")
        return False
    
    # Ensure directory exists
    if not os.path.exists(local_directory):
        print(f"Error: Directory {local_directory} does not exist")
        return False
    
    converted = False
    for file in os.listdir(local_directory):
        # Skip mp3 files and hidden files
        if file.endswith('.mp3') or file.startswith('.'):
            continue
        
        # Check if this is a video file (common video extensions)
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv']
        is_video = any(file.lower().endswith(ext) for ext in video_extensions)
        
        if not is_video:
            print(f"Skipping {file} - not a recognized video format")
            continue
        
        print(f"Converting {file} to MP3...")
        
        input_path = os.path.join(local_directory, file)
        output_path = os.path.join(local_directory, f"{id}.mp3")
        
        try:
            # Use proper ffmpeg parameters for extracting audio
            cmd = [
                "ffmpeg",
                "-i", input_path,        # Input file
                "-vn",                   # Disable video
                "-acodec", "libmp3lame", # Use MP3 codec
                "-ab", "192k",          # Audio bitrate
                "-ar", "44100",         # Audio sample rate
                "-y",                    # Overwrite output file
                output_path              # Output file
            ]
            
            # Run the command and capture output
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Check if conversion was successful
            if process.returncode == 0:
                print(f"Successfully converted {file} to {id}.mp3")
                converted = True
                # Remove original file
                os.remove(input_path)
            else:
                print(f"Error converting {file}")
                print(f"ffmpeg error: {process.stderr}")
        
        except Exception as e:
            print(f"Conversion failed: {str(e)}")
    
    if not converted:
        print("No files were converted. Check if the directory contains valid video files.")
    
    return converted

def store_response(id: str, response_json: dict):
    """Store response JSON data to a file in the responses folder
    
    Args:
        id: The ID for the response file
        response_json: Dictionary containing the response data
    
    Returns:
        bool: True if successful, False otherwise
    """
    ensure_cache_folders()
    response_path = f"responses/{id}_responses.json"
    
    try:
        with open(response_path, 'w') as response_file:
            json.dump(response_json, response_file, indent=4)
        print(f"Stored response for ID {id} in {response_path}")
        return True
    except Exception as e:
        print(f"Failed to store response: {str(e)}")
        return False
