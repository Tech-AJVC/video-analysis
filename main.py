from utils.google_clients import download_drive_file, read_google_sheets
from utils.audio_transcribe import convert_file_mp3, get_video_transcription
from utils.filter_responses import filter_responses

from constants import APPLICATION_ID, VIDEO_LINK, LOCAL_FOLDER, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME, MODEL_PITCH
from prompts.behavior_prompts import behavior_system_prompt, behavior_user_prompt
from prompts.skill_prompts import skill_system_prompt, skill_user_prompt
from utils.openai_llm import get_response_from_openai
from utils.responses_cache import get_cached_response, store_response
import logging
import json

logging.basicConfig(level=logging.INFO)

def run_scoring_pipeline(local_directory, id):
    filtration_df = read_google_sheets(FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME)
    company_details = filter_responses(id, filtration_df)
    application_id(id, filtration_df, local_directory)
    convert_file_mp3(local_directory, id)
    transcript_dict = get_video_transcription(local_directory, id)

    if get_cached_response(id, "behavior") is not None:
        behavior_response_json = get_cached_response(id, "behavior")
    else:
        behavior_system_prompt_formatted = behavior_system_prompt.format(model_pitch=MODEL_PITCH, company_details= company_details)
        print(transcript_dict)
        behavior_user_prompt_formatted = behavior_user_prompt.format(transcript=transcript_dict[str(id)])
        behavior_response = get_response_from_openai(behavior_system_prompt_formatted, behavior_user_prompt_formatted)
        behavior_response_json = json.loads(behavior_response)
        store_response(id, behavior_response_json, "behavior")
        print(behavior_response_json)

    if get_cached_response(id, "skill") is not None:
        skill_response_json = get_cached_response(id, "skill")
    else:
        skill_system_prompt_formatted = skill_system_prompt.format(model_pitch=MODEL_PITCH, company_details= company_details)
        skill_user_prompt_formatted = skill_user_prompt.format(transcript=transcript_dict[str(id)])
        skill_response = get_response_from_openai(skill_system_prompt_formatted, skill_user_prompt_formatted)
        skill_response_json = json.loads(skill_response)
        store_response(id, skill_response_json, "skill")
        print(skill_response_json)
    return behavior_response_json, skill_response_json
    
def application_id(id, filtration_df, local_directory):  
    print(filtration_df[filtration_df[APPLICATION_ID]==id])
    drive_link = filtration_df[filtration_df[APPLICATION_ID]==id][VIDEO_LINK].values[0]
    print(drive_link)
    if "drive.google.com" in drive_link:
        download_drive_file(id, drive_link, local_directory)
    else:
        logging.error("Non-drive link cannot process video")
        raise ValueError("Non-drive link cannot process video")

if __name__ == "__main__":
    run_scoring_pipeline(LOCAL_FOLDER, 688)