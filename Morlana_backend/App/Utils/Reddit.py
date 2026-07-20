import random
import time

import praw
import requests

USER_AGENTS: list[str] = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux i686; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
]


REDDIT_FETCH_URL = """https://old.reddit.com/r/{subreddit}/top/.json?t={frequency}"""


class RedditScrapper:

    def __init__(self, user_agents: list[str] = USER_AGENTS):
        """
        Initialize Reddit Scrapper.

        Args:
            user_agents (List str): List of User agent  for Reddit scrapper call.
            time_range (tuple int int): Time range used for random fetch scrapping.

        """

        # PUBLIC
        self.user_agents: list[str] = user_agents

    @staticmethod
    def _random_user_agent():
        """
        Choose random user agent
        """

        max_index: int = len(USER_AGENTS) - 1
        chose_option: int = random.randint(0, max_index)

        return USER_AGENTS[chose_option]

    def fetch_top_posts(
        self,
        subreddit: str,
        number_of_upvotes: int,
        number_comment_threshold: int = None,
    ) -> list[dict[str, any]]:
        """
        Fetch top posts from a subreddit based on upvotes and comment count.

        Args:
            subreddit (str): Name of the subreddit to fetch posts from.
            number_of_upvotes (int): Minimum number of upvotes a post must have to be included.
            number_comment_threshold (int): Minimum number of comments a post must have to be included.

        Returns:
            list[dict[str, any]]: List of dictionaries containing post data.

        Raises:
            AssertionError: If number_of_upvotes or number_comment_threshold are negative.

        Post Structure:
            {
                'text': str,
                'title': str,
                'url': str,
                'author': str,
                'is_text': bool,
                'category': str,
                'is_18plus': bool,
                'subreddit': str,
                'nb_upvote': int,
                'nb_downvote': int,
                'nb_comment': int,
                'date': float,
                "type" : "successful"
            }
        """

        url: str = REDDIT_FETCH_URL.format(subreddit=subreddit, frequency="week")

        try:
            user_agent: str = self._random_user_agent()
            headers: dict[str, str] = {
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }

            with requests.Session() as session:
                session.headers.update(headers)
                # Warm up: grab real cookies from the HTML page first, like a browser would,
                # instead of hitting .json cold with no session state.
                session.get(f"https://old.reddit.com/r/{subreddit}/", timeout=10)

                response = session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

            top_posts = data["data"]["children"]

        except Exception as e:
            print(f"There was an error here : {e}")
            top_posts = []

        # Filter posts based on upvotes and comment count
        filtered_posts = []

        for post in top_posts:

            post_data = post["data"]

            if post_data["ups"] >= number_of_upvotes:
                if (
                    number_comment_threshold is None
                    or post_data["num_comments"] >= number_comment_threshold
                ):
                    filtered_posts.append(
                        {
                            "id": post_data["id"],
                            "text": post_data.get("selftext", ""),
                            "title": post_data["title"],
                            "url": post_data["url"],
                            "author": post_data["author"],
                            "is_text": post_data["is_self"],
                            "category": "Top",
                            "is_18plus": post_data["over_18"],
                            "subreddit": subreddit,
                            "nb_upvote": post_data["ups"],
                            "nb_downvote": post_data["downs"],
                            "nb_comment": post_data["num_comments"],
                            "date": post_data["created_utc"],
                            "type": "successful",
                        }
                    )

        return filtered_posts


