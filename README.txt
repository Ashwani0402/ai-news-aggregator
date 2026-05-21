# 📘 **AI News Aggregator – Complete Setup & Run Guide**

> *A production‑ready, multi‑source Big Data pipeline that fetches AI news from YouTube, Hacker News, Florida Man API, Google News, BBC, TechCrunch, Wired, and The Verge, summarizes them using AI (Groq/Gemini), and delivers a stunning interactive dashboard with personalised interests, feedback collection, and email digests.*

---

## 🧭 **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Step‑by‑Step Setup](#step-by-step-setup)
   - 3.1. Clone / Download the Project
   - 3.2. Create Virtual Environment
   - 3.3. Install Dependencies
   - 3.4. Configure API Keys (Optional)
   - 3.5. Run the Data Pipeline (Fetch Articles)
   - 3.6. Start the Unified API Server
   - 3.7. Start the Web Server
   - 3.8. Open the Dashboard
4. [Using the Dashboard](#using-the-dashboard)
5. [Email Commands (CLI)](#email-commands-cli)
6. [Troubleshooting](#troubleshooting)
7. [Customisation & Extending](#customisation--extending)

---

## 1️⃣ **Prerequisites**

- **Operating System:** Windows 10/11, macOS, or Linux.
- **Python 3.10 or higher** ([Download Python](https://python.org))
- **Git** (optional, for cloning)
- **Internet connection** (for API calls)
- **Gmail account** (optional, for sending email digests)

---

## 2️⃣ **Project Structure**

```
my-ai-project/
├── main.py                      # Main pipeline (fetch & summarise)
├── unified_api.py               # Backend API (port 8081)
├── ultimate_dashboard.html      # Interactive dashboard
├── email_agent.py               # Email sending script
├── youtube_service.py           # YouTube API wrapper
├── hacker_news_fetcher.py
├── florida_man_fetcher.py
├── backup_news_fetcher.py
├── scraper.py                   # AI summariser (Groq/Gemini)
├── database.py                  # JSON storage
├── saved_articles.json          # All fetched articles (auto‑created)
├── subscribers.json             # Email subscribers (auto‑created)
├── user_profiles.json           # User interests (auto‑created)
├── feedback.json                # User feedback (auto‑created)
├── requirements.txt             # Python dependencies
└── myenv/                       # Virtual environment (created later)
```

---

## 3️⃣ **Step‑by‑Step Setup**

### **3.1. Clone / Download the Project**

If you received a `.zip` file, extract it to a folder (e.g. `C:\Users\YourName\Desktop\my-ai-project`).

If using Git:
```bash
git clone <repository-url>
cd my-ai-project
```

### **3.2. Create Virtual Environment**

Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux).

**Windows:**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

You should see `(myenv)` at the beginning of the command line.

### **3.3. Install Dependencies**

Make sure `requirements.txt` exists in the project folder. If not, create it with:

```text
requests
feedparser
praw
google-generativeai
openai
python-dotenv
schedule
flask
```

Then install:
```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:
```bash
pip install requests feedparser praw google-generativeai openai python-dotenv schedule
```

### **3.4. Configure API Keys (Optional but Recommended)**

The project uses **free sources** by default, but for AI summarisation you may want to add a Groq or Gemini key.

- **Groq** (free): sign up at [console.groq.com](https://console.groq.com), get an API key.
- **Gemini** (free student plan): sign up at [aistudio.google.com](https://aistudio.google.com).

Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your_groq_key_here
# or
GEMINI_API_KEY=your_gemini_key_here
```

If you skip this, the summariser will use a basic fallback (still works but less accurate).

### **3.5. Run the Data Pipeline (Fetch Articles)**

This step collects articles from all sources, generates AI summaries, and saves them to `saved_articles.json`.

```bash
python main.py
```

When prompted `Clear old articles before fetching? (y/n):`, type `y` and press Enter.

Wait 2‑3 minutes. You should see:
```
✅ PROCESSING COMPLETE!
   Total articles saved: 85
```

### **3.6. Start the Unified API Server**

**Open a new terminal** (keep the previous one if you want). Activate the environment again and run:

```bash
myenv\Scripts\activate   # Windows
# or source myenv/bin/activate (Mac/Linux)

python unified_api.py
```

You will see:
```
🚀 Unified API server starting on port 8081
```

Keep this terminal **running**.

### **3.7. Start the Web Server**

**Open another new terminal**. Activate the environment and run:

```bash
myenv\Scripts\activate
python -m http.server 8080
```

You will see:
```
Serving HTTP on :: port 8080 (http://[::]:8080/) ...
```

Keep this terminal **running**.

### **3.8. Open the Dashboard**

Open your web browser (Chrome, Edge, Firefox) and go to:

```
http://localhost:8080/ultimate_dashboard.html
```

**Do NOT double‑click the HTML file** – you must use the `http://localhost:8080` URL to avoid CORS errors.

---

## 4️⃣ **Using the Dashboard**

Once loaded, you will see:

- **Animated particle background** (cyber‑style)
- **Stats cards**: Total articles, Avg summary length, Unique keywords, Subscriber count
- **Charts**: Top keywords bar chart, Source distribution pie chart
- **Interest selector**: Click **AI/ML**, **Sports**, **Entertainment** (up to 3) – articles re‑rank instantly.
- **Subscription box**: Enter your email and click **Subscribe** – you will be added to `subscribers.json`.
- **Action buttons**:
  - **Run Data Pipeline** – triggers `main.py` in the background, fetches fresh articles (takes ~2 min). After completion, click **Refresh Data** to see updates.
  - **Send Test Email** – sends a personalised digest to any email address (even not subscribed).
  - **Send to All Subscribers** – sends the digest to everyone in `subscribers.json`.
- **Article feed**: 15 articles per source (YouTube, Hacker News, Florida Man, News) with source badges, summaries, and feedback buttons (👍😐👎).

**Feedback** is stored in `feedback.json` and can be used later for analytics.

---

## 5️⃣ **Email Commands (CLI)**

If you prefer to send emails from the terminal (instead of the dashboard), use `email_agent.py`:

| Command | Description |
|---------|-------------|
| `python email_agent.py --send-test someone@example.com` | Send a test digest to any email |
| `python email_agent.py --send` | Send digest to all subscribers |
| `python email_agent.py --subscribe` | Add a subscriber interactively |
| `python email_agent.py --list` | List all subscribers |

**Important:** The email sender uses Gmail SMTP. The credentials are hardcoded inside `email_agent.py` (`FROM_EMAIL` and `APP_PASSWORD`). If you want to use a different email, edit those variables.

---

## 6️⃣ **Troubleshooting**

| Problem | Solution |
|---------|----------|
| **Dashboard shows no articles** | Run `python main.py` first, then refresh the dashboard. |
| **CORS errors (fetch blocked)** | You double‑clicked the HTML file. Use `http://localhost:8080/ultimate_dashboard.html`. |
| **API not responding (dashboard shows errors)** | Make sure `unified_api.py` is running (port 8081). |
| **Email not sending** | Check that `FROM_EMAIL` and `APP_PASSWORD` in `email_agent.py` are correct. Generate an App Password from Google Account (not your regular password). |
| **Non‑YouTube links don’t work** | The email template uses the `url` field from each article. If an article lacks a URL, it falls back to `#`. Ensure your pipeline saves the `url` properly (the provided code does). |
| **Pipeline takes very long** | The first run may be slow due to many API calls. Subsequent runs (with `--clear n`) are faster because duplicates are skipped. |
| **Port 8080 or 8081 already in use** | Change the ports in `unified_api.py` and the `http.server` command, e.g. `python -m http.server 8082`. Also update the dashboard’s `fetch` URLs accordingly. |

---

## 7️⃣ **Customisation & Extending**

### **Add More News Sources**

Edit `backup_news_fetcher.py` or `main.py` to include additional RSS feeds or APIs.

### **Change the AI Summariser**

Modify `scraper.py` – replace `client.chat.completions.create` with any OpenAI‑compatible endpoint (Groq, Gemini, local LLM).

### **Deploy to the Cloud**

- **API server**: Use a cloud VM (AWS, DigitalOcean) or services like Render (free tier).
- **Dashboard**: Upload static files to GitHub Pages or Netlify.
- **Scheduler**: Use a cron job or cloud function to run `main.py` daily.

### **Personalise Email Design**

The email HTML is generated inside `email_agent.py` – you can change colours, fonts, layout, or add your logo.

---

## ✅ **Final Check**

- [ ] Virtual environment activated.
- [ ] All dependencies installed.
- [ ] `python main.py` ran successfully (≥ 85 articles).
- [ ] `unified_api.py` is running (terminal stays open).
- [ ] `python -m http.server 8080` is running.
- [ ] Dashboard opens at `http://localhost:8080/ultimate_dashboard.html`.

**Congratulations!** You now have a fully functional, multi‑source AI news aggregator with an interactive dashboard, user interests, feedback, and email digests.

For any issues, please refer to the [Troubleshooting](#troubleshooting) section or contact the developer.

---

*End of documentation* 🚀
