import requests
import time
import json
import os
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def get_category(title):
    title_lower = title.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None  # ignore if no match


def main():
    try:
        # Step 1: Fetch top story IDs
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        story_ids = response.json()[:500]  # first 500
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    collected_data = []
    category_count = {cat: 0 for cat in categories}

    # Loop through categories
    for category in categories:
        print(f"Processing category: {category}")

        for story_id in story_ids:
            # Stop if we already have 25 stories for this category
            if category_count[category] >= 25:
                break

            try:
                story_res = requests.get(ITEM_URL.format(story_id), headers=headers)
                story_res.raise_for_status()
                story = story_res.json()
            except Exception as e:
                print(f"Failed to fetch story {story_id}: {e}")
                continue

            # Skip if no title
            if not story or "title" not in story:
                continue

            # Assign category
            assigned_category = get_category(story["title"])

            # Check if it matches current category
            if assigned_category == category:
                data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": assigned_category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(data)
                category_count[category] += 1

        # Sleep AFTER each category (important rule)
        time.sleep(2)

    # Step 3: Save JSON file
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"Collected {len(collected_data)} stories. Saved to {filename}")


# Run the script
if __name__ == "__main__":
    main()