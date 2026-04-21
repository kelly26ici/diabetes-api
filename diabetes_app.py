import streamlit as st
import requests
import json
import time

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DiabetesIQ · Risk Assessment",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #0a0e1a;
    color: #e8eaf0;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1100px; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #4fc3f7;
    margin-bottom: 1rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 3.4rem;
    line-height: 1.1;
    color: #ffffff;
    margin: 0 0 1rem 0;
}
.hero h1 em {
    font-style: italic;
    color: #4fc3f7;
}
.hero-sub {
    font-size: 1.05rem;
    color: #8892a4;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Section label ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4fc3f7;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.08);
}

/* ── Card ── */
.card {
    background: #111827;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
}

/* ── Sliders & inputs ── */
[data-testid="stSlider"] > div > div > div {
    background: #4fc3f7 !important;
}
[data-testid="stSlider"] label {
    font-size: 0.82rem !important;
    color: #8892a4 !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stNumberInput"] input {
    background: #1a2235 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #4fc3f7 0%, #0288d1 100%);
    color: #0a0e1a;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border: none;
    border-radius: 10px;
    padding: 0.85rem 2rem;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-top: 1rem;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(79,195,247,0.35);
}

/* ── Result cards ── */
.result-positive {
    background: linear-gradient(135deg, #1a1020 0%, #2d1a2e 100%);
    border: 1px solid rgba(239, 83, 80, 0.4);
    border-radius: 16px;
    padding: 2.2rem;
    text-align: center;
}
.result-negative {
    background: linear-gradient(135deg, #0d1a14 0%, #0a2218 100%);
    border: 1px solid rgba(38, 198, 128, 0.4);
    border-radius: 16px;
    padding: 2.2rem;
    text-align: center;
}
.result-icon {
    font-size: 3rem;
    margin-bottom: 0.6rem;
}
.result-label {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    margin: 0.3rem 0;
}
.result-positive .result-label { color: #ef5350; }
.result-negative .result-label { color: #26c680; }

.result-sub {
    font-size: 0.88rem;
    color: #8892a4;
    margin-top: 0.4rem;
}
.confidence-badge {
    display: inline-block;
    margin-top: 1rem;
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    padding: 0.35rem 1.1rem;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}
.result-positive .confidence-badge { color: #ef9a9a; }
.result-negative .confidence-badge { color: #80cbc4; }

/* ── Metric row ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-top: 1.2rem;
}
.metric-box {
    flex: 1;
    background: #0d1117;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #4fc3f7;
}
.metric-lbl {
    font-size: 0.72rem;
    color: #8892a4;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* ── API status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(38, 198, 128, 0.1);
    border: 1px solid rgba(38, 198, 128, 0.3);
    border-radius: 999px;
    padding: 0.25rem 0.85rem;
    font-size: 0.75rem;
    font-weight: 600;
    color: #26c680;
    letter-spacing: 0.06em;
}
.status-pill-err {
    background: rgba(239, 83, 80, 0.1);
    border-color: rgba(239, 83, 80, 0.3);
    color: #ef5350;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 2rem 0;
}

/* ── Disclaimer ── */
.disclaimer {
    font-size: 0.75rem;
    color: #4a5568;
    text-align: center;
    line-height: 1.7;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}
</style>
""", unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🩺 Clinical Decision Support</div>
    <h1>Diabetes <em>Risk</em> Assessment</h1>
    <p class="hero-sub">
        Enter patient clinical markers below. Our model will return an instant
        diabetes risk prediction backed by machine learning.
    </p>
</div>
""", unsafe_allow_html=True)

# ── API Config (sidebar) ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ API Configuration")
    api_url = st.text_input(
        "FastAPI Base URL",
        value="http://diabetes-api-bwxa.onrender.com/docs",
        help="The base URL where your FastAPI server is running."
    )
    st.markdown("---")
    st.markdown("**Endpoint**")
    st.code(f"{api_url}/diabetes_prediction", language="text")

    # Health check
    if st.button("Check API Health"):
        try:
            r = requests.get(f"{api_url}/health", timeout=3)
            if r.status_code == 200:
                st.success("✅ API is online")
            else:
                st.error(f"⚠️ Status {r.status_code}")
        except Exception:
            st.error("❌ Cannot reach API")

# ── Input Form ────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 0.9], gap="large")

with col_left:
    st.markdown('<div class="section-label">Patient Markers</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    pregnancies = st.slider("Pregnancies", 0, 20, 1,
        help="Number of times the patient has been pregnant.")
    glucose = st.slider("Glucose (mg/dL)", 0, 300, 120,
        help="Plasma glucose concentration (2-hour oral glucose tolerance test).")
    blood_pressure = st.slider("Blood Pressure (mm Hg)", 0, 200, 70,
        help="Diastolic blood pressure.")
    skin_thickness = st.slider("Skin Thickness (mm)", 0, 100, 20,
        help="Triceps skin fold thickness.")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Metabolic Indicators</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    insulin = st.slider("Insulin (mu U/ml)", 0, 900, 80,
        help="2-hour serum insulin.")
    bmi = st.slider("BMI", 0.0, 70.0, 28.5, step=0.1,
        help="Body Mass Index (weight in kg / height in m²).")
    dpf = st.slider("Diabetes Pedigree Function", 0.0, 3.0, 0.5, step=0.01,
        help="A function that scores likelihood of diabetes based on family history.")
    age = st.slider("Age (years)", 1, 120, 30)

    st.markdown('</div>', unsafe_allow_html=True)

    predict_btn = st.button("⚡ Run Prediction", use_container_width=True)

# ── Results Panel ─────────────────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="section-label">Result</div>', unsafe_allow_html=True)

    if not predict_btn:
        st.markdown("""
        <div class="card" style="text-align:center; padding: 3rem 2rem; color: #4a5568;">
            <div style="font-size:2.5rem; margin-bottom:1rem;">🔬</div>
            <div style="font-size:0.9rem; line-height:1.7;">
                Fill in the patient markers<br>and click <strong style="color:#8892a4;">Run Prediction</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        payload = {
            "pregnancies": pregnancies,
            "glucose": glucose,
            "blood_pressure": blood_pressure,
            "skin_thickness": skin_thickness,
            "insulin": insulin,
            "bmi": round(bmi, 1),
            "diabetes_pedigree_function": round(dpf, 2),
            "age": age,
        }

        with st.spinner("Analyzing..."):
            time.sleep(0.4)  # slight delay for UX polish
            try:
                response = requests.post(
                    f"{api_url}/diabetes_prediction",
                    json=payload,
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()

                pred = data.get("prediction")
                result = data.get("result", "Unknown")
                confidence = data.get("confidence")

                if pred == 1:
                    conf_text = f"Confidence: {confidence*100:.1f}%" if confidence else ""
                    st.markdown(f"""
                    <div class="result-positive">
                        <div class="result-icon">⚠️</div>
                        <div class="result-label">Diabetic</div>
                        <div class="result-sub">High risk indicated — clinical review recommended</div>
                        {f'<div class="confidence-badge">{conf_text}</div>' if conf_text else ""}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    conf_text = f"Confidence: {confidence*100:.1f}%" if confidence else ""
                    st.markdown(f"""
                    <div class="result-negative">
                        <div class="result-icon">✅</div>
                        <div class="result-label">Not Diabetic</div>
                        <div class="result-sub">Low risk indicated — routine monitoring advised</div>
                        {f'<div class="confidence-badge">{conf_text}</div>' if conf_text else ""}
                    </div>
                    """, unsafe_allow_html=True)

                # Metric summary
                st.markdown(f"""
                <div class="metric-row">
                    <div class="metric-box">
                        <div class="metric-val">{glucose}</div>
                        <div class="metric-lbl">Glucose</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-val">{bmi}</div>
                        <div class="metric-lbl">BMI</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-val">{age}</div>
                        <div class="metric-lbl">Age</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Raw JSON expander
                with st.expander("📦 Raw API Response"):
                    st.json(data)

                with st.expander("📤 Request Payload"):
                    st.json(payload)

            except requests.exceptions.ConnectionError:
                st.markdown("""
                <div class="card" style="border-color:rgba(239,83,80,0.3);">
                    <strong style="color:#ef5350;">❌ Connection Failed</strong><br>
                    <span style="color:#8892a4; font-size:0.85rem;">
                    Make sure your FastAPI server is running.<br>
                    Check the API URL in the sidebar.
                    </span>
                </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.HTTPError as e:
                st.markdown(f"""
                <div class="card" style="border-color:rgba(239,83,80,0.3);">
                    <strong style="color:#ef5350;">⚠️ API Error {response.status_code}</strong><br>
                    <span style="color:#8892a4; font-size:0.85rem;">{str(e)}</span>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"""
                <div class="card" style="border-color:rgba(239,83,80,0.3);">
                    <strong style="color:#ef5350;">🔥 Unexpected Error</strong><br>
                    <span style="color:#8892a4; font-size:0.85rem;">{str(e)}</span>
                </div>
                """, unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
    ⚕️ <strong>Medical Disclaimer</strong> — This tool is intended for research and educational purposes only.<br>
    It is not a substitute for professional medical advice, diagnosis, or treatment.<br>
    Always consult a qualified healthcare provider for clinical decisions.
</div>
""", unsafe_allow_html=True)