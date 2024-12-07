import streamlit as st
import requests
from datetime import date

def display():
    st.title("Saved Jobs")

    # Ask for student ID
    student_id = st.sidebar.text_input("Enter Student ID", "1")
    if not student_id.isdigit():
        st.error("Please enter a valid numeric Student ID.")
        return

    st.write("Your saved jobs:")

    # Fetch saved jobs for this student
    # Assuming the backend route is now /student/savedjobs?studentID=<id>
    response = requests.get(f"http://api:4000/student/savedjobs?studentID={student_id}")
    if response.status_code == 200:
        saved_jobs = response.json()
        if saved_jobs:
            for i, job in enumerate(saved_jobs):
                st.subheader(f"{job['job_title']} at {job['company_name']}")
                st.write(f"Saved on: {job.get('save_date', 'N/A')}")

                # Use a unique key by including the index 'i'
                if st.button("Remove Saved Job", key=f"remove_{job['id']}_{i}"):
                    remove_saved_job(job['id'])

        else:
            st.info("No saved jobs found for this student.")
    else:
        st.error("Unable to fetch saved jobs.")

    st.write("---")
    st.subheader("Add a Saved Job")
    # Instead of job_title/company_name, we must provide a JobID (from the Jobs table)
    job_id_input = st.text_input("Job ID")
    if not job_id_input.isdigit() and job_id_input.strip():
        st.error("Please enter a valid numeric Job ID.")
        return
    
    # Optionally allow user to select a date or default to today's date
    save_date = st.date_input("Save Date", value=date.today())
    if st.button("Add Saved Job"):
        add_saved_job(student_id, job_id_input, save_date)

def add_saved_job(student_id, job_id, save_date):
    # POST /student/savedjobs with JSON: { "StudentID": ..., "JobID": ..., "SaveDate": "YYYY-MM-DD" }
    payload = {
        "StudentID": int(student_id),
        "JobID": int(job_id),
        "SaveDate": save_date.isoformat()
    }
    response = requests.post("http://api:4000/student/savedjobs", json=payload)
    if response.status_code == 201:
        st.success("Saved job added successfully!")
        st.experimental_rerun()  # Refresh the page to show updated list
    else:
        st.error("Failed to add saved job.")

def remove_saved_job(save_id):
    # DELETE /student/savedjobs/<save_id>
    response = requests.delete(f"http://api:4000/student/savedjobs/{save_id}")
    if response.status_code == 200:
        st.success("Saved job removed successfully!")
        st.experimental_rerun()
    else:
        st.error("Failed to remove saved job.")

if __name__ == "__main__":
    display()
