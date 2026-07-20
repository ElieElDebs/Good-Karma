"""
This script handles posts fetching from Reddit and adding their embeddings to the Qdrant database.
"""

import os
import random
import time

import pandas as pd
from App.Database.qdrant import add_embeddings
from App.Utils.Reddit import RedditScrapper
from App.Utils.utils import convert_to_uuids, preprocess_text

FETCHER = None


def init_reddit_fetcher() -> RedditScrapper:
    """
    Initializes the Reddit fetcher.

    Returns:
        RedditFetcher: An instance of RedditFetcher.
    """

    global FETCHER

    if FETCHER is None:
        FETCHER = RedditScrapper()

    return FETCHER


# TODO: Delete this function To Delete, we dont fetch unseccessful posts
def fetch_unsuccessful_posts(
    threshold_configuration: list[dict] = None,
) -> pd.DataFrame:
    """
    Fetch posts from 'new' that are older than min_age_days and have less than max_upvotes and max_comments.

    Args:
        threshold_configuration (list[dict], optional): List of dicts defining upvote and comment thresholds per subreddit.

    Returns:
        pd.DataFrame: DataFrame containing the fetched posts.
    """

    if FETCHER is None:
        raise Exception(
            "Reddit fetcher not initialized. Call __init_reddit_fetcher first."
        )

    for config in threshold_configuration:

        subreddit_name: str = list(config.keys())[0]
        max_upvotes: int = config.get(subreddit_name, {}).get("max_upvotes", 5)
        max_comments: int = config.get(subreddit_name, {}).get("max_comments", 2)

        posts = FETCHER.fetch_unsuccessful_posts(
            subreddit=subreddit_name,
            max_upvotes=max_upvotes,
            max_comments=max_comments,
            min_age_days=1,
        )

    return pd.DataFrame(posts)


def fetch_hot_posts(threshold_configuration: list[dict] = None) -> pd.DataFrame:
    """
    Fetch hot posts from specified subreddits based on the given threshold configuration.

    Args:
        threshold_configuration (list[dict], optional): List of dicts defining upvote and comment thresholds per subreddit.

    Returns:
        pd.DataFrame: DataFrame containing the fetched posts.
    """

    if FETCHER is None:
        raise Exception(
            "Reddit fetcher not initialized. Call __init_reddit_fetcher first."
        )

    if not isinstance(threshold_configuration, list):
        raise TypeError("Threshold configuration must be a list.")

    all_posts: list[dict] = []

    for config in threshold_configuration:

        subreddit_name: str = list(config.keys())[0]
        min_upvotes: int = config.get(subreddit_name, {}).get("min_upvotes", 1000)
        min_comments: int = config.get(subreddit_name, {}).get("min_comments", 1000)

        posts = FETCHER.fetch_hot_posts(
            subreddit=subreddit_name,
            number_of_upvotes=min_upvotes,
            number_comment_threshold=min_comments,
        )

        all_posts.extend(posts)

    return pd.DataFrame(all_posts)


def fetch_rising_posts(threshold_configuration: list[dict] = None) -> pd.DataFrame:
    """
    Fetch rising posts from specified subreddits based on the given threshold configuration.

    Args:
        threshold_configuration (list[dict], optional): List of dicts defining upvote and comment thresholds per subreddit.

    Returns:
        pd.DataFrame: DataFrame containing the fetched posts.
    """

    if FETCHER is None:
        raise Exception(
            "Reddit fetcher not initialized. Call __init_reddit_fetcher first."
        )

    if not isinstance(threshold_configuration, list):
        raise TypeError("Threshold configuration must be a list.")

    all_posts: list[dict] = []

    for config in threshold_configuration:

        subreddit_name: str = list(config.keys())[0]
        min_upvotes: int = config.get(subreddit_name, {}).get("min_upvotes", 1000)
        min_comments: int = config.get(subreddit_name, {}).get("min_comments", 1000)

        posts = FETCHER.fetch_rising_posts(
            subreddit=subreddit_name,
            number_of_upvotes=min_upvotes,
            number_comment_threshold=min_comments,
        )

        all_posts.extend(posts)

    return pd.DataFrame(all_posts)


