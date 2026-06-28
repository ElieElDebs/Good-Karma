from fastapi import APIRouter, Security

from App.Middleware.subreddits import get_subreddits_names
from Morlana_backend.App.Utils.security import get_api_key

router = APIRouter()


@router.get("/subreddits", dependencies=[Security(get_api_key)])
def get_subreddits():
    """
    ## Description:
    Retrieve a list of available subreddits.

    ## Returns:
        dict: A dictionary containing status and a list of subreddits.
    """
    subreddits = get_subreddits_names()

    return {"status": 200, "data": {"subreddits": subreddits}}
