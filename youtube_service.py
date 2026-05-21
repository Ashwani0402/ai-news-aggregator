import requests

# PUT YOUR WORKING YOUTUBE KEY HERE
import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_videos(query, max_results=5):
    """Search YouTube videos"""
    url = "https://www.googleapis.com/youtube/v3/search"
    
    params = {
        'part': 'snippet',
        'q': query,
        'maxResults': max_results,
        'key': YOUTUBE_API_KEY,
        'type': 'video'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        videos = []
        
        for item in data.get('items', []):
            video = {
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'url': f"https://youtube.com/watch?v={item['id']['videoId']}"
            }
            videos.append(video)
        
        return videos
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        return []

if __name__ == "__main__":
    print("Testing YouTube API...")
    videos = search_videos("AI tutorial", 3)
    for v in videos:
        print(f"📹 {v['title']}")