
NEURAL OBSERVATORY – BIG DATA GENAI PIPELINE

Python Version: 3.10+  |  License: MIT  |  Streamlit Cloud Ready  |  Apache Airflow  |  Apache Spark  |  Apache Kafka

A production-grade, end-to-end Big Data pipeline that ingests AI news from 8+ sources, processes them using Generative AI, and delivers personalized intelligence via real-time dashboard and automated email digests.

TABLE OF CONTENTS

- Overview
- The Problem It Solves
- Architecture and Workflow
- Tech Stack
- Features
- Project Structure
- Installation and Setup
- Running the Project
- Deployment
- Screenshots
- Future Enhancements
- Contributing
- License
- Contact

OVERVIEW

Neural Observatory is an end-to-end Big Data pipeline that collects AI-related news from 8+ sources, summarizes them using Generative AI (Groq LLM), and delivers personalized intelligence to users via:

- Interactive Dashboard – Real-time stats, charts, and personalized article feed.
- Daily Email Digests – Beautiful HTML emails with summaries, thumbnails, and source badges.
- Scalable ETL Pipeline – Powered by Kafka, PySpark, and Airflow for production-grade data processing.

Why This Project?
Information overload is a real problem in the AI space. Professionals spend 2-3 hours daily skimming content. Neural Observatory curates, summarizes, and personalizes AI news, saving users 85% of their reading time.

THE PROBLEM IT SOLVES

Problem: Information Overload -> Solution: Curates and summarizes 200+ articles daily
Problem: Time Wastage -> Solution: 2-3 hours to 10 minutes daily reading time
Problem: Scattered Sources -> Solution: Aggregates 8+ sources in one place
Problem: No Personalization -> Solution: Personalized feed based on user interests (AI/ML, Sports, Entertainment)
Problem: No Analytics -> Solution: Real-time dashboard with stats, charts, and keyword trends
Problem: No Automation -> Solution: Fully automated daily pipeline with Airflow

ARCHITECTURE AND WORKFLOW

High-Level Architecture

Data Sources (YouTube API, Hacker News, Florida Man, Google News, BBC, TechCrunch, Wired, The Verge, Sports, Entertainment) -> Fetchers -> Kafka (Message Queue) -> PySpark (Parallel Processing, AI Summarization) -> MySQL (Storage) -> Unified API (REST) -> Dashboard (Ultimate + Streamlit) and Email Agent (Daily Digests)

Orchestration: Apache Airflow (daily at 9 AM with retries and monitoring)

End-to-End Data Flow (Simplified)

1. Airflow triggers the pipeline daily at 9 AM.
2. main.py runs, calling all fetchers to collect raw data from 8+ sources.
3. Each fetcher standardizes data into a common dictionary format.
4. Data is sent to Kafka topic "news-articles-topic" (decoupling).
5. PySpark reads from Kafka, processes in parallel: cleans, summarizes with Groq LLM, deduplicates.
6. Processed data is written to MySQL tables (articles, subscribers, user_profiles, feedback, pipeline_stats, last_run).
7. Unified API serves data to the dashboard (stats, personalized feed, subscription, feedback).
8. Email Agent reads from MySQL, generates HTML email, sends via Gmail SMTP to all subscribers.

TECH STACK

Languages: Python 3.10+
Big Data: Apache Kafka, PySpark, Apache Airflow
Database: MySQL (with connection pooling)
AI/LLM: Groq API (Llama 3) with intelligent fallback
Backend: Custom HTTP server (REST API)
Frontend: HTML5, CSS3 (glass-morphism), JavaScript (Chart.js)
DevOps: Docker, Git, GitHub, Environment Variables
Security: API key authentication, .env secrets, SQL injection prevention
Testing: Local HTTP server + API server

FEATURES

Data Ingestion (8+ Sources)
- YouTube Data API v3
- Hacker News Firebase API
- Florida Man API
- Google News RSS
- BBC News RSS
- TechCrunch RSS
- Wired RSS
- The Verge RSS
- Sports News (ESPN, BBC Sport, Sky Sports)
- Entertainment News (Variety, Hollywood Reporter, IGN)

AI-Powered Summarization
- Groq Llama 3 LLM for 2-3 sentence summaries
- Intelligent fallback (keyword-based extraction)
- 85% reading time reduction

Big Data Processing
- Apache Kafka for message queuing (decoupling)
- PySpark for distributed, parallel processing
- Apache Airflow for workflow orchestration (daily at 9 AM)
- Batch processing with retries and monitoring

Interactive Dashboard
- Real-time stats (total articles, avg length, unique keywords, subscribers)
- Charts (keyword frequency, source distribution, delta analysis)
- Personalized article feed (based on user interests)
- Feedback buttons (satisfied, neutral, dissatisfied)
- Subscription management
- Pipeline health monitoring

Email Digests
- Beautiful, sci-fi themed HTML emails
- Thumbnails and source badges
- Working links
- Unsubscribe functionality
- Bulk email delivery

Security
- API key authentication for protected endpoints
- Environment variables for secrets
- SQL injection prevention
- CORS handling
- Input sanitization

Scalability
- Horizontally scalable (Kafka, PySpark, Airflow)
- Connection pooling for database
- Parallel processing (ThreadPoolExecutor, PySpark)

