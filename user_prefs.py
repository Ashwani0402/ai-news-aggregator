import json
import os
from datetime import datetime

USER_FILE = "user_profiles.json"
FEEDBACK_FILE = "feedback.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, 'r') as f:
        return json.load(f)

def save_feedback(feedback):
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback, f, indent=2)

def set_user_interests(email, interests):
    """interests = list of 3 categories e.g. ['AIML', 'Sports', 'Entertainment']"""
    users = load_users()
    if email not in users:
        users[email] = {}
    users[email]['interests'] = interests[:3]
    save_users(users)
    return True

def add_feedback(email, article_id, rating):
    """rating: 'satisfied', 'neutral', 'dissatisfied'"""
    fb = load_feedback()
    fb.append({
        'email': email,
        'article_id': article_id,
        'rating': rating,
        'timestamp': str(datetime.now())
    })
    save_feedback(fb)
    return True

def rank_articles_by_interests(articles, email):
    """Return articles sorted by relevance to user's interests"""
    users = load_users()
    interests = users.get(email, {}).get('interests', [])
    if not interests:
        return articles

    scored = []
    for art in articles:
        text = (art.get('title','') + ' ' + art.get('summary','')).lower()
        score = 0
        for i, interest in enumerate(interests):
            if interest.lower() in text:
                score += (3 - i)   # higher weight for first interest
        scored.append((score, art))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [art for score, art in scored]