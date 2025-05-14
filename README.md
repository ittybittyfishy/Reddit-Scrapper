# Reddit Sentiment Analyzer (Terminal)

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

   git clone https://github.com/ittybittyfishy/Reddit-Scrapper.git
   cd reddit-sentiment-analyzer

2. Install the required libraries:

   pip install -r requirements.txt

3. Create a `.env` file with your Reddit app credentials:
   ```
   REDDIT_CLIENT_ID=your_id_here
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USER_AGENT=analyzer by u/your_username
   REDDIT_USERNAME=your_username
   REDDIT_PASSWORD=your_password
   ```

   Create a Reddit API App. Go to: https://www.reddit.com/prefs/apps

   1. Scroll down to “Developed Applications” -> Click “Create App”

   2. Fill in:
         - Name: e.g. reddit-sentiment-analyzer
         - Type: Script
         - Redirect URI: http://localhost:8080 (required, even if unused)

   3. Submit -> Copy:
         - client_id (right under the app name)
         - client_secret

   4. Then plug those into a .env file

## Usage

Run the program:

   python reddit_scraper.py

- Input subreddit, keyword, and number of posts.
- Choose how to view data: pie chart, bar graph, sentiment over time.
- Optionally browse posts by sentiment category.
- Repeat or exit.
