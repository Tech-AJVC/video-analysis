"""
Utility functions for interacting with Hugging Face Datasets.
"""
import os
import logging
from huggingface_hub import HfApi, hf_hub_download, upload_file
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Constants --- #
# TODO: Replace with your actual Hugging Face Dataset repository ID
# e.g., "your_username/your_dataset_name"
DATASET_REPO_ID = "tech-ajvc/video_responses"
REPO_TYPE = "dataset"

# --- Hugging Face API Client --- #
# The HfApi client will automatically use the HF_TOKEN environment variable if set.
HF_TOKEN = os.getenv("HF_TOKEN")
api = HfApi(token=HF_TOKEN)


def upload_file_to_hf_dataset(local_file_path: str, path_in_repo: str, repo_id: str = DATASET_REPO_ID):
    """
    Uploads a local file to a specified path in a Hugging Face Dataset repository.

    Args:
        local_file_path (str): The path to the local file to upload.
        path_in_repo (str): The desired path (including filename) in the Hugging Face repository.
        repo_id (str): The Hugging Face repository ID (e.g., 'username/dataset_name').
                           Defaults to DATASET_REPO_ID.

    Returns:
        str: The URL of the uploaded file in the repository, or None if upload failed.
    """
    if not os.path.exists(local_file_path):
        logger.error(f"Local file not found: {local_file_path}")
        return None

    try:
        logger.info(f"Uploading {local_file_path} to {repo_id}/{path_in_repo}...")
        response = upload_file(
            path_or_fileobj=local_file_path,
            path_in_repo=path_in_repo,
            repo_id=repo_id,
            repo_type=REPO_TYPE,
            token=HF_TOKEN  # Explicitly pass the token
        )
        logger.info(f"Successfully uploaded {local_file_path} to {response}")
        return response  # response is the URL of the uploaded file
    except Exception as e:
        logger.error(f"Failed to upload {local_file_path} to {repo_id}: {e}")
        return None


def download_file_from_hf_dataset(path_in_repo: str, local_destination_path: str, repo_id: str = DATASET_REPO_ID):
    """
    Downloads a file from a Hugging Face Dataset repository to a local path.

    Args:
        path_in_repo (str): The path (including filename) of the file in the Hugging Face repository.
        local_destination_path (str): The local path where the file should be saved.
        repo_id (str): The Hugging Face repository ID (e.g., 'username/dataset_name').
                           Defaults to DATASET_REPO_ID.

    Returns:
        str: The local path to the downloaded file, or None if download failed.
    """
    try:
        logger.info(f"Downloading {repo_id}/{path_in_repo} to {local_destination_path}...")
        downloaded_file_path = hf_hub_download(
            repo_id=repo_id,
            filename=path_in_repo,
            repo_type=REPO_TYPE,
            local_dir=os.path.dirname(local_destination_path),
            local_dir_use_symlinks=False,  # To ensure the file is actually downloaded
            token=HF_TOKEN  # Explicitly pass the token
        )

        # hf_hub_download might save with a different name if revisions/cache are involved.
        # We want to ensure it's at the exact local_destination_path.
        # However, the best practice is to use the path returned by hf_hub_download.
        # For simplicity and direct control, we can rename/move if needed,
        # but let's first check if the dirname matches.

        final_path = os.path.join(os.path.dirname(local_destination_path), os.path.basename(path_in_repo))
        if downloaded_file_path != final_path:
            # If hf_hub_download saved it to a specific cache structure, move/rename it to the desired path.
            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(final_path), exist_ok=True)
            os.rename(downloaded_file_path, final_path)
            logger.info(f"File moved from {downloaded_file_path} to {final_path}")
            downloaded_file_path = final_path

        logger.info(f"Successfully downloaded {path_in_repo} to {downloaded_file_path}")
        return downloaded_file_path
    except Exception as e:
        logger.error(f"Failed to download {path_in_repo} from {repo_id}: {e}")
        # Clean up potentially partially downloaded file if local_destination_path exists and is empty or error-related
        # For now, we'll just log the error.
        return None


if __name__ == '__main__':
    # Example Usage (requires a valid DATASET_REPO_ID and a dummy file):
    logger.info("Testing Hugging Face Utils...")

    # --- Create a dummy file for testing upload --- #
    DUMMY_FILE_NAME = "/Users/abhinavbhatnagar/Documents/Compliance/video-analysis/responses/1019_responses_behavior.json"
    DUMMY_FILE_CONTENT = "."
    # with open(DUMMY_FILE_NAME, "w") as f:
    #     f.write(DUMMY_FILE_CONTENT)
    # logger.info(f"Created dummy file: {DUMMY_FILE_NAME}")

    # --- Test Upload --- #
    # Ensure DATASET_REPO_ID is correctly set in the constants above
    # And that you have write permissions (HF_TOKEN with write access)
    if DATASET_REPO_ID == "USER_HF_USERNAME/DATASET_NAME":
        logger.warning(
            "Please update DATASET_REPO_ID in hf_utils.py with your actual Hugging Face Dataset repository ID to test.")
    else:
        file_basename_for_repo = os.path.basename(DUMMY_FILE_NAME)
        repo_path_for_dummy_file = f"{file_basename_for_repo}"

        uploaded_file_url = upload_file_to_hf_dataset(DUMMY_FILE_NAME, repo_path_for_dummy_file)
        if uploaded_file_url:
            logger.info(f"Upload test successful. File URL: {uploaded_file_url}")

            # --- Test Download --- #
            # Ensure the destination directory exists if it's not the current directory or a predefined one.
            # For this test, we'll download to the 'responses' directory.
            responses_dir = "responses"
            os.makedirs(responses_dir, exist_ok=True)  # Ensure responses directory exists
            DOWNLOAD_DESTINATION = os.path.join(responses_dir, file_basename_for_repo)

            downloaded_path = download_file_from_hf_dataset(repo_path_for_dummy_file, DOWNLOAD_DESTINATION)
            if downloaded_path and os.path.exists(downloaded_path):
                logger.info(f"Download test successful. File saved to: {downloaded_path}")
                with open(downloaded_path, "r") as f_read:
                    content = f_read.read()
                    print(content)
                # os.remove(downloaded_path)  # Clean up downloaded file
            else:
                logger.error("Download test failed.")
        else:
            logger.error("Upload test failed, skipping download test.")

    # --- Clean up dummy file --- #
    # if os.path.exists(DUMMY_FILE_NAME):
    #     os.remove(DUMMY_FILE_NAME)
    #     logger.info(f"Cleaned up dummy file: {DUMMY_FILE_NAME}")

    logger.info("Hugging Face Utils testing finished.")
