"""
╔══════════════════════════════════════════════════════════════════╗
║         Exam Samachar — Smart Hindi Newspaper Analyzer           ║
║         Powered by Groq Llama 4 Scout Vision (FREE & FAST)      ║
║         Upload newspaper image/PDF → Summary + MCQs + Study     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import io
import json
import time
import base64
import streamlit as st
from PIL import Image

# ─────────────────────────────────────────────────────────────────
# CONFIGURATION  —  only change GROQ_API_KEY
# ─────────────────────────────────────────────────────────────────
GROQ_API_KEY = "your api key here"
GROQ_MODEL   = "meta-llama/llama-4-scout-17b-16e-instruct"

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Exam Samachar",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS  —  Editorial Dark Ink Theme
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

/* ── KEYFRAMES ─────────────────────────────────────────────────── */
@keyframes fadeUp {
  from { opacity:0; transform:translateY(18px); }
  to   { opacity:1; transform:translateY(0); }
}
@keyframes inkDrop {
  0%   { clip-path: circle(0% at 50% 50%); opacity:0; }
  100% { clip-path: circle(150% at 50% 50%); opacity:1; }
}
@keyframes scanLine {
  from { transform: translateX(-100%); }
  to   { transform: translateX(100%); }
}
@keyframes pulseGlow {
  0%,100% { box-shadow: 0 0 0 0 rgba(255,200,50,0.0); }
  50%      { box-shadow: 0 0 0 6px rgba(255,200,50,0.15); }
}
@keyframes marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
@keyframes blink {
  0%,100% { opacity:1; } 50% { opacity:0; }
}
@keyframes stampIn {
  0%   { transform: rotate(-12deg) scale(1.3); opacity:0; }
  70%  { transform: rotate(2deg) scale(0.95); }
  100% { transform: rotate(-3deg) scale(1); opacity:1; }
}

/* ── ROOT VARS ─────────────────────────────────────────────────── */
:root {
  --ink:       #0f0d0a;
  --paper:     #faf7f2;
  --cream:     #f5ede0;
  --gold:      #c9901a;
  --gold-lt:   #f0c040;
  --red:       #c0392b;
  --teal:      #1a6b6b;
  --blue:      #1a3a6b;
  --muted:     #7a6f5e;
  --rule:      rgba(15,13,10,0.12);
  --card:      rgba(255,255,255,0.85);
  --study-bg:  #0d1b2a;
  --study-acc: #38bdf8;
}

/* ── GLOBAL ─────────────────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif !important;
  color: var(--ink) !important;
}
.stApp {
  background: var(--paper) !important;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 31px, rgba(15,13,10,0.04) 32px),
    repeating-linear-gradient(90deg, transparent, transparent 31px, rgba(15,13,10,0.02) 32px) !important;
}

/* ── MASTHEAD ────────────────────────────────────────────────────── */
.masthead {
  border-top: 4px solid var(--ink);
  border-bottom: 4px solid var(--ink);
  padding: 0.6rem 0 0.4rem;
  text-align: center;
  position: relative;
  margin-bottom: 0;
  animation: fadeUp 0.6s ease both;
}
.masthead::before {
  content: '';
  position: absolute;
  top: 6px; left: 0; right: 0;
  height: 1px;
  background: var(--ink);
}
.masthead::after {
  content: '';
  position: absolute;
  bottom: 6px; left: 0; right: 0;
  height: 1px;
  background: var(--ink);
}
.masthead-title {
  font-family: 'Playfair Display', serif;
  font-size: 4.2rem;
  font-weight: 900;
  letter-spacing: -2px;
  color: var(--ink);
  line-height: 1;
  margin: 0.3rem 0 0;
}
.masthead-sub {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.7rem;
  letter-spacing: 5px;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 0.2rem;
  font-weight: 500;
}
.masthead-rule {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
  margin: 0.25rem 0;
}
.masthead-rule span {
  height: 1px;
  width: 80px;
  background: var(--ink);
  display: inline-block;
}

/* ── TICKER BAR ──────────────────────────────────────────────────── */
.ticker-wrap {
  background: var(--ink);
  color: var(--gold-lt);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  letter-spacing: 1.5px;
  padding: 5px 0;
  overflow: hidden;
  white-space: nowrap;
  margin-bottom: 1.2rem;
}
.ticker-inner {
  display: inline-block;
  animation: marquee 25s linear infinite;
}
.ticker-inner span { margin: 0 2.5rem; }

/* ── SECTION HEADS ───────────────────────────────────────────────── */
.sec-head {
  font-family: 'Playfair Display', serif;
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--ink);
  border-bottom: 2px solid var(--ink);
  padding-bottom: 0.3rem;
  margin: 1.8rem 0 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  animation: fadeUp 0.4s ease both;
}
.sec-head .kicker {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: white;
  background: var(--ink);
  padding: 2px 7px;
  border-radius: 2px;
}
.sec-head .kicker.gold-kicker  { background: var(--gold); }
.sec-head .kicker.red-kicker   { background: var(--red); }
.sec-head .kicker.teal-kicker  { background: var(--teal); }
.sec-head .kicker.blue-kicker  { background: var(--blue); }

/* ── NEWS CARD ───────────────────────────────────────────────────── */
.news-card {
  background: white;
  border: 1.5px solid rgba(15,13,10,0.1);
  border-radius: 4px;
  padding: 1.5rem 1.8rem;
  margin: 0.8rem 0;
  position: relative;
  box-shadow: 3px 3px 0 rgba(15,13,10,0.06);
  animation: fadeUp 0.5s ease both;
}
.edition-stamp {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.64rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: white;
  background: var(--ink);
  display: inline-block;
  padding: 2px 10px;
  margin-bottom: 0.8rem;
  border-radius: 1px;
}
.headline-text {
  font-family: 'Playfair Display', serif;
  font-size: 1.7rem;
  font-weight: 900;
  line-height: 1.2;
  color: var(--ink);
  margin-bottom: 0.8rem;
  border-bottom: 1.5px solid var(--rule);
  padding-bottom: 0.7rem;
}
.summary-text {
  font-family: 'Crimson Pro', serif;
  font-size: 1.08rem;
  line-height: 1.85;
  color: #3a3228;
  padding: 0.7rem 1rem;
  border-left: 3px solid var(--gold);
  background: rgba(201,144,26,0.04);
  border-radius: 0 4px 4px 0;
}

/* ── METRICS ─────────────────────────────────────────────────────── */
.metric-strip {
  display: flex;
  gap: 1rem;
  margin: 1rem 0 1.5rem;
  flex-wrap: wrap;
}
.metric-box {
  flex: 1;
  min-width: 110px;
  border: 1.5px solid var(--ink);
  padding: 0.8rem 1rem;
  text-align: center;
  position: relative;
  background: white;
  box-shadow: 3px 3px 0 rgba(15,13,10,0.08);
  animation: fadeUp 0.4s ease both;
  transition: transform 0.15s ease;
}
.metric-box:hover { transform: translate(-2px,-2px); box-shadow: 5px 5px 0 rgba(15,13,10,0.1); }
.metric-box .val {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: 900;
  color: var(--ink);
  line-height: 1;
}
.metric-box .lbl {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.58rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--muted);
  margin-top: 4px;
}
.metric-box.gold-box { border-color: var(--gold); background: rgba(201,144,26,0.06); }
.metric-box.red-box  { border-color: var(--red);  background: rgba(192,57,43,0.05); }
.metric-box.teal-box { border-color: var(--teal); background: rgba(26,107,107,0.05); }
.metric-box.blue-box { border-color: var(--blue); background: rgba(26,58,107,0.05); }

/* ── FACT CARDS ──────────────────────────────────────────────────── */
.fact-card {
  border: 1px solid rgba(15,13,10,0.1);
  background: white;
  padding: 0.65rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.9rem;
  line-height: 1.55;
  border-left: 3px solid var(--teal);
  border-radius: 0 4px 4px 0;
  animation: fadeUp 0.3s ease both;
  transition: all 0.15s ease;
}
.fact-card:hover { transform: translateX(4px); border-left-color: var(--gold); }

/* ── ENTITY TAGS ─────────────────────────────────────────────────── */
.entity-group { margin: 0.6rem 0; }
.entity-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: var(--muted);
  display: block;
  margin-bottom: 4px;
}
.e-tag {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 2px;
  margin: 3px 3px;
  border: 1px solid transparent;
  font-family: 'DM Sans', sans-serif;
  transition: transform 0.1s ease;
}
.e-tag:hover { transform: scale(1.05); }
.e-person { background: rgba(26,58,107,0.1); color: var(--blue); border-color: rgba(26,58,107,0.2); }
.e-place  { background: rgba(26,107,107,0.1); color: var(--teal); border-color: rgba(26,107,107,0.2); }
.e-org    { background: rgba(192,57,43,0.1); color: var(--red); border-color: rgba(192,57,43,0.2); }
.e-scheme { background: rgba(201,144,26,0.12); color: var(--gold); border-color: rgba(201,144,26,0.25); }
.e-topic  { background: rgba(15,13,10,0.07); color: var(--ink); border-color: rgba(15,13,10,0.12); }
.e-stat   { background: rgba(100,30,120,0.1); color: #6b21a8; border-color: rgba(100,30,120,0.2); }

/* ── RELEVANCE BOX ───────────────────────────────────────────────── */
.relevance-box {
  border: 1.5px solid var(--teal);
  background: rgba(26,107,107,0.05);
  padding: 0.9rem 1.2rem;
  border-radius: 4px;
  font-family: 'Crimson Pro', serif;
  font-size: 1.02rem;
  color: #134040;
  line-height: 1.7;
  margin: 0.8rem 0;
}

/* ── MCQ CARDS ───────────────────────────────────────────────────── */
.mcq-card {
  background: white;
  border: 1.5px solid rgba(15,13,10,0.1);
  border-radius: 4px;
  padding: 1.3rem 1.5rem 1.1rem;
  margin: 0.9rem 0;
  position: relative;
  overflow: hidden;
  box-shadow: 2px 2px 0 rgba(15,13,10,0.05);
  animation: fadeUp 0.4s ease both;
  transition: box-shadow 0.2s ease;
}
.mcq-card:hover { box-shadow: 4px 4px 0 rgba(15,13,10,0.1); }
.mcq-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 3px;
  background: var(--ink);
}
.mcq-num {
  font-family: 'Playfair Display', serif;
  font-size: 3rem;
  font-weight: 900;
  color: rgba(15,13,10,0.07);
  position: absolute;
  top: 0.1rem; right: 1rem;
  line-height: 1;
  pointer-events: none;
}
.topic-pill {
  float: right;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  background: var(--ink);
  color: white;
  padding: 2px 8px;
  border-radius: 2px;
  margin-bottom: 0.5rem;
}
.mcq-q {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.97rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 0.9rem;
  padding-right: 3rem;
  line-height: 1.5;
}
.opt {
  padding: 0.4rem 0.85rem;
  margin: 0.22rem 0;
  border-radius: 3px;
  font-size: 0.9rem;
  border: 1.5px solid transparent;
  transition: all 0.12s ease;
  font-weight: 500;
}
.opt.correct {
  background: rgba(26,107,107,0.1);
  border-color: rgba(26,107,107,0.4);
  color: #0f4040;
  font-weight: 700;
}
.opt.wrong {
  background: rgba(15,13,10,0.03);
  color: rgba(15,13,10,0.38);
  border-color: rgba(15,13,10,0.07);
}
.explain-box {
  background: rgba(201,144,26,0.08);
  border-left: 3px solid var(--gold);
  border-radius: 0 3px 3px 0;
  padding: 0.65rem 0.9rem;
  margin-top: 0.8rem;
  font-size: 0.87rem;
  color: #5a3e0a;
  line-height: 1.6;
  font-family: 'Crimson Pro', serif;
  font-size: 0.97rem;
}

/* ── STUDY PANEL (dark) ──────────────────────────────────────────── */
.study-panel {
  background: var(--study-bg);
  border-radius: 6px;
  padding: 1.5rem 1.8rem;
  margin: 0.6rem 0;
  position: relative;
  overflow: hidden;
  animation: fadeUp 0.5s ease both;
  border: 1px solid rgba(56,189,248,0.15);
}
.study-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--study-acc), #818cf8, #f472b6);
}
.study-panel-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--study-acc);
  margin-bottom: 1rem;
}
.study-topic-card {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(56,189,248,0.15);
  border-radius: 4px;
  padding: 1rem 1.2rem;
  margin: 0.6rem 0;
  transition: all 0.15s ease;
}
.study-topic-card:hover {
  background: rgba(56,189,248,0.07);
  border-color: rgba(56,189,248,0.3);
  transform: translateX(3px);
}
.stc-name {
  font-family: 'DM Sans', sans-serif;
  font-size: 0.97rem;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 0.35rem;
}
.stc-chapters {
  font-size: 0.82rem;
  color: rgba(226,232,240,0.6);
  margin: 0.3rem 0;
  font-family: 'Crimson Pro', serif;
  font-size: 0.9rem;
  line-height: 1.5;
}
.stc-why {
  font-size: 0.78rem;
  color: var(--study-acc);
  margin-top: 0.3rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  letter-spacing: 0.5px;
}
.stc-books {
  margin-top: 0.5rem;
}
.book-tag {
  display: inline-block;
  font-size: 0.72rem;
  background: rgba(56,189,248,0.12);
  color: var(--study-acc);
  border: 1px solid rgba(56,189,248,0.25);
  padding: 2px 8px;
  border-radius: 2px;
  margin: 2px 3px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
}
.pyq-hint {
  background: rgba(248,113,113,0.08);
  border: 1px solid rgba(248,113,113,0.2);
  border-radius: 3px;
  padding: 0.5rem 0.8rem;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: #fca5a5;
  font-family: 'DM Sans', sans-serif;
  line-height: 1.5;
}
.study-summary-box {
  background: rgba(56,189,248,0.06);
  border: 1px solid rgba(56,189,248,0.2);
  border-radius: 4px;
  padding: 0.8rem 1.1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #bae6fd;
  line-height: 1.65;
  font-family: 'DM Sans', sans-serif;
}

/* ── INFO CARDS (homepage) ───────────────────────────────────────── */
.info-card {
  background: white;
  border: 1.5px solid rgba(15,13,10,0.1);
  border-radius: 4px;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.2s ease;
  box-shadow: 3px 3px 0 rgba(15,13,10,0.06);
  animation: fadeUp 0.5s ease both;
}
.info-card:hover { transform: translate(-2px,-2px); box-shadow: 5px 5px 0 rgba(15,13,10,0.1); }
.info-card .ic-icon { font-size:2.2rem; margin-bottom:0.6rem; }
.info-card .ic-head { font-family:'Playfair Display',serif; font-weight:700; font-size:1rem; color:var(--ink); margin-bottom:0.4rem; }
.info-card .ic-body { font-size:0.85rem; color:var(--muted); line-height:1.7; }

/* ── SIDEBAR ─────────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: #0f0d0a !important;
  border-right: 2px solid rgba(201,144,26,0.3) !important;
}
section[data-testid="stSidebar"] * { color: #d4c5a9 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #f0c040 !important; font-family: 'Playfair Display', serif !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stSelectSlider label {
  color: #a89070 !important;
  font-size: 0.72rem !important;
  letter-spacing: 2px !important;
  text-transform: uppercase !important;
  font-weight: 600 !important;
  font-family: 'JetBrains Mono', monospace !important;
}

/* ── UPLOAD ZONE ─────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
  border-radius: 4px !important;
  border: 2px dashed rgba(15,13,10,0.2) !important;
  background: rgba(255,255,255,0.6) !important;
}

/* ── DIVIDER ─────────────────────────────────────────────────────── */
.ink-divider {
  border: none;
  height: 1px;
  background: var(--ink);
  margin: 2rem 0;
  opacity: 0.12;
}

/* ── BUTTON ──────────────────────────────────────────────────────── */
.stButton>button[kind="primary"] {
  background: var(--ink) !important;
  color: white !important;
  border: none !important;
  border-radius: 3px !important;
  font-family: 'JetBrains Mono', monospace !important;
  letter-spacing: 2px !important;
  font-size: 0.8rem !important;
  text-transform: uppercase !important;
  padding: 0.6rem 1.5rem !important;
  transition: all 0.15s ease !important;
}
.stButton>button[kind="primary"]:hover {
  background: var(--gold) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(201,144,26,0.3) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# GROQ SETUP
# ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_groq_client():
    try:
        from groq import Groq
        return Groq(api_key=GROQ_API_KEY)
    except ImportError:
        return None


# ─────────────────────────────────────────────────────────────────
# IMAGE HELPER
# ─────────────────────────────────────────────────────────────────
def prepare_image(img: Image.Image, max_px: int) -> Image.Image:
    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")
    img.thumbnail((max_px, max_px), Image.LANCZOS)
    return img


# ─────────────────────────────────────────────────────────────────
# ULTRA-OPTIMIZED PROMPT  (with Study Guide output)
# ─────────────────────────────────────────────────────────────────
def build_prompt(language: str, exam_type: str, num_mcqs: int, difficulty: str) -> str:
    lang_instruction = {
        "Hindi":              "Respond ENTIRELY in Hindi (Devanagari script). All text including questions, options, explanations must be in Hindi.",
        "English":            "Respond ENTIRELY in English.",
        "Both (Hindi + English)": "Provide headline and summary in Hindi. Provide MCQ questions, explanations and study guide in English.",
    }.get(language, "Respond in English.")

    difficulty_guide = {
        "Easy":   "beginner-level, direct recall questions with obvious distractors",
        "Medium": "application-level, require context and moderate general knowledge",
        "Hard":   "analytical, multi-concept, confusing distractors, requires strong GK",
    }.get(difficulty, "medium difficulty")

    return f"""You are a MASTER newspaper analyst and {exam_type} competitive exam specialist with 20+ years of experience. You have set questions for UPSC, SSC CGL, IBPS PO, RRB NTPC, and State PSC exams.

