import logging
import streamlit as st
import requests

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("View Student Progress")

# Input student ID to fetch their progress
student_id = st.text_input("Enter Student ID to View Progress")
=======
# Retrieve student profile and progress via the API (GET request)
response = requests.get('http://api:4000/Student_Progress')  # API URL for student profile


# Proceed only if a valid student ID is entered
if student_id:
    # Retrieve student profile and progress via the API (GET request)
    response = requests.get(f'http://api:4000/Student_Progress/{student_id}')  # API URL for student profile

    if response.status_code == 200:
        student_data = response.json()

        # Display career interests
        st.subheader("Career Interests:")
        st.write(student_data.get("career_interests", "N/A"))

        # Display skills
        st.subheader("Skills:")
        st.write(student_data.get("skills", []))

        # Display progress
        st.subheader("Progress:")
        st.write(student_data.get("progress", "No progress data available"))
        
        # Adding functionality for updating progress
        if st.button("Update Progress", key=f"update_progress_{student_id}"):
            # For simplicity, let’s assume we just allow updating the progress status here
            new_progress = st.text_area("Enter New Progress Status", "Progress details...")
            if st.button("Save Progress", key=f"save_progress_{student_id}"):
                # Send an update request (POST or PUT) to the API
                update_data = {"progress": new_progress}
                update_response = requests.put(f'http://api:4000/Student_Progress/{student_id}', json=update_data)

                if update_response.status_code == 200:
                    st.success("Progress updated successfully.")
                else:
                    st.error(f"Error updating progress: {update_response.status_code}")
    else:
        st.error("Error fetching student progress data.")
else:
    st.warning("Please enter a valid Student ID.")
