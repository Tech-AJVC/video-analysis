import streamlit as st
import os
import json
import pandas as pd
from utils.audio_transcribe import ensure_cache_folders
from utils.responses_cache import get_cached_response, store_response
from utils.google_clients import read_google_sheets
from constants import APPLICATION_ID, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME
from utils.filter_responses import filter_responses
from main import run_scoring_pipeline
from constants import APPLICATION_ID, VIDEO_LINK, LOCAL_FOLDER, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME, MODEL_PITCH

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
        for skill, data in json_data.items():
            rows.append({
                "Skill": skill,
                "Rating": data.get("Rating", "N/A"),
                "Reasoning": data.get("Reasoning", "N/A")
            })
        return pd.DataFrame(rows)
    
    # For behavior JSON structure (assuming a different structure)
    elif "Conviction" in json_data:
        # Adjust based on actual behavior JSON structure
        rows = []
        for behavior, data in json_data.items():
            rows.append({
                "Behavior": behavior,
                "Rating": data.get("Rating", "N/A"),
                "Reasoning": data.get("Reasoning", "N/A")
            })
        return pd.DataFrame(rows)
    
    # Generic fallback for any other JSON structure
    else:
        # Convert the JSON to DataFrame directly
        # This is a simplistic approach that might need adjustment
        # based on the actual structure of your JSON
        return pd.DataFrame([json_data])

def display_json_response(app_id, response_type):
    """Display JSON response in a neat tabular fashion"""
    filename = f"{app_id}_responses_{response_type}.json"
    filepath = os.path.join("responses", filename)
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        st.markdown(f"<div class='section-header'>{response_type.title()} Analysis</div>", unsafe_allow_html=True)
        
        # Convert to DataFrame for display
        df = format_json_for_display(data)
        
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
            st.error(f"Error generating analysis: {str(e)}")

def main():
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
                generate_analysis(selected_id)
        
        with col2:
            if st.button("Clear"):
                # Generate new analysis
                generate_analysis(selected_id)
        
        # Display JSON responses
        if selected_id:
            skill_tab, behavior_tab = st.tabs(["Skill Analysis", "Behavior Analysis"])
            
            with skill_tab:
                display_json_response(selected_id, "skill")
            
            with behavior_tab:
                display_json_response(selected_id, "behavior")
    else:
        st.error("No application IDs found. Please check your Google Sheets connection.")
        
        
if __name__ == "__main__":
    main()
