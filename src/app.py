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
from helper import qol_suggestion
from helper import disaster_suggestion
from helper import retirement_suggestion
from helper import chart

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
            div[data-testid="column"]:nth-of-type(2)
            {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    #connect to sql database and get user data

    USER_DATA = get_user_data(name)
    print(USER_DATA)

    # Input section
    with st.container():
        col1, col2, col3 = st.columns((2, 4.2, 2), gap='medium')
        with col1:
            st.write("## Your Information")
            with st.form("my_form"):
                housing = ['1&2-Room Flat', '4-Room Flat', '3-Room Flat', '5-Room', 'Executive Flat','Condominium','Landed Property']
                age = st.number_input("Present Age", min_value=0, max_value=100, value=USER_DATA[2], disabled=False)
                housing_name = st.selectbox("Current Housing Type", housing, index=housing.index(USER_DATA[3]), disabled=False)
                housing_type = housing_name
                cpf = st.number_input("CPF amount", min_value=0, value=round(USER_DATA[4]+USER_DATA[5]+USER_DATA[6]),step=1000, disabled=False)
                income = st.number_input("Monthly Income", min_value=0, value=8000,step=1000)
                expenditure = st.number_input("Monthly Expenditure", min_value=0, value=5000, step=1000)
                savings = st.number_input("Savings", min_value=0, value=8000,step=1000)
                submitted = st.form_submit_button("Calculate Score")
        with col2:
            st.write("## Lobang&sup3; Score")
            lobang_info = [float(arr[0]) for arr in getInfo(age,housing_type,income*12,cpf,expenditure*12,savings)]
            # print(lobang_info)
            lobang_score = getLobang(lobang_info[0],lobang_info[1],lobang_info[2])
            lobang = make_donut(lobang_score,str(lobang_score),"blue")    
            st.altair_chart(lobang,on_select="ignore",use_container_width=True)
            st.markdown(f"#### Quality of Life: {round(lobang_info[0],1)}/10",help="Expected quality of life")
            st.markdown(f"#### Disaster Preparedness: {round(lobang_info[1],1)}/10",help="How safe you are in case of a disaster")
            st.markdown(f"#### Retirement Readiness: {round(lobang_info[2],1)}/10",help="How ready you are for retirement")
        with col3:
            tab1, tab2 = st.tabs(["Suggestions", "Projection"])
            with tab1:
                st.write("## Suggestions")
                lst1 = qol_suggestion(age,housing_type,income*12,cpf,expenditure*12,savings)[-3:]
                lst2 = disaster_suggestion(age,housing_type,income*12,cpf,expenditure*12,savings)[-3:]
                lst3 = retirement_suggestion(age,housing_type,income*12,cpf,expenditure*12,savings)[-3:]
                st.markdown(f"#### Quality of Life")
                for i in range(1,4):
                    st.write(f"{i}. {lst1[-i]}")
                st.markdown(f"#### Disaster Resistance")
                for i in range(1,4):
                    st.write(f"{i}. {lst2[-i]}")
                st.markdown(f"#### Retirement Readiness")
                for i in range(1,4):
                    st.write(f"{i}. {lst3[-i]}")
            with tab2:
                st.write("## Projection")
                chart_data = chart(age,housing_type,income*12,cpf,expenditure*12,savings,55)
                st.line_chart(chart_data.set_index('age'))

    




elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    #st.image("mockpass.jpg", width=200)
    st.warning('Please enter your username and password')
