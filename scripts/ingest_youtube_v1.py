import requests
import json
from google.cloud import storage
import time

API_KEY = "AIzaSyBkmnifGSrVItOfLfyxbLpkIoxDHfXIZS4"
VIDEOS_ENDPOINT = "https://www.googleapis.com/youtube/v3/videos"
CATEGORIES_ENDPOINT = "https://www.googleapis.com/youtube/v3/videoCategories"
BUCKET_NAME = "youtube-trending-raw"

# List of 10 countries with their ISO 3166-1 alpha-2 region codes
COUNTRIES = [
    "US",  # United States
    "IN",  # India
    "GB",  # United Kingdom
    "CA",  # Canada
    "AU",  # Australia
    "BR",  # Brazil
    "DE",  # Germany
    "FR",  # France
    "JP",  # Japan
    "KR"   # South Korea
]

def fetch_video_categories():
    """Fetch category ID-to-name mapping for all regions."""
    params = {
        "part": "snippet",
        "regionCode": "US",  # Use a default region; categories are mostly global
        "key": API_KEY
    }
    response = requests.get(CATEGORIES_ENDPOINT, params=params)
    categories_data = response.json()
    
    # Create a dictionary of category ID to name
    category_map = {
        item["id"]: item["snippet"]["title"]
        for item in categories_data.get("items", [])
    }
    return category_map

def fetch_trending_videos(region_code):
    """Fetch trending videos for a specific region."""
    params = {
        "part": "snippet,statistics,contentDetails",  # Added contentDetails
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": 50,
        "key": API_KEY
    }
    response = requests.get(VIDEOS_ENDPOINT, params=params)
    return response.json()

def upload_to_gcs(data, timestamp, region_code):
    """Upload data to GCS with region-specific path."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"raw/{region_code}/{timestamp}.json")
    blob.upload_from_string(json.dumps(data))

if __name__ == "__main__":
    # Fetch category mapping once (static data, no need to fetch repeatedly)
    category_map = fetch_video_categories()
    print("Fetched category mapping:", category_map)

    while True:
        for region_code in COUNTRIES:
            # Fetch trending videos for the region
            video_data = fetch_trending_videos(region_code)
            
            # Add category names to each video item
            for item in video_data.get("items", []):
                category_id = item["snippet"].get("categoryId")
                if category_id in category_map:
                    item["snippet"]["categoryName"] = category_map[category_id]
                else:
                    item["snippet"]["categoryName"] = "Unknown"

            # Generate timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            
            # Upload to GCS with region-specific folder
            upload_to_gcs(video_data, timestamp, region_code)
            print(f"Uploaded data for {region_code} at {timestamp}")
        
        # Sleep for 15 minutes (900 seconds) after processing all countries
        time.sleep(900)
