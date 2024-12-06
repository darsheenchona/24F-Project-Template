import streamlit as st
import requests

def display():
    st.title("Co-op Applications")
    st.write("Here are your tracked applications:")

    # Fetch applications
    response = requests.get("http://localhost:5000/api/student/applications")
    if response.status_code == 200:
        applications = response.json()
        for app in applications:
            st.subheader(f"{app['job_title']} at {app['company_name']}")
            st.write(f"**Status:** {app['status']}")
            st.write(f"**Deadline:** {app['deadline']}")
            st.button("Update Status", key=f"update_{app['id']}", on_click=update_application, args=(app['id'],))
            st.button("Remove Application", key=f"remove_{app['id']}", on_click=remove_application, args=(app['id'],))
    else:
        st.error("Unable to fetch applications.")

    st.write("---")
    st.subheader("Add a New Application")
    job_title = st.text_input("Job Title")
    company_name = st.text_input("Company Name")
    status = st.selectbox("Status", ["Pending", "Accepted", "Rejected"])
    if st.button("Add Application"):
        add_application(job_title, company_name, status)

def add_application(job_title, company_name, status):
    payload = {"job_title": job_title, "company_name": company_name, "status": status}
    response = requests.post("http://localhost:5000/api/student/applications", json=payload)
    if response.status_code == 201:
        st.success("Application added successfully!")
    else:
        st.error("Failed to add application.")

def update_application(app_id):
    status = st.selectbox("New Status", ["Pending", "Accepted", "Rejected"])
    payload = {"status": status}
    response = requests.put(f"http://localhost:5000/api/student/applications/{app_id}", json=payload)
    if response.status_code == 200:
        st.success("Application updated successfully!")
    else:
        st.error("Failed to update application.")

def remove_application(app_id):
    response = requests.delete(f"http://localhost:5000/api/student/applications/{app_id}")
    if response.status_code == 200:
        st.success("Application removed successfully!")
    else:
        st.error("Failed to remove application.")
