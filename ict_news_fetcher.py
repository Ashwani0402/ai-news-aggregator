"""
ICT News Fetcher - Free news from multiple sources
Supports: ICT News MCP, Hacker News, Florida Man API
"""
# Add at the top with other imports
from backup_news_fetcher import BackupNewsFetcher

# Add this method to the ICTNewsFetcher class
def fetch_with_backup(self, limit_per_source=10):
    """
    Fetch news with automatic backup if ICT News fails
    """
    print("\n📡 Fetching from news sources...")
    
    # Try ICT News first
    ict_articles = self.fetch_latest_news(limit=limit_per_source)
    
    if len(ict_articles) > 0:
        print(f"✅ ICT News: {len(ict_articles)} articles")
        return ict_articles
    else:
        print("⚠️ ICT News unavailable, using backup sources...")
        backup = BackupNewsFetcher()
        return backup.fetch_all_sources(limit_per_source=limit_per_source)

import requests
import json
from datetime import datetime
import sys
import os

# Import the new fetchers
from hacker_news_fetcher import HackerNewsFetcher
from florida_man_fetcher import FloridaManFetcher

class ICTNewsFetcher:
    """Enhanced news fetcher with multiple free sources"""
    
    def __init__(self):
        self.base_url = "https://news.ictinnovations.com"
        self.hacker_news = HackerNewsFetcher()
        self.florida_man = FloridaManFetcher()
        
    def fetch_latest_news(self, limit=20, category=None, source=None):
        """Fetch latest news from ICT MCP"""
        url = f"{self.base_url}/mcp"
        
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "get_latest_news",
                "arguments": {
                    "limit": limit,
                    "category": category,
                    "source": source
                }
            },
            "id": 1
        }
        
        try:
            response = requests.post(url, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return self._parse_news_response(data)
            else:
                print(f"⚠️ ICT News error: {response.status_code}")
                return []
        except Exception as e:
            print(f"⚠️ ICT News connection error: {e}")
            return []
    
    def fetch_all_sources(self, limit_per_source=15):
        """
        Fetch from ALL available free news sources
        Returns combined articles from:
        - ICT News MCP
        - Hacker News
        - Florida Man API
        """
        all_articles = []
        
        print("\n📡 Fetching from multiple free news sources...")
        
        # Source 1: ICT News MCP
        print("  📰 Fetching ICT News MCP...")
        ict_articles = self.fetch_latest_news(limit=limit_per_source)
        for article in ict_articles:
            article['source_category'] = 'news'
        all_articles.extend(ict_articles)
        print(f"    ✓ Got {len(ict_articles)} articles")
        
        # Source 2: Hacker News
        print("  💻 Fetching Hacker News...")
        hn_articles = self.hacker_news.fetch_top_stories(limit=limit_per_source)
        for article in hn_articles:
            article['source_category'] = 'tech'
        all_articles.extend(hn_articles)
        print(f"    ✓ Got {len(hn_articles)} articles")
        
        # Source 3: Florida Man API (real headlines)
        print("  📰 Fetching Florida Man headlines...")
        fm_articles = self.florida_man.fetch_random_headlines(limit=limit_per_source)
        for article in fm_articles:
            article['source_category'] = 'headlines'
        all_articles.extend(fm_articles)
        print(f"    ✓ Got {len(fm_articles)} headlines")
        
        print(f"\n📊 TOTAL: {len(all_articles)} articles from all sources")
        return all_articles
    
    def _parse_news_response(self, data):
        """Parse ICT News MCP response"""
        articles = []
        
        if 'result' in data and 'content' in data['result']:
            for item in data['result']['content']:
                if 'text' in item:
                    try:
                        article_data = json.loads(item['text'])
                        articles.append({
                            'title': article_data.get('title', ''),
                            'description': article_data.get('description', ''),
                            'source': article_data.get('source', 'ICT News'),
                            'url': article_data.get('url', ''),
                            'published': article_data.get('published_at', datetime.now().isoformat()),
                            'category': article_data.get('category', 'general'),
                            'source_type': 'news'
                        })
                    except:
                        articles.append({
                            'title': item['text'][:100],
                            'description': item['text'],
                            'source': 'ICT News',
                            'url': '',
                            'published': datetime.now().isoformat(),
                            'source_type': 'news'
                        })
        
        return articles

# Test the enhanced fetcher
if __name__ == "__main__":
    fetcher = ICTNewsFetcher()
    
    print("="*60)
    print("🚀 Testing Multi-Source News Fetcher")
    print("="*60)
    
    all_articles = fetcher.fetch_all_sources(limit_per_source=10)
    
    print(f"\n📋 Sample of fetched content:")
    for i, article in enumerate(all_articles[:10], 1):
        print(f"{i:2}. [{article.get('source', 'Unknown')}] {article['title'][:70]}...")