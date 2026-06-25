import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CallBreak AI Oracle",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Share+Tech+Mono&display=swap');

/* ── Root variables ── */
:root {
  --gold:   #FFD700;
  --red:    #FF3B5C;
  --cyan:   #00F5FF;
  --purple: #8B5CF6;
  --dark:   #0A0A1A;
  --card:   #111130;
  --border: rgba(255,215,0,0.25);
}

/* ── App background ── */
.stApp {
    background: radial-gradient(ellipse at 20% 50%, #0d0d2b 0%, #0A0A1A 60%, #050510 100%);
    color: #e0e0ff;
    font-family: 'Rajdhani', sans-serif;
}

/* ── Animated starfield ── */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 10% 15%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 45%, rgba(255,215,0,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 25%, rgba(0,245,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 60%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 10%, rgba(255,215,0,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 80%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1px 1px at 85% 35%, rgba(0,245,255,0.3) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0d0d2b 0%, #1a0a2e 30%, #0a1a2e 70%, #0d0d2b 100%);
    border: 1px solid var(--gold);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 30px;
    box-shadow: 0 0 60px rgba(255,215,0,0.15), 0 0 120px rgba(139,92,246,0.1), inset 0 0 60px rgba(0,0,0,0.5);
}

.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(255,215,0,0.03) 60deg, transparent 120deg, rgba(0,245,255,0.03) 180deg, transparent 240deg, rgba(139,92,246,0.03) 300deg, transparent 360deg);
    animation: rotate 20s linear infinite;
}

@keyframes rotate { to { transform: rotate(360deg); } }

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #FFD700, #FF3B5C, #00F5FF, #8B5CF6, #FFD700);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
    letter-spacing: 4px;
    position: relative;
    z-index: 1;
}

@keyframes shimmer { to { background-position: 300% center; } }

.hero-sub {
    font-family: 'Share Tech Mono', monospace;
    color: rgba(0,245,255,0.8);
    font-size: 1rem;
    letter-spacing: 6px;
    margin-top: 10px;
    position: relative;
    z-index: 1;
}

.hero-badges {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 20px;
    flex-wrap: wrap;
    position: relative;
    z-index: 1;
}

.badge {
    background: rgba(255,215,0,0.1);
    border: 1px solid rgba(255,215,0,0.4);
    border-radius: 20px;
    padding: 5px 15px;
    font-size: 0.75rem;
    font-family: 'Share Tech Mono', monospace;
    color: var(--gold);
    letter-spacing: 2px;
}

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 20px 0;
}

.metric-card {
    background: linear-gradient(135deg, #111130, #0d0d25);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
}

.metric-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 2.2rem;
    font-weight: 900;
    color: var(--gold);
}

.metric-label {
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: rgba(224,224,255,0.5);
    margin-top: 5px;
    text-transform: uppercase;
}

/* ── Prediction result box ── */
.pred-result {
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin: 20px 0;
}

.pred-result.win {
    background: linear-gradient(135deg, rgba(0,255,127,0.1), rgba(0,245,255,0.05));
    border: 2px solid rgba(0,255,127,0.5);
    box-shadow: 0 0 40px rgba(0,255,127,0.2);
}

.pred-result.lose {
    background: linear-gradient(135deg, rgba(255,59,92,0.1), rgba(139,92,246,0.05));
    border: 2px solid rgba(255,59,92,0.5);
    box-shadow: 0 0 40px rgba(255,59,92,0.2);
}

.pred-outcome {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    letter-spacing: 5px;
}

.win .pred-outcome { color: #00FF7F; }
.lose .pred-outcome { color: var(--red); }

.confidence-bar-bg {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 12px;
    margin: 15px 0 5px;
    overflow: hidden;
}

.confidence-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 1s ease;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    letter-spacing: 4px;
    color: var(--cyan);
    border-left: 3px solid var(--gold);
    padding-left: 15px;
    margin: 25px 0 15px;
    text-transform: uppercase;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080818 0%, #0d0d25 100%) !important;
    border-right: 1px solid rgba(255,215,0,0.2);
}

section[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Orbitron', monospace !important;
    color: var(--gold) !important;
    font-size: 0.8rem !important;
    letter-spacing: 3px !important;
}