PROJECT STRUCTURE

my-ai-project/
├── .env                          (secrets, not in Git)
├── .gitignore
├── requirements.txt
├── README.md
├── database_mysql.py             (MySQL database layer)
├── scraper.py                    (Groq AI summarizer)
├── youtube_service.py            (YouTube API wrapper)
├── hacker_news_fetcher.py
├── florida_man_fetcher.py
├── backup_news_fetcher.py        (RSS news sources)
├── sports_fetcher.py
├── entertainment_fetcher.py
├── unified_saver.py              (Article saving logic)
├── main.py                       (Data pipeline)
├── unified_api.py                (Backend API server)
├── email_agent.py                (Email sending system)
├── ultimate_dashboard.html       (Ultimate Dashboard)
├── streamlit_dashboard.py        (Streamlit Dashboard)
├── subscribers.json              (local backup)
├── user_profiles.json            (local backup)
├── feedback.json
├── last_run.json
├── previous_stats.json
├── api.log                       (auto-generated logs)
├── email.log
├── pipeline.log
└── myenv/                        (virtual environment)

INSTALLATION AND SETUP

Prerequisites:
- Python 3.10 or higher
- MySQL Server
- Git
- (Optional) Docker for Kafka/PySpark/Airflow

Step 1: Clone the Repository
git clone https://github.com/Ashwani0402/ai-news-aggregator.git
cd ai-news-aggregator

Step 2: Create Virtual Environment
python -m venv myenv
myenv\Scripts\activate   (Windows)
source myenv/bin/activate   (macOS/Linux)

Step 3: Install Dependencies
pip install -r requirements.txt

Step 4: Configure Environment Variables
Create .env file in root directory with:
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-16-digit-app-password
YOUTUBE_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...
API_ADMIN_KEY=your-32-char-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=news_aggregator
ENVIRONMENT=development
DEBUG=False

Step 5: Initialize Database
python -c "from database_mysql import init_db; init_db()"

Step 6: Run Data Pipeline (First Time)
python main.py
Answer y when asked to clear old articles.

RUNNING THE PROJECT

Terminal 1 – Start API Server (Keep Running)
cd C:\Users\ashwa\OneDrive\Desktop\my-ai-project
myenv\Scripts\activate
python unified_api.py

Terminal 2 – Start Web Server (Ultimate Dashboard)
cd C:\Users\ashwa\OneDrive\Desktop\my-ai-project
myenv\Scripts\activate
python -m http.server 8080

Terminal 3 – Start Streamlit Dashboard
cd C:\Users\ashwa\OneDrive\Desktop\my-ai-project
myenv\Scripts\activate
streamlit run streamlit_dashboard.py

Terminal 4 – Run Data Pipeline (Once)
cd C:\Users\ashwa\OneDrive\Desktop\my-ai-project
myenv\Scripts\activate
python main.py

Terminal 5 – Send Test Email (Optional)
cd C:\Users\ashwa\OneDrive\Desktop\my-ai-project
myenv\Scripts\activate
python email_agent.py --send-test your-email@gmail.com

Open Dashboards:
Ultimate Dashboard: http://localhost:8080/ultimate_dashboard.html
Streamlit Dashboard: http://localhost:8501

DEPLOYMENT

Deploy to Streamlit Cloud:
1. Push code to GitHub.
2. Go to Streamlit Cloud (streamlit.io/cloud).
3. Connect your GitHub repo.
4. Set streamlit_dashboard.py as main file.
5. Add secrets (.streamlit/secrets.toml in dashboard).

Deploy Backend API to Render:
1. Push code to GitHub.
2. Go to Render (render.com).
3. Create a Web Service.
4. Build command: pip install -r requirements.txt.
5. Start command: python unified_api.py.
6. Add environment variables.

Deploy Ultimate Dashboard to GitHub Pages:
1. Push ultimate_dashboard.html to GitHub.
2. Go to Settings -> Pages.
3. Select main branch.
4. Live URL: https://yourusername.github.io/repo/ultimate_dashboard.html

SCREENSHOTS

(Add screenshots to a screenshots/ folder and reference them here)

FUTURE ENHANCEMENTS

- User authentication (OAuth 2.0)
- Real-time WebSocket updates
- Recommendation engine (based on feedback)
- Mobile app (React Native)
- Sentiment analysis (TextBlob/Transformers)
- Topic clustering (K-Means)
- Multi-language support
- Integration with Slack/Teams
- Advanced analytics (Spark ML)

CONTRIBUTING

Contributions are welcome! Please fork the repository, create a feature branch, commit changes, push, and open a Pull Request.

LICENSE

This project is for personal/educational use only. All original content belongs to its respective owners. Summaries are AI-generated.

CONTACT

Author: Ashwani Rai
Email: ashwanirai710@gmail.com
GitHub: Ashwani0402
LinkedIn: (your LinkedIn URL)

ACKNOWLEDGEMENTS

YouTube Data API
Groq Llama 3
Hacker News Firebase API
Florida Man API
Google News RSS
BBC, TechCrunch, Wired, The Verge RSS feeds
Apache Kafka, PySpark, Airflow
Streamlit, Plotly, Chart.js

Star the Project

If you found this project useful, please star it on GitHub!

Built with love by Ashwani Rai
