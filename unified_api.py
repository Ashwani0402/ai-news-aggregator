#!/usr/bin/env python3
"""
Unified API for AI News Aggregator – with sci‑fi email built-in
"""

import json
import os
import subprocess
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ==================== CONFIGURATION ====================
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== CONFIGURATION ====================
SUBSCRIBERS_FILE = "subscribers.json"
USER_PROFILES_FILE = "user_profiles.json"
FEEDBACK_FILE = "feedback.json"
ARTICLES_FILE = "saved_articles.json"
PORT = 8081

# Email credentials – now read from .env
FROM_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")
# ==================== FILE HELPERS ====================
def load_json(file, default=None):
    if not os.path.exists(file):
        return default if default is not None else []
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==================== SUBSCRIBERS ====================
def load_subscribers():
    return load_json(SUBSCRIBERS_FILE, [])

def save_subscribers(subs):
    save_json(SUBSCRIBERS_FILE, subs)

def add_subscriber(email):
    email = email.strip().lower()
    subs = load_subscribers()
    if email in subs:
        return False, "Already subscribed"
    subs.append(email)
    save_subscribers(subs)
    return True, "Subscribed"

def list_subscribers():
    return load_subscribers()

# ==================== USER INTERESTS ====================
def load_user_profiles():
    return load_json(USER_PROFILES_FILE, {})

def save_user_profiles(profiles):
    save_json(USER_PROFILES_FILE, profiles)

def set_user_interests(email, interests):
    profiles = load_user_profiles()
    if email not in profiles:
        profiles[email] = {}
    profiles[email]['interests'] = interests[:3]
    save_user_profiles(profiles)
    return True

def get_user_interests(email):
    profiles = load_user_profiles()
    return profiles.get(email, {}).get('interests', [])

# ==================== FEEDBACK ====================
def add_feedback(email, article_id, rating):
    fb = load_json(FEEDBACK_FILE, [])
    fb.append({
        'email': email,
        'article_id': article_id,
        'rating': rating,
        'timestamp': datetime.now().isoformat()
    })
    save_json(FEEDBACK_FILE, fb)
    return True

# ==================== ARTICLE STATS ====================
def get_article_stats():
    articles = load_json(ARTICLES_FILE, [])
    if not articles:
        return {"total": 0, "avg_length": 0, "unique_keywords": 0, "top_keywords": [], "source_distribution": {}}
    
    total = len(articles)
    sum_len = sum(len(a.get('summary', '')) for a in articles)
    avg_len = sum_len // total if total else 0
    
    stop_words = {'this','that','these','those','from','with','they','will','have','was','were','about','into','through','what','which','their','there','would','could','should'}
    word_count = {}
    for a in articles:
        text = (a.get('summary', '') + ' ' + a.get('title', '')).lower()
        words = [w for w in text.split() if len(w) > 3 and w.isalpha() and w not in stop_words]
        for w in words:
            word_count[w] = word_count.get(w, 0) + 1
    
    top_keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
    src_dist = {}
    for a in articles:
        src = a.get('source', a.get('source_name', 'youtube')).lower()
        src_dist[src] = src_dist.get(src, 0) + 1
    
    return {
        "total": total,
        "avg_length": avg_len,
        "unique_keywords": len(word_count),
        "top_keywords": top_keywords,
        "source_distribution": src_dist
    }

def get_previous_stats():
    prev = load_json("previous_stats.json", None)
    return prev if prev else {"total": 0, "unique_keywords": 0}

def update_previous_stats():
    save_json("previous_stats.json", get_article_stats())

def get_last_run_time():
    data = load_json("last_run.json", None)
    return data.get('timestamp', 'Never') if data else 'Never'

