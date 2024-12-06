import streamlit as st
import requests

def display():
    st.title("Recommendations")
    st.write("Fetching your personalized co-op recommendations...")

    response = requests.get("http://localhost:5000/api/student/recommendations")
    if response.status_code == 200:
        recommendations = response.json()
        for rec in recommendations:
            st.subheader(f"{rec['job_title']} at {rec['company_name']}")
            st.write(f"**Match Score:** {rec['match_score']}")
    else:
        st.error("Unable to fetch recommendations.")
