import os
from dotenv import load_dotenv
import praw
from textblob import TextBlob
from collections import Counter

load_dotenv()  # Load Reddit project inforamtion from .env

# PRAW Credentials 
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# TextBlob Sentiment Analyzer 
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity >= 0.2:
        return "Very Positive"
    elif polarity >= 0.1 and polarity < 0.2:
        return "Positive"
    elif polarity >= 0.05 and polarity < 0.1:
        return "Slightly Positive"
    elif polarity <= -0.05 and polarity > -0.1:
        return "Slightly Negative"
    elif polarity <= -0.1:
        return "Negative"
    elif polarity <= -0.2 and polarity > -0.1:
        return "Very Negative"
    else:
        return "Neutral"

# Holds resulting sentiments 
sentiments = []

# User input to get results
subreddit_name = input("Enter subreddit (or 'all'): ")
keyword = input("Enter search keyword: ")
limit = int(input("How many posts? "))

# Ensure subreddit exists
subreddit = reddit.subreddit(subreddit_name)

# Analyze title and content of post and assign sentimanet score
for post in subreddit.search(keyword, limit=limit):
    if post.selftext:
        content = f"{post.title}\n{post.selftext}"
    else: 
        content = post.title
    label = analyze_sentiment(content)
    sentiments.append((content, label))

for comment in subreddit.comments(limit=limit):
    if keyword.lower() in comment.body.lower():
        label = analyze_sentiment(comment.body)
        sentiments.append((comment.body, label))

for text, label in sentiments:
    print(f"\n[{label}]\n{text[:300]}...\n")

sentiment_counts = Counter([label for _, label in sentiments])
print(sentiment_counts)