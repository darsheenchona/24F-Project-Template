import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("Manage Employers")

# Retrieve list of employers from the API
try:
    employer_response = requests.get('http://localhost:8501/employers')  # Adjust the URL if needed

    # Check if the response status is OK (200)
    if employer_response.status_code == 200:
        employers = employer_response.json()  # If the response is valid JSON, parse it
        if employers:  # Check if the response contains data
            st.subheader("Employer List:")
            for employer in employers:
                st.write(f"**Employer ID:** {employer['id']} - {employer['name']}")
        else:
            st.warning("No employers found.")
    else:
        st.error(f"Error: Unable to fetch employer data. Status code: {employer_response.status_code}")
        logger.error(f"Failed API request with status code: {employer_response.status_code}")
except requests.exceptions.RequestException as e:
    # Handle exceptions like network errors, connection issues, etc.
    st.error(f"An error occurred: {str(e)}")
    logger.error(f"Error occurred while making the request: {str(e)}")

