import smtplib
import json
import os
import requests

from dotenv import load_dotenv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

# =========================================================
# CONFIGURATION
# =========================================================

FROM_EMAIL = os.getenv("EMAIL_USER", "ashwanirai710@gmail.com")
APP_PASSWORD = os.getenv("EMAIL_PASS", "htqq ndfp zfrq qiex")

SUBSCRIBERS_FILE = "subscribers.json"
API_URL = "http://localhost:8081"

# =========================================================
# SUBSCRIBER MANAGEMENT
# =========================================================


def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, "w") as f:
        json.dump(subscribers, f, indent=2)


def add_subscriber(email):

    email = email.strip().lower()

    subscribers = load_subscribers()

    if email in subscribers:
        return False, "Already subscribed"

    subscribers.append(email)

    save_subscribers(subscribers)

    return True, "Subscribed"


def list_subscribers():

    subscribers = load_subscribers()

    if not subscribers:
        print("No subscribers.")
    else:
        print(f"\nSubscribers ({len(subscribers)}):")

        for sub in subscribers:
            print(f" - {sub}")

    return subscribers


# =========================================================
# EMAIL SENDER
# =========================================================


def send_single_email(to_email, subject, html_content):

    try:

        print(f"📧 Sending email to {to_email}...")

        msg = MIMEMultipart("alternative")

        msg["Subject"] = subject
        msg["From"] = FROM_EMAIL
        msg["To"] = to_email

        msg.attach(MIMEText(html_content, "html"))

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

        server.login(FROM_EMAIL, APP_PASSWORD)

        server.send_message(msg)

        server.quit()

        print(f"✅ Sent successfully to {to_email}")

        return True

    except Exception as e:

        print(f"❌ Email error: {e}")

        return False


# =========================================================
# GET ARTICLES
# =========================================================