def set_last_run_time():
    save_json("last_run.json", {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

# ==================== PERSONALIZED RANKING ====================
def rank_articles_by_interests(articles, email):
    interests = get_user_interests(email)
    if not interests:
        return articles
    scored = []
    for art in articles:
        text = (art.get('title', '') + ' ' + art.get('summary', '')).lower()
        score = 0
        for i, interest in enumerate(interests):
            if interest.lower() in text:
                score += (3 - i)
        scored.append((score, art))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [art for _, art in scored]

# ==================== SCI-FI EMAIL GENERATOR ====================
def generate_scifi_email_html(articles, subscriber_email=""):
    """Generate the beautiful sci‑fi email template"""
    subscriber_name = subscriber_email.split('@')[0] if subscriber_email else "Agent"
    
    # Group articles by source
    groups = {'youtube': [], 'hacker_news': [], 'florida_man': [], 'news': []}
    for art in articles[:60]:
        src = (art.get('source') or art.get('source_name') or 'youtube').lower()
        if src in groups:
            groups[src].append(art)
        else:
            groups['news'].append(art)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ NEURAL OBSERVATORY – INTELLIGENCE DIGEST</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Orbitron:wght@400;600;800&display=swap');
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
            background: radial-gradient(ellipse at 20% 30%, #0a0f1e 0%, #03050b 100%);
            margin: 0;
            padding: 20px;
        }}
        .email-container {{
            max-width: 700px;
            margin: 0 auto;
            background: rgba(10, 20, 35, 0.85);
            backdrop-filter: blur(8px);
            border-radius: 48px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.8), 0 0 30px rgba(0,255,255,0.2);
        }}
        .header {{
            background: linear-gradient(135deg, rgba(0,255,255,0.1), rgba(255,0,255,0.05));
            padding: 35px 30px;
            text-align: center;
            border-bottom: 1px solid rgba(0,255,255,0.3);
        }}
        .glitch {{
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(45deg, #fff, #0ff, #f0f);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 5px rgba(0,255,255,0.5);
            letter-spacing: 3px;
        }}
        .subhead {{
            font-size: 0.75rem;
            letter-spacing: 2px;
            color: #88aaff;
            border-top: 1px solid rgba(0,255,255,0.4);
            border-bottom: 1px solid rgba(0,255,255,0.4);
            display: inline-block;
            padding: 6px 16px;
            margin-top: 12px;
        }}
        .greeting {{
            margin-top: 15px;
            font-size: 0.9rem;
            color: #ccf;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            background: rgba(0,0,0,0.4);
            padding: 15px 20px;
            flex-wrap: wrap;
            gap: 10px;
            border-bottom: 1px solid rgba(0,255,255,0.2);
        }}
        .stat-item {{ text-align: center; }}
        .stat-number {{
            font-size: 1.6rem;
            font-weight: 700;
            color: #0ff;
            font-family: monospace;
        }}
        .stat-label {{
            font-size: 0.65rem;
            text-transform: uppercase;
            color: #aaf;
        }}
        .section {{
            padding: 20px 25px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid;
        }}
        .section-icon {{ font-size: 1.8rem; }}
        .section-title {{ font-size: 1.3rem; font-weight: 700; letter-spacing: 1px; }}
        .youtube .section-header {{ border-bottom-color: #ff0040; }}
        .youtube .section-title {{ color: #ff0040; }}
        .hacker .section-header {{ border-bottom-color: #ff6600; }}
        .hacker .section-title {{ color: #ff6600; }}
        .florida .section-header {{ border-bottom-color: #ffaa00; }}
        .florida .section-title {{ color: #ffaa00; }}
        .news .section-header {{ border-bottom-color: #2e7d32; }}
        .news .section-title {{ color: #2e7d32; }}
        .article {{
            background: rgba(20, 30, 55, 0.6);
            backdrop-filter: blur(4px);
            border-radius: 24px;
            margin-bottom: 18px;
            padding: 16px;
            display: flex;
            gap: 15px;
            transition: 0.2s;
            border-left: 4px solid;
        }}
        .article:hover {{
            background: rgba(40, 55, 85, 0.8);
            transform: translateX(6px);
        }}
        .youtube .article {{ border-left-color: #ff0040; }}
        .hacker .article {{ border-left-color: #ff6600; }}
        .florida .article {{ border-left-color: #ffaa00; }}
        .news .article {{ border-left-color: #2e7d32; }}
        .thumb {{
            width: 100px;
            height: 70px;
            border-radius: 16px;
            object-fit: cover;
            background: #112;
        }}
        .content {{ flex: 1; }}
        .source-badge {{
            display: inline-block;
            font-size: 0.65rem;
            padding: 3px 10px;
            border-radius: 20px;
            margin-bottom: 8px;
            background: rgba(0,0,0,0.5);
        }}
        .badge-yt {{ color: #ff0040; border: 1px solid #ff0040; }}
        .badge-hn {{ color: #ff6600; border: 1px solid #ff6600; }}
        .badge-fm {{ color: #ffaa00; border: 1px solid #ffaa00; }}
        .badge-news {{ color: #2e7d32; border: 1px solid #2e7d32; }}
        .article-title {{
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .article-title a {{ color: #ffffff; text-decoration: none; }}
        .article-title a:hover {{ color: #0ff; text-decoration: underline; }}
        .article-summary {{
            font-size: 0.75rem;
            color: #bbddff;
            line-height: 1.4;
            margin-bottom: 8px;
        }}
        .meta-link {{
            font-size: 0.7rem;
            color: #0ff;
            text-decoration: none;
        }}
        .cta {{
            text-align: center;
            padding: 25px;
            background: linear-gradient(90deg, #0ff22, #f0f22);
            margin: 20px 25px;
            border-radius: 40px;
        }}
        .cta p {{ color: #000; font-weight: 600; }}
        .footer {{
            background: #01010c;
            padding: 20px;
            text-align: center;
            font-size: 0.65rem;
            color: #668;
        }}
        .footer a {{ color: #0ff; text-decoration: none; }}
        .disclaimer {{
            font-size: 0.6rem;
            color: #557;
            margin-top: 8px;
            border-top: 1px solid rgba(0,255,255,0.2);
            padding-top: 10px;
        }}
        @media (max-width: 550px) {{
            .article {{ flex-direction: column; }}
            .thumb {{ width: 100%; height: 120px; }}
            .stats {{ flex-direction: column; align-items: center; }}
        }}
    </style>
</head>
<body>
<div class="email-container">
    <div class="header">
        <div class="glitch">⚡ NEURAL OBSERVATORY</div>
        <div class="subhead">QUANTUM INTELLIGENCE FEED • ENCRYPTED</div>
        <div class="greeting">🧠 Agent {subscriber_name}, your daily briefing is ready.</div>
    </div>
    <div class="stats">
        <div class="stat-item"><div class="stat-number">{len(articles)}</div><div class="stat-label">INTEL ASSETS</div></div>
        <div class="stat-item"><div class="stat-number">{len(groups['youtube'])}</div><div class="stat-label">VIDEO STREAMS</div></div>
        <div class="stat-item"><div class="stat-number">{len(groups['hacker_news']) + len(groups['news'])}</div><div class="stat-label">TEXT SIGNALS</div></div>
        <div class="stat-item"><div class="stat-number">{datetime.now().strftime('%d %b')}</div><div class="stat-label">CYCLE</div></div>
    </div>
"""
    
    # YouTube section
    if groups['youtube']:
        html += '<div class="section youtube"><div class="section-header"><span class="section-icon">📹</span><span class="section-title">VIDEO INTELLIGENCE</span></div>'
        for art in groups['youtube'][:12]:
            title = art.get('title', 'Untitled')
            summary = (art.get('summary', '') or '')[:130]
            vid = art.get('video_id', '')
            url = f"https://www.youtube.com/watch?v={vid}" if vid else '#'
            thumb = f"https://img.youtube.com/vi/{vid}/mqdefault.jpg" if vid else 'https://placehold.co/100x70/1a1f2e/0ff?text=YT'
            html += f"""
        <div class="article">
            <img class="thumb" src="{thumb}" onerror="this.src='https://placehold.co/100x70/1a1f2e/0ff?text=YT'">
            <div class="content">
                <div class="source-badge badge-yt">🎥 YOUTUBE</div>
                <div class="article-title"><a href="{url}" target="_blank">{title}</a></div>
                <div class="article-summary">{summary}...</div>
                <a class="meta-link" href="{url}" target="_blank">▶ WATCH FULL STREAM</a>
            </div>
        </div>"""
        html += '</div>'
    
    # Hacker News
    if groups['hacker_news']:
        html += '<div class="section hacker"><div class="section-header"><span class="section-icon">💻</span><span class="section-title">CYBER FORUM // HACKER NEWS</span></div>'
        for art in groups['hacker_news'][:10]:
            title = art.get('title', 'Untitled')
            summary = (art.get('summary', '') or '')[:130]
            url = art.get('url', '#')
            if not url.startswith('http'):
                url = '#'
            html += f"""
        <div class="article">
            <img class="thumb" src="https://placehold.co/100x70/1a1f2e/ff6600?text=HN" alt="hn">
            <div class="content">
                <div class="source-badge badge-hn">💬 HACKER NEWS</div>
                <div class="article-title"><a href="{url}" target="_blank">{title}</a></div>
                <div class="article-summary">{summary}...</div>
                <a class="meta-link" href="{url}" target="_blank">🔗 READ DISCUSSION</a>
            </div>
        </div>"""
        html += '</div>'
    
    # Florida Man
    if groups['florida_man']:
        html += '<div class="section florida"><div class="section-header"><span class="section-icon">🌴</span><span class="section-title">FLORIDA MAN • SIGNAL</span></div>'
        for art in groups['florida_man'][:8]:
            title = art.get('title', 'Untitled')
            summary = (art.get('description') or art.get('summary') or '')[:130]
            url = art.get('url', '#')
            html += f"""
        <div class="article">
            <img class="thumb" src="https://placehold.co/100x70/1a1f2e/ffaa00?text=FL" alt="fl">
            <div class="content">
                <div class="source-badge badge-fm">🌴 FLORIDA MAN</div>
                <div class="article-title"><a href="{url}" target="_blank">{title}</a></div>
                <div class="article-summary">{summary}...</div>
                <a class="meta-link" href="{url}" target="_blank">📖 READ STORY</a>
            </div>
        </div>"""
        html += '</div>'
    
    # News
    if groups['news']:
        html += '<div class="section news"><div class="section-header"><span class="section-icon">📰</span><span class="section-title">GLOBAL NEWS FEED</span></div>'
        for art in groups['news'][:15]:
            title = art.get('title', 'Untitled')
            summary = (art.get('summary', '') or '')[:130]
            url = art.get('url', '#')
            src_name = (art.get('source') or art.get('source_name') or 'News').title()
            html += f"""
        <div class="article">
            <img class="thumb" src="https://placehold.co/100x70/1a1f2e/0ff?text=NEWS" alt="news">
            <div class="content">
                <div class="source-badge badge-news">📌 {src_name}</div>
                <div class="article-title"><a href="{url}" target="_blank">{title}</a></div>
                <div class="article-summary">{summary}...</div>
                <a class="meta-link" href="{url}" target="_blank">🔗 FULL ARTICLE</a>
            </div>
        </div>"""
        html += '</div>'
    
    html += f"""
    <div class="cta">
        <p>🔒 THIS INTELLIGENCE WAS CURATED BY AI • FEEDBACK DRIVES THE NETWORK</p>
        <p style="font-size:0.7rem; margin-top:8px;">Reply with 👍😐👎 to tune your profile</p>
    </div>
    <div class="footer">
        <p>⚡ NEURAL OBSERVATORY – AI‑generated digest for personal/educational use.</p>
        <p>All original content belongs to their respective owners. Summaries produced by Groq/Gemini LLM.</p>
        <hr>
        <p>© 2025 Neural Observatory | Big Data Pipeline | Non‑commercial</p>
        <p><a href="#">Privacy Protocol</a> • <a href="#">Report Issue</a></p>
        <div class="disclaimer">
            <p>To unsubscribe, reply with "UNSUBSCRIBE"</p>
        </div>
    </div>
</div>
</body>
</html>"""
    return html

# ==================== EMAIL SENDING ====================
def send_single_email(to_email, subject, html_content):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg.attach(MIMEText(html_content, 'html'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_test_email(to_email):
    articles = load_json(ARTICLES_FILE, [])
    if not articles:
        return False, "No articles. Run main.py first."
    html = generate_scifi_email_html(articles, to_email)
    subject = f"⚡ NEURAL DIGEST – {datetime.now().strftime('%b %d, %Y')}"
    success = send_single_email(to_email, subject, html)
    return success, "Sent" if success else "Failed"

def send_bulk_email():
    subscribers = load_subscribers()
    if not subscribers:
        return False, "No subscribers"
    articles = load_json(ARTICLES_FILE, [])
    if not articles:
        return False, "No articles"
    
    success_count = 0
    for email in subscribers:
        html = generate_scifi_email_html(articles, email)
        subject = f"⚡ NEURAL DIGEST – {datetime.now().strftime('%b %d, %Y')}"
        if send_single_email(email, subject, html):
            success_count += 1
        # Small delay to avoid rate limiting
        import time
        time.sleep(1)
    return True, f"Sent to {success_count}/{len(subscribers)}"

# ==================== RUN PIPELINE ====================
def run_pipeline_async():
    def target():
        try:
            update_previous_stats()
            subprocess.run(["python", "main.py"], cwd=os.path.dirname(__file__), capture_output=True)
            set_last_run_time()
        except Exception as e:
            print(f"Pipeline error: {e}")
    t = threading.Thread(target=target)
    t.daemon = True
    t.start()

# ==================== HTTP HANDLER ====================
class APIHandler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()
    
    def _json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._send_cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        if path == '/list_subscribers':
            self._json({'subscribers': list_subscribers()})
        elif path == '/stats':
            self._json(get_article_stats())
        elif path == '/stats_compare':
            current = get_article_stats()
            previous = get_previous_stats()
            self._json({'current': current, 'previous': previous})
        elif path == '/last_run':
            self._json({'last_run': get_last_run_time()})
        elif path == '/get_preferences':
            qs = parse_qs(parsed.query)
            email = qs.get('email', [''])[0]
            if not email:
                self._json({'error': 'Missing email'}, 400)
                return
            self._json({'interests': get_user_interests(email)})
        else:
            self._json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8')
        try:
            data = json.loads(body) if body else {}
        except:
            self._json({'error': 'Invalid JSON'}, 400)
            return
        
        path = urlparse(self.path).path
        if path == '/subscribe':
            email = data.get('email')
            if not email:
                self._json({'error': 'Missing email'}, 400)
                return
            success, msg = add_subscriber(email)
            self._json({'success': success, 'message': msg})
        elif path == '/set_preferences':
            email = data.get('email')
            interests = data.get('interests', [])
            if not email:
                self._json({'error': 'Missing email'}, 400)
                return
            set_user_interests(email, interests)
            self._json({'success': True})
        elif path == '/feedback':
            email = data.get('email')
            article_id = data.get('article_id')
            rating = data.get('rating')
            if not all([email, article_id, rating]):
                self._json({'error': 'Missing fields'}, 400)
                return
            add_feedback(email, article_id, rating)
            self._json({'success': True})
        elif path == '/personalized_feed':
            email = data.get('email')
            if not email:
                self._json({'error': 'Missing email'}, 400)
                return
            articles = load_json(ARTICLES_FILE, [])
            ranked = rank_articles_by_interests(articles, email)
            self._json({'articles': ranked[:50]})
        elif path == '/run_pipeline':
            run_pipeline_async()
            self._json({'success': True, 'message': 'Pipeline started'})
        elif path == '/send_test_email':
            email = data.get('email')
            if not email:
                self._json({'error': 'Missing email'}, 400)
                return
            success, msg = send_test_email(email)
            self._json({'success': success, 'message': msg})
        elif path == '/send_bulk_email':
            success, msg = send_bulk_email()
            self._json({'success': success, 'message': msg})
        else:
            self._json({'error': 'Not found'}, 404)

def run():
    print(f"🚀 Unified API on port {PORT}")
    print("   Endpoints: /subscribe, /send_test_email, /send_bulk_email, /stats, /personalized_feed, /run_pipeline")
    server = HTTPServer(('localhost', PORT), APIHandler)
    server.serve_forever()

if __name__ == '__main__':
    run()