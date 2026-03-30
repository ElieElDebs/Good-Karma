import os
import pandas as pd

import numpy as np
from fastapi import APIRouter, Query

from App.Middleware.search import calculcate_posts_kpi_new
from App.Utils.utils import get_best_times_to_post

router = APIRouter()


@router.get("/search")
def search(
    title: str,
    body: str,
    subreddits: list[str] = Query(
        ..., description="List of subreddits to analyze", min_length=1
    ),
):
    """
    ## Description:
    Search for posts similar to the given query and analyze KPIs.

    ## Args:
        title (str): The title of the post.
        body (str): The input request body containing the query string.
        subreddits (list[str]): List of subreddits to analyze (required).

    ## Returns:
        dict: A dictionary containing status and data with KPIs, DataFrame with KPIs, and analyzed post details.
    """
    import math

    print(subreddits)

    def convert(obj):
        if isinstance(obj, np.generic):
            return obj.item()
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj
        if isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [convert(v) for v in obj]
        if isinstance(obj, tuple):
            return tuple(convert(v) for v in obj)
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
        if isinstance(obj, pd.Series):
            return obj.to_dict()
        return obj

    result = calculcate_posts_kpi_new(
        title=title,
        body=body,
        top_k=10,
        subreddits=subreddits,
        min_score=os.getenv("MIN_SCORE", None),
    )

    # Get the best time to post for the given subreddits from the json file
    best_times = get_best_times_to_post(subreddits)

    result["best_times_to_post"] = best_times

    return {"status": 200, "data": convert(result)}
