import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================
# FALLBACK SUMMARIZER (No API Key Required)
# ============================================
def smart_fallback_summary(text, title):
    """Generate intelligent fallback summary without API"""
    if not text or len(text) < 20:
        return f"Analysis of: {title[:100]}"
    
    # Extract key sentences
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    key_sentences = []
    
    # Find sentences with important keywords
    keywords = ['AI', 'artificial', 'intelligence', 'machine', 'learning', 'model', 'data', 'new', 'breakthrough', 'release', 'update']
    
    for sent in sentences:
        sent_lower = sent.lower()
        if any(kw in sent_lower for kw in keywords):
            key_sentences.append(sent.strip())
        if len(key_sentences) >= 3:
            break
    
    if key_sentences:
        summary = '. '.join(key_sentences[:3]) + '.'
    else:
        summary = sentences[0] if sentences else title
    
    return summary[:250] + '...' if len(summary) > 250 else summary

# ============================================
# GROQ API SETUP (Read from .env)
# ============================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client (only if key exists)
client = None
if GROQ_API_KEY:
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        print("✅ Groq API initialized")
    except ImportError:
        print("⚠️ Groq library not installed. Run: pip install groq")
        client = None
    except Exception as e:
        print(f"⚠️ Groq initialization error: {e}")
        client = None
else:
    print("⚠️ GROQ_API_KEY not found in .env. Using fallback summarizer only.")

# ============================================
# MAIN SUMMARIZER FUNCTION
# ============================================
def summarize_text(text, title=""):
    """Use AI to summarize text - handles both text and title"""
    if not text or len(text) < 20:
        # If no description, create summary from title
        if title:
            return f"Analysis of: {title[:150]}..."
        return "No detailed description available for this content."
    
    # Try Groq API if available
    if client:
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes content in 2-3 concise sentences."},
                    {"role": "user", "content": f"Please summarize this in 2-3 sentences: {text[:800]}"}
                ],
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Groq API error: {e}")
            # Fall through to fallback
    
    # Fallback: intelligent extraction (works offline)
    sentences = text.replace('!', '.').replace('?', '.').split('.')
    key_sentences = []
    keywords = ['AI', 'artificial', 'intelligence', 'new', 'breakthrough', 'launch', 'research', 'study']
    
    for sent in sentences:
        sent_lower = sent.lower()
        if any(kw in sent_lower for kw in keywords) and len(sent.strip()) > 30:
            key_sentences.append(sent.strip())
        if len(key_sentences) >= 2:
            break
    
    if key_sentences:
        summary = '. '.join(key_sentences) + '.'
    else:
        summary = sentences[0][:200] if sentences else title
    
    return summary[:250] + '...' if len(summary) > 250 else summary

# ============================================
# VIDEO PROCESSOR
# ============================================
def process_video(video_title, description):
    """Process a video and generate summary with intelligent fallback"""
    summary = summarize_text(description, video_title)
    
    # If AI summary failed or is garbage, use enhanced fallback
    if not summary or 'Could not summarize' in summary or len(summary) < 20:
        summary = smart_fallback_summary(description, video_title)
        print(f"   ⚡ Using smart fallback for: {video_title[:40]}...")
    
    return {
        'title': video_title,
        'original_text': description,
        'summary': summary
    }

# ============================================
# TEST FUNCTION
# ============================================
if __name__ == "__main__":
    test_text = "This video explains how artificial intelligence works in simple terms for beginners. It covers machine learning basics and real-world applications."
    print("Testing summarizer...")
    result = summarize_text(test_text)
    print(f"Summary: {result}")