def get_articles(email="test@example.com"):

    """
    Fetch personalized articles from backend API.
    Falls back to local JSON if API fails.
    """

    try:

        response = requests.post(
            f"{API_URL}/personalized_feed",
            json={"email": email},
            timeout=10
        )

        if response.status_code == 200:

            articles = response.json().get("articles", [])

            if articles:
                return articles

    except Exception as e:
        print(f"⚠ API fetch failed: {e}")

    # fallback local file

    try:

        with open("saved_articles.json", "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []


# =========================================================
# PROFESSIONAL HTML GENERATOR
# =========================================================


def generate_professional_html(articles, subscriber_email=""):

    """
    Generate beautiful HTML email with sections:
    AI, Sports, Entertainment
    """

    subscriber_name = (
        subscriber_email.split("@")[0]
        if subscriber_email else "Reader"
    )

    # =====================================================
    # CATEGORY GROUPING
    # =====================================================

    ai_articles = []
    sports_articles = []
    entertainment_articles = []

    for article in articles:

        source = (
            article.get("source") or
            article.get("source_name") or
            ""
        ).lower()

        title = article.get("title", "").lower()

        # SPORTS
        if (
            "sports" in source or
            "sport" in title or
            any(
                kw in title for kw in [
                    "football",
                    "basketball",
                    "cricket",
                    "tennis",
                    "fifa",
                    "ipl",
                    "nba"
                ]
            )
        ):

            sports_articles.append(article)

        # ENTERTAINMENT
        elif (
            "entertainment" in source or
            any(
                kw in title for kw in [
                    "movie",
                    "movies",
                    "film",
                    "series",
                    "netflix",
                    "hollywood",
                    "anime"
                ]
            )
        ):

            entertainment_articles.append(article)

        # AI DEFAULT
        else:
            ai_articles.append(article)

    ai_top = ai_articles[:10]
    sports_top = sports_articles[:10]
    entertainment_top = entertainment_articles[:10]

    # =====================================================
    # SECTION RENDERER
    # =====================================================

    def render_section(section_title, section_articles, icon):

        if not section_articles:

            return f"""
            <div class="section-header">
                <span class="icon">{icon}</span>
                <h2>{section_title}</h2>
            </div>

            <p>No articles available.</p>
            """

        html = f"""
        <div class="section-header">
            <span class="icon">{icon}</span>
            <h2>{section_title}</h2>
        </div>
        """

        for article in section_articles:

            title = article.get("title", "Untitled")

            summary = (
                article.get("summary", "No summary available")
            )[:160]

            url = article.get("url", "")

            if not url and article.get("video_id"):

                url = (
                    f"https://youtube.com/watch?"
                    f"v={article['video_id']}"
                )

            # thumbnail

            if article.get("video_id"):

                thumbnail = f"""
                <img
                    src="https://img.youtube.com/vi/{article['video_id']}/mqdefault.jpg"
                    class="thumb"
                    onerror="this.style.display='none'"
                >
                """

            else:

                thumbnail = """
                <div class="thumb placeholder"></div>
                """

            html += f"""
            <div class="article">

                {thumbnail}

                <div class="article-content">

                    <div class="article-title">
                        <a href="{url}" target="_blank">
                            {title}
                        </a>
                    </div>

                    <div class="article-summary">
                        {summary}...
                    </div>

                    <div class="article-link">
                        <a href="{url}" target="_blank">
                            Read more →
                        </a>
                    </div>

                </div>

            </div>
            """

        return html

    # =====================================================
    # MAIN EMAIL HTML
    # =====================================================

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>Neural Observatory – Daily Digest</title>

<style>

body {{
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f0f2f5;
    margin: 0;
    padding: 20px;
}}

.container {{
    max-width: 720px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.header {{
    background: linear-gradient(135deg, #1a73e8, #0d47a1);
    color: white;
    padding: 30px 20px;
    text-align: center;
}}

.header h1 {{
    margin: 0;
    font-size: 28px;
}}

.header p {{
    margin: 8px 0 0;
    opacity: 0.9;
}}

.section {{
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
}}

.section-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    border-bottom: 2px solid #1a73e8;
    padding-bottom: 8px;
}}

.section-header .icon {{
    font-size: 24px;
}}

.section-header h2 {{
    font-size: 20px;
    color: #1a73e8;
    margin: 0;
}}

.article {{
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #f0f0f0;
}}

.thumb {{
    width: 110px;
    height: 75px;
    background: #ddd;
    border-radius: 8px;
    object-fit: cover;
}}

.placeholder {{
    background: #e0e0e0;
}}

.article-content {{
    flex: 1;
}}

.article-title {{
    font-weight: 600;
    margin-bottom: 6px;
}}

.article-title a {{
    color: #1a73e8;
    text-decoration: none;
}}

.article-summary {{
    font-size: 13px;
    color: #444;
    margin-bottom: 6px;
    line-height: 1.5;
}}

.article-link a {{
    font-size: 12px;
    color: #1a73e8;
    text-decoration: none;
}}

.footer {{
    background: #f8f9fa;
    padding: 20px;
    text-align: center;
    font-size: 12px;
    color: #666;
}}

@media (max-width: 550px) {{

    .article {{
        flex-direction: column;
    }}

    .thumb {{
        width: 100%;
        height: auto;
    }}
}}

</style>

</head>

<body>

<div class="container">

    <div class="header">

        <h1>🤖 Neural Observatory</h1>

        <p>Your Daily Curated Intelligence Feed</p>

        <p style="font-size:12px;">
            {datetime.now().strftime('%A, %B %d, %Y')}
        </p>

    </div>

    <div class="section">
        {render_section('AI & Machine Learning', ai_top, '🧠')}
    </div>

    <div class="section">
        {render_section('Sports', sports_top, '⚽')}
    </div>

    <div class="section">
        {render_section('Entertainment', entertainment_top, '🎬')}
    </div>

    <div class="footer">

        <p>
            You received this email because you subscribed
            to Neural Observatory.
        </p>

        <p>
            Reply with "UNSUBSCRIBE" to stop receiving emails.
        </p>

        <p>
            © 2025 Neural Observatory | Big Data Pipeline
        </p>

    </div>

</div>

</body>

</html>
"""

    return html


# =========================================================
# TEST EMAIL
# =========================================================


def send_test_email(to_email):

    print(f"\n📨 Preparing test email for {to_email}...")

    articles = get_articles(to_email)

    if not articles:
        return False, "No articles found. Run main.py first."

    html = generate_professional_html(
        articles,
        to_email
    )

    subject = (
        f"Neural Observatory – "
        f"{datetime.now().strftime('%b %d, %Y')}"
    )

    success = send_single_email(
        to_email,
        subject,
        html
    )

    return success, "Email sent" if success else "Failed"


# =========================================================
# BULK EMAIL
# =========================================================


def send_bulk_email():

    subscribers = load_subscribers()

    if not subscribers:
        return False, "No subscribers"

    success_count = 0

    for email in subscribers:

        articles = get_articles(email)

        if not articles:
            continue

        html = generate_professional_html(
            articles,
            email
        )

        success = send_single_email(
            email,
            f"Neural Observatory – {datetime.now().strftime('%b %d, %Y')}",
            html
        )

        if success:
            success_count += 1

    return (
        True,
        f"Sent to {success_count}/{len(subscribers)}"
    )


# =========================================================
# CLI
# =========================================================


if __name__ == "__main__":

    import sys

    if len(sys.argv) > 1:

        if (
            sys.argv[1] == "--send-test"
            and len(sys.argv) > 2
        ):

            success, msg = send_test_email(
                sys.argv[2]
            )

            print(msg)

        elif sys.argv[1] == "--send":

            success, msg = send_bulk_email()

            print(msg)

        elif sys.argv[1] == "--subscribe":

            email = input("Email: ").strip()

            success, msg = add_subscriber(email)

            print(msg)

        elif sys.argv[1] == "--list":

            list_subscribers()

        else:

            print(
                "Commands:\n"
                "  --send\n"
                "  --send-test EMAIL\n"
                "  --subscribe\n"
                "  --list"
            )

    else:

        print("\n1. Send to all")
        print("2. Send test email")
        print("3. List subscribers")

        choice = input("\nChoice: ").strip()

        if choice == "1":

            success, msg = send_bulk_email()

            print(msg)

        elif choice == "2":

            email = input("Email: ").strip()

            success, msg = send_test_email(email)

            print(msg)

        elif choice == "3":

            list_subscribers()