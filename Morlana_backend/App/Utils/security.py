import os

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-KEY")

API_KEY = os.getenv("API_KEY")


def get_api_key(api_key: str = Security(api_key_header)):
    """
    Validate the API key provided in the request header.

    Args:
        api_key (str): The API key provided in the request header.

    Raises:
        HTTPException: If the provided API key is invalid.

    Returns:
        str: The valid API key.
    """
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    return api_key