def fetch_top_posts(threshold_configuration: list[dict] = None) -> pd.DataFrame:
    """
    Fetches top posts from specified subreddits based on the given threshold configuration.

    Args:
        threshold_configuration (list[dict], optional): List of dicts defining upvote and comment thresholds per subreddit.

    Returns:
        pd.DataFrame: DataFrame containing the fetched posts.

    Example of threshold_configuration:
        [
            {"subreddit": "subreddit1", "min_upvotes": 100, "min_comments": 10},
            {"subreddit": "subreddit2", "min_upvotes": 50, "min_comments": 5}
        ]
    """

    if FETCHER is None:
        raise Exception(
            "Reddit fetcher not initialized. Call __init_reddit_fetcher first."
        )

    if not isinstance(threshold_configuration, list):
        raise TypeError("Threshold configuration must be a list.")

    all_posts: list[dict] = []

    for config in threshold_configuration:

        subreddit_name: str = list(config.keys())[0]
        min_upvotes: int = config.get(subreddit_name, {}).get("min_upvotes", 1000)
        min_comments: int = config.get(subreddit_name, {}).get("min_comments", 1000)

        time_to_wait:int = random.randint(40, 90)
        print (f"Waiting {time_to_wait} seconds ....")
        time.sleep(time_to_wait)
        print ("Successfully Waited, proceeding")

        posts = FETCHER.fetch_top_posts(
            subreddit=subreddit_name,
            number_of_upvotes=min_upvotes,
            number_comment_threshold=min_comments,
        )

        if len(posts) > 0:
            print("Adding Post in all post")
            all_posts.extend(posts)


    return pd.DataFrame(all_posts)


def calculate_best_date_to_post(posts: pd.DataFrame) -> dict:
    """
    Analyzes the posting times of posts to determine the best day and hour to post for each day of the week.
    Returns comprehensive engagement statistics for each day and subreddit.

    Args:
        posts (pd.DataFrame): DataFrame containing posts data with 'subreddit', 'date', 'nb_upvote', 'nb_comment'.

    Returns:
        dict: Structure with best posting times for each day:
              {
                "subreddit": {
                  "best_overall_day": "Tuesday",
                  "best_overall_hour": 20,
                  "average_engagement": {"upvotes": 3000, "comments": 350},
                  "weekly_schedule": {
                    "Monday": {
                      "best_hour": 14,
                      "avg_upvotes": 2400,
                      "avg_comments": 290,
                      "engagement_score": 2690
                    },
                    ...
                  }
                }
              }
    """
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    best_times = dict()

    for subreddit, group in posts.groupby("subreddit"):
        group["date"] = pd.to_datetime(group["date"], unit="s")
        group["hour"] = group["date"].dt.hour
        group["day_of_week"] = group["date"].dt.day_name()

        engagement_by_time = (
            group.groupby(["day_of_week", "hour"])
            .agg({"nb_upvote": "mean", "nb_comment": "mean"})
            .reset_index()
        )

        engagement_by_time["engagement_score"] = (
            engagement_by_time["nb_upvote"] + engagement_by_time["nb_comment"]
        )

        # Find overall best time slot
        best_overall = engagement_by_time.loc[
            engagement_by_time["engagement_score"].idxmax()
        ]

        # Calculate best hour for each day of week
        weekly_schedule = {}
        for day in days_order:
            day_data = engagement_by_time[engagement_by_time["day_of_week"] == day]

            if len(day_data) > 0:
                best_hour_idx = day_data["engagement_score"].idxmax()
                best_hour_row = day_data.loc[best_hour_idx]

                weekly_schedule[day] = {
                    "best_hour": int(best_hour_row["hour"]),
                    "avg_upvotes": round(float(best_hour_row["nb_upvote"]), 2),
                    "avg_comments": round(float(best_hour_row["nb_comment"]), 2),
                    "engagement_score": round(
                        float(best_hour_row["engagement_score"]), 2
                    ),
                }
            else:
                weekly_schedule[day] = {
                    "best_hour": None,
                    "avg_upvotes": 0,
                    "avg_comments": 0,
                    "engagement_score": 0,
                }

        # Calculate overall average engagement
        avg_upvotes_overall = round(float(group["nb_upvote"].mean()), 2)
        avg_comments_overall = round(float(group["nb_comment"].mean()), 2)

        best_times[subreddit] = {
            "best_overall_day": str(best_overall["day_of_week"]),
            "best_overall_hour": int(best_overall["hour"]),
            "average_engagement": {
                "upvotes": avg_upvotes_overall,
                "comments": avg_comments_overall,
            },
            "weekly_schedule": weekly_schedule,
        }

    return best_times


def write_best_times_to_file(best_times: list[dict[str, str]], file_path: str) -> None:
    """
    Write the json list of best posting times to a file.

    Args:
        best_times (list[dict[str, str]]): List of best posting times per subreddit.
        file_path (str): Path to the output file.

    Returns:
        None
    """

    # If the file does not exist, create it and write an empty list
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("[]")

    with open(file_path, "w") as file:
        import json

        json.dump(best_times, file, indent=4)


