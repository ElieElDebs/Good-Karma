REWRITE_PROMPT = """You are an expert in Reddit post optimization. Your goal is to rewrite posts to increase engagement.

### CURRENT POST:
Title: {draft_title}
Body: {draft_body}

### KPIs AND STRENGTHS/WEAKNESSES:
{weakness_and_strength}

### TITLE METRICS (yours vs. top-performing posts in r/{subreddit}):
{title_metrics}

### BODY METRICS (yours vs. top-performing posts in r/{subreddit}):
{body_metrics}

### IMPROVEMENT TIPS:
{advices}

### EXEMPLARY POSTS (To study):
{examples}

### Words to use if it's possible in the title :
- Popular keywords: {ideal_words_to_use_title}

### Words to use if it's possible in the body :
- Popular keywords: {ideal_words_to_use_body}


IMPORTANT TASK:
1. Improve the title: bring its length, polarity (emotional tone) and subjectivity closer to the target TITLE METRICS above
2. Improve the body while keeping the main message: bring its length, polarity, subjectivity and readability closer to the target BODY METRICS above, and make it clearer
3. Naturally incorporate popular keywords when it's possible.
4. Follow the guideline of the community : {community_guidelines}

RETURN ONLY valid JSON in this exact format, with no other text. You must also write in the same language as the current post's body and title:
{{"title": "new title here", "body": "new content here"}}
"""
