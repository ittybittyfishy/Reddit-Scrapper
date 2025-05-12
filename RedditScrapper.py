import os
from dotenv import load_dotenv
import praw
from textblob import TextBlob
from collections import Counter
import matplotlib.pyplot as plt


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

def draw_pie_chart(keyword, subreddit_name, sizes, labels):

    plt.pie(sizes, labels=labels, autopct='%1.1f%%',startangle=140)
    plt.axis('equal') # Make it a circle
    plt.title(f"Sentiment Analysis for '{keyword}' in r/{subreddit_name}")
    plt.show()

def draw_bar_chart(keyword, subreddit_name, sizes, labels):

    plt.bar(labels, sizes)
    plt.xticks(rotation=30)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Posts/Comments")
    plt.title(f"Sentiment Analysis for '{keyword}' in r/{subreddit_name}")
    plt.tight_layout()
    plt.show()

def main():

    newSearch = True

    while newSearch:
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
            # Ensure that the post body is not empty
            if post.selftext:
                content = f"{post.title}\n{post.selftext}"
            else: 
                # If the post body is empty, only analyze post title
                content = post.title
            label = analyze_sentiment(content)
            sentiments.append((content, label))

        # Analyze reddit post comments 
        for comment in subreddit.comments(limit=limit):
            if keyword.lower() in comment.body.lower():
                label = analyze_sentiment(comment.body)
                sentiments.append((comment.body, label))

        # for text, label in sentiments:
        #     print(f"\n[{label}]\n{text[:300]}...\n")

        # Count number of each label 
        sentiment_counts = Counter([label for _, label in sentiments])

        # Sort the labels
        ordered_labels = [
            "Very Positive",
            "Positive",
            "Slightly Positive",
            "Neutral",
            "Slightly Negative",
            "Negative",
            "Very Negative"
        ]

        labels = []
        sizes = []

        for label in ordered_labels:
            if label in sentiment_counts:
                labels.append(label)
                sizes.append(sentiment_counts[label])

        # Print the sentiment analysis
        print(sentiment_counts)

        # Ask user if they would like to see the data put into a graph 
        chooseGraph = ""

        while chooseGraph not in ["1","2","3"]:
            chooseGraph = input("Would you like to see the inforion displayed as: \n1. Bar graph\n2. Pie chart\n3. New search\n")
        
        # Load graph the user asks for
        match chooseGraph:
            case "1":
                # Bar graph
                draw_bar_chart(keyword, subreddit_name, sizes, labels)
                otherGraph = input("Would you like to see the pie graph? (Yes/No)")
                if otherGraph.lower() == 'yes':
                    draw_pie_chart(keyword, subreddit_name, sizes, labels)
                else:
                    continue
            
            case "2":
                # pie chart
                draw_pie_chart(keyword, subreddit_name, sizes, labels)
                otherGraph = input("Would you like to see the bar graph? (Yes/No)")
                if otherGraph.lower() == 'yes':
                    draw_bar_chart(keyword, subreddit_name, sizes, labels)
                else:
                    continue
            case "3":
                # New Search
                continue
        
        # Ask user if they would lilke to do a new search
        nextSearch = input("Would you like to do a new search? (Yes/No)")
        if nextSearch.lower() != 'yes':
            newSearch = False

main()