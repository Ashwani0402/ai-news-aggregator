#!/usr/bin/env python3
"""
Enhanced Unified Backend API for AI News Aggregator
Optimized + Personalized + Production Ready
Compatible with PRO Dashboard – All endpoints included
"""

import json
import os
import subprocess
import threading
import smtplib
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# ==================== CONFIGURATION ====================

SUBSCRIBERS_FILE = "subscribers.json"
USER_PROFILES_FILE = "user_profiles.json"
FEEDBACK_FILE = "feedback.json"
ARTICLES_FILE = "saved_articles.json"
PREV_STATS_FILE = "previous_stats.json"
LAST_RUN_FILE = "last_run.json"
PIPELINE_STATS_FILE = "pipeline_stats.json"

PORT = 8081

# ==================== EMAIL CONFIG ====================

try:
    from dotenv import load_dotenv

    load_dotenv()

    FROM_EMAIL = os.getenv("EMAIL_USER", "ashwanirai710@gmail.com")
    APP_PASSWORD = os.getenv("EMAIL_PASS", "htqq ndfp zfrq qiex")

except Exception:
    FROM_EMAIL = "ashwanirai710@gmail.com"
    APP_PASSWORD = "htqq ndfp zfrq qiex"

# ==================== FILE HELPERS ====================


def load_json(file_path, default=None):
    if not os.path.exists(file_path):
        return default if default is not None else []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return default if default is not None else []


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ==================== SUBSCRIBERS ====================


def load_subscribers():
    return load_json(SUBSCRIBERS_FILE, [])


def save_subscribers(subscribers):
    save_json(SUBSCRIBERS_FILE, subscribers)


def add_subscriber(email):
    email = email.strip().lower()

    subscribers = load_subscribers()

    if email in subscribers:
        return False, "Already subscribed"

    subscribers.append(email)

    save_subscribers(subscribers)

    return True, "Subscribed successfully"


def remove_subscriber(email):
    email = email.strip().lower()

    subscribers = load_subscribers()

    if email not in subscribers:
        return False, "Subscriber not found"

    subscribers.remove(email)

    save_subscribers(subscribers)

    return True, "Removed successfully"


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

    profiles[email]["interests"] = interests[:3]

    save_user_profiles(profiles)

    return True


def get_user_interests(email):
    profiles = load_user_profiles()

    return profiles.get(email, {}).get("interests", [])


# ==================== FEEDBACK ====================


def add_feedback(email, article_id, rating):
    feedback = load_json(FEEDBACK_FILE, [])

    feedback.append({
        "email": email,
        "article_id": article_id,
        "rating": rating,
        "timestamp": datetime.now().isoformat()
    })

    save_json(FEEDBACK_FILE, feedback)

    return True


# ==================== ARTICLE STATS ====================


