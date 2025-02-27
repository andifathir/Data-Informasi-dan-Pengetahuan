import praw
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

try:
    subreddit = reddit.subreddit("Python")
    for post in subreddit.hot(limit=5):
        print(post.title)
except Exception as e:
    print(f"Error: {e}")
