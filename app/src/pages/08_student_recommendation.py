import streamlit as st
import requests

def display():
    st.title("Recommendations")

    # Similar to the Co-op Applications page, let's allow selecting Student ID
    student_id = st.sidebar.text_input("Enter Student ID", "1")
    if not student_id.isdigit():
        st.error("Please enter a valid numeric Student ID.")
        return

    st.write("Fetching your personalized co-op recommendations...")

    # Based on other working endpoints, the URL should likely match:
    # http://api:4000/student/recommendations?studentID=<value>
    url = f"http://api:4000/student/recommendations?studentID={student_id}"

    response = requests.get(url)
    if response.status_code == 200:
        recommendations = response.json()
        if recommendations:
            for rec in recommendations:
                # The backend returns jobTitle, companyName, matchScore
                job_title = rec.get('job_title', 'N/A')
                company_name = rec.get('company_name', 'N/A')
                match_score = rec.get('match_score', 'N/A')

                st.subheader(f"{job_title} at {company_name}")
                st.write(f"**Match Score:** {match_score}")
        else:
            st.info("No recommendations found for this student.")
    else:
        st.error("Unable to fetch recommendations.")


if __name__ == "__main__":
    display()
