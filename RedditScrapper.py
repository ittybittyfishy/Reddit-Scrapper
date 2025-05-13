import os
from dotenv import load_dotenv
import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import datetime as dt

# ============================
# Reddit Sentiment Analyzer
# ============================

# Load Reddit project inforamtion from .env
load_dotenv()  

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Configure PRAW Credentials from env
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# Function to analyze sentiment and assign a label
def analyze_sentiment(text):
    # Get sentiment scoresL compound score ranges from -1(negative) to +1 (positive)
    score = analyzer.polarity_scores(text)
    compound = score['compound']  # Ranges from -1 to 1

    # Categorize the score into a human-readable label
    if compound >= 0.5:
        label = "Very Positive"
    elif compound >= 0.2:
        label = "Positive"
    elif compound >= 0.05:
        label = "Slightly Positive"
    elif compound <= -0.5:
        label = "Very Negative"
    elif compound <= -0.2:
        label = "Negative"
    elif compound <= -0.05:
        label = "Slightly Negative"
    else:
        label = "Neutral"

    return label, compound

# Plot a pie chart to show the distrbution of sentiment categories
def draw_pie_chart(keyword, subreddit_name, sizes, labels):
    plt.pie(
        sizes, 
        labels=labels, 
        autopct='%1.1f%%',
        startangle=140, 
        wedgeprops={'width': 0.2}
        )
    plt.axis('equal') # Keeps it circular
    plt.title(f"Sentiment Analysis for '{keyword}' in r/{subreddit_name}")
    plt.show()

# Plot a bar chart to compare sentiment catergory frequencies 
def draw_bar_chart(keyword, subreddit_name, sizes, labels):
    plt.bar(labels, sizes)
    plt.xticks(rotation=30)
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Posts/Comments")
    plt.title(f"Sentiment Analysis for '{keyword}' in r/{subreddit_name}")
    plt.tight_layout()
    plt.show()

# Plot a scatterplot of average sentiment score by day
def draw_line_graph(average_scores):
    # Get average sentiment score based on date
    dates = sorted(average_scores.keys())
    avg_values = [average_scores[date] for date in dates]

    plt.scatter(dates, avg_values, c=avg_values, cmap='coolwarm', edgecolors='k')
    plt.xticks(rotation=30)
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment Score")
    plt.title("Sentiment Over Time")
    plt.tight_layout()
    plt.show()

# Allow users to view posts grouped by a specific sentiment label
def viewPosts(labels, grouped_by_label):
    userViewPosts = True
    while userViewPosts:
        print("Available categories:")
        for label in labels:
            print(f"- {label}")

        # Ask the user for which sentiment they want to review     
        selected_label = input("Which sentiment would you like to see posts from?: ")
        posts = grouped_by_label.get(selected_label, [])

        # If the chosen sentiment has posts, print them 
        if posts:
            print(f"\n--- Showing posts/comments labeled '{selected_label}' ---")
            for i, text in enumerate(posts, 1):
                # Limit the length of the post
                print(f"\n#{i}:\n{text[:500]}{'...' if len(text) > 500 else ''}")
        else:
            print("No posts found for that sentiment.")

        # Ask if they'd like to continue browsing posts              
        choice = input("\nWould you like to see posts with a different sentiment? (Yes/No)\n")
        if choice.lower() != 'yes':
            userViewPosts = False

# Display visualizations or allow post review based on user selection
def see_graphs(keyword, subreddit_name, sizes, labels, average_scores, grouped_by_label):
    repeat = True
    while repeat:

        # Get user choice for option
        chooseGraph = ""
        while chooseGraph not in ["1","2","3","4","5"]:
            chooseGraph = input("Would you like to see the data in a graph:\n1. Pie Chart\n2. Bar Graph\n3. Sentiments over time\n4. See posts based on specific sentiment\n5. New Search\n")
        
        # Load graph the user asks for
        match chooseGraph:
            case "1":
                # pie chart
                draw_pie_chart(keyword, subreddit_name, sizes, labels)
            
            case "2":
                # Bar graph
                draw_bar_chart(keyword, subreddit_name, sizes, labels)
            
            case "3":
                # Sentiment over time
                draw_line_graph(average_scores)

            case "4":
                # View other user posts
                viewPosts(labels, grouped_by_label)

            case "5":
                repeat = False

# Main program loop: handles user input and runs analysis
def main():
    newSearch = True

    while newSearch:
        sentiments = [] # stores (text, label)
        timestamps_and_scores = [] # stores (date, polarity score)
        grouped_by_label = defaultdict(list) # stores label -> list of text

        # Get user input
        subreddit_name = input("Enter desired subreddit (or 'all'): ")
        keyword = input("Enter search keyword: ")
        limit = int(input("How many posts would you like to parse? "))

        # Set subreddit
        subreddit = reddit.subreddit(subreddit_name)

        # Analyze reddit posts
        for post in subreddit.search(keyword, limit=limit):
            # Ensure that the post body is not empty
            if post.selftext:
                content = f"{post.title}\n{post.selftext}"
            else: 
                # If the post body is empty, only analyze post title
                content = post.title

            timestamp = dt.datetime.fromtimestamp(post.created_utc)
            label, polarity = analyze_sentiment(content)

            sentiments.append((content, label))
            timestamps_and_scores.append((timestamp.date(), polarity))
            grouped_by_label[label].append(content)

        # Analyze subreddit comments 
        for comment in subreddit.comments(limit=limit):
            if keyword.lower() in comment.body.lower():
                timestamp = dt.datetime.fromtimestamp(comment.created_utc)
                label, polarity = analyze_sentiment(comment.body)

                sentiments.append((comment.body, label))
                timestamps_and_scores.append((timestamp.date(), polarity))
                grouped_by_label[label].append(comment.body)

        # Prepare sorted label list and their corresponding counts
        sentiment_counts = Counter([label for _, label in sentiments])

        # Sort the labels from Very Postive to Very Negative
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

        # Organize scores by date for trend analysis
        daily_scores = defaultdict(list)
        for date, score in timestamps_and_scores:
            daily_scores[date].append(score)

        # Calculate daily average sentiment score
        average_scores = {date: sum(scores)/len(scores) for date, scores in daily_scores.items()}
        average_scores = dict(sorted(average_scores.items()))
        
        # Show visualizations and allow post exploration
        see_graphs(keyword, subreddit_name, sizes, labels, average_scores, grouped_by_label)

        # Ask if user wants to start a new analysis
        choice = input("Would you like to make a new search? (Yes/No)\n")
        if choice.lower() != 'yes':
            print("Thank you for using my Reddit Scraper! Bye bye!")
            newSearch = False

# Run the program   
main()