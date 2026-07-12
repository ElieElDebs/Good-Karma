import json
from fastapi import APIRouter, Security
from pydantic import BaseModel

from App.Utils.security import get_api_key
from App.Utils.prompt.prompt import REWRITE_PROMPT
from App.Utils.llm import ask_model

router = APIRouter()


class RewriteRequest(BaseModel):
    subreddit: str
    draft_title: str
    draft_body: str
    weakness_and_strength: str
    advices: str
    examples: str
    ideal_title_length: str
    ideal_words_to_use: str


@router.post("/rewrite", dependencies=[Security(get_api_key)])
def rewrite_post(request: RewriteRequest):
    """
    Enhance post using AI based on analysis data.

    Accepts POST request with JSON body containing:
    - subreddit: target subreddit name
    - draft_title: current post title
    - draft_body: current post body
    - weakness_and_strength: JSON string with GES scores
    - advices: pipe-separated improvement suggestions
    - examples: JSON string with reference posts
    - ideal_title_length: recommended title length
    - ideal_words_to_use: comma-separated keywords

    Returns:
        dict: {"status": 200, "data": {"title": "...", "body": "..."}}
    """

    prompt = REWRITE_PROMPT.format(
        draft_title=request.draft_title,
        draft_body=request.draft_body,
        weakness_and_strength=request.weakness_and_strength,
        advices=request.advices,
        examples=request.examples,
        subreddit=request.subreddit,
        ideal_title_length=request.ideal_title_length,
        ideal_words_to_use=request.ideal_words_to_use,
    )

    response = ask_model(query=prompt)

    # Extract text from response tuple structure
    # response[1] is the Message object, content[0] is a dict with 'text' key
    try:
        result_text = response[1].content[0]["text"]
    except (IndexError, KeyError, TypeError):
        # Fallback if structure is different
        try:
            result_text = response[1].content[0].text
        except (AttributeError, TypeError):
            result_text = str(response)

    # Parse the JSON response from the LLM
    try:
        parsed_result = json.loads(result_text)
        return {
            "status": 200,
            "data": {
                "title": parsed_result.get("title", ""),
                "body": parsed_result.get("body", ""),
            },
        }
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse LLM JSON response: {e}")
        print(f"Raw response: {result_text}")
        return {
            "status": 400,
            "error": "Failed to parse LLM response as JSON",
            "data": {"title": "", "body": result_text},
        }
