import logging
import streamlit as st
from modules.nav import SideBarLinks

logging.basicConfig(format="%(filename)s:%(lineno)s:%(levelname)s -- %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")

SideBarLinks()

st.title(f"Welcome Recruiter, {st.session_state['first_name']}!")
st.write("")
st.write("### What would you like to do today?")

if st.button("Go to Dashboard", type="primary", use_container_width=True):
    st.switch_page("pages/41_Recruiter_Dashboard.py")

if st.button("Manage Job Posts", type="primary", use_container_width=True):
    st.switch_page("pages/42_Recruiter_Jobs.py")

if st.button("Manage Candidates", type="primary", use_container_width=True):
    st.switch_page("pages/43_Recruiter_Job_Details.py")

if st.button("View Notifications", type="primary", use_container_width=True):
    st.switch_page("pages/44_Recruiter_Notifications.py")

if st.button("Generate Reports", type="primary", use_container_width=True):
    st.switch_page("pages/45_Recruiter_Reports.py")

if st.button("Manage Profile", type="primary", use_container_width=True):
    st.switch_page("pages/46_Recruiter_Profile.py")
