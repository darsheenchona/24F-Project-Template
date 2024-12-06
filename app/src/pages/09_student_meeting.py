import streamlit as st
import requests

def display():
    st.title("Advisor Meetings")
    st.write("Your upcoming meetings with advisors:")

    response = requests.get("http://localhost:5000/api/student/advisor-meetings")
    if response.status_code == 200:
        meetings = response.json()
        for meeting in meetings:
            st.subheader(f"Meeting with {meeting['advisor_name']}")
            st.write(f"**Date:** {meeting['date']}")
            st.write(f"**Time:** {meeting['time']}")
            st.write(f"**Purpose:** {meeting['purpose']}")
            st.button("Update Meeting", key=f"update_{meeting['id']}", on_click=update_meeting, args=(meeting['id'],))
            st.button("Cancel Meeting", key=f"remove_{meeting['id']}", on_click=remove_meeting, args=(meeting['id'],))
    else:
        st.error("Unable to fetch meetings.")

    st.write("---")
    st.subheader("Schedule a New Meeting")
    advisor_name = st.text_input("Advisor Name")
    date = st.date_input("Date")
    time = st.time_input("Time")
    purpose = st.text_area("Purpose")
    if st.button("Schedule Meeting"):
        schedule_meeting(advisor_name, date, time, purpose)

def schedule_meeting(advisor_name, date, time, purpose):
    payload = {"advisor_name": advisor_name, "date": str(date), "time": str(time), "purpose": purpose}
    response = requests.post("http://localhost:5000/api/student/advisor-meetings", json=payload)
    if response.status_code == 201:
        st.success("Meeting scheduled successfully!")
    else:
        st.error("Failed to schedule meeting.")

def update_meeting(meeting_id):
    purpose = st.text_area("New Purpose")
    payload = {"purpose": purpose}
    response = requests.put(f"http://localhost:5000/api/student/advisor-meetings/{meeting_id}", json=payload)
    if response.status_code == 200:
        st.success("Meeting updated successfully!")
    else:
        st.error("Failed to update meeting.")

def remove_meeting(meeting_id):
    response = requests.delete(f"http://localhost:5000/api/student/advisor-meetings/{meeting_id}")
    if response.status_code == 200:
        st.success("Meeting canceled successfully!")
    else:
        st.error("Failed to cancel meeting.")
