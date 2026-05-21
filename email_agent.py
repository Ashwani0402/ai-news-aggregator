import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

# ============================================
# CONFIGURATION – UPDATE THESE!
# ============================================
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# CONFIGURATION - Now read from .env
# ============================================
FROM_EMAIL = os.getenv("EMAIL_USER")
APP_PASSWORD = os.getenv("EMAIL_PASS")
SUBSCRIBERS_FILE = "subscribers.json"
API_URL = "http://localhost:8081"
# ============================================
# ============================================

def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(subscribers, f, indent=2)

def send_single_email(to_email, subject, html_content):
    try:
        print(f"📧 Sending to {to_email}...")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg.attach(MIMEText(html_content, 'html'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent to {to_email}")
        return True
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

def get_articles():
    """Get articles from API or local JSON"""
    try:
        resp = requests.get(f"{API_URL}/stats", timeout=5)
        if resp.status_code == 200:
            resp2 = requests.post(f"{API_URL}/personalized_feed", json={'email': 'test@example.com'}, timeout=10)
            if resp2.status_code == 200:
                return resp2.json().get('articles', [])
    except:
        pass
    try:
        with open('saved_articles.json', 'r') as f:
            return json.load(f)
    except:
        return []

def generate_scifi_html(articles, subscriber_email=""):
    """Sci‑fi email with ethical disclaimer footer"""
    from datetime import datetime
    subscriber_name = subscriber_email.split('@')[0] if subscriber_email else "Agent"
    
    # Group articles
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
        .footer a:hover {{ text-decoration: underline; }}
        .disclaimer {{
            font-size: 0.6rem;
            color: #557;
            margin-top: 8px;
            border-top: 1px solid rgba(0,255,255,0.2);
            padding-top: 10px;
        }}
        hr {{ border: none; border-top: 1px solid rgba(0,255,255,0.2); margin: 10px 0; }}
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
            if not url.startswith('http'): url = '#'
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

    # Footer with ethical disclaimer
    html += f"""
    <div class="cta">
        <p>🔒 THIS INTELLIGENCE WAS CURATED BY AI • FEEDBACK DRIVES THE NETWORK</p>
        <p style="font-size:0.7rem; margin-top:8px;">Reply with 👍😐👎 to tune your profile</p>
    </div>
    <div class="footer">
        <p>⚡ NEURAL OBSERVATORY – AI‑generated digest for personal/educational use.</p>
        <p>All original content (video titles, descriptions, news articles) belongs to their respective owners.</p>
        <p>Summaries produced by Groq/Gemini LLM. If you are a copyright holder and wish to remove your content, please contact us.</p>
        <hr>
        <p>© 2025 Neural Observatory | Big Data Pipeline | Non‑commercial</p>
        <p><a href="#">Privacy Protocol</a> • <a href="#">Decryption Key</a> • <a href="#">Report Issue</a></p>
        <div class="disclaimer">
            <p>To unsubscribe from this digest, reply with "UNSUBSCRIBE".</p>
        </div>
    </div>
</div>
</body>
</html>"""
    return html

def send_test_email(to_email):
    print(f"\n📧 Preparing sci‑fi email for {to_email}...")
    articles = get_articles()
    if not articles:
        return False, "No articles. Run main.py first."
    html = generate_scifi_html(articles, to_email)
    subject = f"⚡ NEURAL DIGEST – {datetime.now().strftime('%b %d, %Y')}"
    success = send_single_email(to_email, subject, html)
    return success, "Sent" if success else "Failed"

def send_bulk_email():
    subs = load_subscribers()
    if not subs:
        return False, "No subscribers"
    ok = 0
    for email in subs:
        success, _ = send_test_email(email)
        if success:
            ok += 1
    return True, f"Sent to {ok}/{len(subs)}"

def add_subscriber(email):
    email = email.strip().lower()
    subs = load_subscribers()
    if email in subs:
        return False, "Already subscribed"
    subs.append(email)
    save_subscribers(subs)
    return True, "Subscribed"

def list_subscribers():
    subs = load_subscribers()
    if not subs:
        print("No subscribers.")
    else:
        print(f"\nSubscribers ({len(subs)}):")
        for s in subs:
            print(f"  - {s}")
    return subs

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--send":
            success, msg = send_bulk_email()
            print(msg)
        elif sys.argv[1] == "--send-test" and len(sys.argv) > 2:
            success, msg = send_test_email(sys.argv[2])
            print(msg)
        elif sys.argv[1] == "--subscribe":
            email = input("Email: ").strip()
            success, msg = add_subscriber(email)
            print(msg)
        elif sys.argv[1] == "--list":
            list_subscribers()
        else:
            print("Commands: --send, --send-test EMAIL, --subscribe, --list")
    else:
        print("1. Send to all\n2. Send test email\n3. List subscribers")
        choice = input("Choice: ")
        if choice == '1':
            success, msg = send_bulk_email()
            print(msg)
        elif choice == '2':
            email = input("Email: ")
            success, msg = send_test_email(email)
            print(msg)
        elif choice == '3':
            list_subscribers()