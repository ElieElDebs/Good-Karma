"""
This scripts handles all the function to calculate poste KPI.
"""

import re
from collections import Counter
from nltk.corpus import stopwords

import pandas as pd
from textblob import TextBlob

import datetime

from App.Utils.GlobalEngagementScore import DynamicGESCalculator
from App.Utils.GlobalEngagementScoreNew import GlobalEngagementScoreNew


def is_there_link_in_text(text: str) -> bool:
    """
    Checks if there is a link in the given text.

    Args:
        text (str): The text to check.
    Returns:
        bool: True if there is a link, False otherwise.
    """
    url_pattern = re.compile(r"(https?://[^\s]+)|(www\.[^\s]+)", re.IGNORECASE)
    return bool(url_pattern.search(text))


def count_words(text: str) -> int:
    """
    Counts the number of words in the given text.

    Args:
        text (str): The text to count words in.
    Returns:
        int: The number of words in the text.
    """
    words = re.findall(r"\b\w+\b", text)
    return len(words)


def count_sentences(text: str) -> int:
    """
    Counts the number of sentences in the given text.

    Args:
        text (str): The text to count sentences in.
    Returns:
        int: The number of sentences in the text.
    """
    sentences = re.split(r"[.!?]+", text)
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)


def coutn_question_marks(text: str) -> int:
    """
    Counts the number of question marks in the given text.

    Args:
        text (str): The text to count question marks in.
    Returns:
        int: The number of question marks in the text.
    """
    return text.count("?")


def count_exclamation_marks(text: str) -> int:
    """
    Counts the number of exclamation marks in the given text.

    Args:
        text (str): The text to count exclamation marks in.
    Returns:
        int: The number of exclamation marks in the text.
    """
    return text.count("!")


def count_uppercase_words(text: str) -> int:
    """
    Counts the number of uppercase words in the given text.

    Args:
        text (str): The text to count uppercase words in.
    Returns:
        int: The number of uppercase words in the text.
    """
    words = re.findall(r"\b\w+\b", text)
    uppercase_words = [word for word in words if word.isupper()]
    return len(uppercase_words)


def count_links(text: str) -> int:
    """
    Counts the number of links in the given text.

    Args:
        text (str): The text to count links in.
    Returns:
        int: The number of links in the text.
    """
    url_pattern = re.compile(r"(https?://[^\s]+)|(www\.[^\s]+)", re.IGNORECASE)
    links = url_pattern.findall(text)
    return len(links)


def calculate_readability_score(text: str) -> float:
    """
    Calculates the Flesch Reading Ease score for the given text.

    Args:
        text (str): The text to calculate the readability score for.
    Returns:
        float: The Flesch Reading Ease score.
    """
    total_words = count_words(text)
    total_sentences = count_sentences(text)

    if total_sentences == 0 or total_words == 0:
        return 0.0

    # Average sentence length
    asl = total_words / total_sentences

    # Average syllables per word (approximation: average English word has 1.5 syllables)
    asw = 1.5

    # Flesch Reading Ease formula
    flesch_score = 206.835 - (1.015 * asl) - (84.6 * asw)

    return round(flesch_score, 2)


def calculate_polarity(text: str) -> float:
    """
    Calculates the sentiment polarity of the given text.

    Args:
        text (str): The text to analyze.
    Returns:
        float: The sentiment polarity score (-1.0 to 1.0).
    """
    blob = TextBlob(text)
    return round(blob.sentiment.polarity, 3)


def calculate_subjectivity(text: str) -> float:
    """
    Calculates the sentiment subjectivity of the given text.

    Args:
        text (str): The text to analyze.
    Returns:
        float: The sentiment subjectivity score (0.0 to 1.0).
    """
    blob = TextBlob(text)
    return round(blob.sentiment.subjectivity, 3)


