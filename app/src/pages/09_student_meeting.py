import streamlit as st
import requests
from datetime import datetime

# Set up the page
st.set_page_config(layout="wide", page_title="Student Meetings")
st.title("Student Meetings Management")

# Sidebar for student ID input
student_id = st.sidebar.text_input("Enter Student ID")

if student_id:
    # Fetch and display existing meetings
    st.subheader("Your Meetings")
    response = requests.get("http://api:4000/advisor-meetings", params={"studentID": student_id})

    if response.status_code == 200:
        meetings = response.json()
        if meetings:
            for meeting in meetings:

                with st.expander(f"Meeting with Advisor ID: {meeting['advisor_id']}"):
                    st.write(f"**DateTime:** {meeting['meeting_date_time']}")
                    st.write(f"**Purpose:** {meeting['purpose']}")
                    st.write(f"**Notes:** {meeting.get('notes', 'N/A')}")

                    meeting_date = None
                    meeting_time = None
                    # Form to update the meeting
                    with st.form(key=f"update_form_{meeting['meeting_id']}"):
                        new_date = st.date_input("Date", value=meeting_date)
                        new_time = st.time_input("Time", value=meeting_time)
                        new_purpose = st.text_area("New Purpose", value=meeting['purpose'])
                        new_notes = st.text_area("New Notes", value=meeting.get('notes', ''))
                        submitted = st.form_submit_button("Update Meeting")
                        if submitted:
                            new_datetime = datetime.combine(new_date, new_time)
                            payload = {
                                "meetingDateTime": new_datetime.isoformat(),
                                "purpose": new_purpose,
                                "notes": new_notes,
                            }
                            update_response = requests.put(
                                f"http://api:4000/advisor-meetings/{meeting['meeting_id']}",
                                json=payload
                            )
                            if update_response.status_code == 200:
                                st.success("Meeting updated successfully.")
                            else:
                                st.error("Failed to update meeting.")

                    # Button to cancel the meeting
                    if st.button("Cancel Meeting", key=f"cancel_{meeting['meeting_id']}"):
                        cancel_response = requests.delete(f"http://api:4000/advisor-meetings/{meeting['meeting_id']}")
                        if cancel_response.status_code == 200:
                            st.success("Meeting canceled successfully.")
                        else:
                            st.error("Failed to cancel meeting.")
        else:
            st.info("No meetings found.")
    else:
        st.error("Failed to fetch meetings.")

    # Schedule a new meeting
    st.subheader("Schedule a New Meeting")
    with st.form(key="schedule_meeting_form"):
        advisor_id = st.text_input("Advisor ID")
        date_input = st.date_input("Date", key="schedule_date")
        time_input = st.time_input("Time", key="schedule_time")
        purpose = st.text_area("Purpose")
        notes = st.text_area("Notes (Optional)")
        submitted = st.form_submit_button("Schedule Meeting")
        if submitted:
            new_datetime = datetime.combine(date_input, time_input)
            payload = {
                "StudentID": student_id,
                "AdvisorID": advisor_id,
                "MeetingDateTime": new_datetime.isoformat(),
                "Purpose": purpose,
                "Notes": notes,
            }
            response = requests.post("http://api:4000/advisor-meetings", json=payload)
            if response.status_code == 201:
                st.success("Meeting scheduled successfully.")
            else:
                st.error("Failed to schedule meeting.")
