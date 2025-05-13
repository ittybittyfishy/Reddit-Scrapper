# Reddit Sentiment Analyzer (Terminal Edition)

A command-line tool that scrapes Reddit posts & comments using PRAW,
analyzes their sentiment with VADER (Valence Aware Dictionary), and 
displays the results using pie charts, bar graphs, and emotional 
trends over time.

## Features

- Search Reddit for posts and comments by keyword
- Sentiment analysis with 7 categories:
  - Very Positive, Positive, Slightly Positive
  - Neutral
  - Slightly Negative, Negative, Very Negative
- Graphing support:
  - Pie chart
  - Bar graph
  - Scatterplot over time
- Option to view posts grouped by sentiment

## Technologies Used

- Python
- PRAW (Reddit API)
- VADER Sentiment Analyzer
- Matplotlib
- python-dotenv

## Setup Instructions

1. Clone the repo:

   git clone https://github.com/YOUR_USERNAME/reddit-sentiment-analyzer.git
   cd reddit-sentiment-analyzer

2. Install the required libraries:

   pip install -r requirements.txt

3. Create a `.env` file with your Reddit app credentials:

   REDDIT_CLIENT_ID=your_id_here
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USER_AGENT=analyzer by u/your_username
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password

## Usage

Run the program:

   python reddit_scraper.py

- Input subreddit, keyword, and number of posts.
- Choose how to view data: pie chart, bar graph, sentiment over time.
- Optionally browse posts by sentiment category.
- Repeat or exit.
