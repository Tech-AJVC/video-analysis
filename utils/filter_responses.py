from constants import APPLICATION_ID, VIDEO_LINK, LOCAL_FOLDER, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME, GOOGLE_SHEET_ESTIMATES, SUBMITTED_AT, TOKEN
import pandas as pd

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def filter_responses(id: str, filtration_details: pd.DataFrame):
    company_details = {}
    filtration_id_key = list(filtration_details[filtration_details[APPLICATION_ID]==id].T.to_dict().keys())[0]
    filtration_id = filtration_details[filtration_details[APPLICATION_ID]==id].T.to_dict()[filtration_id_key]
    company_response = without_keys(filtration_id, [APPLICATION_ID,GOOGLE_SHEET_ESTIMATES ,SUBMITTED_AT, TOKEN])
    return company_response