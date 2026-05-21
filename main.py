"""
AI NEWS AGGREGATOR - MULTI-SOURCE EDITION
Fetches from: YouTube, Hacker News, Florida Man, Google News, BBC, TechCrunch, Wired, The Verge
"""

from youtube_service import search_videos
from hacker_news_fetcher import HackerNewsFetcher
from florida_man_fetcher import FloridaManFetcher
from backup_news_fetcher import BackupNewsFetcher
from unified_saver import save_unified_article, clear_all_articles
import time

def main():
    print("="*70)
    print("🚀 AI NEWS AGGREGATOR - MULTI-SOURCE EDITION")
    print("="*70)
    
    # Ask if user wants to clear old data
    choice = input("\nClear old articles before fetching? (y/n): ").strip().lower()
    if choice == 'y':
        clear_all_articles()
    
    total_saved = 0
    
    # ========== SOURCE 1: YouTube ==========
    print("\n" + "="*70)
    print("📹 SOURCE 1: YOUTUBE (30 videos)")
    print("="*70)
    
    youtube_videos = search_videos("artificial intelligence news", 30)
    print(f"Found {len(youtube_videos)} videos")
    
    for video in youtube_videos:
        print(f"\n🎬 Processing: {video['title'][:60]}...")
        if save_unified_article(video, 'youtube'):
            total_saved += 1
        time.sleep(0.2)
    
    # ========== SOURCE 2: Hacker News ==========
    print("\n" + "="*70)
    print("💻 SOURCE 2: HACKER NEWS (15 articles)")
    print("="*70)
    
    hn_fetcher = HackerNewsFetcher()
    hn_articles = hn_fetcher.fetch_top_stories(limit=15)
    print(f"Found {len(hn_articles)} articles")
    
    for article in hn_articles:
        print(f"\n💻 Processing: {article['title'][:60]}...")
        if save_unified_article(article, 'hacker_news'):
            total_saved += 1
        time.sleep(0.2)
    
    # ========== SOURCE 3: Florida Man ==========
    print("\n" + "="*70)
    print("📰 SOURCE 3: FLORIDA MAN (10 headlines)")
    print("="*70)
    
    fm_fetcher = FloridaManFetcher()
    fm_articles = fm_fetcher.fetch_random_headlines(limit=10)
    print(f"Found {len(fm_articles)} headlines")
    
    for article in fm_articles:
        print(f"\n📰 Processing: {article['title'][:60]}...")
        if save_unified_article(article, 'florida_man'):
            total_saved += 1
        time.sleep(0.2)
    
    # ========== SOURCE 4: Backup News ==========
    print("\n" + "="*70)
    print("📡 SOURCE 4: NEWS SOURCES (Google, BBC, TechCrunch, Wired, The Verge)")
    print("="*70)
    
    backup_fetcher = BackupNewsFetcher()
    news_articles = backup_fetcher.fetch_all_sources(limit_per_source=6)
    print(f"Found {len(news_articles)} articles")
    
    for article in news_articles:
        print(f"\n📡 Processing: {article['title'][:60]}...")
        if save_unified_article(article, 'news'):
            total_saved += 1
        time.sleep(0.2)
    
    # ========== SUMMARY ==========
    print("\n" + "="*70)
    print("✅ PROCESSING COMPLETE!")
    print("="*70)
    print(f"📊 Total articles saved: {total_saved}")
    print("="*70)

if __name__ == "__main__":
    main()