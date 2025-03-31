import sys
import os
import json
import base64
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import socket
import datetime
import re
import io


"""
This module demonstrates how to implement reusable authentication
for several Google APIs including Gmail, Google Drive, and Google Calendar
using a service account (or a pre‐authenticated credential).
No interactive authorization is needed at runtime.
"""

import os
import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from google.oauth2 import service_account
import pandas as pd

SCOPES = [
"https://www.googleapis.com/auth/gmail.compose",  # For creating Gmail drafts or sending emails.
"https://www.googleapis.com/auth/drive.file",     # For uploading files to Drive.
"https://www.googleapis.com/auth/calendar" , 
"https://www.googleapis.com/auth/gmail.send",     # For creating Google Calendar events.
"https://www.googleapis.com/auth/drive",           # For full access to Drive files
"https://www.googleapis.com/auth/spreadsheets",         # For full access to Google Sheets
"https://www.googleapis.com/auth/spreadsheets.readonly"  # For reading Google Sheets
]



GOOGLE_APPLICATION_CREDENTIALS = 'utils/neat-height-449308-h8-2a37363e5a04.json'


def get_credentials(subject_email: str = None):
    """
    Returns credentials from a service account file with the configured scopes.
    If a subject_email is provided (required for delegated access, e.g. Gmail),
    credentials will be impersonated to that user.

    The code expects the environment variable GOOGLE_APPLICATION_CREDENTIALS
    to point to the service account JSON key file.

    Args:
    subject_email: (Optional) User email to impersonate for domain-wide delegation.
    Returns:
    google.oauth2.service_account.Credentials object.
    """
    service_account_file = GOOGLE_APPLICATION_CREDENTIALS
    if not service_account_file:
        raise EnvironmentError("Environment variable GOOGLE_APPLICATION_CREDENTIALS is not set")

    creds = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)

    # If you need to access user data with Gmail, you must delegate domain-wide access.
    if subject_email:
        creds = creds.with_subject(subject_email)

    return creds

def download_drive_file(id: str, drive_link: str, local_folder_path: str):
    """
    Downloads a file from a Google Drive link to a local folder.
    
    Args:
    drive_link: The Google Drive link to the file (https://drive.google.com/file/d/FILE_ID/...).  
    local_folder_path: The local folder path where the file should be saved.
    
    Returns:
    Dictionary containing the downloaded file's local path and filename.
    """
    if id is not None:
        mp3_path = os.path.join(local_folder_path, f"{id}.mp3")
        if os.path.exists(mp3_path) or os.path.exists(f"transcriptions/{id}.json"):
            print(f"[Drive] MP3 file or its transcription for ID {id} already exists at {mp3_path}. Skipping download.")
            return {
                'local_path': mp3_path,
                'filename': f"{id}.mp3",
                'mime_type': 'audio/mp3',
                'cached': True
        }
    
    
    # For Drive we do not need to impersonate unless required
    creds = get_credentials()
    
    try:
        # Extract file ID from the Drive link
        file_id_match = re.search(r'(/d/|id=)([a-zA-Z0-9_-]+)', drive_link)
        if not file_id_match:
            raise ValueError(f"Could not extract file ID from Drive link: {drive_link}")
            
        file_id = file_id_match.group(2)
        
        # Build the Drive service
        service = build("drive", "v3", credentials=creds)
        
        # Get file metadata to determine the filename
        file_metadata = service.files().get(fileId=file_id, fields="name,mimeType").execute()
        filename = file_metadata.get('name')
        mime_type = file_metadata.get('mimeType')
        
        # Make sure the local folder exists
        os.makedirs(local_folder_path, exist_ok=True)
        
        # Build the local file path
        local_file_path = os.path.join(local_folder_path, filename)
        
        # Download the file
        request = service.files().get_media(fileId=file_id)
        file_handle = io.BytesIO()
        downloader = MediaIoBaseDownload(file_handle, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"[Drive] Download progress: {int(status.progress() * 100)}%")
        
        # Save the file to disk
        file_handle.seek(0)
        with open(local_file_path, 'wb') as f:
            f.write(file_handle.read())
        
        print(f"[Drive] File downloaded to: {local_file_path}")
        
        # Return details about the downloaded file
        return {
            'local_path': local_file_path,
            'filename': filename,
            'mime_type': mime_type,
            'cached': False
        }
        
    except HttpError as error:
        print(f"[Drive] An error occurred: {error}")
        return None
    except Exception as e:
        print(f"[Drive] An unexpected error occurred: {e}")
        return None

