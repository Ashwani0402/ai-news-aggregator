"""
Unified Article Saver - Saves all sources to saved_articles.json
"""

import json
import os
from datetime import datetime
from scraper import process_video

ARTICLES_FILE = "saved_articles.json"

def save_unified_article(article, source_type):
    """Save any article (YouTube or News) to the unified database"""
    
    # Generate a unique ID
    if source_type == 'youtube':
        article_id = article.get('video_id', '')
    else:
        article_id = article.get('url', article.get('title', str(hash(article.get('title', '')))))
    
    # Get content for summarization
    if source_type == 'youtube':
        content = article.get('description', article.get('title', ''))
    else:
        content = article.get('description', article.get('title', ''))
    
    # Process with AI summarizer
    print(f"   🤖 Summarizing: {article.get('title', 'Untitled')[:50]}...")
    try:
        result = process_video(article.get('title', 'Untitled'), content)
        summary = result.get('summary', 'No summary available')
    except Exception as e:
        summary = f"Summary temporarily unavailable. {article.get('title', '')[:100]}"
        print(f"   ⚠️ Summarizer error: {e}")
    
    # Load existing articles
    try:
        with open(ARTICLES_FILE, 'r') as f:
            articles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        articles = []
    
    # Check for duplicates
    existing_ids = [a.get('unique_id', '') for a in articles]
    if article_id in existing_ids:
        print(f"   ⏭️ Skipping duplicate: {article.get('title', '')[:40]}...")
        return False
    
    # Create unified article object
    new_article = {
        'unique_id': article_id,
        'title': article.get('title', 'Untitled'),
        'summary': summary[:500] if summary else "No summary available",
        'content': content[:500] if content else "",
        'source': source_type,
        'source_name': article.get('source', source_type.upper()),
        'url': article.get('url', f"https://youtube.com/watch?v={article.get('video_id', '')}") if source_type == 'youtube' else article.get('url', ''),
        'video_id': article.get('video_id', '') if source_type == 'youtube' else None,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    articles.append(new_article)
    
    # Save back
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)
    
    print(f"   ✅ Saved: {new_article['title'][:50]}...")
    return True

def get_all_articles():
    """Get all saved articles"""
    try:
        with open(ARTICLES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []
    
def clear_all_articles():
    """Clear all articles (for fresh start)"""
    with open(ARTICLES_FILE, 'w') as f:
        json.dump([], f)
    print("🗑️ All articles cleared")