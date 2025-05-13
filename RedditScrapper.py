import os
from dotenv import load_dotenv
import praw
from textblob import TextBlob
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import datetime as dt


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
    label = ""
    if polarity >= 0.2:
        label = "Very Positive"
    elif polarity >= 0.1 and polarity < 0.2:
        label = "Positive"
    elif polarity >= 0.05 and polarity < 0.1:
        label = "Slightly Positive"
    elif polarity <= -0.05 and polarity > -0.1:
        label = "Slightly Negative"
    elif polarity <= -0.1:
        label = "Negative"
    elif polarity <= -0.2 and polarity > -0.1:
        label = "Very Negative"
    else:
        label = "Neutral"
    return label, polarity

def draw_pie_chart(keyword, subreddit_name, sizes, labels):

    # Draw a pie chart of the labels from the data
    plt.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',
        startangle=140, 
        wedgeprops={'width': 0.2}
        )
    plt.axis('equal') # Make it a circle
    plt.title(f"Sentiment Analysis for '{keyword}' in r/{subreddit_name}")
    plt.show()

def draw_bar_chart(keyword, subreddit_name, sizes, labels):

    # Draw a bar graph of the data
    plt.bar(labels, sizes)
    plt.xticks(rotation=30)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Posts/Comments")
    plt.title(f"Sentiment Analysis for '{keyword}' in r/{subreddit_name}")
    plt.tight_layout()
    plt.show()

def draw_line_graph(average_scores):
    dates = sorted(average_scores.keys())
    avg_values = [average_scores[date] for date in dates]

    plt.scatter(dates, avg_values, c=avg_values, cmap='coolwarm', edgecolors='k')
    plt.xticks(rotation=30)
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment Score")
    plt.title("Sentiment Over Time")
    plt.tight_layout()
    plt.show()

def see_graphs(keyword, subreddit_name, sizes, labels, average_scores):
    repeat = True
    while repeat:
        # Ask user if they would like to see the data put into a graph 
        chooseGraph = ""

        while chooseGraph not in ["1","2","3","4"]:
            chooseGraph = input("Would you like to see the data in a graph:\n1. Pie Chart\n2. Bar Graph\n3. Sentiments over time\n4. New Search\n")
        
        # Load graph the user asks for
        match chooseGraph:
            case "1":
                # Bar graph
                draw_bar_chart(keyword, subreddit_name, sizes, labels)
            
            case "2":
                # pie chart
                draw_pie_chart(keyword, subreddit_name, sizes, labels)
            
            case "3":
                # Sentiment over time
                draw_line_graph(average_scores)

            case "4":
                repeat = False


def main():

    newSearch = True

    while newSearch:
        # Holds resulting sentiments 
        sentiments = []
        timestamps_and_scores = []

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
            timestamp = dt.datetime.fromtimestamp(post.created_utc)
            label, polarity = analyze_sentiment(content)
            timestamps_and_scores.append((timestamp.date(), polarity))
            sentiments.append((content, label))

        # Analyze reddit post comments 
        for comment in subreddit.comments(limit=limit):
            if keyword.lower() in comment.body.lower():
                timestamp = dt.datetime.fromtimestamp(comment.created_utc)
                label, polarity = analyze_sentiment(comment.body)
                timestamps_and_scores.append((timestamp.date(), polarity))
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

        daily_scores = defaultdict(list)
        for date, score in timestamps_and_scores:
            daily_scores[date].append(score)

        average_scores = {date: sum(scores)/len(scores) for date, scores in daily_scores.items()}
        average_scores = dict(sorted(average_scores.items()))
        
        see_graphs(keyword, subreddit_name, sizes, labels, average_scores)

        choice = input("Would you like to make a new search? (Yes/No)\n")
        if choice.lower() != 'yes':
            print("Thank you for using my Reddit Scrapepr! Bye bye!")
            newSearch = False
    
main()