def add_posts_embeddings(collection_name: str, posts_df: pd.DataFrame) -> None:
    """
    Converts posts DataFrame to embeddings and adds them to the Qdrant database.
    Verify that the DataFrame contains a 'preprocessed_text' column.
    Check if the posts is already in the database to avoid duplicates.

    Args:
        collection_name (str): The name of the Qdrant collection.
        posts_df (pd.DataFrame): DataFrame containing the posts data.

    Returns:
        None
    """

    if "preprocessed_text" not in posts_df.columns:
        raise ValueError("DataFrame must contain a 'preprocessed_text' column.")

    for _, row in posts_df.iterrows():

        text = f'{row["preprocessed_title"]} \n  {row["preprocessed_title"]} \n {row["preprocessed_title"]} \n\n {row["preprocessed_text"]}'

        embedding = add_embeddings(
            collection_name=collection_name,
            texts=[text],
            ids=[convert_to_uuids(row["id"])],
            payloads=[row.to_dict()],
        )
        print("Added embedding for post with title:", row.get("title", "N/A"))


def preprocess_posts_dataframe(posts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the text of posts in the DataFrame.

    Args:
        posts_df (pd.DataFrame): DataFrame containing the posts data.

    Returns:
        pd.DataFrame: DataFrame with an additional 'preprocessed_text' column.
    """

    if "text" not in posts_df.columns:
        raise ValueError("DataFrame must contain a 'text' column.")

    posts_df["preprocessed_title"] = posts_df["title"].apply(preprocess_text)

    posts_df["preprocessed_text"] = posts_df["text"].apply(preprocess_text)

    return posts_df


def call_fetching_pipeline(treshold_configuration: dict, collection_name: str) -> None:
    """
    Calls the entire fetching pipeline: fetches posts, preprocesses them, and adds their embeddings to Qdrant.

    Args:
        treshold_configuration (dict): Configuration defining subreddit names, upvote and comment thresholds.
        collection_name (str): The name of the Qdrant collection.

    Exception:
        Raises an exception if the Reddit fetcher is not initialized.

    Returns:
        None
    """

    global FETCHER

    if FETCHER is None:
        raise Exception(
            "Reddit fetcher not initialized. Call __init_reddit_fetcher first."
        )

    print("Starting fetching pipeline...")
    posts_df = fetch_top_posts(treshold_configuration)
    print(f"Fetched {len(posts_df)} posts.")

    print("Calculating best date to post...")
    best_times = calculate_best_date_to_post(posts_df)
    print("Best posting times calculated:", best_times)

    print("Writing best posting times to file...")
    write_best_times_to_file(best_times, "./Configuration/best_posting_times.json")
    print("Best posting times written to 'best_posting_times.json'.")

    print("Preprocessing posts...")
    posts_df = preprocess_posts_dataframe(posts_df)
    print("Preprocessing completed.")

    print(f"Adding embeddings to Qdrant collection '{collection_name}'...")
    add_posts_embeddings(collection_name, posts_df)
    print("Embeddings added to Qdrant. Pipeline finished.")


def export_pipeline(treshold_configuration: dict) -> pd.DataFrame:
    """
    Calls the entire fetching pipeline: fetches posts, preprocesses them, and adds their embeddings to Qdrant.

    Args:
        treshold_configuration (dict): Configuration defining subreddit names, upvote and comment thresholds.

    Exception:
        Raises an exception if the Reddit fetcher is not initialized.

    Returns:
        pd.DataFrame: DataFrame containing the fetched posts.
    """

    global FETCHER

    if FETCHER is None:
        raise Exception(
            "Reddit fetcher not initialized. Call __init_reddit_fetcher first."
        )

    print("Starting fetching pipeline...")
    posts_df = fetch_top_posts(treshold_configuration)
    print(f"Fetched {len(posts_df)} posts.")

    print("Fetching Hot posts...")
    hot_posts_df = fetch_hot_posts(treshold_configuration)
    print(f"Fetched {len(hot_posts_df)} hot posts.")

    print("Fetching Rising posts...")
    rising_posts_df = fetch_rising_posts(treshold_configuration)
    print(f"Fetched {len(rising_posts_df)} rising posts.")

    posts_df = (
        pd.concat([posts_df, hot_posts_df, rising_posts_df])
        .drop_duplicates(subset=["id"])
        .reset_index(drop=True)
    )

    return posts_df
