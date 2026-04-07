

import pandas as pd
import os

# Step 1: Load JSON file
file_path = "data/trends_20260407.json"   # change date if needed

try:
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()


# Step 2: Clean the data


# Remove duplicates based on post_id
before = len(df)
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# Remove rows with missing values in important columns
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert score and num_comments to integer
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low-quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra spaces from title
df["title"] = df["title"].str.strip()


# Step 3: Save as CSV

output_path = "data/trends_clean.csv"

df.to_csv(output_path, index=False)

print(f"\nSaved {len(df)} rows to {output_path}")



print("\nStories per category:")
print(df["category"].value_counts())