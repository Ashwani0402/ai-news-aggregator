"""
Backup News Fetcher - Reliable Free News Sources
No API keys required - Works immediately
"""

import requests
import feedparser
from datetime import datetime
import urllib.parse

class BackupNewsFetcher:
    """Reliable free news sources that always work"""
    
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    def fetch_google_news_rss(self, query='artificial+intelligence', limit=15):
        """Fetch from Google News RSS - Fixed URL encoding"""
        try:
            # Encode the query properly (replace spaces with +)
            encoded_query = query.replace(' ', '+')
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if entry.description else entry.title,
                    'source': 'Google News',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'news',
                    'platform': 'google_news'
                })
            print(f"✅ Google News: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ Google News error: {e}")
            return []
    
    def fetch_bbc_news_rss(self, limit=15):
        """Fetch from BBC News RSS"""
        try:
            url = "http://feeds.bbci.co.uk/news/technology/rss.xml"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'BBC News',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'news',
                    'platform': 'bbc'
                })
            print(f"✅ BBC News: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ BBC News error: {e}")
            return []
    
    def fetch_reuters_rss(self, limit=10):
        """Fetch from Reuters Technology RSS"""
        try:
            url = "https://www.reuters.com/technology/feed/"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'Reuters',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'news',
                    'platform': 'reuters'
                })
            print(f"✅ Reuters: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ Reuters error: {e}")
            return []
    
    def fetch_techcrunch_rss(self, limit=15):
        """Fetch from TechCrunch RSS"""
        try:
            url = "https://techcrunch.com/feed/"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'TechCrunch',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'tech',
                    'platform': 'techcrunch'
                })
            print(f"✅ TechCrunch: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ TechCrunch error: {e}")
            return []
    
    def fetch_wired_rss(self, limit=10):
        """Fetch from Wired RSS"""
        try:
            url = "https://www.wired.com/feed/rss"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'Wired',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'tech',
                    'platform': 'wired'
                })
            print(f"✅ Wired: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ Wired error: {e}")
            return []
    
    def fetch_venturebeat_rss(self, limit=10):
        """Fetch from VentureBeat AI section"""
        try:
            url = "https://venturebeat.com/category/ai/feed/"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'VentureBeat',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'ai_news',
                    'platform': 'venturebeat'
                })
            print(f"✅ VentureBeat AI: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ VentureBeat error: {e}")
            return []
    
    def fetch_theverge_rss(self, limit=10):
        """Fetch from The Verge AI section"""
        try:
            url = "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
            feed = feedparser.parse(url)
            
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'The Verge',
                    'url': entry.link,
                    'published': entry.get('published', datetime.now().isoformat()),
                    'source_type': 'ai_news',
                    'platform': 'theverge'
                })
            print(f"✅ The Verge AI: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"⚠️ The Verge error: {e}")
            return []
    
    def fetch_all_sources(self, limit_per_source=8):
        """Fetch from all reliable news sources"""
        all_articles = []
        
        print("\n📰 Fetching from backup news sources...")
        
        # Source 1: Google News
        google_articles = self.fetch_google_news_rss(limit=limit_per_source)
        all_articles.extend(google_articles)
        
        # Source 2: TechCrunch
        techcrunch_articles = self.fetch_techcrunch_rss(limit=limit_per_source)
        all_articles.extend(techcrunch_articles)
        
        # Source 3: BBC News
        bbc_articles = self.fetch_bbc_news_rss(limit=limit_per_source)
        all_articles.extend(bbc_articles)
        
        # Source 4: Reuters
        reuters_articles = self.fetch_reuters_rss(limit=limit_per_source)
        all_articles.extend(reuters_articles)
        
        # Source 5: Wired
        wired_articles = self.fetch_wired_rss(limit=limit_per_source)
        all_articles.extend(wired_articles)
        
        # Source 6: VentureBeat AI (NEW!)
        vb_articles = self.fetch_venturebeat_rss(limit=limit_per_source)
        all_articles.extend(vb_articles)
        
        # Source 7: The Verge AI (NEW!)
        verge_articles = self.fetch_theverge_rss(limit=limit_per_source)
        all_articles.extend(verge_articles)
        
        print(f"\n📊 TOTAL backup news: {len(all_articles)} articles")
        return all_articles

if __name__ == "__main__":
    fetcher = BackupNewsFetcher()
    articles = fetcher.fetch_all_sources(limit_per_source=6)
    
    print("\n" + "="*50)
    print("Sample articles:")
    for article in articles[:10]:
        print(f"  📰 [{article['source']}] {article['title'][:60]}...")