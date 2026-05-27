#!/usr/bin/env python3
"""
Enhanced Main Pipeline for AI News Aggregator
Fetches from: YouTube, Hacker News, Florida Man, Google News, BBC, TechCrunch, Wired, The Verge
PLUS: Sports News (ESPN, BBC Sport, Sky Sports) and Entertainment News (Variety, Hollywood Reporter, IGN)
Tracks performance metrics for dashboard
"""

import time
import json
import os
from datetime import datetime
from youtube_service import search_videos
from hacker_news_fetcher import HackerNewsFetcher
from florida_man_fetcher import FloridaManFetcher
from backup_news_fetcher import BackupNewsFetcher
from sports_fetcher import SportsFetcher
from entertainment_fetcher import EntertainmentFetcher
from unified_saver import save_unified_article
from database import create_database

# ==================== CONFIGURATION ====================
PIPELINE_STATS_FILE = "pipeline_stats.json"
LAST_RUN_FILE = "last_run.json"

def update_pipeline_stats(duration_seconds, success=True, articles_count=0):
    """Update pipeline statistics for dashboard health"""
    stats = {}
    if os.path.exists(PIPELINE_STATS_FILE):
        with open(PIPELINE_STATS_FILE, 'r') as f:
            stats = json.load(f)
    
    runs = stats.get("runs", [])
    runs.append({
        "duration": round(duration_seconds, 2),
        "success": success,
        "articles": articles_count,
        "timestamp": datetime.now().isoformat()
    })
    if len(runs) > 10:
        runs = runs[-10:]
    
    success_count = sum(1 for r in runs if r["success"])
    success_rate = (success_count / len(runs)) * 100 if runs else 100
    
    stats["last_duration"] = round(duration_seconds, 2)
    stats["success_rate"] = round(success_rate, 1)
    stats["last_articles"] = articles_count
    stats["runs"] = runs
    stats["last_updated"] = datetime.now().isoformat()
    
    with open(PIPELINE_STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

def update_last_run_time():
    """Store last run timestamp for dashboard"""
    with open(LAST_RUN_FILE, 'w') as f:
        json.dump({"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, f, indent=2)

def save_article_with_source(article, source_type):
    """Save article from any source using unified saver"""
    return save_unified_article(article, source_type)

def main():
    start_time = time.time()
    total_saved = 0
    
    print("="*70)
    print("🚀 AI NEWS AGGREGATOR - ENHANCED PIPELINE")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Sources: YouTube, Hacker News, Florida Man, News, SPORTS, ENTERTAINMENT")
    print("="*70)
    
    # Ask if user wants to clear old articles
    choice = input("\nClear old articles before fetching? (y/n): ").strip().lower()
    if choice == 'y':
        # Backup old data before clearing
        if os.path.exists("saved_articles.json"):
            backup_name = f"saved_articles_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.rename("saved_articles.json", backup_name)
            print(f"📦 Old data backed up to: {backup_name}")
        create_database()
        print("🗑️ Database cleared for fresh fetch")
    
    # ========== SOURCE 1: YouTube ==========
    print("\n" + "="*70)
    print("📹 SOURCE 1: YOUTUBE (30 videos)")
    print("="*70)
    
    try:
        youtube_videos = search_videos("artificial intelligence news", 30)
        print(f"Found {len(youtube_videos)} videos")
        
        for video in youtube_videos:
            print(f"\n🎬 Processing: {video['title'][:60]}...")
            if save_article_with_source(video, 'youtube'):
                total_saved += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ YouTube error: {e}")
    
    # ========== SOURCE 2: Hacker News ==========
    print("\n" + "="*70)
    print("💻 SOURCE 2: HACKER NEWS (15 articles)")
    print("="*70)
    
    try:
        hn_fetcher = HackerNewsFetcher()
        hn_articles = hn_fetcher.fetch_top_stories(limit=15)
        print(f"Found {len(hn_articles)} articles")
        
        for article in hn_articles:
            print(f"\n💻 Processing: {article['title'][:60]}...")
            if save_article_with_source(article, 'hacker_news'):
                total_saved += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ Hacker News error: {e}")
    
    # ========== SOURCE 3: Florida Man ==========
    print("\n" + "="*70)
    print("📰 SOURCE 3: FLORIDA MAN (10 headlines)")
    print("="*70)
    
    try:
        fm_fetcher = FloridaManFetcher()
        fm_articles = fm_fetcher.fetch_random_headlines(limit=10)
        print(f"Found {len(fm_articles)} headlines")
        
        for article in fm_articles:
            print(f"\n📰 Processing: {article['title'][:60]}...")
            if save_article_with_source(article, 'florida_man'):
                total_saved += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ Florida Man error: {e}")
    
    # ========== SOURCE 4: Backup News (AI/Tech) ==========
    print("\n" + "="*70)
    print("📡 SOURCE 4: NEWS SOURCES (Google, BBC, TechCrunch, Wired, The Verge)")
    print("="*70)
    
    try:
        backup_fetcher = BackupNewsFetcher()
        news_articles = backup_fetcher.fetch_all_sources(limit_per_source=6)
        print(f"Found {len(news_articles)} articles")
        
        for article in news_articles:
            print(f"\n📡 Processing: {article['title'][:60]}...")
            if save_article_with_source(article, 'news'):
                total_saved += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ News sources error: {e}")
    
    # ========== SOURCE 5: SPORTS NEWS ==========
    print("\n" + "="*70)
    print("🏆 SOURCE 5: SPORTS NEWS")
    print("="*70)
    
    try:
        sports_fetcher = SportsFetcher()
        sports_articles = sports_fetcher.fetch_all_sports(limit_per_source=6)
        print(f"Found {len(sports_articles)} sports articles")
        
        for article in sports_articles:
            print(f"\n🏆 Processing: {article['title'][:60]}...")
            if save_article_with_source(article, 'sports'):
                total_saved += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ Sports error: {e}")
    
    # ========== SOURCE 6: ENTERTAINMENT NEWS ==========
    print("\n" + "="*70)
    print("🎬 SOURCE 6: ENTERTAINMENT NEWS")
    print("="*70)
    
    try:
        ent_fetcher = EntertainmentFetcher()
        ent_articles = ent_fetcher.fetch_all_entertainment(limit_per_source=6)
        print(f"Found {len(ent_articles)} entertainment articles")
        
        for article in ent_articles:
            print(f"\n🎬 Processing: {article['title'][:60]}...")
            if save_article_with_source(article, 'entertainment'):
                total_saved += 1
            time.sleep(0.2)
    except Exception as e:
        print(f"❌ Entertainment error: {e}")
    
    # ========== SUMMARY ==========
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*70)
    print("✅ PIPELINE EXECUTION COMPLETE!")
    print("="*70)
    print(f"📊 Total articles saved: {total_saved}")
    print(f"⏱️ Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    print(f"📁 Data stored in: saved_articles.json")
    print("="*70)
    print("\n📋 Articles by category:")
    print("  - AI/Tech: YouTube + Hacker News + News sources")
    print("  - Sports: ESPN, BBC Sport, Sky Sports")
    print("  - Entertainment: Variety, Hollywood Reporter, IGN")
    print("="*70)
    
    # Update tracking files for dashboard
    update_pipeline_stats(duration, success=True, articles_count=total_saved)
    update_last_run_time()
    
    return total_saved

if __name__ == "__main__":
    main()