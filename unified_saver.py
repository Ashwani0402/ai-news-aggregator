"""
Unified Article Saver - Saves all sources to saved_articles.json
Enhanced Version with Thumbnail Support + Better Metadata
"""

import json
import os
from datetime import datetime
from scraper import process_video

ARTICLES_FILE = "saved_articles.json"

# ============================================
# SOURCE PLACEHOLDER THEMES
# ============================================
SOURCE_PLACEHOLDERS = {
    "youtube": "https://placehold.co/90x70/1a1f2e/ff0033?text=YOUTUBE",
    "hacker_news": "https://placehold.co/90x70/1a1f2e/ff6600?text=HN",
    "florida_man": "https://placehold.co/90x70/1a1f2e/ffaa00?text=FL",
    "sports": "https://placehold.co/90x70/1a1f2e/00ccff?text=SPORTS",
    "entertainment": "https://placehold.co/90x70/1a1f2e/cc00ff?text=ENT",
    "news": "https://placehold.co/90x70/1a1f2e/00ffaa?text=NEWS"
}


def generate_thumbnail(article, source_type):
    """
    Generate thumbnail URL based on source type
    """

    # YouTube thumbnail
    if source_type == "youtube" and article.get("video_id"):
        return f"https://img.youtube.com/vi/{article['video_id']}/mqdefault.jpg"

    # Use article image if available
    if article.get("thumbnail_url"):
        return article["thumbnail_url"]

    if article.get("image"):
        return article["image"]

    # Source-specific placeholders
    return SOURCE_PLACEHOLDERS.get(
        source_type.lower(),
        f"https://placehold.co/90x70/1a1f2e/0ff?text={source_type.upper()}"
    )


def detect_category(article, source_type):
    """
    Auto-detect article category
    """

    text = (
        article.get("title", "") + " " +
        article.get("description", "") + " " +
        article.get("summary", "")
    ).lower()

    sports_keywords = [
        "football", "basketball", "cricket",
        "tennis", "fifa", "nba", "ipl",
        "soccer", "sports", "match"
    ]

    entertainment_keywords = [
        "movie", "film", "series",
        "netflix", "hollywood", "anime",
        "celebrity", "music", "entertainment"
    ]

    ai_keywords = [
        "ai", "artificial intelligence",
        "machine learning", "llm",
        "openai", "gpt", "neural",
        "deep learning"
    ]

    if any(k in text for k in sports_keywords):
        return "sports"

    if any(k in text for k in entertainment_keywords):
        return "entertainment"

    if any(k in text for k in ai_keywords):
        return "ai"

    return source_type


def save_unified_article(article, source_type):
    """
    Save any article (YouTube or News) to the unified database
    """

    # ============================================
    # UNIQUE ARTICLE ID
    # ============================================

    if source_type == "youtube":
        article_id = article.get("video_id", "")
    else:
        article_id = article.get(
            "url",
            article.get("title", str(hash(article.get("title", ""))))
        )

    # ============================================
    # CONTENT EXTRACTION
    # ============================================

    content = article.get(
        "description",
        article.get("content", article.get("title", ""))
    )

    # ============================================
    # AI SUMMARIZATION
    # ============================================

    print(f"   🤖 Summarizing: {article.get('title', 'Untitled')[:60]}...")

    try:
        result = process_video(
            article.get("title", "Untitled"),
            content
        )

        summary = result.get(
            "summary",
            "No summary available"
        )

    except Exception as e:
        summary = f"Summary temporarily unavailable. {article.get('title', '')[:100]}"
        print(f"   ⚠️ Summarizer error: {e}")

    # ============================================
    # LOAD EXISTING ARTICLES
    # ============================================

    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        articles = []

    # ============================================
    # DUPLICATE CHECK
    # ============================================

    existing_ids = [a.get("unique_id", "") for a in articles]

    if article_id in existing_ids:
        print(f"   ⏭️ Skipping duplicate: {article.get('title', '')[:50]}...")
        return False

    # ============================================
    # CATEGORY DETECTION
    # ============================================

    category = detect_category(article, source_type)

    # ============================================
    # THUMBNAIL GENERATION
    # ============================================

    thumbnail_url = generate_thumbnail(article, source_type)

    # ============================================
    # ARTICLE OBJECT
    # ============================================

    new_article = {
        "unique_id": article_id,

        "title": article.get("title", "Untitled"),

        "summary": (
            summary[:500]
            if summary else
            "No summary available"
        ),

        "content": (
            content[:1000]
            if content else
            ""
        ),

        "source": source_type,

        "category": category,

        "source_name": article.get(
            "source",
            source_type.upper()
        ),

        "url": (
            article.get(
                "url",
                f"https://youtube.com/watch?v={article.get('video_id', '')}"
            )
            if source_type == "youtube"
            else article.get("url", "")
        ),

        "video_id": (
            article.get("video_id", "")
            if source_type == "youtube"
            else None
        ),

        # ============================================
        # NEW ENHANCED FIELDS
        # ============================================

        "thumbnail_url": thumbnail_url,

        "author": article.get("author", "Unknown"),

        "published_at": article.get(
            "published_at",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ),

        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "reading_time": max(
            1,
            len(content.split()) // 200
        ),

        "engagement_score": 0,

        "language": "en",

        "ai_processed": True
    }

    # ============================================
    # APPEND + SORT
    # ============================================

    articles.append(new_article)

    # Latest first
    articles = sorted(
        articles,
        key=lambda x: x.get("created_at", ""),
        reverse=True
    )

    # ============================================
    # SAVE DATABASE
    # ============================================

    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump(
            articles,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"   ✅ Saved: {new_article['title'][:60]}...")
    return True


def get_all_articles():
    """
    Get all saved articles
    """

    try:
        with open(ARTICLES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []


def clear_all_articles():
    """
    Clear all articles (for fresh start)
    """

    with open(ARTICLES_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

    print("🗑️ All articles cleared")


def get_articles_by_category(category):
    """
    Filter articles by category
    """

    articles = get_all_articles()

    return [
        a for a in articles
        if a.get("category", "").lower() == category.lower()
    ]


def get_articles_by_source(source):
    """
    Filter articles by source
    """

    articles = get_all_articles()

    return [
        a for a in articles
        if a.get("source", "").lower() == source.lower()
    ]


# ============================================
# TESTING
# ============================================

if __name__ == "__main__":

    print("📡 Unified Article System")
    print("=" * 40)

    articles = get_all_articles()

    print(f"📚 Total Articles: {len(articles)}")

    if articles:
        print("\n📰 Latest Article:")
        print(f"Title: {articles[0].get('title')}")
        print(f"Source: {articles[0].get('source')}")
        print(f"Category: {articles[0].get('category')}")
        print(f"Thumbnail: {articles[0].get('thumbnail_url')}")