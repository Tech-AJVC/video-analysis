import pandas as pd

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


def get_company_details(filtration_details: pd.DataFrame):
    company_details = {}

    for keys in list(filtration_details.T.to_dict().keys())[-60:]:
        company_response = without_keys(filtration_details.T.to_dict()[keys], ['Enter your application number here','Share a Google Sheet/Research Report that links to your estimates', 'Submitted At', 'Token'])
        company_details[filtration_details.T.to_dict()[keys]['Share a private YouTube link to a video pitch of your company']] = company_response
    return company_details