/* ── Sliders & inputs ── */
.stSlider > div > div > div {
    background: linear-gradient(90deg, var(--purple), var(--cyan)) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a0a2e, #0a1a2e) !important;
    border: 1px solid var(--gold) !important;
    color: var(--gold) !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 3px !important;
    font-size: 0.75rem !important;
    border-radius: 10px !important;
    padding: 12px 30px !important;
    transition: all 0.3s !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(0,245,255,0.1)) !important;
    box-shadow: 0 0 20px rgba(255,215,0,0.4) !important;
    transform: translateY(-2px) !important;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(0,0,0,0.3) !important;
    border-radius: 10px !important;
    padding: 5px !important;
    gap: 5px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    color: rgba(224,224,255,0.5) !important;
    border-radius: 8px !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(255,215,0,0.2), rgba(139,92,246,0.2)) !important;
    color: var(--gold) !important;
}

/* ── Plotly chart background ── */
.js-plotly-plot .plotly .bg { fill: transparent !important; }

/* ── Card deck display ── */
.card-display {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    justify-content: center;
    padding: 10px;
}

.playing-card {
    width: 38px; height: 52px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: bold;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 2px 8px rgba(0,0,0,0.5);
    animation: cardFloat 3s ease-in-out infinite;
}

.card-spade { background: linear-gradient(135deg, #1a1a3e, #2a2a5e); color: #FFD700; }
.card-heart { background: linear-gradient(135deg, #3e1a1a, #5e2a2a); color: #FF6B8A; }
.card-diamond { background: linear-gradient(135deg, #1a2e3e, #2a3e5e); color: #00C8FF; }
.card-club  { background: linear-gradient(135deg, #1e3e1a, #2e5e2a); color: #00FF7F; }

@keyframes cardFloat {
    0%,100% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0A0A1A; }
::-webkit-scrollbar-thumb { background: linear-gradient(var(--gold), var(--purple)); border-radius: 3px; }

/* ── Dataframe ── */
.stDataFrame { border: 1px solid var(--border) !important; border-radius: 10px !important; }

/* ── Info/warning boxes ── */
.stAlert { border-radius: 10px !important; }

/* ── Number input ── */
.stNumberInput > label, .stSelectbox > label, .stSlider > label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    color: var(--cyan) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA & MODELS ────────────────────────────────────────────────────────
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_path(filename):
    return os.path.join(BASE_DIR, filename)

@st.cache_resource
def load_models():
    # Load XGBoost
    with open(get_path('best_xgboost_model.pkl'), 'rb') as f:
        xgb = pickle.load(f)

    # Load or auto-generate Logistic Regression
    lr_path = get_path('lr_model.pkl')
    if os.path.exists(lr_path):
        with open(lr_path, 'rb') as f:
            lr = pickle.load(f)
    else:
        # Auto-retrain if pkl missing
        from sklearn.linear_model import LogisticRegression
        _df = pd.read_csv(get_path('callbreak_prediction_dataset.csv'))
        _feats = ['game_id','round_number','player_position','num_spades_trump',
                  'num_hearts','num_diamonds','num_clubs','total_high_cards',
                  'trump_high_cards','hand_strength_score','longest_suit_length',
                  'void_suits','opponent_avg_bid','player_bid']
        lr = LogisticRegression(max_iter=1000)
        lr.fit(_df[_feats], _df['bid_success'])
        with open(lr_path, 'wb') as f:
            pickle.dump(lr, f)
    return xgb, lr

@st.cache_data
def load_data():
    return pd.read_csv(get_path('callbreak_prediction_dataset.csv'))

xgb_model, lr_model = load_models()
df = load_data()

FEATURES = ['game_id','round_number','player_position','num_spades_trump',
            'num_hearts','num_diamonds','num_clubs','total_high_cards',
            'trump_high_cards','hand_strength_score','longest_suit_length',
            'void_suits','opponent_avg_bid','player_bid']

# ─── HERO BANNER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">🃏 CALLBREAK AI ORACLE</div>
  <div class="hero-sub">◆ NEURAL BID PREDICTION ENGINE ◆ MACHINE LEARNING POWERED ◆</div>
  <div class="hero-badges">
    <span class="badge">⚡ XGBOOST ENGINE</span>
    <span class="badge">🧠 LOGISTIC REGRESSION</span>
    <span class="badge">📊 500 GAMES TRAINED</span>
    <span class="badge">🎯 97.6% ACCURACY</span>
    <span class="badge">♠ TRUMP ANALYSIS</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TOP METRICS ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
total = len(df)
wins = df['bid_success'].sum()
avg_score = df.loc[df['bid_success']==1,'round_score'].mean()
avg_bid = df['player_bid'].mean()

for col, val, label in zip(
    [col1, col2, col3, col4],
    [f"{total}", f"{wins/total*100:.1f}%", f"{avg_score:.1f}", f"{avg_bid:.2f}"],
    ["TOTAL GAMES", "WIN RATE", "AVG WIN SCORE", "AVG BID"]
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-value">{val}</div>
          <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔮 PREDICT", "📊 ANALYTICS", "🧠 MODEL INTEL", "🎮 SIMULATOR", "📁 DATASET"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PREDICT
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">⚙️ Configure Your Hand</div>', unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🃏 HAND SETUP")
        game_id         = st.number_input("Game ID",        1, 1000, 1)
        round_number    = st.slider("Round Number",          1, 10,   1)
        player_position = st.selectbox("Player Position",   [1, 2, 3, 4])
        st.markdown("### ♠ SUIT DISTRIBUTION")
        num_spades   = st.slider("♠ Spades (Trump)",  0, 13, 3)
        num_hearts   = st.slider("♥ Hearts",          0, 13, 3)
        num_diamonds = st.slider("♦ Diamonds",        0, 13, 4)
        num_clubs    = st.slider("♣ Clubs",           0, 13, 3)
        st.markdown("### 🎯 STRENGTH METRICS")
        total_high   = st.slider("High Cards (A,K,Q,J,10)", 0, 13, 4)
        trump_high   = st.slider("Trump High Cards",         0, 8,  2)
        hand_str     = st.slider("Hand Strength Score",      0, 50, 15)
        longest      = st.slider("Longest Suit Length",      1, 13, 5)
        void_suits   = st.slider("Void Suits",               0, 4,  0)
        opp_bid      = st.slider("Opponent Avg Bid",         1, 8,  3)
        player_bid   = st.slider("Your Bid",                 1, 8,  2)

        st.markdown("### 🤖 MODEL SELECT")
        model_choice = st.radio("Select Model", ["XGBoost ⚡", "Logistic Regression 📐"], label_visibility="collapsed")

    # Live card visualization
    st.markdown('<div class="section-header">🂠 Your Hand Visualization</div>', unsafe_allow_html=True)
    cards_html = '<div class="card-display">'
    suit_icons = {'spade': '♠', 'heart': '♥', 'diamond': '♦', 'club': '♣'}
    suit_counts = {'spade': num_spades, 'heart': num_hearts, 'diamond': num_diamonds, 'club': num_clubs}
    suit_classes = {'spade': 'card-spade', 'heart': 'card-heart', 'diamond': 'card-diamond', 'club': 'card-club'}
    for suit, count in suit_counts.items():
        for _ in range(min(count, 13)):
            cards_html += f'<div class="playing-card {suit_classes[suit]}" style="animation-delay:{np.random.uniform(0,2):.1f}s">{suit_icons[suit]}</div>'
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Suit radar chart
    col_a, col_b = st.columns([1, 1])
    with col_a:
        radar = go.Figure(go.Scatterpolar(
            r=[num_spades, num_hearts, num_diamonds, num_clubs, num_spades],
            theta=['♠ Spades','♥ Hearts','♦ Diamonds','♣ Clubs','♠ Spades'],
            fill='toself',
            fillcolor='rgba(139,92,246,0.3)',
            line=dict(color='#FFD700', width=2),
            marker=dict(size=8, color='#00F5FF')
        ))
        radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 13], gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='rgba(255,255,255,0.4)')),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#FFD700', size=14))
            ),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text="SUIT DISTRIBUTION RADAR", font=dict(family='Orbitron', color='#FFD700', size=12)),
            height=320, margin=dict(l=40, r=40, t=50, b=20)
        )
        st.plotly_chart(radar, width="stretch")

    with col_b:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=hand_str,
            delta={'reference': 20, 'increasing': {'color': '#00FF7F'}, 'decreasing': {'color': '#FF3B5C'}},
            gauge={
                'axis': {'range': [0, 50], 'tickcolor': '#FFD700'},
                'bar': {'color': '#FFD700'},
                'bgcolor': 'rgba(0,0,0,0)',
                'borderwidth': 1, 'bordercolor': 'rgba(255,215,0,0.3)',
                'steps': [
                    {'range': [0, 15], 'color': 'rgba(255,59,92,0.3)'},
                    {'range': [15, 30], 'color': 'rgba(255,215,0,0.2)'},
                    {'range': [30, 50], 'color': 'rgba(0,255,127,0.3)'}
                ],
                'threshold': {'line': {'color': '#00F5FF', 'width': 3}, 'thickness': 0.75, 'value': hand_str}
            },
            title={'text': "HAND STRENGTH", 'font': {'family': 'Orbitron', 'color': '#FFD700', 'size': 12}},
            number={'font': {'family': 'Orbitron', 'color': '#FFD700', 'size': 36}}
        ))
        gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=320, margin=dict(l=20, r=20, t=50, b=20),
            font=dict(color='#e0e0ff')
        )
        st.plotly_chart(gauge, width="stretch")

    # PREDICT button
    st.markdown('<div class="section-header">🔮 Oracle Prediction</div>', unsafe_allow_html=True)
    if st.button("⚡ SUMMON THE ORACLE ⚡"):
        input_data = pd.DataFrame([[game_id, round_number, player_position, num_spades,
                                     num_hearts, num_diamonds, num_clubs, total_high,
                                     trump_high, hand_str, longest, void_suits, opp_bid, player_bid]],
                                   columns=FEATURES)
        model = xgb_model if "XGBoost" in model_choice else lr_model
        pred = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0]
        conf = proba[pred] * 100
        win_prob = proba[1] * 100

        result_class = "win" if pred == 1 else "lose"
        outcome_text = "✅ BID SUCCESS" if pred == 1 else "❌ BID FAIL"
        bar_color = "linear-gradient(90deg,#00FF7F,#00C8FF)" if pred==1 else "linear-gradient(90deg,#FF3B5C,#8B5CF6)"

        st.markdown(f"""
        <div class="pred-result {result_class}">
          <div style="font-family:'Share Tech Mono';color:rgba(224,224,255,0.5);font-size:0.75rem;letter-spacing:4px;margin-bottom:10px;">ORACLE VERDICT</div>
          <div class="pred-outcome">{outcome_text}</div>
          <div style="margin:15px 0;font-family:'Orbitron';color:rgba(224,224,255,0.7);font-size:0.9rem;">
            WIN PROBABILITY: <span style="color:#FFD700">{win_prob:.1f}%</span> &nbsp;|&nbsp; CONFIDENCE: <span style="color:#00F5FF">{conf:.1f}%</span>
          </div>
          <div class="confidence-bar-bg">
            <div class="confidence-bar-fill" style="width:{win_prob}%;background:{bar_color};"></div>
          </div>
          <div style="font-family:'Share Tech Mono';color:rgba(224,224,255,0.4);font-size:0.65rem;letter-spacing:2px;margin-top:5px;">
            MODEL: {"XGBOOST ⚡" if "XGBoost" in model_choice else "LOGISTIC REGRESSION 📐"}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Probability breakdown
        prob_fig = go.Figure()
        prob_fig.add_trace(go.Bar(
            x=['BID FAIL', 'BID SUCCESS'], y=[proba[0]*100, proba[1]*100],
            marker=dict(color=['#FF3B5C','#00FF7F'],
                        line=dict(color=['rgba(255,59,92,0.5)','rgba(0,255,127,0.5)'], width=1)),
            text=[f'{proba[0]*100:.1f}%', f'{proba[1]*100:.1f}%'],
            textposition='outside', textfont=dict(family='Orbitron', color='#FFD700', size=14)
        ))
        prob_fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
            xaxis=dict(tickfont=dict(family='Orbitron', color='#00F5FF')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.4)')),
            title=dict(text='PROBABILITY DISTRIBUTION', font=dict(family='Orbitron', color='#FFD700', size=13)),
            height=280, margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(prob_fig, width="stretch")

        # Feature importance (XGB only)
        if "XGBoost" in model_choice and hasattr(xgb_model, 'feature_importances_'):
            imp = pd.DataFrame({'Feature': FEATURES, 'Importance': xgb_model.feature_importances_}).sort_values('Importance')
            fi_fig = go.Figure(go.Bar(
                x=imp['Importance'], y=imp['Feature'], orientation='h',
                marker=dict(
                    color=imp['Importance'],
                    colorscale=[[0,'#8B5CF6'],[0.5,'#FFD700'],[1,'#00F5FF']],
                    line=dict(color='rgba(255,255,255,0.1)', width=1)
                ),
                text=[f'{v:.3f}' for v in imp['Importance']],
                textposition='outside', textfont=dict(family='Share Tech Mono', color='#FFD700', size=10)
            ))
            fi_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
                xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.4)')),
                yaxis=dict(tickfont=dict(family='Share Tech Mono', color='#00F5FF', size=10)),
                title=dict(text='FEATURE IMPORTANCE (XGBoost)', font=dict(family='Orbitron', color='#FFD700', size=13)),
                height=420, margin=dict(l=160, r=60, t=50, b=20)
            )
            st.plotly_chart(fi_fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">📊 Dataset Analytics Dashboard</div>', unsafe_allow_html=True)

    # Row 1: Score distribution + Win rate by bid
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[df['bid_success']==1]['round_score'],
            name='WIN', nbinsx=20,
            marker=dict(color='rgba(0,255,127,0.7)', line=dict(color='#00FF7F',width=1))
        ))
        fig.add_trace(go.Histogram(
            x=df[df['bid_success']==0]['round_score'],
            name='LOSE', nbinsx=20,
            marker=dict(color='rgba(255,59,92,0.7)', line=dict(color='#FF3B5C',width=1))
        ))
        fig.update_layout(
            barmode='overlay',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
            title=dict(text='SCORE DISTRIBUTION BY OUTCOME', font=dict(family='Orbitron',color='#FFD700',size=12)),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.5)')),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.5)')),
            legend=dict(font=dict(family='Share Tech Mono', color='#e0e0ff')),
            height=320
        )
        st.plotly_chart(fig, width="stretch")

    with c2:
        wr = df.groupby('player_bid')['bid_success'].mean().reset_index()
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=wr['player_bid'], y=wr['bid_success']*100,
            marker=dict(
                color=wr['bid_success']*100,
                colorscale=[[0,'#FF3B5C'],[0.5,'#FFD700'],[1,'#00FF7F']],
                line=dict(color='rgba(255,255,255,0.1)',width=1)
            ),
            text=[f'{v:.0f}%' for v in wr['bid_success']*100],
            textposition='outside', textfont=dict(family='Orbitron',color='#FFD700',size=11)
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
            title=dict(text='WIN RATE BY BID VALUE', font=dict(family='Orbitron',color='#FFD700',size=12)),
            xaxis=dict(title=dict(text='BID',font=dict(color='#00F5FF')),
                       tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)'),
            yaxis=dict(title=dict(text='WIN %',font=dict(color='#00F5FF')),
                       tickfont=dict(color='rgba(255,255,255,0.5)'), gridcolor='rgba(255,255,255,0.05)'),
            height=320
        )
        st.plotly_chart(fig2, width="stretch")

    # Row 2: 3D scatter
    st.markdown('<div class="section-header">🌐 3D Feature Space</div>', unsafe_allow_html=True)
    fig3d = go.Figure(data=go.Scatter3d(
        x=df['hand_strength_score'],
        y=df['num_spades_trump'],
        z=df['total_high_cards'],
        mode='markers',
        marker=dict(
            size=4,
            color=df['bid_success'],
            colorscale=[[0,'#FF3B5C'],[1,'#00FF7F']],
            opacity=0.8,
            line=dict(width=0),
            colorbar=dict(title=dict(text='WIN', font=dict(color='#FFD700')),
                         tickfont=dict(color='#e0e0ff'))
        ),
        text=[f"Score:{s} Spades:{sp} High:{h} {'✅WIN' if w else '❌LOSE'}"
              for s,sp,h,w in zip(df['hand_strength_score'],df['num_spades_trump'],df['total_high_cards'],df['bid_success'])],
        hovertemplate='%{text}<extra></extra>'
    ))
    fig3d.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        scene=dict(
            bgcolor='rgba(10,10,26,0.8)',
            xaxis=dict(title=dict(text='HAND STRENGTH', font=dict(color='#FFD700',family='Orbitron',size=10)),
                       gridcolor='rgba(255,215,0,0.1)', tickfont=dict(color='rgba(255,255,255,0.5)')),
            yaxis=dict(title=dict(text='SPADES (TRUMP)', font=dict(color='#00F5FF',family='Orbitron',size=10)),
                       gridcolor='rgba(0,245,255,0.1)', tickfont=dict(color='rgba(255,255,255,0.5)')),
            zaxis=dict(title=dict(text='HIGH CARDS', font=dict(color='#8B5CF6',family='Orbitron',size=10)),
                       gridcolor='rgba(139,92,246,0.1)', tickfont=dict(color='rgba(255,255,255,0.5)'))
        ),
        title=dict(text='3D FEATURE SPACE: HAND STRENGTH vs SPADES vs HIGH CARDS',
                   font=dict(family='Orbitron',color='#FFD700',size=13)),
        height=520, margin=dict(l=0,r=0,t=50,b=0)
    )
    st.plotly_chart(fig3d, width="stretch")

    # Row 3: Heatmap correlation
    c3, c4 = st.columns(2)
    with c3:
        corr_cols = ['num_spades_trump','total_high_cards','trump_high_cards',
                     'hand_strength_score','player_bid','tricks_won','bid_success','round_score']
        corr = df[corr_cols].corr()
        heat = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.columns,
            colorscale=[[0,'#FF3B5C'],[0.5,'#0A0A1A'],[1,'#00FF7F']],
            zmid=0, text=np.round(corr.values,2), texttemplate='%{text}',
            textfont=dict(size=9, family='Share Tech Mono'),
            colorbar=dict(tickfont=dict(color='#e0e0ff'))
        ))
        heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            title=dict(text='CORRELATION MATRIX', font=dict(family='Orbitron',color='#FFD700',size=12)),
            xaxis=dict(tickfont=dict(family='Share Tech Mono',color='#00F5FF',size=9)),
            yaxis=dict(tickfont=dict(family='Share Tech Mono',color='#00F5FF',size=9)),
            height=400
        )
        st.plotly_chart(heat, width="stretch")

    with c4:
        wr2 = df.groupby('round_number')['bid_success'].agg(['mean','count']).reset_index()
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=wr2['round_number'], y=wr2['mean']*100,
            mode='lines+markers',
            line=dict(color='#FFD700', width=3),
            marker=dict(size=10, color='#00F5FF',
                        line=dict(color='#FFD700', width=2)),
            fill='tozeroy', fillcolor='rgba(255,215,0,0.05)',
            name='WIN RATE %'
        ))
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
            title=dict(text='WIN RATE BY ROUND', font=dict(family='Orbitron',color='#FFD700',size=12)),
            xaxis=dict(title='Round', gridcolor='rgba(255,255,255,0.05)',
                       tickfont=dict(color='rgba(255,255,255,0.5)')),
            yaxis=dict(title='Win %', gridcolor='rgba(255,255,255,0.05)',
                       tickfont=dict(color='rgba(255,255,255,0.5)')),
            height=400
        )
        st.plotly_chart(fig_line, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MODEL INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">🧠 Model Intelligence Report</div>', unsafe_allow_html=True)

    from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
    X = df[FEATURES]
    y = df['bid_success']

    c1, c2 = st.columns(2)
    for col, model, name, color in zip([c1,c2],[xgb_model,lr_model],['XGBoost ⚡','Logistic Regression 📐'],['#FFD700','#00F5FF']):
        with col:
            preds = model.predict(X)
            probs = model.predict_proba(X)[:,1]
            acc = (preds == y).mean()
            fpr, tpr, _ = roc_curve(y, probs)
            roc_auc = auc(fpr, tpr)
            cm = confusion_matrix(y, preds)

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#111130,#0d0d25);border:1px solid {color};border-radius:15px;padding:20px;margin-bottom:15px;">
              <div style="font-family:'Orbitron';color:{color};font-size:1rem;letter-spacing:3px;margin-bottom:15px;">{name}</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:10px;padding:15px;">
                  <div style="font-family:'Orbitron';font-size:1.8rem;color:{color}">{acc*100:.1f}%</div>
                  <div style="font-size:0.65rem;letter-spacing:2px;color:rgba(224,224,255,0.5)">ACCURACY</div>
                </div>
                <div style="text-align:center;background:rgba(0,0,0,0.3);border-radius:10px;padding:15px;">
                  <div style="font-family:'Orbitron';font-size:1.8rem;color:{color}">{roc_auc:.3f}</div>
                  <div style="font-size:0.65rem;letter-spacing:2px;color:rgba(224,224,255,0.5)">ROC AUC</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ROC
            roc_fig = go.Figure()
            roc_fig.add_trace(go.Scatter(x=fpr, y=tpr, fill='tozeroy',
                fillcolor=f'rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.15)',
                line=dict(color=color, width=2), name=f'AUC={roc_auc:.3f}'))
            roc_fig.add_trace(go.Scatter(x=[0,1], y=[0,1], line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dash'), showlegend=False))
            roc_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
                title=dict(text='ROC CURVE', font=dict(family='Orbitron',color=color,size=11)),
                xaxis=dict(title='FPR', gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.4)')),
                yaxis=dict(title='TPR', gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='rgba(255,255,255,0.4)')),
                legend=dict(font=dict(family='Share Tech Mono',color='#e0e0ff')),
                height=280, margin=dict(l=40,r=20,t=40,b=40)
            )
            st.plotly_chart(roc_fig, width="stretch")

            # Confusion Matrix
            cm_fig = go.Figure(go.Heatmap(
                z=cm, x=['PRED FAIL','PRED WIN'], y=['ACTUAL FAIL','ACTUAL WIN'],
                colorscale=[[0,'#0A0A1A'],[0.5,color.replace('#','rgba(').replace('FFD700','255,215,0,')+'0.3)' if color=='#FFD700' else f'rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.3)'],[1,color]],
                text=cm, texttemplate='%{text}',
                textfont=dict(size=20, family='Orbitron', color='white')
            ))
            cm_fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                title=dict(text='CONFUSION MATRIX', font=dict(family='Orbitron',color=color,size=11)),
                xaxis=dict(tickfont=dict(family='Share Tech Mono',color='#00F5FF',size=9)),
                yaxis=dict(tickfont=dict(family='Share Tech Mono',color='#00F5FF',size=9)),
                height=260, margin=dict(l=80,r=20,t=40,b=40)
            )
            st.plotly_chart(cm_fig, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">🎮 Monte Carlo Battle Simulator</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:rgba(139,92,246,0.1);border:1px solid rgba(139,92,246,0.3);border-radius:12px;padding:15px;margin-bottom:20px;font-family:'Share Tech Mono';color:rgba(224,224,255,0.7);font-size:0.8rem;letter-spacing:1px;">
    🎲 Simulate N random hands and see how the AI oracle performs across the entire distribution.
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2 = st.columns([1, 2])
    with sc1:
        n_sim = st.slider("Number of Simulations", 50, 500, 200, 50)
        sim_model_choice = st.radio("Model", ["XGBoost ⚡", "Logistic Regression 📐"], key='sim_model')
        run_sim = st.button("🚀 LAUNCH SIMULATION")

    if run_sim:
        sim_model = xgb_model if "XGBoost" in sim_model_choice else lr_model
        np.random.seed(42)
        sim_results = []
        for i in range(n_sim):
            row = {
                'game_id': i+1,
                'round_number': np.random.randint(1,11),
                'player_position': np.random.randint(1,5),
                'num_spades_trump': np.random.randint(0,8),
                'num_hearts': np.random.randint(0,7),
                'num_diamonds': np.random.randint(0,7),
                'num_clubs': np.random.randint(0,7),
                'total_high_cards': np.random.randint(0,9),
                'trump_high_cards': np.random.randint(0,5),
                'hand_strength_score': np.random.randint(0,40),
                'longest_suit_length': np.random.randint(3,10),
                'void_suits': np.random.randint(0,3),
                'opponent_avg_bid': np.random.randint(1,7),
                'player_bid': np.random.randint(1,6)
            }
            sim_results.append(row)

        sim_df = pd.DataFrame(sim_results)
        preds = sim_model.predict(sim_df[FEATURES])
        probs = sim_model.predict_proba(sim_df[FEATURES])[:,1]
        sim_df['prediction'] = preds
        sim_df['win_prob'] = probs

        with sc2:
            win_count = preds.sum()
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:20px;">
              <div class="metric-card">
                <div class="metric-value">{n_sim}</div><div class="metric-label">SIMULATED</div>
              </div>
              <div class="metric-card">
                <div class="metric-value" style="color:#00FF7F">{win_count}</div><div class="metric-label">PREDICTED WINS</div>
              </div>
              <div class="metric-card">
                <div class="metric-value">{win_count/n_sim*100:.1f}%</div><div class="metric-label">WIN RATE</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Win probability distribution
        prob_hist = go.Figure()
        prob_hist.add_trace(go.Histogram(
            x=probs, nbinsx=30,
            marker=dict(
                color=probs,
                colorscale=[[0,'#FF3B5C'],[0.5,'#FFD700'],[1,'#00FF7F']],
                line=dict(color='rgba(0,0,0,0.3)',width=1)
            ),
            opacity=0.9
        ))
        prob_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
            title=dict(text='WIN PROBABILITY DISTRIBUTION ACROSS SIMULATIONS',font=dict(family='Orbitron',color='#FFD700',size=12)),
            xaxis=dict(title='Win Probability',gridcolor='rgba(255,255,255,0.05)',tickfont=dict(color='rgba(255,255,255,0.5)')),
            yaxis=dict(title='Count',gridcolor='rgba(255,255,255,0.05)',tickfont=dict(color='rgba(255,255,255,0.5)')),
            height=320
        )
        st.plotly_chart(prob_hist, width="stretch")

        # Scatter: hand strength vs prob
        scatter = go.Figure(go.Scatter(
            x=sim_df['hand_strength_score'], y=sim_df['win_prob']*100,
            mode='markers',
            marker=dict(
                size=8, color=sim_df['num_spades_trump'],
                colorscale=[[0,'#FF3B5C'],[0.5,'#8B5CF6'],[1,'#00F5FF']],
                showscale=True,
                colorbar=dict(title=dict(text='Spades',font=dict(color='#FFD700')),tickfont=dict(color='#e0e0ff')),
                opacity=0.8, line=dict(width=0)
            ),
            text=[f"Strength:{s} Spades:{sp} Prob:{p:.0f}%"
                  for s,sp,p in zip(sim_df['hand_strength_score'],sim_df['num_spades_trump'],sim_df['win_prob']*100)],
            hovertemplate='%{text}<extra></extra>'
        ))
        scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.3)',
            title=dict(text='HAND STRENGTH vs WIN PROBABILITY (colored by Spades)',font=dict(family='Orbitron',color='#FFD700',size=11)),
            xaxis=dict(title='Hand Strength',gridcolor='rgba(255,255,255,0.05)',tickfont=dict(color='rgba(255,255,255,0.5)')),
            yaxis=dict(title='Win Probability %',gridcolor='rgba(255,255,255,0.05)',tickfont=dict(color='rgba(255,255,255,0.5)')),
            height=360
        )
        st.plotly_chart(scatter, width="stretch")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — DATASET
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">📁 Raw Dataset Explorer</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        success_filter = st.selectbox("Bid Outcome", ["All", "Win ✅", "Lose ❌"])
    with col_f2:
        bid_filter = st.multiselect("Player Bid", sorted(df['player_bid'].unique()), default=sorted(df['player_bid'].unique()))
    with col_f3:
        round_filter = st.slider("Round Range", 1, 10, (1, 10))

    filtered = df.copy()
    if success_filter == "Win ✅": filtered = filtered[filtered['bid_success']==1]
    elif success_filter == "Lose ❌": filtered = filtered[filtered['bid_success']==0]
    if bid_filter: filtered = filtered[filtered['player_bid'].isin(bid_filter)]
    filtered = filtered[(filtered['round_number']>=round_filter[0]) & (filtered['round_number']<=round_filter[1])]

    st.markdown(f"""
    <div style="font-family:'Share Tech Mono';color:#00F5FF;font-size:0.8rem;letter-spacing:2px;margin-bottom:10px;">
    🔍 SHOWING {len(filtered)} / {len(df)} RECORDS
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        filtered.style.background_gradient(subset=['hand_strength_score'], cmap='YlOrRd')
                      .background_gradient(subset=['round_score'], cmap='RdYlGn'),
        width="stretch", height=400
    )

    csv_out = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ EXPORT FILTERED DATA", csv_out, "callbreak_filtered.csv", "text/csv")

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:30px;margin-top:30px;border-top:1px solid rgba(255,215,0,0.15);">
  <div style="font-family:'Orbitron';color:rgba(255,215,0,0.4);font-size:0.65rem;letter-spacing:5px;">
    ♠ CALLBREAK AI ORACLE ♥ POWERED BY XGBOOST + LOGISTIC REGRESSION ♦ ML PREDICTION ENGINE ♣
  </div>
</div>
""", unsafe_allow_html=True)