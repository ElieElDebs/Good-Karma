import json
import uuid
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def get_best_times_to_post(
    subreddits: list[str], filepath: str = "best_posting_times.json"
) -> dict:
    """
    Get the best times to post for the given subreddits from a JSON file.

    Args:
        subreddits (list[str]): List of subreddits to get best posting times for.
        filepath (str): Path to the JSON file containing best posting times.

    Returns:
        dict: A dictionary with subreddits as keys and their best posting times as values.
    """
    with open(filepath, "r") as file:
        best_times_data = json.load(file)

    best_times_dict = {}

    for subreddit in subreddits:
        best_times_dict[subreddit] = best_times_data[subreddit]

    return best_times_dict


def convert_to_uuids(id: str) -> str:
    """
    Convert a string ID to a UUID.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, id))


def download_nltk_resources() -> None:
    """
    Download necessary NLTK resources.
    """
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("stopwords")
    nltk.download("punkt_tab")


def remove_stopwords(text: str, language: str = "english") -> str:
    """
    Remove stopwords from the input text.
    Args:
        text (str): The input text from which to remove stopwords.
        language (str): The language of the stopwords to remove. Default is 'english'.

    Returns:
        str: The text with stopwords removed.
    """
    stop_words = set(stopwords.words(language))
    words = nltk.word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return " ".join(filtered_words)


def lemmatize_text(text: str) -> str:
    """
    Lemmatize the input text.
    Args:
        text (str): The input text to lemmatize.
    Returns:
        str: The lemmatized text.
    """
    lemmatizer = WordNetLemmatizer()
    words = nltk.word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(lemmatized_words)


def preprocess_text(text: str, language: str = "english") -> str:
    """
    Preprocess the input text by removing stopwords and lemmatizing.
    Args:
        text (str): The input text to preprocess.
        language (str): The language of the stopwords to remove. Default is 'english'.
    Returns:
        str: The preprocessed text.
    """
    text_no_stopwords = remove_stopwords(text, language)
    lemmatized_text = lemmatize_text(text_no_stopwords)

    return lemmatized_text


def generate_scientific_empirical_advice(
    comparaison_dict: dict,
) -> tuple[list[str], list[str]]:
    """
    Generate actionable advice to follow and avoid by comparing the KPIs of the post with those of successful and unsuccessful posts.
    Each advice includes the current state of the post.
    Also includes advice for the title.
    """
    conseils_a_suivre = []
    conseils_a_eviter = []

    # Retrieve KPIs
    post_kpis_body = comparaison_dict.get("post_kpis_body", {})
    post_kpis_title = comparaison_dict.get("post_kpis_title", {})
    successful_kpis_body = comparaison_dict.get("successful_kpis_body", {})
    unsuccessful_kpis_body = comparaison_dict.get("unsuccessful_kpis_body", {})
    successful_kpis_title = comparaison_dict.get("successful_kpis_title", {})
    unsuccessful_kpis_title = comparaison_dict.get("unsuccessful_kpis_title", {})

    # Compatibility for grouped KPIs (new version)
    if "words_and_sentences" in successful_kpis_body:
        s_body = successful_kpis_body["words_and_sentences"]
        s_read = successful_kpis_body["polarity_and_readability_subjectivity"]
    else:
        s_body = successful_kpis_body
        s_read = successful_kpis_body

    if "words_and_sentences" in unsuccessful_kpis_body:
        u_body = unsuccessful_kpis_body["words_and_sentences"]
        u_read = unsuccessful_kpis_body["polarity_and_readability_subjectivity"]
    else:
        u_body = unsuccessful_kpis_body
        u_read = unsuccessful_kpis_body

    # --- TITLE KPIs ---
    # Successful
    if post_kpis_title and successful_kpis_title:
        s_title_words = successful_kpis_title.get(
            "words_and_sentences", successful_kpis_title
        )
        s_title_read = successful_kpis_title.get(
            "polarity_and_readability_subjectivity", successful_kpis_title
        )
        # Word count
        if post_kpis_title.get("word_count", 0) < s_title_words.get(
            "median_word_count", 0
        ):
            conseils_a_suivre.append(
                f"Try to make your title longer to reach at least {s_title_words.get('median_word_count', 0)} words (successful titles median). Current title length: {post_kpis_title.get('word_count', 0)} words."
            )
        if post_kpis_title.get("word_count", 0) > s_title_words.get(
            "median_word_count", 0
        ):
            conseils_a_suivre.append(
                f"Try to shorten your title to get closer to {s_title_words.get('median_word_count', 0)} words (successful titles median). Current title length: {post_kpis_title.get('word_count', 0)} words."
            )
        # Polarity
        if post_kpis_title.get("polarity", 0) < s_title_read.get("average_polarity", 0):
            conseils_a_suivre.append(
                f"Try to make your title more positive to match successful titles. Current title polarity: {post_kpis_title.get('polarity', 0)}."
            )
        # Subjectivity
        if post_kpis_title.get("subjectivity", 0) < s_title_read.get(
            "average_subjectivity", 0
        ):
            conseils_a_suivre.append(
                f"Add more personal touch to your title to increase subjectivity (as seen in successful titles). Current title subjectivity: {post_kpis_title.get('subjectivity', 0)}."
            )
        # Readability
        if post_kpis_title.get("readability_score", 0) < s_title_read.get(
            "average_readability_score", 0
        ):
            conseils_a_suivre.append(
                f"Improve your title's readability to reach the average score of successful titles. Current title readability score: {post_kpis_title.get('readability_score', 0)}."
            )
        # Most used words
        mots_succes_title = [w for w, _ in s_title_words.get("most_used_words", [])]
        missing_title = [
            w
            for w in mots_succes_title
            if w not in post_kpis_title.get("preprocessed_text", "").split()
        ]
        if missing_title:
            conseils_a_suivre.append(
                f"Consider including these commonly used words from successful titles: {', '.join(missing_title)}. Your title is currently missing them."
            )

    # Unsuccessful
    if post_kpis_title and unsuccessful_kpis_title:
        u_title_words = unsuccessful_kpis_title.get(
            "words_and_sentences", unsuccessful_kpis_title
        )
        u_title_read = unsuccessful_kpis_title.get(
            "polarity_and_readability_subjectivity", unsuccessful_kpis_title
        )
        if post_kpis_title.get("word_count", 0) >= u_title_words.get(
            "median_word_count", 0
        ):
            conseils_a_eviter.append(
                f"Avoid making your title longer than {u_title_words.get('median_word_count', 0)} words, as longer titles tend to perform worse. Current title length: {post_kpis_title.get('word_count', 0)} words."
            )
        if post_kpis_title.get("polarity", 0) <= u_title_read.get(
            "average_polarity", 0
        ):
            conseils_a_eviter.append(
                f"Avoid being too negative in your title, as this is common in underperforming titles. Current title polarity: {post_kpis_title.get('polarity', 0)}."
            )
        if post_kpis_title.get("subjectivity", 0) >= u_title_read.get(
            "average_subjectivity", 0
        ):
            conseils_a_eviter.append(
                f"Avoid being overly subjective in your title, as this is common in underperforming titles. Current title subjectivity: {post_kpis_title.get('subjectivity', 0)}."
            )
        if post_kpis_title.get("readability_score", 0) <= u_title_read.get(
            "average_readability_score", 0
        ):
            conseils_a_eviter.append(
                f"Avoid low readability in your title, as poorly readable titles tend to perform worse. Current title readability score: {post_kpis_title.get('readability_score', 0)}."
            )
        mots_echec_title = [w for w, _ in u_title_words.get("most_used_words", [])]
        present_title = [
            w
            for w in mots_echec_title
            if w in post_kpis_title.get("preprocessed_text", "").split()
        ]
        if present_title:
            conseils_a_eviter.append(
                f"Avoid overusing these words associated with underperforming titles: {', '.join(present_title)}. Your title currently contains them."
            )

    # --- BODY KPIs ---
    # Advice to follow (based on successful)
    if post_kpis_body and s_body:
        # Word count
        if post_kpis_body.get("word_count", 0) < s_body.get("median_word_count", 0):
            conseils_a_suivre.append(
                f"Try to increase your post length to at least {s_body.get('median_word_count', 0)} words (successful posts median). Current length: {post_kpis_body.get('word_count', 0)} words."
            )
        if post_kpis_body.get("word_count", 0) > s_body.get("median_word_count", 0):
            conseils_a_suivre.append(
                f"Try to condense your post to get closer to {s_body.get('median_word_count', 0)} words (successful posts median). Current length: {post_kpis_body.get('word_count', 0)} words."
            )
        # Polarity
        if post_kpis_body.get("polarity", 0) < s_read.get("average_polarity", 0):
            conseils_a_suivre.append(
                f"Try to make your post more positive to match successful posts. Current polarity: {post_kpis_body.get('polarity', 0)}."
            )
        # Subjectivity
        if post_kpis_body.get("subjectivity", 0) < s_read.get(
            "average_subjectivity", 0
        ):
            conseils_a_suivre.append(
                f"Add more personal opinions to increase subjectivity (as seen in successful posts). Current subjectivity: {post_kpis_body.get('subjectivity', 0)}."
            )
        # Readability
        if post_kpis_body.get("readability_score", 0) < s_read.get(
            "average_readability_score", 0
        ):
            conseils_a_suivre.append(
                f"Improve your post's readability to reach the average score of successful posts. Current readability score: {post_kpis_body.get('readability_score', 0)}."
            )
        # Most used words
        mots_succes = [w for w, _ in s_body.get("most_used_words", [])]
        missing = [
            w
            for w in mots_succes
            if w not in post_kpis_body.get("preprocessed_text", "").split()
        ]
        if missing:
            conseils_a_suivre.append(
                f"Consider including these commonly used words from successful posts: {', '.join(missing)}. Your post is currently missing them."
            )

    # Advice to avoid (based on unsuccessful)
    if post_kpis_body and u_body:
        if post_kpis_body.get("word_count", 0) >= u_body.get("median_word_count", 0):
            conseils_a_eviter.append(
                f"Avoid exceeding {u_body.get('median_word_count', 0)} words, as longer posts tend to perform worse. Current length: {post_kpis_body.get('word_count', 0)} words."
            )
        if post_kpis_body.get("polarity", 0) <= u_read.get("average_polarity", 0):
            conseils_a_eviter.append(
                f"Avoid being too negative, as this is common in underperforming posts. Current polarity: {post_kpis_body.get('polarity', 0)}."
            )
        if post_kpis_body.get("subjectivity", 0) >= u_read.get(
            "average_subjectivity", 0
        ):
            conseils_a_eviter.append(
                f"Avoid being overly subjective, as this is common in underperforming posts. Current subjectivity: {post_kpis_body.get('subjectivity', 0)}."
            )
        if post_kpis_body.get("readability_score", 0) <= u_read.get(
            "average_readability_score", 0
        ):
            conseils_a_eviter.append(
                f"Avoid low readability, as poorly readable posts tend to perform worse. Current readability score: {post_kpis_body.get('readability_score', 0)}."
            )
        mots_echec = [w for w, _ in u_body.get("most_used_words", [])]
        present = [
            w
            for w in mots_echec
            if w in post_kpis_body.get("preprocessed_text", "").split()
        ]
        if present:
            conseils_a_eviter.append(
                f"Avoid overusing these words associated with underperforming posts: {', '.join(present)}. Your post currently contains them."
            )

    return conseils_a_suivre, conseils_a_eviter