class RedditFetcher:

    def __init__(self, reddit_id: str, reddit_secret: str, user_agent: str) -> None:
        """
        Initialize RedditFetcher instance.

        Args:
            reddit_id (str): Reddit API client ID.
            reddit_secret (str): Reddit API client secret.
            user_agent (str): User agent string for Reddit API requests.

        Returns:
            None
        """

        self._reddit_id = reddit_id
        self._reddit_secret = reddit_secret
        self._user_agent = user_agent
        self._reddit_client = None

        self._initialize_reddit_client()

    def _initialize_reddit_client(self):
        """
        Internal method to initialize Reddit API client.
        """
        # Try catching potential exceptions during Reddit client initialization
        try:
            self._reddit_client = praw.Reddit(
                client_id=self._reddit_id,
                client_secret=self._reddit_secret,
                user_agent=self._user_agent,
            )
        except Exception as e:
            print(f"Error initializing Reddit client: {e}")

    def fetch_unsuccessful_posts(
        self,
        subreddit: str,
        max_upvotes: int = 5,
        max_comments: int = 5,
        min_age_days: int = 1,
    ) -> list[dict[str, any]]:
        """
        Fetch posts from 'new' that are older than min_age_days and have less than max_upvotes and max_comments.

        Args:
            subreddit (str): Name of the subreddit.
            max_upvotes (int): Maximum upvotes allowed.
            max_comments (int): Maximum comments allowed.
            min_age_days (int): Minimum age of post in days.

        Returns:
            list[dict[str, any]]: List of post dicts.
        """
        now = time.time()
        min_age_seconds = min_age_days * 86400
        subreddit_instance = self._reddit_client.subreddit(subreddit)
        new_posts = subreddit_instance.new(limit=2000)
        filtered_posts = []

        for post in new_posts:
            age = now - post.created_utc
            if (
                age > min_age_seconds
                and post.ups < max_upvotes
                and post.num_comments < max_comments
            ):
                filtered_posts.append(
                    {
                        "id": post.id,
                        "text": post.selftext if hasattr(post, "selftext") else "",
                        "title": post.title,
                        "url": post.url,
                        "author": str(post.author),
                        "is_text": post.is_self,
                        "category": "Unsuccessful",
                        "is_18plus": post.over_18,
                        "subreddit": subreddit,
                        "nb_upvote": post.ups,
                        "nb_downvote": post.downs,
                        "nb_comment": post.num_comments,
                        "date": post.created_utc,
                        "type": "unsuccessful",
                    }
                )
        return filtered_posts

    def fetch_hot_posts(
        self,
        subreddit: str,
        number_of_upvotes: int,
        number_comment_threshold: int = None,
    ) -> list[dict[str, any]]:
        """
        Fetch hot posts from a subreddit based on upvotes and comment count.

        Args:
            subreddit (str): Name of the subreddit to fetch posts from.
            number_of_upvotes (int): Minimum number of upvotes a post must have to be included.
            number_comment_threshold (int): Minimum number of comments a post must have to be included.

        Returns:
            list[dict[str, any]]: List of dictionaries containing post data.

        Raises:
            AssertionError: If number_of_upvotes or number_comment_threshold are negative.

        Post Structure:
            {
                'text': str,
                'title': str,
                'url': str,
                'author': str,
                'is_text': bool,
                'category': str,
                'is_18plus': bool,
                'subreddit': str,
                'nb_upvote': int,
                'nb_downvote': int,
                'nb_comment': int,
                'date': float,
                "type" : "successful"
            }
        """

        # Fetch the hot posts from the specified subreddit
        subreddit_instance = self._reddit_client.subreddit(subreddit)
        hot_posts = subreddit_instance.hot(limit=2000)

        # Filter posts based on upvotes and comment count
        filtered_posts = []

        for post in hot_posts:

            if post.ups >= number_of_upvotes:
                if (
                    number_comment_threshold is None
                    or post.num_comments >= number_comment_threshold
                ):
                    filtered_posts.append(
                        {
                            "id": post.id,
                            "text": post.selftext if hasattr(post, "selftext") else "",
                            "title": post.title,
                            "url": post.url,
                            "author": str(post.author),
                            "is_text": post.is_self,
                            "category": "Hot",
                            "is_18plus": post.over_18,
                            "subreddit": subreddit,
                            "nb_upvote": post.ups,
                            "nb_downvote": post.downs,
                            "nb_comment": post.num_comments,
                            "date": post.created_utc,
                            "type": "successful",
                        }
                    )

        return filtered_posts

    def fetch_rising_posts(
        self,
        subreddit: str,
        number_of_upvotes: int,
        number_comment_threshold: int = None,
    ) -> list[dict[str, any]]:
        """
        Fetch rising posts from a subreddit based on upvotes and comment count.

        Args:
            subreddit (str): Name of the subreddit to fetch posts from.
            number_of_upvotes (int): Minimum number of upvotes a post must have to be included.
            number_comment_threshold (int): Minimum number of comments a post must have to be included.

        Returns:
            list[dict[str, any]]: List of dictionaries containing post data.

        Raises:
            AssertionError: If number_of_upvotes or number_comment_threshold are negative.

        Post Structure:
            {
                'text': str,
                'title': str,
                'url': str,
                'author': str,
                'is_text': bool,
                'category': str,
                'is_18plus': bool,
                'subreddit': str,
                'nb_upvote': int,
                'nb_downvote': int,
                'nb_comment': int,
                'date': float,
                "type" : "successful"
            }
        """

        # Fetch the rising posts from the specified subreddit
        subreddit_instance = self._reddit_client.subreddit(subreddit)
        rising_posts = subreddit_instance.rising(limit=2000)

        # Filter posts based on upvotes and comment count
        filtered_posts = []

        for post in rising_posts:

            if post.ups >= number_of_upvotes:
                if (
                    number_comment_threshold is None
                    or post.num_comments >= number_comment_threshold
                ):
                    filtered_posts.append(
                        {
                            "id": post.id,
                            "text": post.selftext if hasattr(post, "selftext") else "",
                            "title": post.title,
                            "url": post.url,
                            "author": str(post.author),
                            "is_text": post.is_self,
                            "category": "Rising",
                            "is_18plus": post.over_18,
                            "subreddit": subreddit,
                            "nb_upvote": post.ups,
                            "nb_downvote": post.downs,
                            "nb_comment": post.num_comments,
                            "date": post.created_utc,
                            "type": "successful",
                        }
                    )

        return filtered_posts

    def fetch_top_posts(
        self,
        subreddit: str,
        number_of_upvotes: int,
        number_comment_threshold: int = None,
    ) -> list[dict[str, any]]:
        """
        Fetch top posts from a subreddit based on upvotes and comment count.

        Args:
            subreddit (str): Name of the subreddit to fetch posts from.
            number_of_upvotes (int): Minimum number of upvotes a post must have to be included.
            number_comment_threshold (int): Minimum number of comments a post must have to be included.

        Returns:
            list[dict[str, any]]: List of dictionaries containing post data.

        Raises:
            AssertionError: If number_of_upvotes or number_comment_threshold are negative.

        Post Structure:
            {
                'text': str,
                'title': str,
                'url': str,
                'author': str,
                'is_text': bool,
                'category': str,
                'is_18plus': bool,
                'subreddit': str,
                'nb_upvote': int,
                'nb_downvote': int,
                'nb_comment': int,
                'date': float,
                "type" : "successful"
            }
        """

        # Fetch the top posts from the specified subreddit
        subreddit_instance = self._reddit_client.subreddit(subreddit)
        top_posts = subreddit_instance.top(limit=2000)

        # Filter posts based on upvotes and comment count
        filtered_posts = []

        for post in top_posts:

            if post.ups >= number_of_upvotes:
                if (
                    number_comment_threshold is None
                    or post.num_comments >= number_comment_threshold
                ):
                    filtered_posts.append(
                        {
                            "id": post.id,
                            "text": post.selftext if hasattr(post, "selftext") else "",
                            "title": post.title,
                            "url": post.url,
                            "author": str(post.author),
                            "is_text": post.is_self,
                            "category": "Top",
                            "is_18plus": post.over_18,
                            "subreddit": subreddit,
                            "nb_upvote": post.ups,
                            "nb_downvote": post.downs,
                            "nb_comment": post.num_comments,
                            "date": post.created_utc,
                            "type": "successful",
                        }
                    )

        return filtered_posts