def get_article_stats():
    articles = load_json(ARTICLES_FILE, [])

    if not articles:
        return {
            "total": 0,
            "avg_length": 0,
            "unique_keywords": 0,
            "top_keywords": [],
            "source_distribution": {}
        }

    total = len(articles)

    avg_length = (
        sum(len(a.get("summary", "")) for a in articles) // total
    )

    stop_words = {
        "this", "that", "these", "those", "from",
        "with", "they", "will", "have", "were",
        "been", "being", "about", "their"
    }

    keyword_count = {}

    for article in articles:

        text = (
            article.get("title", "") + " " +
            article.get("summary", "")
        ).lower()

        words = [
            w for w in text.split()
            if len(w) > 3 and w.isalpha() and w not in stop_words
        ]

        for word in words:
            keyword_count[word] = keyword_count.get(word, 0) + 1

    top_keywords = sorted(
        keyword_count.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    source_distribution = {}

    for article in articles:

        source = (
            article.get("source") or
            article.get("source_name") or
            "unknown"
        ).lower()

        source_distribution[source] = (
            source_distribution.get(source, 0) + 1
        )

    return {
        "total": total,
        "avg_length": avg_length,
        "unique_keywords": len(keyword_count),
        "top_keywords": top_keywords,
        "source_distribution": source_distribution
    }


def get_previous_stats():
    return load_json(PREV_STATS_FILE, {
        "total": 0,
        "unique_keywords": 0,
        "avg_length": 0
    })


def update_previous_stats():
    current = get_article_stats()

    save_json(PREV_STATS_FILE, {
        "total": current["total"],
        "unique_keywords": current["unique_keywords"],
        "avg_length": current["avg_length"],
        "timestamp": datetime.now().isoformat()
    })


# ==================== LAST RUN ====================


def get_last_run_time():
    data = load_json(LAST_RUN_FILE, {})

    return data.get("timestamp", "Never")


def set_last_run_time():
    save_json(LAST_RUN_FILE, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# ==================== PIPELINE HEALTH ====================


def get_pipeline_health():
    stats = load_json(PIPELINE_STATS_FILE, {})

    return {
        "last_duration_seconds": stats.get("last_duration", 0),
        "success_rate": stats.get("success_rate", 100),
        "last_articles": stats.get("last_articles", 0),
        "youtube_status": "online",
        "groq_status": "online",
        "last_run_time": get_last_run_time()
    }


def update_pipeline_stats(duration_seconds, success=True, articles_count=0):
    stats = load_json(PIPELINE_STATS_FILE, {})

    runs = stats.get("runs", [])

    runs.append({
        "duration": duration_seconds,
        "success": success,
        "articles": articles_count
    })

    if len(runs) > 10:
        runs = runs[-10:]

    success_rate = (
        sum(1 for r in runs if r["success"]) / len(runs)
    ) * 100 if runs else 100

    stats["last_duration"] = round(duration_seconds, 2)
    stats["success_rate"] = round(success_rate, 1)
    stats["last_articles"] = articles_count
    stats["runs"] = runs

    save_json(PIPELINE_STATS_FILE, stats)


# ==================== PERSONALIZED RANKING ====================

# IMPORTANT:
# DOES NOT FILTER BY SOURCE
# ONLY RANKS ARTICLES BASED ON USER INTERESTS


def rank_articles_by_interests(articles, email):

    interests = get_user_interests(email)

    if not interests:
        return articles

    ranked_articles = []

    for article in articles:

        text = (
            article.get("title", "") + " " +
            article.get("summary", "") + " " +
            article.get("category", "")
        ).lower()

        score = 0

        for index, interest in enumerate(interests):

            if interest.lower() in text:
                score += (5 - index)

        # trending boost
        if article.get("trending"):
            score += 2

        # recency boost
        if article.get("published"):
            score += 1

        ranked_articles.append((score, article))

    ranked_articles.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [article for score, article in ranked_articles]


# ==================== EMAIL GENERATOR ====================


def generate_digest_html(articles, subscriber_email=""):

    subscriber_name = (
        subscriber_email.split("@")[0]
        if subscriber_email else "Subscriber"
    )

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>NEURAL OBSERVATORY</title>

<style>

body {{
    background: #0a0f1e;
    color: white;
    font-family: Arial;
    padding: 20px;
}}

.container {{
    max-width: 700px;
    margin: auto;
    background: #111827;
    padding: 25px;
    border-radius: 20px;
}}

.article {{
    background: #1f2937;
    padding: 15px;
    border-radius: 14px;
    margin-top: 15px;
}}

.article a {{
    color: cyan;
    text-decoration: none;
}}

.footer {{
    margin-top: 30px;
    text-align: center;
    color: #aaa;
}}

</style>
</head>

<body>

<div class="container">

<h1>⚡ NEURAL OBSERVATORY</h1>

<p>Hello {subscriber_name}, here are your latest AI-curated news insights.</p>
"""

    for article in articles[:15]:

        title = article.get("title", "Untitled")

        summary = article.get("summary", "No summary available")[:180]

        video_id = article.get("video_id", "")

        url = (
            f"https://youtube.com/watch?v={video_id}"
            if video_id else "#"
        )

        html += f"""
<div class="article">

<h3>
<a href="{url}" target="_blank">
{title}
</a>
</h3>

<p>{summary}...</p>

</div>
"""

    html += """
<div class="footer">
<p>© Neural Observatory</p>
<p>AI-powered intelligence digest</p>
</div>

</div>
</body>
</html>
"""

    return html


# ==================== EMAIL SENDER ====================


def send_single_email(to_email, subject, html_content):

    try:

        msg = MIMEMultipart("alternative")

        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email

        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        server.login(FROM_EMAIL, APP_PASSWORD)

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:
        print(f"Email Error: {e}")
        return False


def send_test_email(to_email):

    articles = load_json(ARTICLES_FILE, [])

    if not articles:
        return False, "No articles available"

    html = generate_digest_html(articles[:30], to_email)

    success = send_single_email(
        to_email,
        f"NEURAL DIGEST – {datetime.now().strftime('%b %d, %Y')}",
        html
    )

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

        personalized_articles = rank_articles_by_interests(
            articles,
            email
        )

        html = generate_digest_html(
            personalized_articles[:30],
            email
        )

        if send_single_email(
            email,
            f"NEURAL DIGEST – {datetime.now().strftime('%b %d, %Y')}",
            html
        ):
            success_count += 1

        time.sleep(0.5)

    return True, f"Sent to {success_count}/{len(subscribers)}"


# ==================== PIPELINE ====================


def run_pipeline_async():

    def target():

        start_time = time.time()

        try:

            update_previous_stats()

            result = subprocess.run(
                ["python", "main.py"],
                cwd=os.path.dirname(__file__),
                capture_output=True,
                text=True
            )

            duration = time.time() - start_time

            success = result.returncode == 0

            articles_count = 0

            for line in result.stdout.split("\n"):

                if "Total articles saved:" in line:

                    try:
                        articles_count = int(
                            line.split(":")[1].strip()
                        )
                    except Exception:
                        pass

            update_pipeline_stats(
                duration,
                success,
                articles_count
            )

            if success:
                set_last_run_time()

        except Exception as e:

            duration = time.time() - start_time

            update_pipeline_stats(duration, False, 0)

            print(f"Pipeline Error: {e}")

    thread = threading.Thread(target=target)

    thread.daemon = True

    thread.start()


# ==================== API HANDLER ====================


class APIHandler(BaseHTTPRequestHandler):

    def _send_cors(self):

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

    def do_OPTIONS(self):

        self.send_response(200)

        self._send_cors()

        self.end_headers()

    # REQUIRED REPLACEMENT
    def _send_json(self, data, status=200):

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self._send_cors()

        self.end_headers()

        self.wfile.write(
            json.dumps(data).encode("utf-8")
        )

    # ==================== GET ====================

    def do_GET(self):

        parsed = urlparse(self.path)

        path = parsed.path

        if path == "/list_subscribers":

            self._send_json({
                "subscribers": list_subscribers()
            })

        elif path == "/stats":

            self._send_json(get_article_stats())

        elif path == "/stats_compare":

            self._send_json({
                "current": get_article_stats(),
                "previous": get_previous_stats()
            })

        elif path == "/last_run":

            self._send_json({
                "last_run": get_last_run_time()
            })

        elif path == "/pipeline_health":

            self._send_json(get_pipeline_health())

        elif path == "/get_preferences":

            qs = parse_qs(parsed.query)

            email = qs.get("email", [""])[0]

            if not email:
                self._send_json({
                    "error": "Missing email"
                }, 400)
                return

            self._send_json({
                "interests": get_user_interests(email)
            })

        else:

            self._send_json({
                "error": "Not found"
            }, 404)

    # ==================== POST ====================

    def do_POST(self):

        length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(length).decode("utf-8")

        try:
            data = json.loads(body) if body else {}

        except Exception:

            self._send_json({
                "error": "Invalid JSON"
            }, 400)

            return

        path = urlparse(self.path).path

        # ==================== SUBSCRIBE ====================

        if path == "/subscribe":

            email = data.get("email")

            if not email:
                self._send_json({
                    "error": "Missing email"
                }, 400)
                return

            success, message = add_subscriber(email)

            self._send_json({
                "success": success,
                "message": message
            })

        # ==================== UNSUBSCRIBE ====================

        elif path == "/unsubscribe":

            email = data.get("email")

            if not email:
                self._send_json({
                    "error": "Missing email"
                }, 400)
                return

            success, message = remove_subscriber(email)

            self._send_json({
                "success": success,
                "message": message
            })

        # ==================== PREFERENCES ====================

        elif path == "/set_preferences":

            email = data.get("email")

            interests = data.get("interests", [])

            if not email:
                self._send_json({
                    "error": "Missing email"
                }, 400)
                return

            set_user_interests(email, interests)

            self._send_json({
                "success": True
            })

        # ==================== FEEDBACK ====================

        elif path == "/feedback":

            email = data.get("email")
            article_id = data.get("article_id")
            rating = data.get("rating")

            if not all([email, article_id, rating]):

                self._send_json({
                    "error": "Missing fields"
                }, 400)

                return

            add_feedback(email, article_id, rating)

            self._send_json({
                "success": True
            })

        # ==================== PERSONALIZED FEED ====================

        elif path == "/personalized_feed":

            email = data.get("email")

            if not email:

                self._send_json({
                    "error": "Missing email"
                }, 400)

                return

            articles = load_json(ARTICLES_FILE, [])

            ranked = rank_articles_by_interests(
                articles,
                email
            )

            # REQUIRED CHANGE
            self._send_json({
                'articles': ranked[:200]
            })

        # ==================== RUN PIPELINE ====================

        elif path == "/run_pipeline":

            run_pipeline_async()

            self._send_json({
                "success": True,
                "message": "Pipeline started"
            })

        # ==================== TEST EMAIL ====================

        elif path == "/send_test_email":

            email = data.get("email")

            if not email:

                self._send_json({
                    "error": "Missing email"
                }, 400)

                return

            success, message = send_test_email(email)

            self._send_json({
                "success": success,
                "message": message
            })

        # ==================== BULK EMAIL ====================

        elif path == "/send_bulk_email":

            success, message = send_bulk_email()

            self._send_json({
                "success": success,
                "message": message
            })

        else:

            self._send_json({
                "error": "Not found"
            }, 404)


# ==================== SERVER ====================


def run_server():

    print(f"🚀 Enhanced Unified API running on port {PORT}")

    print("\nAvailable Endpoints:")

    print("GET:")
    print("  /stats")
    print("  /stats_compare")
    print("  /last_run")
    print("  /pipeline_health")
    print("  /list_subscribers")

    print("\nPOST:")
    print("  /subscribe")
    print("  /unsubscribe")
    print("  /set_preferences")
    print("  /feedback")
    print("  /personalized_feed")
    print("  /run_pipeline")
    print("  /send_test_email")
    print("  /send_bulk_email")

    server = HTTPServer(
        ("localhost", PORT),
        APIHandler
    )

    server.serve_forever()


# ==================== MAIN ====================

if __name__ == "__main__":
    run_server()