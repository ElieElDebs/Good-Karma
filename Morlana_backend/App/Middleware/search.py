import pandas as pd
import os

import App.Database.qdrant as qdrant
from App.Utils.kpi import (
    calculate_body_kpi,
    calculate_titles_kpi,
    calculate_GES,
    calculate_GES_new,
)
from App.Utils.utils import preprocess_text
from qdrant_client.http.models import Filter, FieldCondition, MatchValue


def _search_similar_posts_new(
    query: str, top_k: int = 5, subreddits: list = None, min_score: float = None
) -> dict[str, pd.DataFrame]:
    """
    Search for posts in the database in regards of the given subreddits names and the query.
    only fetch successful posts.

    Args:
        query (str): The input query string.
        top_k (int): The number of top similar posts to retrieve.
        subreddits (list, optional): List of subreddits to filter the searchy results.
                                     If None, no filtering is applied.

    Returns:
        A dictionary with subreddit names as keys and DataFrames of posts as values.
    """

    if qdrant.MODEL is None or qdrant.CLIENT is None:
        raise Exception(
            "Qdrant client or model not initialized. Call initialize_qdrant_client and initialize_model first."
        )

    results_by_subreddit = {}

    for subreddit in subreddits:
        successful_filter = Filter(
            must=[
                FieldCondition(
                    key="subreddit",
                    match=MatchValue(value=subreddit),
                )
            ]
        )

        results = qdrant.search_embeddings(
            collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
            query=query,
            top_k=top_k,
            filter=successful_filter,
        )

        # Transform the content of EACH PAYLOAD TO Dataframe
        df = pd.DataFrame([r["payload"] for r in results])
        df["score"] = [r["score"] for r in results]

        results_by_subreddit[subreddit] = df

    return results_by_subreddit


def calculcate_posts_kpi_new(
    title: str, body: str, top_k: int, subreddits: list = None, min_score: float = None
) -> dict[str, any]:
    """
    Calcultate returned Posts kpi for each subreddit

    Args:
        title (str): The title of the post.
        body (str): The body content of the post.
        top_k (int): The number of top similar posts to consider for KPI calculation.
        subreddits (list, optional): List of subreddits to filter the searchy results.
                                     If None, no filtering is applied.
        min_score (float): Minimum score threshold for filtering similar posts.

    Returns:
        dict[str | any]: A dictionary containing KPIs and advice for each subreddit.
    """

    # Step 1 : Preprocess the input titmle and the input body
    preprocessed_title = preprocess_text(title)
    preprocessed_body = preprocess_text(body)

    # Step 2 : Create the query by combining the preprocessed title and body
    query = f"{preprocessed_title} {preprocessed_title} {preprocessed_title} \n\n {preprocessed_body}"

    # Step 3 : Search for similar posts
    posts_by_subreddit = _search_similar_posts_new(
        query=query, top_k=top_k, subreddits=subreddits, min_score=min_score
    )

    api_response: dict[str, any] = {}
    subreddits_kpi_dict: dict[str, any] = {}

    # Prepare posts_by_subreddit for API response (list of dicts per subreddit)
    posts_by_subreddit_api = {}
    for subreddit, posts in posts_by_subreddit.items():
        posts_by_subreddit_api[subreddit] = (
            posts.to_dict(orient="records") if not posts.empty else []
        )

        # Step 4 : Calculate KPIs for posts in the subreddit
        title_posts_kpi = calculate_titles_kpi(posts, text_column="preprocessed_title")
        b_global_kpis, posts_with_kpi = calculate_body_kpi(
            posts, text_column="preprocessed_text"
        )

        subreddits_kpi_dict[subreddit] = {
            "global_title_kpi": title_posts_kpi,
            "global_body_kpi": b_global_kpis,
            "posts_with_kpi": posts_with_kpi,
        }

    api_response["kpi_by_subreddit"] = subreddits_kpi_dict

    # Step 5 : Calculate Draft KPI for the input post
    draft_post = pd.DataFrame(
        [
            {
                "title": title,
                "text": body,
                "preprocessed_title": preprocessed_title,
                "preprocessed_text": preprocessed_body,
            }
        ]
    )
    draft_title_kpi = calculate_titles_kpi(draft_post, text_column="preprocessed_title")
    draft_body_kpi, _ = calculate_body_kpi(draft_post, text_column="preprocessed_text")

    api_response["draft_post_kpi"] = {
        "title_kpi": draft_title_kpi,
        "body_kpi": draft_body_kpi,
    }

    # Step 6 : Calculate GES for each subreddit
    ges_results = {}
    for subreddit in posts_by_subreddit.keys():
        ges_input = {
            "data": {
                "draft_post": api_response["draft_post_kpi"],
                "successful_posts": subreddits_kpi_dict[subreddit],
                "orignal_draft_text": body,
                "orignal_draft_title": title,
                "cleaned_draft_text": preprocessed_body,
                "cleaned_draft_title": preprocessed_title,
            }
        }

        ges_result, advice_list = calculate_GES_new(ges_input)

        ges_results[subreddit] = {
            "GES": {
                "score": ges_result["score_ges"],
                "label": ges_result["label"],
                "factors": ges_result["factors"],
            },
            "advice": advice_list,
        }

    api_response["ges_results"] = ges_results

    # Ajout des posts utilisés pour l'analyse, formaté par subreddit
    api_response["posts_by_subreddit"] = posts_by_subreddit_api

    return api_response


