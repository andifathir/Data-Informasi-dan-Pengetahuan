import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Load dataset
df = pd.read_csv("reddit_fitness_trends.csv")

# Show first few rows
print(df.head())

df["Text"] = df["Text"].fillna("No text")
df["Text"] = df["Text"].fillna("No text")
df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
df["Date"] = df["Timestamp"].dt.date  # Extract only the date
df["Post_Age_Days"] = (pd.to_datetime("today") - df["Timestamp"]).dt.days
df["Text_Length"] = df["Text"].apply(len)
df["High_Engagement"] = df["Upvotes"].apply(lambda x: "Yes" if x > 50 else "No")

# Keep only necessary columns
df = df[["Title", "Text", "Subreddit","Upvotes", "Comments", "Date"]]

# Combine title and post text for better analysis
df["Full_Text"] = df["Title"] + " " + df["Text"]

# Remove empty or very short posts
df = df[df["Full_Text"].str.len() > 10]

nltk.download('stopwords')
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"\W", " ", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    text = " ".join([word for word in text.split() if word not in stop_words])  # Remove stopwords
    return text

df["Clean_Text"] = df["Full_Text"].apply(clean_text)

df.to_csv("transformed_reddit_fitness_data.csv", index=False)



