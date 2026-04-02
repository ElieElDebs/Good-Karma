import yaml


def get_subreddits_names(file_path: str = "Configuration/workflow.yaml") -> list:
    """
    Retrieve the list of subreddits from the workflow configuration file.

    Args:
        file_path (str): Path to the configuration YAML file.
    Returns:
        list: A list of subreddit names.
    """
    # Load Workflow Configuration
    with open(file_path, "r") as config_file:
        config = yaml.safe_load(config_file)

    subreddits_config = config.get("fetch_reddit_posts", {}).get("subreddits", {})
    subreddits = []


    for subreddit in subreddits_config:
        subreddits.append(list(subreddit.keys())[0])

    return subreddits
