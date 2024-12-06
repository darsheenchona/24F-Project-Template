import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime, date, time
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Job Details Management")

# fetch the recruiter's jobs
recruiter_id = st.session_state.get("recruiter_id")
response = requests.get("http://api:4000/jobs", params={"recruiterID": recruiter_id})

if response.status_code == 200:
    jobs = response.json()
    # display job posted by recruiter to manage
    if jobs:
        job_options = {f"{job['title']} at {job['company']}": job['jobID'] for job in jobs}
        job_selection = st.selectbox("Select Job to Manage", options=list(job_options.keys()))
        job_id = job_options[job_selection]
    # warn if no jobs for recruiter
    else:
        st.warning("No jobs found for this recruiter.")
        job_id = None
else:
    st.error("Failed to fetch jobs.")
    job_id = None

# based on selection
if job_id:
    st.write(f"### Managing Job: {job_selection}")

    # fetch candidates and applications
    response_candidates = requests.get(f"http://api:4000/jobs/{job_id}/candidates")
    response_applications = requests.get(f"http://api:4000/jobs/{job_id}/applications")

    if response_candidates.status_code == 200 and response_applications.status_code == 200:
        candidates = response_candidates.json()
        applications = response_applications.json()

        # map applications to candidates, since related
        applications_map = {app["studentID"]: app for app in applications}

        st.write("### Candidates and Applications")
        for candidate in candidates:
            application = applications_map.get(candidate["studentID"], {})
            with st.expander(f"{candidate['candidate_name']} - {candidate['skills']}"):
                st.write(f"**Application ID**: {application.get('applicationID', 'N/A')}")
                st.write(f"**Status**: {application.get('status', 'N/A')}")
                st.write(f"**Review Score**: {application.get('reviewScore', 'N/A')}")
                st.write(f"**Feedback**: {application.get('feedback', 'N/A')}")

                # update application status with form, given a candidate
                with st.form(key=f"update_application_form_{candidate['studentID']}"):
                    status_options = ["Pending", "Accepted", "Rejected"]
                    current_status = application.get("status", "Pending")
                    status_index = status_options.index(current_status) if current_status in status_options else 0
                    status = st.selectbox("Status", status_options, index=status_index)
                    submitted = st.form_submit_button("Submit Update")
                    if submitted:
                        payload = {"status": status}
                        response = requests.put(
                            f"http://api:4000/jobs/{job_id}/applications/{application['applicationID']}",
                            json=payload
                        )
                        if response.status_code == 200:
                            st.success(f"Updated application {application['applicationID']} successfully.")
                        else:
                            st.error("Failed to update application.")
    else:
        st.error("Failed to fetch candidates or applications.")

    # manage interviews for selected job
    st.write("### Interviews for the Job")
    response_interviews = requests.get(f"http://api:4000/jobs/{job_id}/interviews")
    if response_interviews.status_code == 200:
        interviews = response_interviews.json()
        if interviews:
            for interview in interviews:

                with st.expander(f"Interview with {interview['candidate_name']} on {interview['InterviewDateTime']}"):
                    st.write(f"**Interview ID**: {interview['interviewID']}")
                    st.write(f"**Notes**: {interview.get('notes', '')}")

                    interview_date = None
                    interview_time = None

                    # update interview
                    with st.form(key=f"update_interview_form_{interview['interviewID']}"):
                        new_date = st.date_input("Date", value=interview_date, key=f"date_{interview['interviewID']}")
                        new_time = st.time_input("Time", value=interview_time, key=f"time_{interview['interviewID']}")
                        new_notes = st.text_area("Notes", value=interview.get("notes", ""), key=f"notes_{interview['interviewID']}")
                        submitted = st.form_submit_button("Update Interview")
                        if submitted:
                            # Combine new_date and new_time into a datetime object
                            try:
                                new_datetime = datetime.combine(new_date, new_time)
                                payload = {
                                    "InterviewDateTime": new_datetime.isoformat(),
                                    "notes": new_notes
                                }
                                response = requests.put(
                                    f"http://api:4000/jobs/{job_id}/interviews/{interview['interviewID']}",
                                    json=payload
                                )
                                if response.status_code == 200:
                                    st.success("Interview updated successfully.")
                                else:
                                    st.error("Failed to update interview.")
                            except Exception as e:
                                st.error(f"Error updating interview: {e}")

                    # cancel interview option
                    delete_button = st.button(
                        f"Delete Interview {interview['interviewID']}",
                        key=f"delete_interview_{interview['interviewID']}"
                    )
                    # if selected, call delete interview endpoint
                    if delete_button:
                        delete_response = requests.delete(
                            f"http://api:4000/jobs/{job_id}/interviews/{interview['interviewID']}")
                        if delete_response.status_code == 200:
                            st.success(f"Deleted interview {interview['interviewID']} successfully.")
                        else:
                            st.error(f"Failed to delete interview: {delete_response.text}")
        else:
            st.info("No interviews scheduled for this job.")

    else:
        st.error("Failed to fetch interviews.")

    # schedule a new interview for given candidates
    st.write("### Schedule a New Interview")
    if candidates:
        with st.form(key="schedule_interview_form"):
            student_map = {f"{c['candidate_name']} (ID: {c['studentID']})": c['studentID'] for c in candidates}
            student_selection = st.selectbox("Candidate", options=list(student_map.keys()))
            student_id = student_map[student_selection]
            date_input = st.date_input("Date", key="schedule_date")
            time_input = st.time_input("Time", key="schedule_time")
            notes = st.text_area("Notes", key="schedule_notes")
            submitted = st.form_submit_button("Schedule Interview")
            if submitted:
                # combine date and time into a datetime object to match our interview schema
                try:
                    interview_datetime = datetime.combine(date_input, time_input)
                    payload = {
                        "studentID": student_id,
                        "InterviewDateTime": interview_datetime.isoformat(),
                        "notes": notes
                    }
                    response = requests.post(
                        f"http://api:4000/jobs/{job_id}/interviews",
                        json=payload
                    )
                    if response.status_code == 201:
                        st.success("Interview scheduled successfully.")
                    else:
                        st.error("Failed to schedule interview.")
                except Exception as e:
                    st.error(f"Error scheduling interview: {e}")
    else:
        st.warning("No candidates available to schedule an interview.")
