import streamlit as st


def _html(body: str) -> None:
    """Render raw HTML using st.html() (Streamlit ≥ 1.31) or st.markdown fallback."""
    if hasattr(st, "html"):
        st.html(body)
    else:
        st.markdown(body, unsafe_allow_html=True)


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="Premium BMI Calculator",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# PREMIUM CSS DESIGN
# --------------------------------------------------
st.markdown(
    """
    <style>

    /* ── Main background ── */
    .stApp {
        background:
            radial-gradient(circle at 10% 20%, rgba(14,165,233,0.28), transparent 30%),
            radial-gradient(circle at 90% 15%, rgba(168,85,247,0.26),  transparent 28%),
            radial-gradient(circle at 80% 90%, rgba(34,197,94,0.16),   transparent 25%),
            linear-gradient(135deg, #050b18 0%, #0b1530 48%, #111827 100%);
        color: #f8fafc;
        min-height: 100vh;
    }

    /* Subtle grid overlay */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
        background-size: 45px 45px;
        z-index: 0;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        position: relative;
        z-index: 2;
    }

    [data-testid="stHeader"] { background: transparent; }

    /* ── Floating orbs ── */
    .orb {
        position: fixed;
        border-radius: 50%;
        filter: blur(15px);
        opacity: 0.55;
        pointer-events: none;
        z-index: 1;
        animation: float 8s ease-in-out infinite;
    }
    .orb-one {
        width: 260px; height: 260px;
        top: 8%; left: -90px;
        background: rgba(14,165,233,0.28);
    }
    .orb-two {
        width: 320px; height: 320px;
        right: -130px; bottom: 5%;
        background: rgba(168,85,247,0.25);
        animation-delay: 2s;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50%       { transform: translateY(-25px); }
    }

    /* ── Hero ── */
    .hero {
        text-align: center;
        padding: 1.5rem 1rem 2rem 1rem;
    }
    .hero-badge {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 100px;
        border: 1px solid rgba(125,211,252,0.35);
        background: rgba(14,165,233,0.1);
        color: #bae6fd;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }
    .hero h1 {
        margin: 0;
        font-size: clamp(2.7rem, 7vw, 4.7rem);
        font-weight: 800;
        letter-spacing: -0.055em;
        line-height: 1.05;
        background: linear-gradient(90deg, #ffffff, #7dd3fc, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero p {
        color: #aab8ce;
        font-size: 17px;
        max-width: 600px;
        margin: 18px auto 0 auto;
        line-height: 1.7;
    }

    /* ── Unit toggle rail ── */
    .unit-rail-label {
        text-align: center;
        color: #4b5e77;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        margin-bottom: 10px;
    }

    /* Widget outer label ("Weight", "Height") */
    [data-testid="stRadio"] [data-testid="stWidgetLabel"] p {
        color: #5a6e89 !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 6px !important;
    }

    /* Radio option pill styling */
    div[role="radiogroup"] label {
        display: inline-flex !important;
        align-items: center;
        padding: 6px 16px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(148,163,184,0.18) !important;
        background: rgba(30,41,59,0.55) !important;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    div[role="radiogroup"] label:has(input:checked) {
        background: rgba(14,165,233,0.17) !important;
        border-color: rgba(56,189,248,0.5) !important;
    }
    div[role="radiogroup"] label:hover:not(:has(input:checked)) {
        background: rgba(30,41,59,0.8) !important;
        border-color: rgba(148,163,184,0.35) !important;
    }
    /* Hide the radio SVG circle indicator */
    div[role="radiogroup"] label svg { display: none !important; }
    /* Option text */
    div[role="radiogroup"] label p,
    div[role="radiogroup"] label div,
    div[role="radiogroup"] label span {
        color: #94a3b8 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    div[role="radiogroup"] label:has(input:checked) p,
    div[role="radiogroup"] label:has(input:checked) div,
    div[role="radiogroup"] label:has(input:checked) span {
        color: #7dd3fc !important;
    }

    /* ── Form glass card ── */
    [data-testid="stForm"] {
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(148,163,184,0.2);
        border-radius: 26px;
        padding: 28px 30px 30px 30px;
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        box-shadow:
            0 25px 70px rgba(0,0,0,0.38),
            inset 0 1px 0 rgba(255,255,255,0.06);
    }
    .form-heading {
        color: #f8fafc;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .form-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* Number input labels */
    .stNumberInput label p {
        color: #dbeafe !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* Number input fields — multiple selectors for cross-version coverage */
    div[data-baseweb="input"],
    [data-testid="stNumberInput"] div[data-baseweb="input"],
    [data-testid="stNumberInput"] div[data-baseweb="input"] > div,
    [data-testid="stNumberInput"] > div > div {
        background:       rgba(15, 23, 42, 0.90) !important;
        background-color: rgba(15, 23, 42, 0.90) !important;
        border: 1px solid rgba(100, 116, 139, 0.35) !important;
        border-radius: 13px !important;
        transition: all 0.25s ease;
    }
    div[data-baseweb="input"]:focus-within,
    [data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15) !important;
    }
    /* -webkit-text-fill-color overrides WebKit's own text colour for inputs */
    div[data-baseweb="input"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stNumberInput"] input[type="number"] {
        color:                   #e2e8f0 !important;
        -webkit-text-fill-color: #e2e8f0 !important;
        caret-color:             #7dd3fc !important;
        background:              transparent !important;
        background-color:        transparent !important;
        font-weight: 600 !important;
    }
    [data-testid="stNumberInput"] button {
        color: #7dd3fc !important;
    }

    /* Submit button */
    [data-testid="stFormSubmitButton"] button {
        min-height: 52px;
        border: none;
        border-radius: 14px;
        color: white;
        font-size: 16px;
        font-weight: 700;
        background: linear-gradient(90deg, #0284c7, #7c3aed);
        box-shadow: 0 12px 30px rgba(2,132,199,0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 16px 38px rgba(124,58,237,0.3);
    }
    [data-testid="stFormSubmitButton"] button:active { transform: translateY(0px); }

    /* ── Result card ── */
    .result-card {
        margin-top: 28px;
        padding: 28px;
        border-radius: 25px;
        background: linear-gradient(145deg, rgba(30,41,59,0.88), rgba(15,23,42,0.8));
        border: 1px solid rgba(148,163,184,0.18);
        backdrop-filter: blur(18px);
        box-shadow: 0 22px 55px rgba(0,0,0,0.3);
    }
    .result-label {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .bmi-number {
        color: #ffffff;
        font-size: 55px;
        line-height: 1.1;
        font-weight: 800;
        margin-top: 8px;
    }
    .category-pill {
        display: inline-block;
        margin-top: 14px;
        padding: 9px 16px;
        border-radius: 100px;
        font-weight: 700;
        font-size: 14px;
    }
    .result-message {
        margin-top: 18px;
        color: #bdc9dc;
        line-height: 1.65;
        font-size: 15px;
    }
    .result-meta {
        margin-top: 12px;
        color: #4b5e77;
        font-size: 13px;
        font-style: italic;
    }

    /* ── BMI gauge ── */
    .gauge-container { margin-top: 27px; }
    .gauge-track {
        height: 13px;
        border-radius: 100px;
        position: relative;
        background: linear-gradient(
            90deg,
            #facc15 0%,   #facc15 28.3%,
            #22c55e 28.3%, #22c55e 50%,
            #f97316 50%,  #f97316 66.7%,
            #ef4444 66.7%, #ef4444 100%
        );
    }
    .gauge-marker {
        position: absolute;
        top: 50%;
        width: 23px;
        height: 23px;
        border-radius: 50%;
        background: #ffffff;
        border: 4px solid #0f172a;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.3), 0 5px 14px rgba(0,0,0,0.4);
        transform: translate(-50%, -50%);
    }
    .gauge-labels {
        display: flex;
        justify-content: space-between;
        color: #7f8da3;
        font-size: 11px;
        margin-top: 10px;
    }

    /* ── BMI range guide ── */
    .range-title {
        text-align: center;
        color: #f8fafc;
        margin-top: 38px;
        margin-bottom: 18px;
        font-size: 20px;
        font-weight: 700;
    }
    .range-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
    }
    .range-item {
        background: rgba(15,23,42,0.6);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 16px;
        padding: 17px 12px;
        text-align: center;
        backdrop-filter: blur(12px);
    }
    .range-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-bottom: 9px;
    }
    .range-name  { color: #e2e8f0; font-weight: 700; font-size: 13px; }
    .range-value { color: #8391a7; font-size: 12px; margin-top: 4px; }

    .disclaimer {
        text-align: center;
        color: #748198;
        font-size: 12px;
        margin-top: 25px;
        line-height: 1.6;
    }

    /* ── Mobile ── */
    @media (max-width: 700px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; }
        .hero h1 { font-size: 2.8rem; }
        [data-testid="stForm"] { padding: 22px 18px; }
        .range-grid { grid-template-columns: repeat(2, 1fr); }
        .bmi-number { font-size: 45px; }
    }

    </style>
    """,
    unsafe_allow_html=True,
)

