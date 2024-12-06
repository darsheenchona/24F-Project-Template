import streamlit as st
import requests

def display():
    st.title("Student Profile")
    st.write("Fetching your profile information...")
    
    response = requests.get("http://localhost:5000/api/student/students")
    if response.status_code == 200:
        profile = response.json()
        st.subheader("Profile Details")
        st.write(f"**Name:** {profile['name']}")
        st.write(f"**Major:** {profile['major']}")
        st.write(f"**Year:** {profile['year']}")
        st.write(f"**Skills:** {profile['skills']}")
        st.write(f"**Interests:** {profile['interests']}")
    else:
        st.error("Unable to fetch profile information.")
