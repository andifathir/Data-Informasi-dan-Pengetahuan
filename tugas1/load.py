from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Default connection

# Create/select a database
db = client["reddit_fitness"]

# Create/select a collection (like a table in SQL)
collection = db["posts"]

print("Connected to MongoDB!")

# Ensure dataframe is loaded
df = pd.read_csv("transformed_reddit_fitness_data.csv")

# Convert DataFrame to a dictionary format for MongoDB
data_dict = df.to_dict(orient="records")

# Insert data into MongoDB
collection.insert_many(data_dict)

print(f"Inserted {len(data_dict)} posts into MongoDB!")
