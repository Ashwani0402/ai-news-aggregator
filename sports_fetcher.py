"""
Sports News Fetcher – Free sources for sports content
No API keys required – uses public RSS feeds
"""

import feedparser
from datetime import datetime

class SportsFetcher:
    def fetch_espn_rss(self, limit=10):
        """Fetch from ESPN RSS"""
        try:
            feed = feedparser.parse("http://www.espn.com/espn/rss/news")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'ESPN',
                    'url': entry.link,
                    'source_type': 'sports',
                    'category': 'sports',
                    'published': entry.get('published', datetime.now().isoformat())
                })
            return articles
        except Exception as e:
            print(f"ESPN error: {e}")
            return []
    
    def fetch_bbc_sport_rss(self, limit=10):
        """Fetch from BBC Sport RSS"""
        try:
            feed = feedparser.parse("http://feeds.bbci.co.uk/sport/rss.xml")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'BBC Sport',
                    'url': entry.link,
                    'source_type': 'sports',
                    'category': 'sports',
                    'published': entry.get('published', datetime.now().isoformat())
                })
            return articles
        except Exception as e:
            print(f"BBC Sport error: {e}")
            return []
    
    def fetch_sky_sports_rss(self, limit=10):
        """Fetch from Sky Sports RSS"""
        try:
            feed = feedparser.parse("https://www.skysports.com/rss/0,20514,11661,00.xml")
            articles = []
            for entry in feed.entries[:limit]:
                articles.append({
                    'title': entry.title,
                    'description': entry.description[:500] if hasattr(entry, 'description') else entry.title,
                    'source': 'Sky Sports',
                    'url': entry.link,
                    'source_type': 'sports',
                    'category': 'sports',
                    'published': entry.get('published', datetime.now().isoformat())
                })
            return articles
        except Exception as e:
            print(f"Sky Sports error: {e}")
            return []
    
    def fetch_all_sports(self, limit_per_source=8):
        all_articles = []
        print("\n🏆 Fetching Sports News...")
        
        espn = self.fetch_espn_rss(limit_per_source)
        print(f"  ESPN: {len(espn)} articles")
        all_articles.extend(espn)
        
        bbc = self.fetch_bbc_sport_rss(limit_per_source)
        print(f"  BBC Sport: {len(bbc)} articles")
        all_articles.extend(bbc)
        
        sky = self.fetch_sky_sports_rss(limit_per_source)
        print(f"  Sky Sports: {len(sky)} articles")
        all_articles.extend(sky)
        
        return all_articles