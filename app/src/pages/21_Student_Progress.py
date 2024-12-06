import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Set Streamlit page layout
st.set_page_config(layout='wide')

# Display the sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

# Page title
st.title("View Student Progress")

# API URL for retrieving student profile and progress
api_url = 'http://localhost:8501/Student_Progress'  # Update the API URL if necessary

# Retrieve student profile and progress via the API (GET request)
try:
    response = requests.get(api_url)

    # Log the raw response text to see what we are receiving from the API
    logger.info(f"Raw response from API: {response.text}")

    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            student_data = response.json()

            # Display student data
            st.subheader("Career Interests:")
            st.write(student_data.get("career_interests", "N/A"))

            st.subheader("Skills:")
            st.write(student_data.get("skills", []))

            st.subheader("Progress:")
            st.write(student_data.get("progress", "No progress data available"))
        except ValueError:
            # If JSON parsing fails, handle it
            st.error("Error: The server returned an invalid JSON response.")
            logger.error(f"Invalid JSON response: {response.text}")
    else:
        # Handle the case where the API response is not successful
        st.error(f"Error fetching student progress data. Status Code: {response.status_code}")
        logger.error(f"API request failed with status code: {response.status_code}, response: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle network-related errors or invalid URL
    st.error(f"Request failed: {e}")
    logger.error(f"Request failed: {e}")

# Add button to trigger a refresh of student data
if st.button('Refresh Data'):
    st.experimental_rerun()

