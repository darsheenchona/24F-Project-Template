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
def manage_placements():
    student_id = st.text_input("Enter Student ID for Placement Management")
    
    if st.button("View Placements"):
        response = requests.get(f"http://api:4000/coop_advisor/students/{student_id}/placements")
        if response.status_code == 200:
            placements = response.json()
            for placement in placements:
                st.write(f"Company: {placement['company']} - Position: {placement['position']} - Status: {placement['status']}")
        else:
            st.error("No placements found.")

    # Optionally, add functionality for adding or updating placements here.
    if st.button("Add Placement"):
        add_placement(student_id)

def add_placement(student_id):
    company = st.text_input("Enter Company")
    position = st.text_input("Enter Position")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    status = st.selectbox("Status", ["Active", "Completed", "Pending"])
    
    if st.button("Add Placement"):
        data = {
            "company": company,
            "position": position,
            "startDate": start_date,
            "endDate": end_date,
            "status": status
        }
        response = requests.post(f"http://api:4000/coop_advisor/students/{student_id}/placements", json=data)
        if response.status_code == 201:
            st.success("Placement added successfully.")
        else:
            st.error("Failed to add placement.")