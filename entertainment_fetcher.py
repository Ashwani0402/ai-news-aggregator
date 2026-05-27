"""
Entertainment News Fetcher – Free sources for movies, web series, entertainment
No API keys required – uses public RSS feeds
"""

import feedparser
from datetime import datetime

class EntertainmentFetcher:
    def fetch_variety_rss(self, limit=10):
        """Fetch from Variety (movies/entertainment)"""
        try:
            feed = feedparser.parse("https://variety.com/feed/")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'Variety',
                    'url': entry.link,
                    'source_type': 'entertainment',
                    'category': 'entertainment',
                    'published': entry.get('published', datetime.now().isoformat())
                })
            return articles
        except Exception as e:
            print(f"Variety error: {e}")
            return []
    
    def fetch_hollywood_reporter_rss(self, limit=10):
        """Fetch from Hollywood Reporter"""
        try:
            feed = feedparser.parse("https://www.hollywoodreporter.com/feed/")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'Hollywood Reporter',
                    'url': entry.link,
                    'source_type': 'entertainment',
                    'category': 'entertainment',
                    'published': entry.get('published', datetime.now().isoformat())
                })
            return articles
        except Exception as e:
            print(f"Hollywood Reporter error: {e}")
            return []
    
    def fetch_ign_rss(self, limit=10):
        """Fetch from IGN (movies/gaming)"""
        try:
            feed = feedparser.parse("https://www.ign.com/rss")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'IGN',
                    'url': entry.link,
                    'source_type': 'entertainment',
                    'category': 'entertainment',
                    'published': entry.get('published', datetime.now().isoformat())
                })
            return articles
        except Exception as e:
            print(f"IGN error: {e}")
            return []
    
    def fetch_all_entertainment(self, limit_per_source=8):
        all_articles = []
        print("\n🎬 Fetching Entertainment News...")
        
        variety = self.fetch_variety_rss(limit_per_source)
        print(f"  Variety: {len(variety)} articles")
        all_articles.extend(variety)
        
        hr = self.fetch_hollywood_reporter_rss(limit_per_source)
        print(f"  Hollywood Reporter: {len(hr)} articles")
        all_articles.extend(hr)
        
        ign = self.fetch_ign_rss(limit_per_source)
        print(f"  IGN: {len(ign)} articles")
        all_articles.extend(ign)
        
        return all_articles