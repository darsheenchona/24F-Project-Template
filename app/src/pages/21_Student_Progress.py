import logging
import streamlit as st
import requests

# Configure logging
logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
from modules.nav import SideBarLinks
SideBarLinks()

st.title("View Student Progress")

# Input student ID to fetch their progress
student_id = st.text_input("Enter Student ID to View Progress")

# Validate if the entered student_id is a valid integer
if student_id:
    try:
        # Ensure the input is a valid integer
        student_id_int = int(student_id)

        # Fetch student profile via the API (GET request)
        response = requests.get(f'http://api:4000/student_progress/{student_id_int}')
        
        if response.status_code == 200:
            student_data = response.json()

            # Display student profile details
            st.subheader("Major:")
            st.write(student_data.get("Major", "N/A"))

            # Display skills
            st.subheader("Skills:")
            st.write(student_data.get("Skills", "No skills listed"))

            # Display interests
            st.subheader("Interests:")
            st.write(student_data.get("Interests", "No interests listed"))
            
            # Display dashboard preferences
            st.subheader("Dashboard Preferences:")
            st.write(student_data.get("DashboardPreferences", "No preferences set"))
            
            # Display resume link
            st.subheader("Resume Link:")
            st.write(student_data.get("ResumeLink", "No resume link provided"))

            # Display portfolio link
            st.subheader("Portfolio Link:")
            st.write(student_data.get("PortfolioLink", "No portfolio link provided"))
            
            # Update student progress
            st.header("Update Progress or Profile")

            # Display current student data in editable form
            new_skills = st.text_area("Update Skills", student_data.get("Skills", ""))
            new_interests = st.text_area("Update Interests", student_data.get("Interests", ""))
            new_dashboard_preferences = st.text_area("Update Dashboard Preferences", student_data.get("DashboardPreferences", ""))
            new_resume_link = st.text_input("Update Resume Link", student_data.get("ResumeLink", ""))
            new_portfolio_link = st.text_input("Update Portfolio Link", student_data.get("PortfolioLink", ""))

            if st.button("Save Updates", key=f"save_progress_{student_id_int}"):
                # Send an update request (PUT) to the API
                update_data = {
                    "Skills": new_skills,
                    "Interests": new_interests,
                    "DashboardPreferences": new_dashboard_preferences,
                    "ResumeLink": new_resume_link,
                    "PortfolioLink": new_portfolio_link
                }
                
                update_response = requests.put(f'http://api:4000/student_progress/{student_id_int}', json=update_data)

                if update_response.status_code == 200:
                    st.success("Profile updated successfully.")
                else:
                    st.error(f"Error updating profile: {update_response.status_code}")
        
        elif response.status_code == 404:
            st.error("Student not found. Please check the Student ID and try again.")
        else:
            st.error(f"Error fetching student progress: {response.status_code}")
    
    except ValueError:
        st.error("Please enter a valid Student ID (numeric value).")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please enter a valid Student ID.")
