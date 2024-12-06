import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Set Streamlit page configuration
st.set_page_config(layout='wide')

# Display the sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

# Page title
st.title("Update Co-op Placement")

# API URL for retrieving current co-op placement status
api_url = 'http://localhost:8501/co-op/placement'  # Update the API URL if necessary

# Retrieve current placement status via the API (GET request)
try:
    placement_response = requests.get(api_url)

    # Log the raw response content to see what we are receiving from the API
    logger.info(f"Raw response from API: {placement_response.text}")

    # Check if the response is successful (status code 200)
    if placement_response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            placement_data = placement_response.json()

            # Display the current placement status
            st.subheader("Current Placement Status")
            st.write(placement_data.get("placement_status", "N/A"))
            
            # Input fields to update placement status, deadlines, and milestones
            new_status = st.text_input("New Placement Status:", value=placement_data.get("placement_status", ""))
            new_deadline = st.date_input("New Deadline:", value=placement_data.get("deadlines", ""))
            new_milestones = st.text_area("New Milestones:", value=", ".join(placement_data.get("milestones", [])))
            
            # Update the co-op placement when the button is clicked
            if st.button("Update Placement"):
                update_data = {
                    "placement_status": new_status,
                    "deadlines": str(new_deadline),
                    "milestones": new_milestones.split(", ")
                }
                update_response = requests.put(api_url, json=update_data)
                
                if update_response.status_code == 200:
                    st.success("Placement updated successfully!")
                else:
                    st.error(f"Failed to update placement. Status Code: {update_response.status_code}")
                    logger.error(f"Failed to update placement. Response: {update_response.text}")
        except ValueError:
            # If JSON parsing fails, handle it
            st.error("Error: The server returned an invalid JSON response.")
            logger.error(f"Invalid JSON response: {placement_response.text}")
    else:
        # Handle the case where the API response is not successful (e.g., 404 or 500)
        st.error(f"Error fetching current placement data. Status Code: {placement_response.status_code}")
        logger.error(f"API request failed with status code: {placement_response.status_code}, response: {placement_response.text}")

except requests.exceptions.RequestException as e:
    # Handle network-related errors or invalid URL
    st.error(f"Request failed: {e}")
    logger.error(f"Request failed: {e}")

# Add button to trigger a refresh of placement data
if st.button('Refresh Data'):
    st.experimental_rerun()
