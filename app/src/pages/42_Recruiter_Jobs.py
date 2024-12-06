import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime
import requests

st.set_page_config(layout="wide")
SideBarLinks()

recruiter_id = st.session_state.get("recruiter_id")

st.title("Manage Job Posts")


# function to fetch jobs data; we used for purpose of refreshing job UI on updates
def fetch_jobs():
    fetch_job_response = requests.get("http://api:4000/jobs", params={"recruiterID": recruiter_id})
    if fetch_job_response.status_code == 200:
        st.session_state.jobs = fetch_job_response.json()
    else:
        st.error("Failed to fetch job posts.")
        st.session_state.jobs = []


# init session state for jobs
if "jobs" not in st.session_state:
    fetch_jobs()

# Display the list of jobs
st.write("### Job Posts")
if "job_to_update" not in st.session_state:
    st.session_state.job_to_update = None

for job in st.session_state.jobs:
    st.write(f"**{job['title']}** at {job['company']}")
    st.write(f"Status: {job['status']} | Deadline: {job['deadline']}")

    # update job post
    if st.session_state.job_to_update == job["jobID"]:
        with st.form(key=f"update_form_{job['jobID']}"):
            updated_title = st.text_input("Title", value=job["title"])
            updated_company = st.text_input("Company", value=job["company"])
            updated_description = st.text_area("Description", value=job["description"])
            updated_requirements = st.text_area("Requirements", value=job["requirements"])

            # convert string to date object for date_input
            try:
                deadline_date = datetime.strptime(job["deadline"], "%Y-%m-%d").date()
            except (ValueError, TypeError):
                deadline_date = None  # if conversion fails, this tells us to look into data

            updated_deadline = st.date_input("Deadline", value=deadline_date)
            updated_status = st.selectbox(
                "Status", ["Open", "Closed"], index=0 if job["status"] == "Open" else 1
            )

            submitted = st.form_submit_button("Submit Update")
            if submitted:
                update_payload = {
                    "title": updated_title,
                    "company": updated_company,
                    "description": updated_description,
                    "requirements": updated_requirements,
                    "deadline": str(updated_deadline),
                    "status": updated_status,
                }
                response = requests.put(f"http://api:4000/jobs/{job['jobID']}", json=update_payload)
                if response.status_code == 200:
                    st.success(f"Updated {job['title']} successfully.")
                    st.session_state.job_to_update = None  # reset state
                    fetch_jobs()  # refresh jobs list
                else:
                    st.error("Failed to update job post.")

    elif st.session_state.job_to_update is None:
        if st.button(f"Update {job['title']}", key=f"update_btn_{job['jobID']}"):
            st.session_state.job_to_update = job["jobID"]

    # delete job post
    if st.button(f"Delete {job['title']}", key=f"delete_{job['jobID']}"):
        response = requests.delete(f"http://api:4000/jobs/{job['jobID']}")
        if response.status_code == 200:
            st.success(f"Deleted {job['title']} successfully.")
            fetch_jobs()  # refresh jobs list on deletion
        else:
            st.error("Failed to delete job post.")

# create new job post
st.write("### Create New Job Post")
with st.form(key="create_job_form"):
    title = st.text_input("Title")
    company = st.text_input("Company")
    description = st.text_area("Description")
    requirements = st.text_area("Requirements")
    deadline = st.date_input("Deadline")
    status = st.selectbox("Status", ["Open", "Closed"])

    submitted = st.form_submit_button("Create Job")
    if submitted:
        new_job = {
            "title": title,
            "company": company,
            "description": description,
            "requirements": requirements,
            "deadline": str(deadline), # since our deadline needs to be converted to str for json
            "status": status,
        }
        response = requests.post(
            "http://api:4000/jobs", json=new_job, params={"recruiterID": recruiter_id}
        )
        if response.status_code == 201:
            st.success("Job post creation successful.")
            fetch_jobs()  # refresh jobs list
        else:
            st.error("Failed to create job post.")
