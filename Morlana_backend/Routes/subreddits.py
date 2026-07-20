from App.Middleware.subreddits import get_subreddits_names
from App.Utils.security import get_api_key
from fastapi import APIRouter, Security

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
