"""
Hacker News Fetcher - Completely Free, No API Key Required
Fetches top tech/AI stories from Hacker News
"""

import requests
from datetime import datetime
import time

class HackerNewsFetcher:
    """Fetch top stories from Hacker News - No API key needed"""
    
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
        self.session = requests.Session()
    
    def fetch_top_stories(self, limit=25):
        """Fetch top stories from Hacker News"""
        try:
            # Get top story IDs
            response = self.session.get(f"{self.base_url}/topstories.json", timeout=10)
            if response.status_code != 200:
                print(f"❌ Hacker News API error: {response.status_code}")
                return []
            
            story_ids = response.json()[:limit]
            articles = []
            
            for story_id in story_ids:
                # Get individual story details
                story_response = self.session.get(f"{self.base_url}/item/{story_id}.json", timeout=10)
                if story_response.status_code == 200:
                    story = story_response.json()
                    if story and story.get('title'):
                        articles.append({
                            'title': story.get('title', ''),
                            'description': (story.get('text', '') or story.get('title', ''))[:500],
                            'source': 'Hacker News',
                            'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'published': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                            'score': story.get('score', 0),
                            'author': story.get('by', 'unknown'),
                            'source_type': 'tech',
                            'platform': 'hacker_news'
                        })
                
                # Be respectful of rate limits
                time.sleep(0.1)
            
            print(f"✅ Hacker News: {len(articles)} articles fetched")
            return articles
            
        except Exception as e:
            print(f"❌ Hacker News error: {e}")
            return []
    
    def fetch_new_stories(self, limit=15):
        """Fetch newest stories from Hacker News"""
        try:
            response = self.session.get(f"{self.base_url}/newstories.json", timeout=10)
            if response.status_code != 200:
                return []
            
            story_ids = response.json()[:limit]
            articles = []
            
            for story_id in story_ids:
                story_response = self.session.get(f"{self.base_url}/item/{story_id}.json", timeout=10)
                if story_response.status_code == 200:
                    story = story_response.json()
                    if story and story.get('title'):
                        articles.append({
                            'title': story.get('title', ''),
                            'description': (story.get('text', '') or story.get('title', ''))[:500],
                            'source': 'Hacker News (New)',
                            'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                            'published': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                            'source_type': 'tech',
                            'platform': 'hacker_news'
                        })
                time.sleep(0.1)
            
            return articles
        except Exception as e:
            print(f"❌ Hacker News new stories error: {e}")
            return []
    
    def search_hacker_news(self, query='ai', limit=20):
        """Search Hacker News for specific topics"""
        # Note: Hacker News doesn't have a native search API
        # This uses Algolia's HN Search API (free, no key)
        try:
            url = f"https://hn.algolia.com/api/v1/search?query={query}&tags=story&hitsPerPage={limit}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                for hit in data.get('hits', []):
                    articles.append({
                        'title': hit.get('title', ''),
                        'description': hit.get('comment_text', '')[:500] if hit.get('comment_text') else hit.get('title', ''),
                        'source': f'Hacker News Search: {query}',
                        'url': hit.get('url', f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"),
                        'published': datetime.fromtimestamp(hit.get('created_at_i', 0)).isoformat(),
                        'source_type': 'search',
                        'platform': 'hacker_news'
                    })
                print(f"✅ Hacker News Search ({query}): {len(articles)} results")
                return articles
            return []
        except Exception as e:
            print(f"❌ Hacker News search error: {e}")
            return []

# Test the fetcher
if __name__ == "__main__":
    fetcher = HackerNewsFetcher()
    
    print("📱 Testing Hacker News Fetcher...")
    articles = fetcher.fetch_top_stories(limit=10)
    
    for article in articles[:5]:
        print(f"  📰 [{article['source']}] {article['title'][:60]}...")