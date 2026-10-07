import streamlit as st
import pandas as pd
import joblib


# ==========================================
# PAGE CONFIGURATION (must be first st call)
# ==========================================

st.set_page_config(
    page_title="Churn Watch",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("Models/customer_churn_model.pkl")


model = load_model()


# ==========================================
# THEME / CSS
# ==========================================

INK = "#13203A"
PAPER = "#EEF2F7"
LOW = "#0E9F8E"
MID = "#F0A020"
HIGH = "#E5484D"

# --- What this model is about (edit these to match your training data) ---
SECTOR = "Telecommunications"
SECTOR_DETAIL = (
    "A subscription provider selling phone and home internet (DSL or fibre), "
    "with optional add-ons such as online security, tech support and streaming."
)
CHURN_MEANING = "A customer cancels their subscription and leaves the company."
# Share of customers in your training data who churned, in %.
# Check with: df["Churn"].eq("Yes").mean() * 100
BASE_CHURN_RATE = 26.5

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {{
    font-family: 'Figtree', sans-serif;
    color: {INK};
}}
/* Newer Streamlit paints its own background on inner containers, which
   covers .stApp, so set the page background on all of them */
.stApp,
[data-testid="stApp"],
[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(900px 400px at 100% -10%, #D8E4F5 0%, transparent 60%),
        {PAPER} !important;
}}
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"],
[data-testid="stBottom"] {{
    background: transparent !important;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2.2rem; max-width: 1250px; }}

/* ---------- header ---------- */
.hero h1 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    letter-spacing: -0.03em;
    line-height: 1.02;
    margin: 0 0 .5rem 0;
    color: {INK};
}}
.hero p {{
    font-size: 1.08rem;
    max-width: 38rem;
    color: #4A5A78;
    margin: 0;
}}
.hero .dot {{
    display:inline-block; width:.55em; height:.55em; border-radius:50%;
    background:{HIGH}; margin-right:.35em; vertical-align:.12em;
    box-shadow: 0 0 0 .22em rgba(229,72,77,.18);
}}

