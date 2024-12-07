import logging
import streamlit as st
import requests
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

# Set page layout
st.set_page_config(layout="wide", page_title="Co-op Advisor Management")

# Base API URL (adjust to match your setup)
BASE_URL = "http://api:4000"

# Sidebar links for navigation (optional)
from modules.nav import SideBarLinks
SideBarLinks()

# Title
st.title("Co-op Advisor Management System")


# ------------------------------------------------------------
# Co-op Advisor Profile Section
st.header("Co-op Advisor Profile")

# Advisor ID input
advisor_id = st.text_input("Enter Advisor ID:")

if advisor_id:
    # Fetch and display advisor profile
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/profile", params={"advisorID": advisor_id})
        if response.status_code == 200:
            profile = response.json()
            st.subheader("Profile Information")
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Email:** {profile['Email']}")
            st.write(f"**Department:** {profile['Department']}")
            st.write(f"**Advising History Count:** {profile['ActiveStudentCount']}")
        else:
            st.error("Co-op Advisor not found.")
    except Exception as e:
        st.error(f"Error: {e}")

    # Update advisor profile
    st.subheader("Update Profile")
    with st.form(key="update_advisor_profile_form"):
        new_name = st.text_input("New Name", value=profile.get("name", ""))
        new_email = st.text_input("New Email", value=profile.get("email", ""))
        new_department = st.text_input("New Department", value=profile.get("department", ""))
        submitted = st.form_submit_button("Update Profile")

        if submitted:
            try:
                payload = {"name": new_name, "email": new_email, "department": new_department}
                response = requests.put(f"{BASE_URL}/coop_advisor/profile", params={"advisorID": advisor_id}, json=payload)
                if response.status_code == 200:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Failed to update profile.")
            except Exception as e:
                st.error(f"Error: {e}")


# ------------------------------------------------------------
# Students Assigned to Advisor Section
st.header("Students Assigned to Advisor")

if advisor_id:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/Students", params={"advisorID": advisor_id})
        if response.status_code == 200:
            students = response.json()
            st.subheader("Assigned Students")
            for student in students:
                st.write(
                    f"**Student ID:** {student['studentID']} - **Name:** {student['student_name']} - **Major:** {student['major']}"
                )
        else:
            st.error("No students found for this advisor.")
    except Exception as e:
        st.error(f"Error: {e}")


# ------------------------------------------------------------
# Student Details Section
st.header("Student Details")

student_id = st.text_input("Enter Student ID:")

if student_id:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/students/{student_id}")
        if response.status_code == 200:
            student = response.json()
            st.subheader("Student Information")
            st.write(f"**Name:** {student['name']}")
            st.write(f"**Major:** {student['major']}")
            st.write(f"**GPA:** {student['gpa']}")
            st.write(f"**Email:** {student['email']}")

            # Update student details
            st.subheader("Update Student Details")
            with st.form(key="update_student_form"):
                new_major = st.text_input("Major", value=student['major'])
                new_gpa = st.text_input("GPA", value=student['gpa'])
                new_email = st.text_input("Email", value=student['email'])
                submitted = st.form_submit_button("Update Student")

                if submitted:
                    try:
                        payload = {"major": new_major, "gpa": new_gpa, "email": new_email}
                        response = requests.put(f"{BASE_URL}/coop_advisor/students/{student_id}", json=payload)
                        if response.status_code == 200:
                            st.success("Student details updated successfully!")
                        else:
                            st.error("Failed to update student details.")
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.error("Student not found.")
    except Exception as e:
        st.error(f"Error: {e}")


# ------------------------------------------------------------
# Student Placement History Section
st.header("Student Placement History")

placement_student_id = st.text_input("Enter Student ID for Placement History:")

if placement_student_id:
    try:
        response = requests.get(f"{BASE_URL}/coop_advisor/students/{placement_student_id}/placements")
        if response.status_code == 200:
            placements = response.json()
            st.subheader("Placement History")
            for placement in placements:
                st.write(
                    f"**Placement ID:** {placement['placementID']} - **Company:** {placement['company']} - "
                    f"**Position:** {placement['position']} - **Start Date:** {placement['startDate']} - "
                    f"**End Date:** {placement['endDate']} - **Status:** {placement['status']}"
                )
        else:
            st.error("No placement history found.")
    except Exception as e:
        st.error(f"Error: {e}")


# ------------------------------------------------------------
# Reports Section
st.header("Reports Management")

# Fetch existing reports
try:
    response = requests.get(f"{BASE_URL}/reports")
    if response.status_code == 200:
        reports = response.json()
        st.subheader("Existing Reports")
        for report in reports:
            st.write(f"**{report['title']}** - Generated on {report['dateGenerated']}")
            if st.button(f"Delete {report['title']}", key=f"delete_{report['title']}"):
                delete_response = requests.delete(f"{BASE_URL}/reports/{report['ReportID']}")
                if delete_response.status_code == 200:
                    st.success(f"Deleted {report['title']}")
                else:
                    st.error("Failed to delete report.")
except Exception as e:
    st.error(f"Error fetching reports: {e}")

# Generate a new report
st.subheader("Generate New Report")
with st.form(key="generate_report_form"):
    report_title = st.text_input("Report Title")
    report_description = st.text_area("Report Description")
    generate_submitted = st.form_submit_button("Generate Report")

    if generate_submitted:
        try:
            payload = {"title": report_title, "description": report_description}
            response = requests.post(f"{BASE_URL}/reports", params={"advisorID": advisor_id}, json=payload)
            if response.status_code == 201:
                st.success("Report generated successfully.")
            else:
                st.error("Failed to generate report.")
        except Exception as e:
            st.error(f"Error: {e}")
