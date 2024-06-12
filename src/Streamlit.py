import streamlit as st
import altair as alt
import numpy as np
import pandas as pd

# Set page config
st.set_page_config(page_title="Are You Ready for Retirement?", page_icon="💰", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
        }
        .subtitle {
            font-size: 20px;
            margin-top: -10px;
            color: #555;
        }
        .section-header {
            font-size: 30px;
            margin-top: 20px;
            margin-bottom: 10px;
            color: #4CAF50;
        }
        .input-container, .score-container, .suggestions-container {
            background-color: #333;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .stButton>button {
            color: white;
            background: #4CAF50;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">Welcome to the Retirement Readiness Estimator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Let\'s find out if your actual retirement age matches your ideal.</div>', unsafe_allow_html=True)
st.write("---")

# Input section
st.markdown('<div class="section-header">Input Your Information</div>', unsafe_allow_html=True)
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Present Age", min_value=0, max_value=100, value=30)
        housing_type = st.selectbox("Current Housing Type", [
            "2-room", "3-room", "4-room", "5-room", "Executive HDB", 
            "Executive condominium", "Terrace", "Semi-detached house", 
            "Bungalow", "Others"
        ])
    with col2:
        QOL = st.slider("Rate Your Quality of Life (1-10)", 0, 10, 5)
        # Display feedback based on Quality of Life rating
        if QOL >= 7:
            st.write("You're living life!")
        elif QOL >= 5:
            st.write("Life can be better")
        else:
            st.write("Life is not looking good, we will try our best to help")
        income = st.number_input("Yearly Income", min_value=0, value=50000)
        expenditure = st.number_input("Yearly Expenditure", min_value=0, value=30000)

 

# Calculation and scoring logic
if st.button("Calculate"):
    savings = income - expenditure
    if savings > 0:
        st.success(f"You are saving {savings} units per year.")
    else:
        st.error("Your yearly expenditure exceeds your yearly income. This will increase your retirement age")

    # Mock logic to calculate scales
    # Replace these with API calls to actual models
    qol_scale = QOL
    disaster_scale = min(10, max(0, (income - expenditure) / 5000))
    retirement_readiness = min(10, max(0, (income - expenditure) / 10000 + age / 10))

    # Display scores
    st.markdown('<div class="section-header">Your Scores</div>', unsafe_allow_html=True)
    st.markdown('<div class="score-container">', unsafe_allow_html=True)
    st.write(f"**Quality of Life:** {qol_scale}/10")
    st.write(f"**Disaster Preparedness:** {disaster_scale}/10")
    st.write(f"**Retirement Readiness:** {retirement_readiness}/10")
    st.markdown('</div>', unsafe_allow_html=True)

    # Suggestions to improve scores
    st.markdown('<div class="section-header">Suggestions to Improve Your Scores</div>', unsafe_allow_html=True)
    st.markdown('<div class="suggestions-container">', unsafe_allow_html=True)
    suggestions = []
    if qol_scale < 7:
        suggestions.append("- Improve your quality of life by engaging in activities you enjoy.")
    if disaster_scale < 7:
        suggestions.append("- Increase your savings to better prepare for unexpected expenses.")
    if retirement_readiness < 7:
        suggestions.append("- Try to reduce your expenditures or increase your income to save more for retirement.")
    if suggestions:
        for suggestion in suggestions:
            st.write(suggestion)
    else:
        st.write("Great job! You're on the right track.")
    st.markdown('</div>', unsafe_allow_html=True)

# Placeholder for potential CPF data integration
st.markdown('<div class="section-header">Future Enhancements</div>', unsafe_allow_html=True)
st.write("In the future, you will be able to get your CPF data from SingPass.")
