import logging
import streamlit as st
import requests
from datetime import datetime

# Set page layout
st.set_page_config(layout='wide')

# Logging setup
logger = logging.getLogger(__name__)

# Set the base URL for your Flask API (Adjust the URL depending on the Flask app's location)
BASE_URL = "http://api:4000"  # Update with correct address for Flask API (change to localhost if running locally)

# Display the appropriate sidebar links for the role of the logged-in user (optional)
from modules.nav import SideBarLinks
SideBarLinks()

# Streamlit page title
st.title("Co-op Advisor Management")

# ---------------------------------------------------------
# Retrieve and display Co-op Advisor Profile
st.header("Co-op Advisor Profile")

# Input for Advisor ID
advisor_id = st.text_input("Enter Advisor ID:")

# Retrieve Co-op Advisor Profile
if advisor_id:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/profile?advisorID={advisor_id}")
        if response.status_code == 200:
            profile = response.json()
            st.subheader("Profile Information")
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Email:** {profile['email']}")
            st.write(f"**Department:** {profile['department']}")
            st.write(f"**Advising History Count:** {profile['advisingHistoryCount']}")
        else:
            st.error("Co-op Advisor not found")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter an Advisor ID to fetch the profile.")

# ---------------------------------------------------------
# Update Co-op Advisor Profile
st.header("Update Co-op Advisor Profile")

if advisor_id:
    # Allow for updating the profile (department, name, and email)
    department = st.text_input("New Department:")
    name = st.text_input("New Name:")
    email = st.text_input("New Email:")

    if st.button("Update Profile"):
        # Validate inputs before sending the request
        if name and email and department:
            data = {"department": department, "name": name, "email": email}
            try:
                response = requests.put(f"{BASE_URL}/coop_advisor/profile?advisorID={advisor_id}", json=data)
                if response.status_code == 200:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Failed to update profile.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please fill in all fields to update the profile.")
else:
    st.warning("Please enter an Advisor ID to update the profile.")

# ---------------------------------------------------------
# Retrieve and display list of students advised by the co-op advisor
st.header("Students Assigned to This Advisor")

if advisor_id:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/Students?advisorID={advisor_id}")
        if response.status_code == 200:
            students = response.json()
            st.subheader("List of Students:")
            for student in students:
                st.write(f"**Student ID:** {student['studentID']} - **Name:** {student['student_name']} - **Major:** {student['major']}")
        else:
            st.error("No students found for this advisor.")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.warning("Please enter an Advisor ID to see the list of students.")

# ---------------------------------------------------------
# Retrieve and display student details
st.header("Student Details")

StudentID_input = st.text_input("Enter Student ID for details:")

if StudentID_input:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/students/{StudentID_input}")
        if response.status_code == 200:
            student = response.json()
            st.subheader("Student Information")
            st.write(f"**Name:** {student['name']}")
            st.write(f"**Major:** {student['major']}")
            st.write(f"**GPA:** {student['gpa']}")
            st.write(f"**Email:** {student['email']}")
        else:
            st.error("Student not found.")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------------------------------------
# Retrieve and display student placement history
st.header("Student Placement History")

placement_StudentID = st.text_input("Enter Student ID to see placement history:")

if placement_StudentID:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/students/{placement_StudentID}/placements")
        if response.status_code == 200:
            placements = response.json()
            st.subheader("Placement History:")
            for placement in placements:
                st.write(f"**Placement ID:** {placement['placementID']} - **Company:** {placement['company']} - **Position:** {placement['position']} - **Start Date:** {placement['startDate']} - **End Date:** {placement['endDate']} - **Status:** {placement['status']}")
        else:
            st.error("No placement history found for this student.")
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------------------------------------
# Generate New Report
st.header("Generate Report for Advisor")

if advisor_id:
    report_title = st.text_input("Report Title:")
    report_description = st.text_area("Report Description:")

    if st.button("Generate Report"):
        # Validate that report title and description are provided
        if report_title and report_description:
            data = {"title": report_title, "description": report_description}
            try:
                response = requests.post(f"{BASE_URL}/coop_advisor/reports?advisorID={advisor_id}", json=data)
                if response.status_code == 201:
                    st.success("Report generated successfully!")
                else:
                    st.error("Failed to generate report.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please provide both a title and description for the report.")
else:
    st.warning("Please enter an Advisor ID to generate the report.")

# ---------------------------------------------------------
# Delete Report
st.header("Delete Report")

report_id = st.text_input("Enter Report ID to delete:")

if report_id:
    if st.button("Delete Report"):
        try:
            response = requests.delete(f"{BASE_URL}/coop_advisor/reports/{report_id}")
            if response.status_code == 200:
                st.success(f"Report with ID {report_id} deleted successfully!")
            else:
                st.error("Failed to delete report.")
        except Exception as e:
            st.error(f"Error: {e}")
