import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

def get_response_from_openai(system_prompt: str, user_prompt: str, model_name: str = "gpt-4.1-mini") -> str:

    open_ai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=open_ai_api_key)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return response.choices[0].message.content