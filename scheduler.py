#!/usr/bin/env python3

import pandas as pd
import logging
import time
# import schedule
import sys
import os
from datetime import datetime

# Add the current directory to the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.responses_cache import get_last_processed_id, store_last_processed_id, get_all_processed_ids
from utils.google_clients import read_google_sheets
from constants import APPLICATION_ID, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME, LOCAL_FOLDER
from main import run_scoring_pipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("processing.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("application_processor")

def process_new_applications():
    """
    Process applications based on their position in the sheet.
    This function:
    1. Reads the Google Sheet to get all application IDs in their original order
    2. Gets the last processed ID from the tracking file
    3. Finds the position of the last processed ID in the sheet
    4. Processes all applications that appear at positions up to that index
    5. Updates the last processed ID with the ID of the last processed application
    
    Returns:
        int: Number of applications processed
    """
    try:
        logger.info("Starting to process applications based on sheet position")
        
        # Get the last processed ID
        last_processed_id = get_last_processed_id()
        logger.info(f"Last processed ID: {last_processed_id}")
        
        # Read the Google Sheet to get all application IDs
        try:
            filtration_df = read_google_sheets(FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME)
            logger.info(f"Successfully read Google Sheet with {len(filtration_df)} entries")
        except Exception as e:
            logger.error(f"Error reading Google Sheet: {str(e)}")
            return 0
        
        # Convert application IDs to integers
        try:
            filtration_df[APPLICATION_ID] = pd.to_numeric(filtration_df[APPLICATION_ID], errors='coerce')
            # Drop rows with invalid application IDs
            filtration_df = filtration_df.dropna(subset=[APPLICATION_ID])
            filtration_df[APPLICATION_ID] = filtration_df[APPLICATION_ID].astype(int)
            logger.info(f"Converted {len(filtration_df)} application IDs to integers")
        except Exception as e:
            logger.error(f"Error converting application IDs to integers: {str(e)}")
            return 0
        
        # Get all application IDs from the sheet in their original order
        all_app_ids = filtration_df[APPLICATION_ID].tolist()
        
        # Find the index position of the last processed ID in the sheet
        last_processed_index = -1
        
        # If last_processed_id is in the sheet, find its position
        if last_processed_id in all_app_ids:
            last_processed_index = all_app_ids.index(last_processed_id)
            logger.info(f"Found last processed ID {last_processed_id} at position {last_processed_index}")
        else:
            # If the ID isn't in the sheet, we'll process all applications
            logger.info(f"Last processed ID {last_processed_id} not found in sheet, will process all applications")
            last_processed_index = len(all_app_ids) - 1
        
        # Process all applications up to and including the last processed index
        logger.info(f"Processing all applications after position {last_processed_index}")
        
        processed_count = 0
        new_last_processed_id = last_processed_id
        
        # Process all applications with index position <= last_processed_index
        for i, app_id in enumerate(all_app_ids):
            if i >= last_processed_index:
                try:
                    logger.info(f"Processing application ID: {app_id} at position {i}")
                    run_scoring_pipeline(LOCAL_FOLDER, app_id)
                    processed_count += 1
                    
                    # Update the last processed ID to this one
                    new_last_processed_id = app_id
                    
                    logger.info(f"Successfully processed application ID: {app_id}")
                except Exception as e:
                    logger.error(f"Error processing application ID {app_id}: {str(e)}")
                    # Continue with the next application even if this one fails
        
        # Update the tracking file with the ID of the last processed application
        if new_last_processed_id != last_processed_id:
            store_last_processed_id(new_last_processed_id)
            logger.info(f"Updated last processed ID to {new_last_processed_id}")
        
        logger.info(f"Finished processing applications. Processed {processed_count} applications")
        return processed_count
        
    except Exception as e:
        logger.error(f"Error in process_new_applications: {str(e)}")
        return 0