/* ---------- about strip ---------- */
.about {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
    margin: 1.6rem 0 .4rem;
}}
.about > div {{
    border-left: 3px solid {INK};
    padding-left: .9rem;
}}
.about h4 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1rem; font-weight: 700; margin: 0 0 .25rem;
}}
.about p {{ margin: 0; font-size: .92rem; color: #4A5A78; line-height: 1.45; }}
@media (max-width: 800px) {{ .about {{ grid-template-columns: 1fr; gap: 1rem; }} }}

/* ---------- form panel ---------- */
[data-testid="stForm"] {{
    background: #FFFFFF;
    border: 1px solid #D5DDEA;
    border-radius: 18px;
    padding: 1.4rem 1.6rem 1.6rem;
    box-shadow: 0 18px 40px -28px rgba(19,32,58,.45);
}}
[data-testid="stForm"] label p {{
    font-weight: 600;
    font-size: .86rem;
    color: #3B4A68;
}}
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
[data-testid="stNumberInput"] input {{
    border-radius: 10px !important;
    background: #F6F8FC !important;
    border-color: #DCE3EF !important;
}}
/* keep typed/selected values readable even when Streamlit is in dark mode */
div[data-baseweb="select"] *,
div[data-baseweb="input"] input,
[data-testid="stNumberInput"] input {{
    color: {INK} !important;
    -webkit-text-fill-color: {INK} !important;
}}
div[data-baseweb="select"] svg {{ fill: {INK} !important; }}
[data-testid="stNumberInput"] button {{
    background: #E8EDF5 !important;
    color: {INK} !important;
}}
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {{ color: #6A7893; }}

/* ---------- tabs ---------- */
/* No .stTabs prefix: newer Streamlit versions changed that wrapper,
   so target the tab buttons directly */
[data-baseweb="tab-list"] {{
    gap: 6px;
    border-bottom: 1px solid #E3E9F3;
}}
button[data-baseweb="tab"],
[data-testid="stTab"] {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    padding: .6rem 1rem;
    border-radius: 10px 10px 0 0;
    background: transparent !important;
    opacity: 1 !important;
}}
button[data-baseweb="tab"] *,
[data-testid="stTab"] * {{
    color: #5B6785 !important;
    -webkit-text-fill-color: #5B6785 !important;
    opacity: 1 !important;
}}
button[data-baseweb="tab"]:hover *,
button[data-baseweb="tab"][aria-selected="true"] *,
[data-testid="stTab"]:hover *,
[data-testid="stTab"][aria-selected="true"] * {{
    color: {INK} !important;
    -webkit-text-fill-color: {INK} !important;
}}
[data-baseweb="tab-highlight"] {{ background: {INK} !important; height: 3px; }}

/* ---------- submit button ---------- */
[data-testid="stFormSubmitButton"] button {{
    width: 100%;
    background: {INK};
    color: #fff;
    border: none;
    border-radius: 12px;
    padding: .85rem 1rem;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    transition: transform .15s ease, background .15s ease;
}}
[data-testid="stFormSubmitButton"] button:hover {{
    background: #22345C; color:#fff; transform: translateY(-1px);
}}
[data-testid="stFormSubmitButton"] button:focus-visible {{
    outline: 3px solid {MID}; outline-offset: 2px;
}}

/* ---------- result panel ---------- */
.result {{
    border-radius: 22px;
    padding: 1.6rem 1.6rem 1.4rem;
    color: #fff;
    position: sticky; top: 1rem;
}}
.result.idle {{ background: #fff; color: {INK}; border: 1.5px dashed #BFCBDF; }}
.result.low  {{ background: linear-gradient(160deg, #0B7F72, {LOW}); }}
.result.mid  {{ background: linear-gradient(160deg, #C9800F, {MID}); color:#2A1A00; }}
.result.high {{ background: linear-gradient(160deg, #B8282D, {HIGH}); }}
.result h2 {{
    font-family:'Bricolage Grotesque',sans-serif; font-weight:800;
    font-size:1.7rem; letter-spacing:-0.02em; margin:.2rem 0 .1rem;
}}
.result .sub {{ opacity:.9; font-size:.98rem; margin:0 0 .8rem; }}
.gauge {{ width:100%; max-width:300px; display:block; margin:0 auto; }}
.gauge .pct {{
    font-family:'Bricolage Grotesque',sans-serif; font-weight:800; font-size:40px;
}}
.gauge .cap {{ font-size:11px; opacity:.85; }}
.drivers {{ margin-top:1rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,.35); }}
.result.mid .drivers {{ border-top-color: rgba(42,26,0,.25); }}
.drivers h4 {{
    font-family:'Bricolage Grotesque',sans-serif; font-size:1rem; margin:0 0 .5rem;
}}
.drivers ul {{ margin:0; padding-left:1.1rem; }}
.drivers li {{ margin:.28rem 0; font-size:.93rem; }}
.idle-title {{
    font-family:'Bricolage Grotesque',sans-serif; font-weight:700; font-size:1.3rem;
}}
.idle p {{ color:#5A6985; margin:.4rem 0 0; }}

@media (prefers-reduced-motion: reduce) {{
    * {{ transition: none !important; animation: none !important; }}
}}
</style>
""",
    unsafe_allow_html=True,
)


def html(markup: str) -> None:
    """Render HTML without markdown treating indented lines as code."""
    cleaned = "\n".join(line.strip() for line in markup.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

html(
    """
<div class="hero">
<h1><span class="dot"></span>Churn Watch</h1>
<p>Describe a customer and see how likely they are to leave, plus the
details in their account that deserve a closer look.</p>
</div>
"""
)

html(
    f"""
<div class="about">
<div>
<h4>Sector: {SECTOR}</h4>
<p>{SECTOR_DETAIL}</p>
</div>
<div>
<h4>What churn means here</h4>
<p>{CHURN_MEANING}</p>
</div>
<div>
<h4>How to read the result</h4>
<p>The percentage is the model's estimated chance that this customer leaves.
In the training data, about {BASE_CHURN_RATE:.1f}% of customers churned.</p>
</div>
</div>
"""
)

st.write("")

left, right = st.columns([3, 2], gap="large")


# ==========================================
# INPUT FORM
# ==========================================

with left:
    with st.form("customer_form", border=False):
        tab_profile, tab_services, tab_billing = st.tabs(
            ["Profile", "Services", "Billing"]
        )

        with tab_profile:
            c1, c2 = st.columns(2)
            with c1:
                gender = st.selectbox("Gender", ["Male", "Female"])
                partner = st.selectbox("Has a partner", ["Yes", "No"])
                tenure = st.slider("Tenure (months)", 0, 72, 12)
            with c2:
                senior_citizen = st.selectbox(
                    "Senior citizen",
                    [0, 1],
                    format_func=lambda x: "Yes" if x == 1 else "No",
                )
                dependents = st.selectbox("Has dependents", ["Yes", "No"])

        with tab_services:
            c1, c2 = st.columns(2)
            with c1:
                phone_service = st.selectbox("Phone service", ["Yes", "No"])
                multiple_lines = st.selectbox(
                    "Multiple lines", ["Yes", "No", "No phone service"]
                )
                internet_service = st.selectbox(
                    "Internet service", ["DSL", "Fiber optic", "No"]
                )
                online_security = st.selectbox(
                    "Online security", ["Yes", "No", "No internet service"]
                )
                online_backup = st.selectbox(
                    "Online backup", ["Yes", "No", "No internet service"]
                )
            with c2:
                device_protection = st.selectbox(
                    "Device protection", ["Yes", "No", "No internet service"]
                )
                tech_support = st.selectbox(
                    "Tech support", ["Yes", "No", "No internet service"]
                )
                streaming_tv = st.selectbox(
                    "Streaming TV", ["Yes", "No", "No internet service"]
                )
                streaming_movies = st.selectbox(
                    "Streaming movies", ["Yes", "No", "No internet service"]
                )

        with tab_billing:
            c1, c2 = st.columns(2)
            with c1:
                contract = st.selectbox(
                    "Contract", ["Month-to-month", "One year", "Two year"]
                )
                paperless_billing = st.selectbox("Paperless billing", ["Yes", "No"])
                payment_method = st.selectbox(
                    "Payment method",
                    [
                        "Electronic check",
                        "Mailed check",
                        "Bank transfer (automatic)",
                        "Credit card (automatic)",
                    ],
                )
            with c2:
                monthly_charges = st.number_input(
                    "Monthly charges (£)", 0.0, 200.0, 70.0, step=0.5
                )
                total_charges = st.number_input(
                    "Total charges (£)", 0.0, 10000.0, 500.0, step=10.0
                )

        submitted = st.form_submit_button("Check churn risk")


# ==========================================
# RESULT PANEL
# ==========================================

def gauge_svg(p: float, color: str) -> str:
    """Semicircle gauge. Arc length = pi * r."""
    r = 90
    length = 3.14159265 * r
    offset = length * (1 - p)
    return f"""
<svg class="gauge" viewBox="0 0 220 135" role="img" aria-label="Churn probability {p*100:.0f} percent">
<path d="M 20 115 A 90 90 0 0 1 200 115" fill="none" stroke="rgba(255,255,255,.28)" stroke-width="16" stroke-linecap="round"/>
<path d="M 20 115 A 90 90 0 0 1 200 115" fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round" stroke-dasharray="{length:.1f}" stroke-dashoffset="{offset:.1f}"/>
<text x="110" y="98" text-anchor="middle" class="pct" fill="currentColor">{p*100:.0f}%</text>
<text x="110" y="118" text-anchor="middle" class="cap" fill="currentColor">chance of leaving</text>
</svg>
"""


def risk_notes(row: dict) -> list[str]:
    """Plain-language account details that tend to go with higher churn."""
    notes = []
    if row["Contract"] == "Month-to-month":
        notes.append("Month-to-month contract: nothing ties them in, so a 1-year offer could help.")
    if row["tenure"] <= 12:
        notes.append("Newer customer (12 months or less): the first year is when most people leave.")
    if row["InternetService"] == "Fiber optic" and row["TechSupport"] == "No":
        notes.append("Fibre without tech support: faults go unresolved, so consider a free support trial.")
    if row["OnlineSecurity"] == "No" and row["InternetService"] != "No":
        notes.append("No online security add-on: bundling it can add stickiness.")
    if row["PaymentMethod"] == "Electronic check":
        notes.append("Pays by electronic check: moving them to automatic payment may reduce friction.")
    if row["MonthlyCharges"] >= 90:
        notes.append("High monthly bill: check they are on the best-value plan.")
    return notes[:4]


with right:
    if not submitted:
        html(
            """
<div class="result idle">
<div class="idle-title">Risk reading appears here</div>
<p>Fill in the three tabs, then press <b>Check churn risk</b>.</p>
</div>
"""
        )
    else:
        customer = pd.DataFrame(
            {
                "gender": [gender],
                "SeniorCitizen": [senior_citizen],
                "Partner": [partner],
                "Dependents": [dependents],
                "tenure": [tenure],
                "PhoneService": [phone_service],
                "MultipleLines": [multiple_lines],
                "InternetService": [internet_service],
                "OnlineSecurity": [online_security],
                "OnlineBackup": [online_backup],
                "DeviceProtection": [device_protection],
                "TechSupport": [tech_support],
                "StreamingTV": [streaming_tv],
                "StreamingMovies": [streaming_movies],
                "Contract": [contract],
                "PaperlessBilling": [paperless_billing],
                "PaymentMethod": [payment_method],
                "MonthlyCharges": [monthly_charges],
                "TotalCharges": [total_charges],
            }
        )

        probability = float(model.predict_proba(customer)[0][1])
        prediction = int(model.predict(customer)[0])

        if prediction == 1 or probability >= 0.5:
            tier, title, line, color = (
                "high",
                "High churn risk",
                "This customer is likely to leave. A retention offer or a support call is worth making.",
                "#FFFFFF",
            )
        elif probability >= 0.3:
            tier, title, line, color = (
                "mid",
                "Moderate churn risk",
                "Not urgent, but worth keeping an eye on.",
                "#2A1A00",
            )
        else:
            tier, title, line, color = (
                "low",
                "Low churn risk",
                "This customer is likely to stay.",
                "#FFFFFF",
            )

        notes = risk_notes(customer.iloc[0].to_dict())
        notes_html = ""
        if notes and tier != "low":
            items = "".join(f"<li>{n}</li>" for n in notes)
            notes_html = f'<div class="drivers"><h4>Worth a closer look</h4><ul>{items}</ul></div>'

        html(
            f"""
<div class="result {tier}">
<h2>{title}</h2>
<p class="sub">{line}</p>
{gauge_svg(probability, color)}
<p class="sub" style="text-align:center;margin:.3rem 0 0;">Typical customer: {BASE_CHURN_RATE:.1f}%</p>
{notes_html}
</div>
"""
        )