TASK: Deeply analyze this newspaper image. Extract ALL visible text, headlines, dates, names, places, statistics, schemes, policies, appointments, sports results, awards, international news, science/tech news, economic data, and any other exam-relevant facts.

LANGUAGE: {lang_instruction}

CRITICAL OUTPUT RULES:
1. Output ONLY a single valid JSON object — NO markdown, NO backticks, NO prose outside JSON.
2. Every string field must be a non-empty string; every list field must be a list (use [] if nothing found).
3. JSON must parse cleanly with Python's json.loads().

EXAM CONTEXT:
- Target Exam: {exam_type}
- MCQ Count: {num_mcqs}
- MCQ Difficulty: {difficulty_guide}

MCQ RULES:
- Each question MUST be 100% based on visible facts in the newspaper image
- Wrong options (distractors) must be plausible, realistic, and related to the topic
- Correct answer must be unambiguously proven by the newspaper
- Questions should test: dates, names, statistics, places, organizations, schemes, policies, appointments, awards
- Vary question types: "Who", "What", "Where", "When", "Which", "How much/many"
- Never repeat similar questions

STUDY GUIDE RULES (most important new feature):
For each MCQ topic, provide deep study guidance so the student can prepare the FULL CHAPTER and related theory, not just this one news item. Think like a teacher mentoring a student: "This news is from this chapter → here is what you should read → here are likely related exam questions."
- suggest_topics: list of broader textbook/syllabus topics this news connects to
- Each topic must include: topic name, relevant chapters/sections to read, recommended standard books, why this is important for the target exam, and likely PYQ (Previous Year Question) style hints

