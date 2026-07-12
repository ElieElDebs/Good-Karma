from fastapi import APIRouter, Security

from App.Utils.security import get_api_key

from App.Utils.prompt.prompt import REWRITE_PROMPT

router = APIRouter()


@router.get("/rewrite", dependencies=[Security(get_api_key)])
def rewrite_post(
    subreddit: str,
    draft_title: str,
    draft_body: str,
    weakness_and_strength: str,
    advices: str,
    examples: str,
    ideal_title_length: str,
    ideal_words_to_use: str,
):
    """
    ## Description:
    Enhance post using

    ## Returns:
        dict: A dictionary containing status and a list of subreddits.
    """
    # subreddits = get_subreddits_names()

    prompt = REWRITE_PROMPT.format(
        draft_title=draft_title,
        draft_body=draft_body,
        weakness_and_strength=weakness_and_strength,
        advices=advices,
        examples=examples,
        subreddit=subreddit,
        ideal_title_length=ideal_title_length,
        ideal_words_to_use=ideal_words_to_use,
    )

    return {"status": 200, "data": {"prompt": prompt}}
