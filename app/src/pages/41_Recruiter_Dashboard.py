import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Recruiter Dashboard")

recruiter_id = st.session_state.get('recruiter_id')
response = requests.get(f"http://api:4000/jobs", params={"recruiterID": recruiter_id})
if response.status_code == 200:
    jobs = response.json()
    st.write("### Open Positions")
    for job in jobs:
        st.write(f"**{job['title']}** at {job['company']} - Progress: {job.get('progress', 0)}%")
else:
    st.error("Failed to fetch jobs.")
