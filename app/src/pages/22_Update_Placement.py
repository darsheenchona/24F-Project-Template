import logging
import requests
import streamlit as st

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("Update Co-op Placement")


def manage_placements():
    # Get student ID from user input
    StudentID = st.text_input("Enter Student ID for Placement Management")
    
    if StudentID:  # Only fetch placements if student ID is provided
        if st.button("View Placements", key=f"view_placements_{StudentID}"):  # Unique key
            response = requests.get(f"http://api:4000/coop_advisor/students/{StudentID}/placements")


            
            # Check the status code of the response
            if response.status_code == 200:
                placements = response.json()
                
                if placements:  # Check if placements data is empty
                    for placement in placements:
                        st.write(f"Company: {placement['company']} - Position: {placement['position']} - Status: {placement['status']}")
                else:
                    st.warning("No placements found for this student.")
            else:
                st.error(f"Failed to fetch placements. Status code: {response.status_code}")
    
    else:
        st.error("Please enter a valid Student ID.")

    # Add functionality to add a new placement for the student
    if st.button("Add Placement", key=f"add_placement_{StudentID}") and StudentID:
        add_placement(StudentID)
    elif not StudentID:
        st.error("Please enter a Student ID before adding a placement.")

def add_placement(StudentID):
    # Get placement details from user input
    company = st.text_input("Enter Company")
    position = st.text_input("Enter Position")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    status = st.selectbox("Status", ["Active", "Completed", "Pending"])

    # When the Add Placement button is pressed, send a POST request to add placement
    if st.button("Add Placement", key=f"submit_add_placement_{StudentID}") and company and position:
        data = {
            "company": company,
            "position": position,
            "startDate": str(start_date),  # Convert date to string format for API compatibility
            "endDate": str(end_date),
            "status": status
        }
        
        response = requests.post(f"http://api:4000/coop_advisor/students/{StudentID}/placements", json=data)
        
        if response.status_code == 201:
            st.success("Placement added successfully.")
        else:
            st.error(f"Failed to add placement. Status code: {response.status_code}")

# Call the manage_placements function to render the UI
manage_placements()
