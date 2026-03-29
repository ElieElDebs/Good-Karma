from fastapi import APIRouter
from App.Middleware.subreddits import get_subreddits_names

router = APIRouter()

@router.get("/subreddits")
def get_subreddits():
    """
    ## Description:
    Retrieve a list of available subreddits.

    ## Returns:
        dict: A dictionary containing status and a list of subreddits.
    """
    subreddits = get_subreddits_names()

    return {
        "status": 200,
        "data": {
            "subreddits": subreddits
        }
    }