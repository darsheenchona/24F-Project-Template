import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Generate Reports")

# fetch existing reports
response = requests.get("http://api:4000/reports")
if response.status_code == 200:
    reports = response.json()
else:
    st.error("Failed to fetch reports.")
    reports = []

st.write("### Existing Reports")
for report in reports:
    st.write(f"**{report['title']}** - Generated on {report['dateGenerated']}")
    if st.button(f"Delete {report['title']}", key=f"delete_{report['reportID']}"):
        response = requests.delete(f"http://api:4000/reports/{report['reportID']}")
        if response.status_code == 200:
            st.success(f"Deleted {report['title']}")
        else:
            st.error("Failed to delete report.")

# generate new report
recruiter_id = st.session_state.get("recruiter_id")
st.write("### Generate New Report")
with st.form(key="generate_report_form"):
    title = st.text_input("Report Title")
    description = st.text_area("Report Description")
    submitted = st.form_submit_button("Generate Report")

    if submitted:
        payload = {
            "title": title,
            "description": description,
        }
        response = requests.post("http://api:4000/reports", json=payload,  params={"recruiterID": recruiter_id})
        if response.status_code == 201:
            st.success("Report generated successfully.")
        else:
            st.error("Failed to generate report.")
