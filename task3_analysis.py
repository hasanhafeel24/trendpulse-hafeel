

import pandas as pd
import numpy as np


# Step 1: Load and Explore


file_path = "data/trends_clean.csv"

try:
    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")


# Step 2: Analysis using NumPy


scores = df["score"].values  # convert to numpy array

print("\n--- NumPy Stats ---")
print(f"Mean score   : {int(np.mean(scores))}")
print(f"Median score : {int(np.median(scores))}")
print(f"Std deviation: {int(np.std(scores))}")
print(f"Max score    : {np.max(scores)}")
print(f"Min score    : {np.min(scores)}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Story with most comments
max_comments_row = df.loc[df["num_comments"].idxmax()]
print(f'\nMost commented story: "{max_comments_row["title"]}" — {max_comments_row["num_comments"]} comments')


# Step 3: Add New Columns


# Engagement = comments per upvote
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular if score > average
df["is_popular"] = df["score"] > avg_score


# Step 4: Save the Result


output_path = "data/trends_analysed.csv"
df.to_csv(output_path, index=False)

print(f"\nSaved to {output_path}")