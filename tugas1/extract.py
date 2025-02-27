import praw
import pandas as pd
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Authenticate with Reddit
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Define subreddits
subreddits = ["loseit", "gainit", "Fitness", "bodyweightfitness"]

# Extract posts with pagination support
def extract_reddit_posts(subreddit_name, post_limit=1000, max_posts=4000):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    after = None

    while len(posts) < max_posts:
        # Get posts, if there is 'after', use it to continue from the last post
        for post in subreddit.hot(limit=post_limit, params={'after': after}):
            posts.append([
                post.title,
                post.selftext,
                post.score,
                post.num_comments,
                post.created_utc,
                subreddit_name
            ])

            # Stop once we hit the max number of posts we want
            if len(posts) >= max_posts:
                break

        # Get the last post name to continue scraping
        after = posts[-1][0]  # Use the last post's identifier as 'after'
        time.sleep(1)  # Sleep to avoid rate limit issues

    return posts

# Collect data from all subreddits
data = []
for sub in subreddits:
    data.extend(extract_reddit_posts(sub))

# Convert to DataFrame
df = pd.DataFrame(data, columns=["Title", "Text", "Upvotes", "Comments", "Timestamp", "Subreddit"])

# Save to CSV
df.to_csv("reddit_fitness_trends.csv", index=False)

print(f"Data scraped and saved to reddit_fitness_trends.csv with {len(df)} posts!")