def read_google_sheets(sheets_link: str, sheet_name: str = None, range_name: str = None):
    """
    Reads data from a Google Sheets document.
    
    Args:
    sheets_link: The Google Sheets URL (https://docs.google.com/spreadsheets/d/SHEET_ID/...).  
    sheet_name: Optional name of the specific sheet to read. If None, reads the first sheet.
    range_name: Optional cell range to read (e.g., 'A1:D10'). If None, reads all data.
    
    Returns:
    DataFrame containing the sheet data.
    """
    # For Sheets we may need to impersonate for proper authorization - using default credential
    # You might need to modify this if the sheets require specific user access
    creds = get_credentials()
    
    try:
        # Method 1: Direct extraction from URL path
        if 'spreadsheets/d/' in sheets_link:
            parts = sheets_link.split('spreadsheets/d/')[1]
            spreadsheet_id = parts.split('/')[0].split('?')[0].split('#')[0]
        elif '/d/' in sheets_link:
            parts = sheets_link.split('/d/')[1]
            spreadsheet_id = parts.split('/')[0].split('?')[0].split('#')[0]
        else:
            raise ValueError(f"Could not extract spreadsheet ID from link: {sheets_link}")
        
        print(f"Extracted spreadsheet ID: {spreadsheet_id}")
        
        # Build the Sheets service
        service = build("sheets", "v4", credentials=creds)
        
        # If sheet_name is provided, we need to find its gid
        if sheet_name:
            # Get all sheet metadata first
            spreadsheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = spreadsheet_metadata.get('sheets', [])
            
            # Find the sheet by name
            sheet_found = False
            for sheet in sheets:
                properties = sheet.get('properties', {})
                if properties.get('title') == sheet_name:
                    sheet_found = True
                    range_to_read = f"'{sheet_name}'" + (f"!{range_name}" if range_name else "")
                    break
                    
            if not sheet_found:
                print(f"[Sheets] Sheet '{sheet_name}' not found. Using first sheet instead.")
                range_to_read = range_name if range_name else ""
        else:
            range_to_read = range_name if range_name else ""
        
        print("Building sheets service...")
        service = build("sheets", "v4", credentials=creds)
        print("Service built successfully")

        # Important: Make sure the Google Sheet is shared with the service account email
        # You can find this email in your service account JSON file or in the Google Cloud Console
        print("Attempting to access spreadsheet...")

        # For debugging
        try:
            info = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            print(f"Successfully connected to sheet: {info.get('properties', {}).get('title')}")
        except HttpError as e:
            print(f"Error accessing spreadsheet: {e}")
            if '404' in str(e):
                print("IMPORTANT: Make sure the spreadsheet exists and is shared with your service account email.")
                print(f"Your service account might be: {creds.service_account_email if hasattr(creds, 'service_account_email') else 'Unknown'}")
            raise

        # Check if we need to target a specific sheet
        if sheet_name:
            sheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute().get('sheets', [])
            sheet_found = False
            for sheet in sheets:
                if sheet.get('properties', {}).get('title') == sheet_name:
                    sheet_found = True
                    range_to_read = f"'{sheet_name}'" + (f"!{range_name}" if range_name else "")
                    break
                    
            if not sheet_found:
                print(f"Sheet '{sheet_name}' not found. Available sheets: {[s.get('properties', {}).get('title') for s in sheets]}")
                range_to_read = range_name if range_name else "Sheet1"
        else:
            # If no sheet name specified, use the first sheet or the range name if provided
            range_to_read = range_name if range_name else "Sheet1"

        print(f"Reading range: {range_to_read if range_to_read else 'default sheet'}")
        
        # Read the data from the sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_to_read,
            valueRenderOption="UNFORMATTED_VALUE"
        ).execute()
        
        # Extract the values
        values = result.get('values', [])
        
        if not values:
            print("[Sheets] No data found in the specified sheet.")
            return pd.DataFrame()
            
        # Convert to DataFrame - assuming first row is headers
        headers = values[0]
        data = values[1:] if len(values) > 1 else []
        
        # Pad rows with None values if they're shorter than the header row
        for row in data:
            while len(row) < len(headers):
                row.append(None)
                
        # Create the DataFrame
        df = pd.DataFrame(data, columns=headers)
        df.rename(columns={"How large do you think your solution's market is?": "How large do you think your solution's market is in Crores", "Large": "Large Competition", "Mid Size": "Mid Size Competition", "Small": "Small Competition", "Product": "How would you best describe the product status of your competition today?", "Technology": "How would you best describe the tech status of your competition today?", "India":"Within India what geography and demography is your customer in?", "US":"Within US what geography and demography is your customer in?","Urban": "In Urban what gender is your focus?", "Rural": "In Rural what gender is your focus?", "Engineering":"What is the level of R&D in Engineering required in your company?", "Product.1": "What is the level of Product R&D required in your company?", "Marketing":"How is your marketing likely to be", "Product/Service Delivery":"How is your product delivery likely to be" }, inplace=True)
        print(f"[Sheets] Successfully read {len(df)} rows from the Google Sheet")
        
        
        return df
        
    except HttpError as error:
        print(f"[Sheets] An error occurred: {error}")
        return pd.DataFrame()
    except Exception as e:
        print(f"[Sheets] An unexpected error occurred: {e}")
        return pd.DataFrame()
    

    