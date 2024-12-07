import streamlit as st
import requests

def display():
    st.title("Co-op Applications")

    # Sidebar input for Student ID (default to 1)
    student_id = st.sidebar.text_input("Enter Student ID", "1")
    if not student_id.isdigit():
        st.error("Please enter a valid numeric Student ID.")
        return

    st.write("Here are your tracked applications:")

    # Fetch applications from the existing endpoint (which returns fields from Applications table)
    # Assuming your backend route is something like: GET /student/applications?studentID=1
    applications_response = requests.get(f"http://api:4000/student/applications?studentID={student_id}")
    if applications_response.status_code == 200:
        applications = applications_response.json()
        if applications:
            for app in applications:
                # The app dictionary should contain fields from the Applications table
                # For example: app['ApplicationID'], app['JobID'], app['Status'], app['DateApplied'], etc.
                
                st.subheader(f"Application ID: {app['ApplicationID']}")
                st.write(f"**Status:** {app.get('Status', 'N/A')}")
                st.write(f"**Date Applied:** {app.get('DateApplied', 'N/A')}")
                st.write(f"**Review Score:** {app.get('ReviewScore', 'N/A')}")
                st.write(f"**Feedback:** {app.get('Feedback', 'N/A')}")

                # If you want job details, you must do another request:
                job_id = app.get('JobID')
                if job_id:
                    job_response = requests.get(f"http://api:4000/jobs/{job_id}")
                    if job_response.status_code == 200:
                        job = job_response.json()
                        # Assuming job returns fields: Title, Company, Deadline, etc.
                        st.write(f"**Job Title:** {job.get('Title', 'N/A')}")
                        st.write(f"**Company:** {job.get('Company', 'N/A')}")
                        st.write(f"**Deadline:** {job.get('Deadline', 'N/A')}")
                    else:
                        st.warning("Unable to fetch job details.")
                else:
                    st.warning("No JobID found for this application.")

                st.write("---")
        else:
            st.info("No applications found for this student.")
    else:
        st.error("Unable to fetch applications.")

    st.subheader("Add a New Application")
    # Since your Applications table requires a JobID, StudentID, and Status, we'll ask for them here
    job_id_input = st.text_input("Job ID")
    status = st.selectbox("Status", ["Pending", "Accepted", "Rejected"])
    date_applied = st.date_input("Date Applied")
    review_score = st.number_input("Review Score", min_value=0, max_value=100, value=0)
    feedback = st.text_area("Feedback")

    if st.button("Add Application"):
        payload = {
            "StudentID": int(student_id),
            "JobID": int(job_id_input),
            "Status": status,
            "DateApplied": str(date_applied),
            "ReviewScore": review_score,
            "Feedback": feedback
        }
        # POST to /student/applications to add a new application
        add_response = requests.post("http://api:4000/student/applications", json=payload)
        if add_response.status_code == 201:
            st.success("Application added successfully!")
        else:
            st.error("Failed to add application.")

if __name__ == "__main__":
    display()
