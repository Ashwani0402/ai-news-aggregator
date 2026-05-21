"""
Florida Man API Fetcher - Free, No API Key Required
Fetches real news headlines (fun but also real news!)
"""

import requests
from datetime import datetime
import random

class FloridaManFetcher:
    """Fetch real news headlines from Florida Man API - Completely free"""
    
    def __init__(self):
        self.base_url = "https://juliayxhuang.github.io/florida-man-api/api"
    
    def fetch_random_headlines(self, limit=20):
        """Fetch random headlines from the dataset"""
        try:
            # Florida Man API has headlines organized by date
            # Get all available months (01-12)
            articles = []
            
            # Fetch from multiple random dates to get variety
            months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            random.shuffle(months)
            
            for month in months[:3]:  # Fetch from 3 random months
                days = [str(d).zfill(2) for d in range(1, 29)]  # Days 01-28
                random.shuffle(days)
                
                for day in days[:2]:  # 2 random days per month
                    url = f"{self.base_url}/{month}/{day}.json"
                    try:
                        response = requests.get(url, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            for item in data[:5]:  # First 5 headlines from that day
                                articles.append({
                                    'title': item.get('title', ''),
                                    'description': item.get('title', ''),
                                    'source': item.get('source', 'News'),
                                    'url': item.get('url', ''),
                                    'date': f"2023-{month}-{day}",
                                    'keywords': item.get('keywords', []),
                                    'source_type': 'news',
                                    'platform': 'florida_man'
                                })
                                if len(articles) >= limit:
                                    break
                        time.sleep(0.5)  # Be respectful
                    except Exception as e:
                        continue
                    
                    if len(articles) >= limit:
                        break
                
                if len(articles) >= limit:
                    break
            
            print(f"✅ Florida Man API: {len(articles)} headlines fetched")
            return articles[:limit]
            
        except Exception as e:
            print(f"❌ Florida Man API error: {e}")
            return []
    
    def fetch_headlines_by_date(self, month, day, limit=20):
        """Fetch headlines from a specific date (month: 01-12, day: 01-31)"""
        try:
            url = f"{self.base_url}/{month}/{day}.json"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                for item in data[:limit]:
                    articles.append({
                        'title': item.get('title', ''),
                        'description': item.get('title', ''),
                        'source': item.get('source', 'News'),
                        'url': item.get('url', ''),
                        'date': f"2023-{month}-{day}",
                        'keywords': item.get('keywords', []),
                        'source_type': 'news',
                        'platform': 'florida_man'
                    })
                print(f"✅ Florida Man API ({month}/{day}): {len(articles)} headlines")
                return articles
            else:
                print(f"⚠️ No headlines found for {month}/{day}")
                return []
        except Exception as e:
            print(f"❌ Florida Man API error: {e}")
            return []

# Test the fetcher
if __name__ == "__main__":
    fetcher = FloridaManFetcher()
    
    print("📰 Testing Florida Man API...")
    articles = fetcher.fetch_random_headlines(limit=10)
    
    for article in articles[:5]:
        print(f"  📰 {article['title'][:80]}...")