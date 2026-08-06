"""
Streamlit Dashboard for Neural Observatory
Run with: streamlit run streamlit_dashboard.py
"""

import streamlit as st
import pandas as pd
from database_mysql import get_all_articles, get_all_subscribers_db, add_subscriber_db
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Neural Observatory", layout="wide", page_icon="🧠")

st.title("🧠 Neural Observatory – Big Data Dashboard")
st.markdown("Real‑time AI news intelligence from 8+ sources")

# ========== LOAD DATA ==========
try:
    articles = get_all_articles(limit=200)
    df = pd.DataFrame(articles)
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.info("Make sure your database is running and secrets are configured.")
    st.stop()

if df.empty:
    st.warning("No articles found. Run `python main.py` first.")
    st.stop()

# ========== STATS ROW ==========
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Articles", len(df))
col2.metric("Avg Summary Len", int(df['summary'].str.len().mean()) if not df.empty else 0)
col3.metric("Sources", df['source'].nunique())
subs = len(get_all_subscribers_db())
col4.metric("Subscribers", subs)

# ========== CHARTS ==========
st.subheader("📊 Source Distribution")
source_counts = df['source'].value_counts().reset_index()
source_counts.columns = ['source', 'count']
fig1 = px.pie(source_counts, values='count', names='source', title='Articles by Source')
st.plotly_chart(fig1, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🏷️ Source Engagement")
    engagement = df.groupby('source').size().reset_index(name='count')
    st.dataframe(engagement, use_container_width=True)

with col2:
    st.subheader("📈 Daily Trend")
    df['date'] = pd.to_datetime(df['created_at'], errors='coerce').dt.date
    daily = df.groupby('date').size().reset_index(name='count')
    fig2 = px.line(daily, x='date', y='count', title='Articles Over Time')
    st.plotly_chart(fig2, use_container_width=True)

# ========== ARTICLE FEED ==========
st.subheader("📰 Recent Intelligence Feed")

def badge(source):
    colors = {
        'youtube': '#ff0000',
        'hacker_news': '#ff6600',
        'sports': '#1e88e5',
        'entertainment': '#9c27b0',
        'news': '#2e7d32',
        'florida_man': '#ffaa00'
    }
    color = colors.get(source, '#666')
    return f"<span style='background:{color};color:white;padding:2px 8px;border-radius:12px;font-size:0.7rem;'>{source.upper()}</span>"

for i, row in df.head(20).iterrows():
    col1, col2 = st.columns([1, 4])
    with col1:
        vid = row.get('video_id', '')
        if row.get('source') == 'youtube' and vid:
            thumb = f"https://img.youtube.com/vi/{vid}/mqdefault.jpg"
        else:
            thumb = f"https://placehold.co/120x90/ccc/333?text={row.get('source','news')[:3].upper()}"
        st.image(thumb, width=120)
    with col2:
        st.markdown(f"**{badge(row.get('source','news'))}** {row.get('title', 'Untitled')}")
        st.caption(row.get('summary', '')[:150] + "...")
        st.markdown(f"[Read more]({row.get('url', '#')})")
    st.divider()

# ========== SUBSCRIPTION ==========
st.sidebar.header("📧 Subscribe")
email = st.sidebar.text_input("Enter your email")
if st.sidebar.button("Subscribe"):
    if email and '@' in email:
        success = add_subscriber_db(email)
        if success:
            st.sidebar.success(f"✅ Subscribed {email}")
        else:
            st.sidebar.warning("Already subscribed or invalid")
    else:
        st.sidebar.error("Enter a valid email")

# ========== RUN PIPELINE ==========
if st.sidebar.button("🔄 Run Pipeline"):
    import subprocess
    with st.spinner("Running pipeline..."):
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        st.sidebar.success("Pipeline completed!")
        st.sidebar.code(result.stdout[:500])

st.sidebar.markdown("---")
st.sidebar.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
