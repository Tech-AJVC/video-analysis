from constants import APPLICATION_ID, VIDEO_LINK, LOCAL_FOLDER, FILTRATION_SHEET_LINK, FILTRATION_SHEET_NAME, GOOGLE_SHEET_ESTIMATES, SUBMITTED_AT, TOKEN
import pandas as pd

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

def filter_responses(id: str, filtration_details: pd.DataFrame):
    company_details = {}
    filtration_id_key = list(filtration_details[filtration_details[APPLICATION_ID]==id].T.to_dict().keys())[0]
    filtration_id = filtration_details[filtration_details[APPLICATION_ID]==id].T.to_dict()[filtration_id_key]
    company_response = without_keys(filtration_id, [APPLICATION_ID,GOOGLE_SHEET_ESTIMATES ,SUBMITTED_AT, TOKEN])
    # return company_response
    return format_company_response(company_response)

def format_company_response(company_response):
    """
    Format the company response to be more readable for the LLM
    
    Args:
        company_response: Original company response dictionary
        
    Returns:
        str: A formatted string with clear sections and readable text
    """
    # Create a structured format with sections
    formatted_text = "COMPANY PROFILE\n" + "=" * 50 + "\n\n"
    
    # Basic Company Info section
    formatted_text += "Basic Information:\n" + "-" * 20 + "\n"
    
    # Extract vision and mission first if they exist
    if "What is your vision for the company?" in company_response:
        formatted_text += f"Vision: {company_response.get('What is your vision for the company?')}\n\n"
    
    if "What is the greater mission beyond building a profitable business?" in company_response:
        formatted_text += f"Mission: {company_response.get('What is the greater mission beyond building a profitable business?')}\n\n"
    
    if "Describe your solution in detail" in company_response:
        formatted_text += f"Solution: {company_response.get('Describe your solution in detail')}\n\n"
    
    # Market Information
    formatted_text += "\nMarket Information:\n" + "-" * 20 + "\n"
    market_fields = [
        "How large do you think your solution's market is in Crores",
        "What do you think will be the contribution margin % of the business in 5 years?",
        "Large Competition", 
        "Mid Size Competition", 
        "Small Competition",
        "What is the market share of the 3 largest competitors?",
        "How would you best describe the product status of your competition today?",
        "How would you best describe the tech status of your competition today?"
    ]
    
    for field in market_fields:
        if field in company_response and company_response[field]:
            formatted_text += f"{field}: {company_response[field]}\n"
    
    # Customer Information
    formatted_text += "\nCustomer Information:\n" + "-" * 20 + "\n"
    customer_fields = [
        "What is your customer type?",
        "Within India what geography and demography is your customer in?",
        "What business size are you focused on?",
        "Which sectors are your customers in?",
        "What is the annual pricing of your product?",
        "In Urban what gender is your focus?",
        "In Rural what gender is your focus?",
        "Choose your target age group",
        "What is the target group's income level?",
        "How much of their annual income could they spend on your product?"
    ]
    
    for field in customer_fields:
        if field in company_response and company_response[field]:
            formatted_text += f"{field}: {company_response[field]}\n"
    
    # Team Skills and Traits
    formatted_text += "\nTeam Skills and Traits:\n" + "-" * 20 + "\n"
    
    # # Skills section
    skills = [
        "Analytical", "Communication", "Judgement", "Negotiation", "Problem Solving",
        "Financial", "Technical", "Sales and Marketing", "Project Management", "Network Building", "Product Management"
    ]
    
    formatted_text += "Skills (rated 1-5):\n"
    for skill in skills:
        if skill in company_response and company_response[skill]:
            formatted_text += f"- {skill}: {company_response[skill]}\n"
    
    # Traits section
    traits = [
        "Conviction/Belief", "Relentlessness", "Resilience", "Curiosity", "Reliability",
        "Courage", "Innovative", "Energetic", "Inspiring", "Clear Thinking", "Pace of Execution"
    ]
    
    formatted_text += "\nTraits (rated 1-5):\n"
    for trait in traits:
        if trait in company_response and company_response[trait]:
            formatted_text += f"- {trait}: {company_response[trait]}\n"
    
    # Product Information
    formatted_text += "\nProduct Information:\n" + "-" * 20 + "\n"
    product_fields = [
        "What will your product require to be used?",
        "How many potential users are available for your product?",
        "What is the level of R&D in Engineering required in your company?",
        "Intellectual Property",
        "What is your expected Gross Margin?",
        "How is your marketing likely to be",
        "How is your product delivery likely to be"
    ]
    
    for field in product_fields:
        if field in company_response and company_response[field]:
            formatted_text += f"{field}: {company_response[field]}\n"
    
    # Team Background
    formatted_text += "\nTeam Background:\n" + "-" * 20 + "\n"
    background_fields = [
        "What is your biggest success and why?",
        "What is your biggest failure and why?",
        "What is a new concept you learnt recently?",
        "What have you built before as a team?",
        "Describe your progress with potential customers"
    ]
    
    for field in background_fields:
        if field in company_response and company_response[field]:
            formatted_text += f"{field}:\n{company_response[field]}\n\n"
    
    # Include any remaining fields that weren't categorized
    remaining_fields = set(company_response.keys()) - set(
        market_fields + customer_fields + skills + traits + product_fields + background_fields + 
        ["What is your vision for the company?", "What is the greater mission beyond building a profitable business?", "Describe your solution in detail"]
    )
    remaining_fields = set(company_response.keys()) - set(
    market_fields + customer_fields + product_fields + background_fields + 
    ["What is your vision for the company?", "What is the greater mission beyond building a profitable business?", "Describe your solution in detail"]
)
    
    if remaining_fields:
        formatted_text += "\nAdditional Information:\n" + "-" * 20 + "\n"
        for field in remaining_fields:
            if company_response[field]:
                formatted_text += f"{field}: {company_response[field]}\n"
    
    return formatted_text