_html('<div class="orb orb-one"></div><div class="orb orb-two"></div>')


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
_html(
    """
    <div class="hero">
        <div class="hero-badge">Smart Health Tool</div>
        <h1>BMI Calculator</h1>
        <p>
            Calculate your Body Mass Index instantly &mdash; choose any unit
            combination that suits you.
        </p>
    </div>
    """
)


# --------------------------------------------------
# UNIT SELECTORS  (outside form → triggers reruns so
# the correct inputs render inside the form below)
# --------------------------------------------------
_html('<p class="unit-rail-label">Choose your preferred units</p>')

col_u1, col_u2 = st.columns([1, 2], gap="large")

with col_u1:
    weight_unit = st.radio(
        "Weight",
        options=["kg", "lb"],
        horizontal=True,
        key="weight_unit",
    )

with col_u2:
    height_unit = st.radio(
        "Height",
        options=["cm", "m", "ft & in"],
        horizontal=True,
        key="height_unit",
    )

st.write("")  # small spacer


# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------
with st.form("bmi_form"):

    _html(
        '<div class="form-heading">Your measurements</div>'
        '<div class="form-description">'
        'Enter your weight and height using the units you selected above.'
        '</div>'
    )

    col1, col2 = st.columns(2, gap="large")

    # ── Weight input ──────────────────────────────
    with col1:
        if weight_unit == "kg":
            weight_val = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=500.0,
                value=70.0,
                step=0.1,
                format="%.1f",
            )
            weight_kg = weight_val
        else:  # lb
            weight_val = st.number_input(
                "Weight (lb)",
                min_value=2.0,
                max_value=1100.0,
                value=154.3,
                step=0.1,
                format="%.1f",
            )
            weight_kg = weight_val * 0.453592

    # ── Height input ──────────────────────────────
    with col2:
        if height_unit == "cm":
            h_val = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=300.0,
                value=170.0,
                step=0.1,
                format="%.1f",
            )
            height_m = h_val / 100.0

        elif height_unit == "m":
            h_val = st.number_input(
                "Height (m)",
                min_value=0.50,
                max_value=3.00,
                value=1.70,
                step=0.01,
                format="%.2f",
            )
            height_m = h_val

        else:  # ft & in
            sub1, sub2 = st.columns(2)
            with sub1:
                feet_val = st.number_input(
                    "Feet",
                    min_value=1,
                    max_value=9,
                    value=5,
                    step=1,
                )
            with sub2:
                inches_val = st.number_input(
                    "Inches",
                    min_value=0.0,
                    max_value=11.9,
                    value=7.0,
                    step=1.0,
                    format="%.0f",
                )
            height_m = (feet_val * 12 + inches_val) * 0.0254

    submitted = st.form_submit_button(
        "Calculate my BMI",
        use_container_width=True,
    )


