import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("Manage Employers")

# Retrieve list of employers
employer_response = requests.get('http://localhost:8501/employers')

if employer_response.status_code == 200:
    employers = employer_response.json()
    st.subheader("Employer List:")
    for employer in employers:
        st.write(f"**Employer ID:** {employer['id']} - {employer['name']}")
    
    # Deactivate employer functionality
    employer_id_to_deactivate = st.number_input("Enter Employer ID to deactivate:", min_value=1)
    if st.button("Deactivate Employer"):
        deactivate_response = requests.put(f'http://localhost:8501/employers/{employer_id_to_deactivate}', json={"status": "inactive"})
        if deactivate_response.status_code == 200:
            st.success(f"Employer with ID {employer_id_to_deactivate} deactivated successfully!")
        else:
            st.error("Failed to deactivate employer.")
else:
    st.error("Error fetching employer data.")
