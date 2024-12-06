import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Notifications")

# assume recruiter_id is stored in session state
recruiter_id = st.session_state.get("recruiter_id")

# initialize session state for notifications
if "notifications" not in st.session_state:
    params = {"recruiterID": recruiter_id}
    response = requests.get("http://api:4000/notifications", params=params)
    if response.status_code == 200:
        notifications = response.json()
        st.session_state.notifications = notifications
    else:
        st.error("Failed to fetch notifications.")
        st.session_state.notifications = []

# split notifications into unread and read for better organization
unread_notifications = [n for n in st.session_state.notifications if not n.get("isRead", False)]
read_notifications = [n for n in st.session_state.notifications if n.get("isRead", False)]

st.write("### Unread Notifications")
if unread_notifications:
    for notification in unread_notifications:
        with st.expander(f"Notification: {notification['notificationType']}"):
            st.write(f"**Content**: {notification['content']}")
            st.write(f"**Date Sent**: {notification['dateSent']}")
            if st.button("Mark as Read", key=f"mark_read_{notification['notificationID']}"):
                # Call the API to mark the notification as read
                response = requests.put(f"http://api:4000/notifications/{notification['notificationID']}")
                if response.status_code == 200:
                    st.success("Notification marked as read.")
                    # Update session state to hide the notification
                    notification["isRead"] = True
else:
    st.info("No unread notifications found.")

# add collapsible section for read notifications
with st.expander("View Read Notifications"):
    if read_notifications:
        for notification in read_notifications:
            st.write(f"**Type**: {notification['notificationType']}")
            st.write(f"**Content**: {notification['content']}")
            st.write(f"**Date Sent**: {notification['dateSent']}")
            st.write("---")
    else:
        st.info("No read notifications found.")

# fetch all candidates for the recruiter, simulating all potential candidates they can notify
response_candidates = requests.get(f"http://api:4000/recruiter/{recruiter_id}/candidates")
if response_candidates.status_code == 200:
    candidates = response_candidates.json()
else:
    st.error("Failed to fetch candidates.")
    candidates = []

# send new notification
st.write("### Send New Notification")
if candidates:
    with st.form(key="send_notification_form"):
        # Create a dropdown of candidates
        candidate_options = {f"{candidate['candidate_name']} (ID: {candidate['studentID']})": candidate['studentID'] for candidate in candidates}
        candidate_selection = st.selectbox("Select Candidate", options=list(candidate_options.keys()))
        user_id = candidate_options[candidate_selection]

        content = st.text_area("Notification Content")
        notification_type = st.selectbox("Notification Type", ["Reminder", "Alert", "Update"], index=0)
        submitted = st.form_submit_button("Send Notification")

        if submitted:
            payload = {
                "userID": user_id,
                "content": content,
                "notificationType": notification_type,
            }
            response = requests.post("http://api:4000/notifications", json=payload)
            if response.status_code == 201:
                st.success("Notification sent successfully.")
            else:
                st.error("Failed to send notification.")
else:
    st.warning("No candidates available to send notifications.")