def get_most_used_words(df, text_column="post", top_n=30, lang="english"):
    """
    Returns the most used words in all posts in the dataframe.

    Args:
        df (pd.DataFrame): DataFrame containing posts.
        text_column (str): Name of the column containing post text.
        top_n (int): Number of top words to return.
        lang (str): Language for stop words.

    Returns:
        List[Tuple[str, int]]: List of tuples (word, count) sorted by count descending.
    """

    stop_words = set(stopwords.words(lang))

    # Exclude numbers expresed as words
    number_words = {
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
        "hundred",
        "thousand",
        "million",
        "billion",
    }

    diver_words = {
        "n",
        "r",
        "also",
        "way",
        "get",
        "like",
        "just",
        "im",
        "dont",
        "know",
        "think",
        "people",
        "time",
        "good",
        "make",
        "even",
        "really",
        "much",
        "want",
        "need",
        "use",
        "used",
        "using",
        "still",
        "see",
        "look",
        "looking",
        "thing",
        "things",
        "post",
        "posts",
        "every",
        "day",
        "days",
        "http",
        "lot",
        "https",
        "com",
        "www",
        "e",
        "let",
        "u",
        "got",
        "get",
        "would",
        "thought",
        "take",
        "say",
        "find",
        "something",
        "anything",
        "nothing",
        "ive",
        "ive",
        "theres",
        "whats",
        "hes",
        "shes",
        "theyre",
        "hey",
        "hello",
        "hi",
        "everyone",
        "go",
        "better",
        "could",
    }

    stop_words.update(number_words)
    stop_words.update(diver_words)

    all_text = " ".join(df[text_column].astype(str))
    words = re.findall(r"\b\w+\b", all_text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    filtered_words = [word for word in filtered_words if not word.isdigit()]

    counter = Counter(filtered_words)

    return counter.most_common(top_n)


def get_optimal_date_to_post(df, date_column="date", upvote_column="nb_upvote"):
    """
    Returns the optimal date to post based on upvotes.

    Args:
        df (pd.DataFrame): DataFrame containing posts.
        date_column (str): Name of the column containing post dates.
        upvote_column (str): Name of the column containing number of upvotes.

    Returns:
        float: The date (timestamp) with the highest average upvotes.
    """

    optimal_date = "None"

    try:
        grouped = df.groupby(date_column)[upvote_column].mean()
        optimal_date = grouped.idxmax()
        optimal_date = datetime.datetime.fromtimestamp(optimal_date).strftime(
            "%A %d %B %Y %H:%M"
        )

    except Exception:
        print("Error in calculating optimal date to post.")

    finally:
        return optimal_date


def calculate_post_to_compare_kpi(text: str, preprocessed_text: str) -> dict:
    """
    Calculate KPIs for a single post text.

    Args:
        text (str): The post text to analyze.
        preprocessed_text (str): The preprocessed text to analyze.

    Returns:
        dict: A dictionary containing the calculated KPIs.
    """
    kpi_dict = dict()

    kpi_dict["is_there_link"] = is_there_link_in_text(text)
    kpi_dict["word_count"] = count_words(text)
    kpi_dict["sentence_count"] = count_sentences(text)
    kpi_dict["question_mark_count"] = coutn_question_marks(text)
    kpi_dict["exclamation_mark_count"] = count_exclamation_marks(text)
    kpi_dict["uppercase_word_count"] = count_uppercase_words(text)
    kpi_dict["link_count"] = count_links(text)
    kpi_dict["readability_score"] = calculate_readability_score(text)
    kpi_dict["polarity"] = calculate_polarity(text)
    kpi_dict["subjectivity"] = calculate_subjectivity(text)
    kpi_dict["text"] = text
    kpi_dict["preprocessed_text"] = preprocessed_text

    return kpi_dict


def calculate_titles_kpi(
    dataframe, text_column: str = "title", raw_column="title"
) -> dict[str, any]:
    """
    Calculate various KPIs for the titles in the given DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame containing posts.
        text_column (str): Name of the column containing title text.
        raw_column (str): Name of the column containing raw title text.

    Returns:
        tuple[dict, pd.DataFrame]: A tuple containing a dictionary of global KPIs and a DataFrame with individual title KPIs.
    """

    copied_dataframe = dataframe.copy()

    # get title length
    copied_dataframe["title_length"] = copied_dataframe[raw_column].apply(len)

    # get title word count
    copied_dataframe["title_word_count"] = copied_dataframe[raw_column].apply(
        count_words
    )

    # Get title most used words
    most_used_words = get_most_used_words(copied_dataframe, text_column)

    # Get title number of questions
    copied_dataframe["title_question_count"] = copied_dataframe[text_column].apply(
        coutn_question_marks
    )

    # Get title number of exclamations
    copied_dataframe["title_exclamation_count"] = copied_dataframe[text_column].apply(
        count_exclamation_marks
    )

    # get title polarity
    copied_dataframe["title_polarity"] = copied_dataframe[raw_column].apply(
        calculate_polarity
    )

    # get title subjectivity
    copied_dataframe["title_subjectivity"] = copied_dataframe[raw_column].apply(
        calculate_subjectivity
    )

    # get title uppercase word count
    copied_dataframe["title_uppercase_word_count"] = copied_dataframe[raw_column].apply(
        count_uppercase_words
    )

    def r2(val):
        return round(float(val), 2)

    return {
        "average_title_length": r2(copied_dataframe["title_length"].mean()),
        "median_title_length": r2(copied_dataframe["title_length"].median()),
        "average_title_word_count": r2(copied_dataframe["title_word_count"].mean()),
        "median_title_word_count": r2(copied_dataframe["title_word_count"].median()),
        "most_used_title_words": most_used_words,
        "average_title_question_count": r2(
            copied_dataframe["title_question_count"].mean()
        ),
        "median_title_question_count": r2(
            copied_dataframe["title_question_count"].median()
        ),
        "average_title_exclamation_count": r2(
            copied_dataframe["title_exclamation_count"].mean()
        ),
        "median_title_exclamation_count": r2(
            copied_dataframe["title_exclamation_count"].median()
        ),
        "average_title_polarity": r2(copied_dataframe["title_polarity"].mean()),
        "median_title_polarity": r2(copied_dataframe["title_polarity"].median()),
        "average_title_subjectivity": r2(copied_dataframe["title_subjectivity"].mean()),
        "median_title_subjectivity": r2(
            copied_dataframe["title_subjectivity"].median()
        ),
        "average_title_uppercase_word_count": r2(
            copied_dataframe["title_uppercase_word_count"].mean()
        ),
        "median_title_uppercase_word_count": r2(
            copied_dataframe["title_uppercase_word_count"].median()
        ),
    }


def calculate_body_kpi(
    dataframe, text_column: str = "text", raw_column="text"
) -> tuple[dict, pd.DataFrame]:
    """
    Calculate various KPIs for the posts in the given DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame containing posts.
        text_column (str): Name of the column containing post text.
        raw_column (str): Name of the column containing raw post text.

    Returns:
        tuple[dict, pd.DataFrame]: A tuple containing a dictionary of global KPIs and a DataFrame with individual post KPIs.
    """
    copied_dataframe = dataframe.copy()

    def r2(val):
        return round(float(val), 2)

    copied_dataframe["is_there_link"] = copied_dataframe[raw_column].apply(
        is_there_link_in_text
    )
    copied_dataframe["word_count"] = copied_dataframe[raw_column].apply(count_words)
    copied_dataframe["sentence_count"] = copied_dataframe[text_column].apply(
        count_sentences
    )
    copied_dataframe["question_mark_count"] = copied_dataframe[text_column].apply(
        coutn_question_marks
    )
    copied_dataframe["exclamation_mark_count"] = copied_dataframe[text_column].apply(
        count_exclamation_marks
    )
    copied_dataframe["uppercase_word_count"] = copied_dataframe[text_column].apply(
        count_uppercase_words
    )
    copied_dataframe["link_count"] = copied_dataframe[text_column].apply(count_links)
    copied_dataframe["readability_score"] = copied_dataframe[raw_column].apply(
        calculate_readability_score
    )
    copied_dataframe["polarity"] = copied_dataframe[raw_column].apply(
        calculate_polarity
    )
    copied_dataframe["subjectivity"] = copied_dataframe[raw_column].apply(
        calculate_subjectivity
    )

    dict_dataframe = copied_dataframe.to_dict(orient="records")

    # Global KPIs
    global_kpis = {
        "words_and_sentences": {
            "average_word_count": r2(copied_dataframe["word_count"].mean()),
            "median_word_count": r2(copied_dataframe["word_count"].median()),
            "average_sentence_count": r2(copied_dataframe["sentence_count"].mean()),
            "median_sentence_count": r2(copied_dataframe["sentence_count"].median()),
            "most_used_words": get_most_used_words(copied_dataframe, text_column),
        },
        "polarity_and_readability_subjectivity": {
            "average_readability_score": r2(
                copied_dataframe["readability_score"].mean()
            ),
            "median_readability_score": r2(
                copied_dataframe["readability_score"].median()
            ),
            "average_polarity": r2(copied_dataframe["polarity"].mean()),
            "median_polarity": r2(copied_dataframe["polarity"].median()),
            "average_subjectivity": r2(copied_dataframe["subjectivity"].mean()),
            "median_subjectivity": r2(copied_dataframe["subjectivity"].median()),
        },
        "scores": {
            "total_posts": int(copied_dataframe.shape[0]),
            "min_score": (
                r2(copied_dataframe["score"].min())
                if "score" in copied_dataframe.columns
                else 0
            ),
            "max_score": (
                r2(copied_dataframe["score"].max())
                if "score" in copied_dataframe.columns
                else 0
            ),
            "average_score": (
                r2(copied_dataframe["score"].mean())
                if "score" in copied_dataframe.columns
                else 0
            ),
            "median_score": (
                r2(copied_dataframe["score"].median())
                if "score" in copied_dataframe.columns
                else 0
            ),
            "min_upvotes": (
                r2(copied_dataframe["nb_upvote"].min())
                if "nb_upvote" in copied_dataframe.columns
                else 0
            ),
            "max_upvotes": (
                r2(copied_dataframe["nb_upvote"].max())
                if "nb_upvote" in copied_dataframe.columns
                else 0
            ),
            "average_upvotes": (
                r2(copied_dataframe["nb_upvote"].mean())
                if "nb_upvote" in copied_dataframe.columns
                else 0
            ),
            "median_upvotes": (
                r2(copied_dataframe["nb_upvote"].median())
                if "nb_upvote" in copied_dataframe.columns
                else 0
            ),
        },
        "links_and_time": {
            "total_posts_with_links": copied_dataframe["is_there_link"].sum(),
            "percentage_posts_with_links": r2(
                copied_dataframe["is_there_link"].mean() * 100
            ),
            "optimal_date_to_post": str(
                get_optimal_date_to_post(
                    copied_dataframe, date_column="date", upvote_column="nb_upvote"
                )
            ),
        },
    }

    return (global_kpis, dict_dataframe)


def calculate_GES_new(kpi_dict: dict) -> dict[str, any]:
    """
    Calculate Global Engagement Score (GES) based on the given KPI dictionary.

    Args:
        kpi_dict (dict): A dictionary containing KPIs.

    Returns:
        dict[str, any]: A dictionary containing GES score, label, and factors.
    """

    # Chech if "Data" key exists in kpi_dict
    if "data" not in kpi_dict:
        kpi_dict = {"data": kpi_dict}

    ges_calculator = GlobalEngagementScoreNew(kpi_dict)
    ges_result = ges_calculator.calculate_global_score()

    return ges_result, ges_result.get("advices", [])


def calculate_GES(kpi_dict: dict) -> dict[str, any]:
    """
    Calculate Global Engagement Score (GES) based on the given KPI dictionary.

    Args:
        kpi_dict (dict): A dictionary containing KPIs.

    Returns:
        dict[str, any]: A dictionary containing GES score, label, and factors.
    """

    # Chech if "Data" key exists in kpi_dict
    if "data" not in kpi_dict:
        kpi_dict = {"data": kpi_dict}

    semantic_similarity_avg = (
        kpi_dict["data"]
        .get("successful_posts", {})
        .get("global_body_kpi", {})
        .get("scores", {})
        .get("average_score", 0.0)
    )

    ges_calculator = DynamicGESCalculator(kpi_dict)
    ges_result = ges_calculator.calculate_ges(semantic_similarity_avg)
    advice_list = ges_calculator.generate_advice_list(ges_result)

    return ges_result, advice_list