def _search_similar_posts(
    query: str, top_k: int = 5, subreddits: list = None, min_score: float = None
) -> tuple[dict, pd.DataFrame]:
    """
    Search for posts similar to the given query.

    Args:
        query (str): The input query string.
        top_k (int): The number of top similar posts to retrieve.
        subreddits (list, optional): List of subreddits to filter the searchy results.
                                     If None, no filtering is applied.

    Returns:
        tuple[dict, pd.DataFrame]: A tuple containing a dictionary of KPIs and a DataFrame with post details.
    """
    if qdrant.MODEL is None or qdrant.CLIENT is None:
        raise Exception(
            "Qdrant client or model not initialized. Call initialize_qdrant_client and initialize_model first."
        )

    successful_filter = Filter(
        must=[
            FieldCondition(
                key="type",
                match=MatchValue(value="successful"),
            )
        ]
    )

    unsuccessful_filter = Filter(
        must=[
            FieldCondition(
                key="type",
                match=MatchValue(value="unsuccessful"),
            )
        ]
    )
    results = qdrant.search_embeddings(
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        query=query,
        top_k=top_k,
        filter=successful_filter,
    )

    print(results)

    # Transform the content of EACH PAYLOAD TO Dataframe
    df = pd.DataFrame([r["payload"] for r in results])
    df["score"] = [r["score"] for r in results]

    results_unsuccessful = qdrant.search_embeddings(
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"),
        query=query,
        top_k=top_k,
        filter=unsuccessful_filter,
    )

    # Transform the content of EACH PAYLOAD TO Dataframe
    df_uns = pd.DataFrame([r["payload"] for r in results_unsuccessful])
    df_uns["score"] = [r["score"] for r in results_unsuccessful]

    if min_score is not None and min_score > 0 and min_score <= 1:
        df = df[df["score"] >= min_score].reset_index(drop=True)
        df_uns = df_uns[df_uns["score"] >= min_score].reset_index(drop=True)

    return df, df_uns


def calculcate_posts_kpi(
    title: str, body: str, top_k: int, min_score: float = None
) -> dict[str, any]:
    """
    Calcultate returned Posts kpi

    Args:
        title (str): The title of the post.
        body (str): The body content of the post.
        top_k (int): The number of top similar posts to consider for KPI calculation.
        min_score (float): Minimum score threshold for filtering similar posts.

    Returns:
        dict[str | any]: A dictionary containing KPIs and advice.
    """

    # Step 1 : Preprocess the input titmle and the input body
    preprocessed_title = preprocess_text(title)
    preprocessed_body = preprocess_text(body)

    # Step 2 : Create the query by combining the preprocessed title and body
    query = f"{preprocessed_title} {preprocessed_title} {preprocessed_title} \n\n {preprocessed_body}"

    # Step 3 : Search for similar posts
    s_posts, u_posts = _search_similar_posts(
        query=query, top_k=top_k, min_score=min_score
    )

    api_response: dict[str, any] = {
        "successful_posts": "",
        "unsuccessful_posts": "",
        "draft_post": "",
        "advice": "",
    }

    # Step 3 : Calculate KPIs for successful posts
    successful_title_posts_kpi = calculate_titles_kpi(
        s_posts, text_column="preprocessed_title"
    )
    s_b_global_kpis, s_posts_with_kpi = calculate_body_kpi(
        s_posts, text_column="preprocessed_text"
    )

    api_response["successful_posts"] = {
        "global_title_kpi": successful_title_posts_kpi,
        "global_body_kpi": s_b_global_kpis,
        "posts_with_kpi": s_posts_with_kpi,
    }

    # Step 5 : Calculate Draft KPI for the input post
    draft_post = pd.DataFrame(
        [
            {
                "title": title,
                "text": body,
                "preprocessed_title": preprocessed_title,
                "preprocessed_text": preprocessed_body,
            }
        ]
    )

    draft_title_kpi = calculate_titles_kpi(draft_post, text_column="preprocessed_title")
    draft_body_kpi, _ = calculate_body_kpi(draft_post, text_column="preprocessed_text")

    api_response["draft_post"] = {
        "title_kpi": draft_title_kpi,
        "body_kpi": draft_body_kpi,
    }

    # Step 6 : Calculate GES
    ges_result, advice_list = calculate_GES({"data": api_response})

    api_response["GES"] = {
        "score": ges_result["score_ges"],
        "label": ges_result["label"],
        "factors": ges_result["factors"],
    }

    api_response["advice"] = advice_list

    return api_response
