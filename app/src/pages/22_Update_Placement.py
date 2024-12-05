import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("Update Co-op Placement")

# Get current placement status
placement_response = requests.get('http://localhost:4000/co-op/placement')

if placement_response.status_code == 200:
    placement_data = placement_response.json()
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
        update_response = requests.put('http://localhost:4000/co-op/placement', json=update_data)
        
        if update_response.status_code == 200:
            st.success("Placement updated successfully!")
        else:
            st.error("Failed to update placement.")
else:
    st.error("Error fetching current placement data.")
