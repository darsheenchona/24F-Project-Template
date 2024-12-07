import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("Manage Employers")

# Retrieve list of employers (adjust the URL to 'localhost' if Flask is local)
employer_response = requests.get('http://api:4000/employers')  # or the appropriate IP

if employer_response.status_code == 200:
    employers = employer_response.json()
    st.subheader("Employer List:")
    
    # Iterate over each employer and display details with a deactivate button
    for employer in employers:
        # Display employer info
        st.write(f"**Employer ID:** {employer['id']} - {employer['name']}")
        
        # Add functionality to deactivate the employer
        if st.button(f"Deactivate Employer {employer['id']}", key=f"deactivate_button_{employer['id']}"):
            # Trigger deactivation for the selected employer
            deactivate_response = requests.put(
                f'http://api:4000/employers/{employer["id"]}',  # Use localhost if Flask is running locally
                json={"status": "inactive"}
            )
            
            # Handle the response from the deactivation request
            if deactivate_response.status_code == 200:
                st.success(f"Employer with ID {employer['id']} deactivated successfully!")
            else:
                st.error(f"Failed to deactivate employer with ID {employer['id']}.")
else:
    st.error("Error fetching employer data.")
