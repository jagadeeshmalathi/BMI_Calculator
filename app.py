import streamlit as st

st.set_page_config(
    page_title="BMI Calculator",
    page_icon="⚖️",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #f5f7fb;
    }
    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        margin-bottom: 30px;
        font-size: 18px;
    }
    .result-box {
        padding: 20px;
        border-radius: 15px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        margin-top: 20px;
    }
    .bmi-value {
        font-size: 28px;
        font-weight: bold;
        color: #111827;
    }
    .category {
        font-size: 22px;
        font-weight: 600;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">⚖️ BMI Calculator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Check your Body Mass Index in a simple and clean way</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    weight = st.number_input(
        "Enter your weight (kg)",
        min_value=1.0,
        step=0.1
    )

with col2:
    height_cm = st.number_input(
        "Enter your height (cm)",
        min_value=1.0,
        step=0.1
    )

if st.button("Calculate BMI", use_container_width=True):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "orange"
        tip = "You may need to improve your nutrition and consult a health expert."
    elif bmi < 25:
        category = "Healthy Weight"
        color = "green"
        tip = "Great! You are in the healthy BMI range."
    elif bmi < 30:
        category = "Overweight"
        color = "darkorange"
        tip = "Try regular exercise and balanced food habits."
    else:
        category = "Obesity"
        color = "red"
        tip = "It may help to consult a doctor or fitness expert."

    st.markdown(f"""
        <div class="result-box">
            <div class="bmi-value">Your BMI: {bmi:.2f}</div>
            <div class="category" style="color:{color};">Category: {category}</div>
            <p>{tip}</p>
        </div>
    """, unsafe_allow_html=True)