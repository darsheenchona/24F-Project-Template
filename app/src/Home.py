import logging
import streamlit as st
from modules.nav import SideBarLinks

logging.basicConfig(format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

st.title("ConnectSphere")
st.write("\n\n")
st.write("### HI! As which user would you like to log in?")

if st.button("Act as Yomayra, a Recruiter", type="primary", use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'recruiter'
    st.session_state['recruiter_id'] = 24  # HARDCODED recruiterID for demo purposes
    st.session_state['first_name'] = 'Yomayra'
    st.switch_page('pages/40_Recruiter_Home.py')
