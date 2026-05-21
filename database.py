import json
import os
from datetime import datetime

ARTICLES_FILE = "saved_articles.json"

def create_database():
    """Create the articles file if it doesn't exist"""
    if not os.path.exists(ARTICLES_FILE):
        with open(ARTICLES_FILE, 'w') as f:
            json.dump([], f)
    print("✅ Storage file ready")

def save_article(article_id, title, summary, content):
    """Save any article (YouTube or News) to JSON file"""
    # Load existing articles
    with open(ARTICLES_FILE, 'r') as f:
        articles = json.load(f)
    
    # Check if article already exists
    for existing in articles:
        if existing.get('video_id') == article_id or existing.get('url') == article_id:
            print(f"   ⏭️ Skipping duplicate: {title[:40]}...")
            return False
    
    # Add new article
    new_article = {
        'video_id': article_id if 'youtube' in str(article_id) else None,
        'url': article_id if 'youtube' not in str(article_id) else None,
        'title': title,
        'summary': summary[:500] if summary else "No summary available",
        'content': content[:500] if content else "",
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    articles.append(new_article)
    
    # Save back to file
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)
    
    return True

def get_all_articles():
    """Get all saved articles"""
    if not os.path.exists(ARTICLES_FILE):
        return []
    with open(ARTICLES_FILE, 'r') as f:
        return json.load(f)