# --------------------------------------------------
# BMI CALCULATION AND RESULT
# --------------------------------------------------
if submitted:

    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category            = "Underweight"
        category_color      = "#facc15"
        category_background = "rgba(250,204,21,0.14)"
        message = "Your BMI is below the standard healthy-weight range used for adults."

    elif bmi < 25:
        category            = "Healthy Weight"
        category_color      = "#4ade80"
        category_background = "rgba(34,197,94,0.14)"
        message = "Your BMI falls within the standard healthy-weight range used for adults."

    elif bmi < 30:
        category            = "Overweight"
        category_color      = "#fb923c"
        category_background = "rgba(249,115,22,0.14)"
        message = "Your BMI is above the standard healthy-weight range used for adults."

    else:
        category            = "Obesity"
        category_color      = "#f87171"
        category_background = "rgba(239,68,68,0.14)"
        message = "Your BMI falls within the adult obesity category."

    # ── Build human-readable measurement summary ─
    if weight_unit == "lb":
        weight_display = f"{weight_val:.1f} lb  ({weight_kg:.1f} kg)"
    else:
        weight_display = f"{weight_val:.1f} kg"

    if height_unit == "ft & in":
        height_display = f"{int(feet_val)} ft {int(inches_val)} in  ({height_m:.2f} m)"
    elif height_unit == "cm":
        height_display = f"{h_val:.1f} cm"
    else:
        height_display = f"{h_val:.2f} m"

    # Gauge: visual scale BMI 10 → 40
    gauge_pos    = max(0.0, min(((bmi - 10) / 30) * 100, 100.0))
    border_color = category_color + "55"

    result_html = (
        '<div class="result-card">'
        '<div class="result-label">Your calculated BMI</div>'
        '<div class="bmi-number">' + f"{bmi:.2f}" + '</div>'
        '<div class="category-pill" style="'
            'color:' + category_color + ';'
            'background:' + category_background + ';'
            'border:1px solid ' + border_color + ';">'
            + category +
        '</div>'
        '<div class="result-message">' + message + '</div>'
        '<div class="result-meta">'
            'Weight: ' + weight_display +
            ' &nbsp;&nbsp;&middot;&nbsp;&nbsp; '
            'Height: ' + height_display +
        '</div>'
        '<div class="gauge-container">'
            '<div class="gauge-track">'
                '<div class="gauge-marker" style="left:' + f"{gauge_pos:.2f}" + '%"></div>'
            '</div>'
            '<div class="gauge-labels">'
                '<span>10</span><span>18.5</span><span>25</span>'
                '<span>30</span><span>40+</span>'
            '</div>'
        '</div>'
        '</div>'
    )

    _html(result_html)


# --------------------------------------------------
# BMI RANGE GUIDE
# --------------------------------------------------
_html(
    """
    <div class="range-title">Adult BMI category guide</div>

    <div class="range-grid">

        <div class="range-item">
            <span class="range-dot" style="background:#facc15;"></span>
            <div class="range-name">Underweight</div>
            <div class="range-value">Below 18.5</div>
        </div>

        <div class="range-item">
            <span class="range-dot" style="background:#22c55e;"></span>
            <div class="range-name">Healthy Weight</div>
            <div class="range-value">18.5 &ndash; 24.9</div>
        </div>

        <div class="range-item">
            <span class="range-dot" style="background:#f97316;"></span>
            <div class="range-name">Overweight</div>
            <div class="range-value">25.0 &ndash; 29.9</div>
        </div>

        <div class="range-item">
            <span class="range-dot" style="background:#ef4444;"></span>
            <div class="range-name">Obesity</div>
            <div class="range-value">30 or greater</div>
        </div>

    </div>

    <div class="disclaimer">
        This calculator is intended for educational purposes only.
        BMI is a screening measure and does not replace professional medical advice.
    </div>
    """
)
