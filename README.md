# AJVC Video Analysis

A tool for analyzing video pitches and generating skill and behavior assessments.

## Local Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Ensure you have ffmpeg installed (required for audio processing):
   - On macOS: `brew install ffmpeg`
   - On Ubuntu: `sudo apt-get install ffmpeg`

3. Run the Streamlit app:
   ```
   python3 -m streamlit run app.py
   ```

## Features

- Automatically downloads videos from Google Drive
- Transcribes video content using OpenAI's transcription API
- Analyzes founder pitches based on skills and behaviors
- Caches MP3 files, transcriptions, and analysis results for efficiency
- Provides a user-friendly interface for interacting with the analysis pipeline

## Hugging Face Spaces Deployment

To deploy this app to Hugging Face Spaces:

1. Create a new Space on [Hugging Face](https://huggingface.co/spaces)
2. Choose "Streamlit" as the SDK
3. Upload your code to the Space repository
4. Ensure the following files are included:
   - app.py
   - requirements.txt
   - All required utility modules
   - Credentials for Google APIs

## Directory Structure

- `app.py`: Streamlit application for UI
- `main.py`: Main pipeline for video analysis
- `utils/`: Utility functions
  - `audio_transcribe.py`: Functions for audio transcription and caching
  - `google_clients.py`: Google Drive and Sheets API clients
  - `filter_responses.py`: Functions for filtering and processing responses
  - `openai_llm.py`: OpenAI API integration
- `responses/`: Cached analysis results
- `transcriptions/`: Cached transcriptions
- `videos/`: Downloaded video files
