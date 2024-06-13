import streamlit as st
import streamlit_authenticator as stauth
import altair as alt
import numpy as np
import pandas as pd
import yaml
from yaml.loader import SafeLoader

from helper import get_user_data
from helper import getLobang
from helper import getInfo
from helper import make_donut

st.set_page_config(page_title="Are You Ready for Retirement?", page_icon="💰", layout="wide")

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'])

authenticator.login(fields={'Form name':'Singpass Login'})

if st.session_state["authentication_status"]:
    # Set page config
    name = st.session_state["name"]
    st.sidebar.write(f'Welcome *{name}*')
    st.sidebar.write("## How to Use:")
    st.sidebar.markdown("1. Check the details")
    st.sidebar.markdown("2. View your Lobang&sup3; score")
    st.sidebar.markdown("3. See which areas are lacking")
    st.sidebar.markdown("4. View the suggestions")
    authenticator.logout(location="sidebar")
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
            section[data-testid="stSidebar"] {
                width: 300px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    #connect to sql database and get user data

    USER_DATA = get_user_data(name)
    print(USER_DATA)

    # Input section
    with st.container():
        col1, col2, col3 = st.columns((2, 4.2, 2), gap='small')
        with col1:
            st.write("#### Your Information")
            with st.form("my_form"):
                housing = ['1&2-Room Flat', '4-Room Flat', '3-Room Flat', '5-Room', 'Executive Flat','Condominium','Landed Property']
                age = st.number_input("Present Age", min_value=0, max_value=100, value=USER_DATA[2])
                housing_type = st.selectbox("Current Housing Type", housing, index=housing.index(USER_DATA[3]))
                income = st.number_input("Monthly Income", min_value=0, value=8000,step=1000)
                expenditure = st.number_input("Monthly Expenditure", min_value=0, value=5000, step=1000)
                submitted = st.form_submit_button("Calculate Score")
        with col2:
            st.write("#### Lobang&sup3; Score")
            lobang = make_donut(75,"75","blue")
            st.altair_chart(lobang)
        with col3:
            st.write("#### Suggestions")
    




elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    #st.image("mockpass.jpg", width=200)
    st.warning('Please enter your username and password')