OUTPUT JSON STRUCTURE (follow EXACTLY — every key is mandatory):
{{
  "newspaper_name": "name or empty string",
  "headline": "single most important headline",
  "date": "date visible in paper or empty string",
  "edition": "city edition or empty string",
  "summary": "comprehensive 4-5 sentence summary of ALL major news on this page",
  "entities": {{
    "people": ["full name 1", "full name 2"],
    "locations": ["place1", "place2"],
    "organizations": ["org1", "org2"],
    "schemes": ["scheme1"],
    "topics": ["topic1", "topic2"],
    "numbers_stats": ["₹X crore for Y", "Z% increase in W"]
  }},
  "exam_based_mcqs": [
    {{
      "question": "Precise question text",
      "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
      "answer": "A",
      "explanation": "Explanation citing the specific newspaper fact, plus the broader context why this answer is correct and others are wrong.",
      "topic_tag": "Polity / Economy / Science / Geography / Current Affairs / History / Environment"
    }}
  ],
  "exam_relevance": "3-4 sentences on why this news matters for {exam_type}, which syllabus topics it touches, and what type of questions may appear.",
  "study_guide": {{
    "overview": "2-3 sentences: what this news is really about in the larger academic context, and why a serious aspirant must understand it deeply.",
    "suggest_topics": [
      {{
        "topic_name": "Name of the broader syllabus topic (e.g., 'Constitutional Amendments', 'RBI Monetary Policy', 'Space Missions')",
        "exam_subject": "Subject area: Polity / Economy / Geography / Science & Tech / Environment / History / International Relations / Current Affairs",
        "chapters_to_read": [
          "Chapter/Section 1 with book name (e.g., Chapter 12: Directive Principles — M. Laxmikanth)",
          "Chapter/Section 2"
        ],
        "recommended_books": ["Standard book 1 (short name)", "Standard book 2"],
        "why_important": "1-2 sentences: why this topic frequently appears in {exam_type} and what subtopics are commonly tested.",
        "pyq_hint": "Style/type of previous year questions asked from this topic. Example pattern: 'Consider the following statements about X... Which is/are correct?' or 'Match List I with List II'. Mention the exam year and approximate frequency if known.",
        "quick_revision_points": [
          "One-liner fact 1 the student should memorize",
          "One-liner fact 2",
          "One-liner fact 3"
        ]
      }}
    ]
  }}
}}"""


# ─────────────────────────────────────────────────────────────────
# CALL GROQ
# ─────────────────────────────────────────────────────────────────
def call_groq(img: Image.Image, prompt: str) -> tuple[str, float]:
    client = get_groq_client()
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    t0 = time.time()
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
                {"type": "text", "text": prompt},
            ],
        }],
        temperature=0.1,
        max_tokens=4096,
        top_p=0.8,
    )
    elapsed = round(time.time() - t0, 2)
    return response.choices[0].message.content, elapsed


# ─────────────────────────────────────────────────────────────────
# ANALYZE PAGE  (with retry + JSON repair)
# ─────────────────────────────────────────────────────────────────
def analyze_page(img, language, exam_type, max_px, num_mcqs, difficulty):
    warns, result, elapsed, raw = [], None, 0.0, ""
    prepared = prepare_image(img, max_px)
    warns.append(f"📐 Image: {prepared.size[0]}×{prepared.size[1]}px")
    prompt = build_prompt(language, exam_type, num_mcqs, difficulty)

    for attempt in range(1, 4):
        try:
            raw, elapsed = call_groq(prepared, prompt)
            if not raw.strip():
                warns.append(f"⚠ Attempt {attempt}: empty response.")
                time.sleep(2); continue

            clean = raw.strip()
            for fence in ["```json", "```JSON", "```"]:
                if clean.startswith(fence): clean = clean[len(fence):]; break
            if clean.endswith("```"): clean = clean[:-3]
            clean = clean.strip()

            try:
                result = json.loads(clean); break
            except json.JSONDecodeError:
                pass

            s, e = clean.find("{"), clean.rfind("}") + 1
            if s != -1 and e > s:
                try:
                    result = json.loads(clean[s:e])
                    warns.append("🔧 JSON auto-extracted.")
                    break
                except json.JSONDecodeError:
                    pass

            warns.append(f"⚠ Attempt {attempt}: JSON parse failed. Retrying...")
        except Exception as ex:
            warns.append(f"❌ Attempt {attempt}: {ex}")
        time.sleep(2)

    if result is None:
        result = {"_raw": raw}
    return result, elapsed, warns


# ─────────────────────────────────────────────────────────────────
# RENDER STUDY GUIDE
# ─────────────────────────────────────────────────────────────────
def render_study_guide(study_guide: dict, exam_type: str):
    if not study_guide:
        return

    overview = study_guide.get("overview", "")
    topics   = study_guide.get("suggest_topics", [])
    if not topics:
        return

    st.markdown('<div class="sec-head"><span class="kicker blue-kicker">📚 Study Guide</span> Further Exam Preparation</div>', unsafe_allow_html=True)

    panel_html = f'<div class="study-panel">'
    panel_html += f'<div class="study-panel-title">◈ AI-Powered Study Roadmap · {exam_type}</div>'
    if overview:
        panel_html += f'<div class="study-summary-box">🧠 {overview}</div>'

    for t in topics:
        name       = t.get("topic_name", "")
        subject    = t.get("exam_subject", "")
        chapters   = t.get("chapters_to_read", [])
        books      = t.get("recommended_books", [])
        why        = t.get("why_important", "")
        pyq        = t.get("pyq_hint", "")
        rev_pts    = t.get("quick_revision_points", [])

        chapters_str = "<br>".join([f"→ {c}" for c in chapters]) if chapters else ""
        books_html   = "".join([f'<span class="book-tag">📖 {b}</span>' for b in books])
        rev_html     = "".join([f'<div style="color:#a5f3fc;font-size:0.82rem;margin:2px 0;padding-left:0.6rem;border-left:2px solid rgba(56,189,248,0.3)">• {r}</div>' for r in rev_pts])

        panel_html += f"""
        <div class="study-topic-card">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:0.5rem;flex-wrap:wrap">
            <div class="stc-name">{name}</div>
            <span style="font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;background:rgba(255,255,255,0.08);color:#94a3b8;padding:2px 8px;border-radius:2px;font-family:'JetBrains Mono',monospace;white-space:nowrap">{subject}</span>
          </div>
          {"<div class='stc-chapters'>" + chapters_str + "</div>" if chapters_str else ""}
          {"<div class='stc-books'>" + books_html + "</div>" if books_html else ""}
          {"<div class='stc-why'>⚡ " + why + "</div>" if why else ""}
          {rev_html}
          {"<div class='pyq-hint'>🗂 PYQ Pattern: " + pyq + "</div>" if pyq else ""}
        </div>"""

    panel_html += '</div>'
    st.markdown(panel_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# RENDER RESULTS
# ─────────────────────────────────────────────────────────────────
def render_results(result, rt: float, warns: list, label: str = "", exam_type: str = "General Knowledge"):
    for w in warns:
        if w.startswith("📐"):   st.caption(w)
        elif w.startswith(("❌","⚠")): st.warning(w)
        elif w.startswith("🔧"): st.info(w)

    if not isinstance(result, dict) or "_raw" in result:
        st.error("⚠️ Model did not return valid JSON. Raw output below:")
        raw = result.get("_raw", str(result)) if isinstance(result, dict) else str(result)
        if raw:
            with st.expander("📄 Raw model output"):
                st.code(raw[:3000])
        return

    mcqs      = result.get("exam_based_mcqs", [])
    key_facts = result.get("key_facts", [])
    entities  = result.get("entities", {})
    all_ents  = sum(len(v) for v in entities.values() if isinstance(v, list))
    study_guide = result.get("study_guide", {})

    # ── Metrics strip ─────────────────────────────────────────────
    st.markdown(f"""
    <div class="metric-strip">
      <div class="metric-box gold-box"><div class="val">{rt}s</div><div class="lbl">⚡ Speed</div></div>
      <div class="metric-box"><div class="val">{len(mcqs)}</div><div class="lbl">📝 MCQs</div></div>
      <div class="metric-box red-box"><div class="val">{len(key_facts)}</div><div class="lbl">🔑 Facts</div></div>
      <div class="metric-box teal-box"><div class="val">{all_ents}</div><div class="lbl">🏷 Entities</div></div>
      <div class="metric-box blue-box"><div class="val">{len(study_guide.get("suggest_topics", []))}</div><div class="lbl">📚 Topics</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── News Summary ──────────────────────────────────────────────
    st.markdown('<div class="sec-head"><span class="kicker">📰 Dispatch</span> News Summary ' + label + '</div>', unsafe_allow_html=True)

    newspaper = result.get("newspaper_name", "")
    date      = result.get("date", "")
    edition   = result.get("edition", "")
    headline  = result.get("headline", "—")
    summary   = result.get("summary", "")

    meta_parts = [p for p in [newspaper, date, edition] if p]
    meta_str = "  ·  ".join(meta_parts) if meta_parts else ""

    st.markdown(f"""
    <div class="news-card">
      {"<div class='edition-stamp'>" + meta_str + "</div>" if meta_str else ""}
      <div class="headline-text">{headline}</div>
      <div class="summary-text">{summary}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key Facts ─────────────────────────────────────────────────
    if key_facts:
        st.markdown('<div class="sec-head"><span class="kicker gold-kicker">🔑 Facts</span> Key Takeaways</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, fact in enumerate(key_facts):
            with cols[i % 2]:
                st.markdown(f'<div class="fact-card">◈ {fact}</div>', unsafe_allow_html=True)

    # ── Entities ──────────────────────────────────────────────────
    tag_config = [
        ("people", "e-person", "👤 People"),
        ("locations", "e-place", "📍 Locations"),
        ("organizations", "e-org", "🏛 Organizations"),
        ("schemes", "e-scheme", "📌 Schemes"),
        ("topics", "e-topic", "🏷 Topics"),
        ("numbers_stats", "e-stat", "📊 Numbers"),
    ]
    tags_html = ""
    for key, cls, lbl in tag_config:
        vals = entities.get(key, [])
        if vals:
            tags_html += f'<div class="entity-group"><span class="entity-label">{lbl}</span>'
            for v in vals:
                tags_html += f'<span class="e-tag {cls}">{v}</span>'
            tags_html += '</div>'

    if tags_html:
        st.markdown('<div class="sec-head"><span class="kicker">🗂 Index</span> Entities & Tags</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="news-card">{tags_html}</div>', unsafe_allow_html=True)

    # ── Exam Relevance ────────────────────────────────────────────
    relevance = result.get("exam_relevance", "")
    if relevance:
        st.markdown(f'<div class="relevance-box"> <strong>Exam Angle:</strong> {relevance}</div>', unsafe_allow_html=True)

    # ── MCQs ──────────────────────────────────────────────────────
    if mcqs:
        st.markdown(f'<div class="sec-head"><span class="kicker red-kicker"> Practice</span> Exam MCQs {label}</div>', unsafe_allow_html=True)
        for idx, q in enumerate(mcqs, 1):
            question    = q.get("question", "")
            options     = q.get("options", [])
            answer      = q.get("answer", "").strip().upper()
            explanation = q.get("explanation", "")
            topic_tag   = q.get("topic_tag", "")

            opts_html = ""
            for opt in options:
                letter = opt.strip()[:1].upper() if opt else ""
                cls    = "correct" if letter == answer else "wrong"
                check  = "✓ " if letter == answer else ""
                opts_html += f'<div class="opt {cls}">{check}{opt}</div>'

            st.markdown(f"""
            <div class="mcq-card">
              <div class="mcq-num">{idx:02d}</div>
              {"<div class='topic-pill'>" + topic_tag + "</div>" if topic_tag else ""}
              <div class="mcq-q">Q{idx}. {question}</div>
              {opts_html}
              {"<div class='explain-box'> " + explanation + "</div>" if explanation else ""}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No MCQs generated. Try a clearer image or increase resolution.")

    # ── Study Guide ───────────────────────────────────────────────
    render_study_guide(study_guide, exam_type)


# ─────────────────────────────────────────────────────────────────
# MASTHEAD
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
  <div class="masthead-sub">Established  ·  Free · Fast · Vision AI</div>
  <div class="masthead-rule"><span></span>✦<span></span></div>
  <div class="masthead-title">Exam Samachar</div>
  <div class="masthead-rule"><span></span>✦<span></span></div>
  <div class="masthead-sub">Smart Newspaper Analyzer for Competitive Exams</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="ticker-wrap">
  <div class="ticker-inner">
    <span> Upload any newspaper page</span>
    <span> AI Study Guide with every analysis</span>
    <span> SSC · Banking · Railway · UPSC · State PSC</span>
    <span> Hindi & English Support</span>
    <span> Upload any newspaper page</span>
    <span> AI Study Guide with every analysis</span>
    <span> SSC · Banking · Railway · UPSC · State PSC</span>
    <span> Hindi & English Support</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Settings")
    st.divider()

    language = st.selectbox(
        " Output Language",
        ["Hindi", "English", "Both (Hindi + English)"],
        index=1,
    )
    exam_type = st.selectbox(
        " Exam Type",
        ["SSC CGL / CHSL", "Banking (IBPS / SBI / RBI)", "Railway (RRB NTPC / Group D)",
         "Defence (CDS / AFCAT / NDA)", "UPSC Prelims / Mains", "State PSC", "General Knowledge"],
    )
    num_mcqs = st.slider(" Number of MCQs", min_value=3, max_value=10, value=5)
    difficulty = st.select_slider(
        "🎚 Difficulty Level",
        options=["Easy", "Medium", "Hard"],
        value="Medium",
    )
    max_px = st.select_slider(
        "🖼 Image Resolution",
        options=[600, 800, 1000, 1200, 1600],
        value=1000,
        help="Higher = better OCR. 1000–1200 is ideal.",
    )

    st.divider()
    st.markdown("""
    <div style="font-size:0.73rem;line-height:1.9;background:rgba(201,144,26,0.1);border-radius:4px;padding:0.8rem 1rem;border:1px solid rgba(201,144,26,0.25)">
    🔑 <b style='color:#f0c040'>Free Groq API Key:</b><br>
    console.groq.com<br>
    → Sign up → API Keys → Create<br>
    → Paste in app.py line 19<br><br>
    ✦ Llama 4 Scout Vision<br>
    🆓 Free · Fast · Hindi-capable
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# API KEY CHECK
# ─────────────────────────────────────────────────────────────────
if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE":
    st.error("🔑 API Key Missing! Set your Groq API key in app.py line 19.")
    st.stop()


# ─────────────────────────────────────────────────────────────────
# UPLOAD AREA
# ─────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "📎 Upload Newspaper Page — JPG / PNG / PDF",
    type=["png", "jpg", "jpeg", "pdf"],
    help="Clear photos work best. PDFs are analyzed page by page.",
)

if not uploaded:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="info-card">
          <div class="ic-icon">📸</div>
          <div class="ic-head">Get Newspaper Image</div>
          <div class="ic-body">Take a clear photo of any newspaper, or visit epaper.bhaskar.com, select city & date, and save the page. Upload JPG, PNG, or PDF.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="info-card">
          <div class="ic-icon">⚡</div>
          <div class="ic-head">Speed & Quality Tips</div>
          <div class="ic-body">Use 1000–1200px resolution for best results. Well-lit, high-contrast photos give sharper MCQs. Analysis takes just 5–15 seconds.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="info-card">
          <div class="ic-icon">📚</div>
          <div class="ic-head">New: AI Study Guide</div>
          <div class="ic-body">Each analysis now includes a Study Roadmap — chapters to read, standard books, PYQ patterns, and quick revision points. Prepare smarter!</div>
        </div>""", unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────────────────────────
# PROCESS UPLOAD
# ─────────────────────────────────────────────────────────────────

# PDF
if uploaded.type == "application/pdf":
    try:
        import fitz
    except ImportError:
        st.error("PyMuPDF not installed. Run: `pip install pymupdf`")
        st.stop()

    doc   = fitz.open(stream=uploaded.read(), filetype="pdf")
    total = len(doc)
    st.info(f"📄 PDF has **{total}** page(s). Select pages to analyze:")
    pg_range = st.slider("Pages to analyze", min_value=1, max_value=total,
                         value=(1, min(2, total)))

    if st.button(" Analyze PDF Pages", type="primary", use_container_width=True):
        pages = list(range(pg_range[0] - 1, pg_range[1]))
        bar   = st.progress(0, text="Initializing...")
        for idx, i in enumerate(pages):
            bar.progress(int(idx / len(pages) * 100), text=f"Analyzing page {i+1} of {total}...")
            pix = doc[i].get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, caption=f"Page {i+1}", use_container_width=True)
            with col2:
                with st.spinner(f"Analyzing page {i+1}..."):
                    result, rt, warns = analyze_page(img, language, exam_type, max_px, num_mcqs, difficulty)
                render_results(result, rt, warns, label=f"(Page {i+1})", exam_type=exam_type)
            st.markdown('<hr class="ink-divider">', unsafe_allow_html=True)
        bar.progress(100, text=" Analysis complete!")

# Image
else:
    img = Image.open(uploaded)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(img, caption="Uploaded Newspaper", use_container_width=True)
        st.caption(f"Original: {img.size[0]}×{img.size[1]}px | Model input: {max_px}px")
    with col2:
        if st.button(" Analyze Newspaper", type="primary", use_container_width=True):
            with st.spinner("Reading your newspaper... (5–15 seconds)"):
                result, rt, warns = analyze_page(img, language, exam_type, max_px, num_mcqs, difficulty)
            render_results(result, rt, warns, exam_type=exam_type)

st.caption("📰 Exam Samachar · Groq Llama 4 Scout · Free & Fast · No GPU needed")