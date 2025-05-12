import streamlit as st
import os
import json
import pandas as pd
import threading
import atexit
from utils.audio_transcribe import ensure_cache_folders
from utils.responses_cache import get_cached_response, store_response
from utils.google_clients import read_google_sheets
from constants import APPLICATION_ID, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME
from utils.filter_responses import filter_responses
from main import run_scoring_pipeline
from constants import APPLICATION_ID, VIDEO_LINK, LOCAL_FOLDER, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME, MODEL_PITCH
# Python program to show time by perf_counter() 
from time import perf_counter

# Import the background scheduler
from background_scheduler import start_background_processing, stop_background_processing

import logging

logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_title="AJVC Video Analysis",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to make the app look more professional
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 1rem;
    }
    .stButton button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #2563EB;
    }
    .response-container {
        padding: 1rem;
        border-radius: 5px;
        background-color: #F3F4F6;
        margin-bottom: 1rem;
    }
    .skill-rating {
        font-weight: bold;
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

def load_application_ids():
    """Load application IDs from the filtration sheet"""
    try:
        # Create cache folders if they don't exist
        ensure_cache_folders()
        
        # Read the filtration sheet
        df = read_google_sheets(FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME)
        
        if APPLICATION_ID in df.columns:
            app_ids = df[APPLICATION_ID].dropna().unique().tolist()
            app_ids = [str(int(id)) for id in app_ids if str(id).strip()]
            return app_ids
        else:
            st.error(f"Column '{APPLICATION_ID}' not found in sheet")
            return []
    except Exception as e:
        st.error(f"Error loading application IDs: {str(e)}")
        return []

def format_json_for_display(json_data):
    """Convert JSON to a pandas DataFrame for better display"""
    if not json_data:
        return pd.DataFrame()
    
    # For skills JSON structure
    if "Analytical" in json_data:
        rows = []
        total_score = 0
        count = 0
        
        for skill, data in json_data.items():
            rating = data.get("Rating", "N/A")
            rows.append({
                "Skill": skill,
                "Rating": rating,
                "Citations": data.get("Citations", "N/A"),
                "Reasoning": data.get("Reasoning", "N/A")
            })
            
            # Add to average calculation if rating is a number
            if isinstance(rating, (int, float)):
                total_score += rating
                count += 1
        
        # Calculate average score
        avg_score = round(total_score / count, 1) if count > 0 else "N/A"
        
        # Create DataFrame with rows
        df = pd.DataFrame(rows)
        
        # Return both DataFrame and average score
        return df, avg_score
    
    # For behavior JSON structure (assuming a different structure)
    elif "Conviction" in json_data:
        # Adjust based on actual behavior JSON structure
        rows = []
        total_score = 0
        count = 0
        
        for behavior, data in json_data.items():
            if isinstance(data, dict) and "Rating" in data:
                rating = data.get("Rating", "N/A")
                rows.append({
                    "Behavior": behavior,
                    "Rating": rating,
                    "Citations": data.get("Citations", "N/A"),
                    "Reasoning": data.get("Reasoning", "N/A")
                })
                
                # Add to average calculation if rating is a number
                if isinstance(rating, (int, float)):
                    total_score += rating
                    count += 1
        
        # Calculate average score
        avg_score = round(total_score / count, 1) if count > 0 else "N/A"
        
        # Create DataFrame with rows
        df = pd.DataFrame(rows)
        
        # Return both DataFrame and average score
        return df, avg_score
        rows = []
        for behavior, data in json_data.items():
            rows.append({
                "Behavior": behavior,
                "Rating": data.get("Rating", "N/A"),
                "Citations": data.get("Citations", "N/A"),
                "Reasoning": data.get("Reasoning", "N/A")
            })
        return pd.DataFrame(rows)
    
    # Generic fallback for any other JSON structure
    else:
        # Convert the JSON to DataFrame directly
        # This is a simplistic approach that might need adjustment
        # based on the actual structure of your JSON
        return pd.DataFrame([json_data]), "N/A"

def display_json_response(app_id, response_type):
    """Display JSON response in a neat tabular fashion using cached data from Hugging Face."""
    # Fetch data using get_cached_response
    data = get_cached_response(app_id, response_type)
    
    if data: # Check if data was successfully retrieved from cache
        st.markdown(f"<div class='section-header'>{response_type.title()} Analysis</div>", unsafe_allow_html=True)
        
        # Convert to DataFrame for display and get average score
        df, avg_score = format_json_for_display(data)
        
        # Display average score at the top with custom styling
        if avg_score != "N/A":
            st.markdown(f"""
            <div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; margin-bottom: 15px;">
                <h3 style="margin: 0; color: #1E3A8A; font-size: 18px;">Average Score: <span style="font-size: 24px; font-weight: bold;">{avg_score}/10</span></h3>
            </div>
            """, unsafe_allow_html=True)
        
        if not df.empty:
            # Apply custom styling
            if "Rating" in df.columns:
                st.dataframe(
                    df,
                    column_config={
                        "Rating": st.column_config.NumberColumn(
                            "Rating",
                            help="Score out of 10",
                            format="%d/10",
                            min_value=0,
                            max_value=10,
                        ),
                        "Citations": st.column_config.TextColumn(
                            "Citations",
                            width="large"
                        ),
                        "Reasoning": st.column_config.TextColumn(
                            "Reasoning",
                            width="large"
                        )
                    },
                    use_container_width=True
                )
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.info(f"No data to display for {response_type}")
    else:
        st.warning(f"No {response_type} analysis found for Application ID {app_id}")

def generate_analysis(app_id, local_folder=LOCAL_FOLDER):
    """Generate skill and behavior analysis for the selected application ID"""
    with st.spinner(f"Generating analysis for Application ID {app_id}..."):
        # Check if responses are already cached
        try:
            # Run the scoring pipeline
            app_id = int(app_id)
            run_scoring_pipeline(local_folder, app_id)
            st.success(f"Analysis generated for Application ID {app_id}")
        except Exception as e:
            logging.exception(f"Error generating analysis: {str(e)}")
            st.error(f"Error generating analysis: {str(e)}")

def main():
    # Initialize session state for controlling UI visibility
    
    if 'show_results' not in st.session_state:
        st.session_state.show_results = True
    
    st.markdown("<div class='main-header'>AJVC Video Analysis</div>", unsafe_allow_html=True)
    
    # Load application IDs
    app_ids = load_application_ids()
    
    # Application ID dropdown
    if app_ids:
        selected_id = st.selectbox(
            "Select Application ID",
            options=app_ids,
            index=0 if app_ids else None,
            format_func=lambda x: f"Application #{x}"
        )
        
        # Generate buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Generate Analysis", type="primary"):
                st.session_state.show_results = True
                # Start the stopwatch / counter
                t1_start = perf_counter() 
                generate_analysis(selected_id)
                # Stop the stopwatch / counter
                t1_stop = perf_counter()
                print("Elapsed time:", t1_stop - t1_start)
        
        with col2:
            if st.button("Clear"):
                # Just clear the UI by setting the flag
                st.session_state.show_results = False
                st.success("Output cleared. The cached analysis is still available.")
        
        # Display JSON responses only if show_results is True
        if selected_id and st.session_state.show_results:
            skill_tab, behavior_tab = st.tabs(["Skill Analysis", "Behavior Analysis"])
            
            with skill_tab:
                display_json_response(selected_id, "skill")
            
            with behavior_tab:
                display_json_response(selected_id, "behavior")
    else:
        st.error("No application IDs found. Please check your Google Sheets connection.")
        
        
# Initialize the background scheduler to run at 2 AM
# This runs in a separate thread and won't affect the Streamlit UI
background_scheduler = start_background_processing()

# Register the shutdown function to stop the scheduler when the app exits
atexit.register(stop_background_processing)

if __name__ == "__main__":
    main()
