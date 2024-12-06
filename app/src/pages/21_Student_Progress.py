import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("View Student Progress")

# Retrieve student profile and progress via the API (GET request)
response = requests.get('http://localhost:8501/Student_Progress')  # API URL for student profile

if response.status_code == 200:
    student_data = response.json()
    st.subheader("Career Interests:")
    st.write(student_data.get("career_interests", "N/A"))

    st.subheader("Skills:")
    st.write(student_data.get("skills", []))

    st.subheader("Progress:")
    st.write(student_data.get("progress", "No progress data available"))
else:
    st.error("Error fetching student progress data.")

# Add additional buttons for more actions if needed
if st.button('Refresh Data'):
    # Trigger a refresh of student data or any updates from the API
    st.experimental_rerun()
