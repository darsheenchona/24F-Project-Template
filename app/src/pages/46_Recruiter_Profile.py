import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Manage Profile")

# fetch recruiter profile details
st.write("### Your Profile")
recruiter_id = st.session_state.get("recruiter_id", 24)
response = requests.get("http://api:4000/recruiter/profile",  params={"recruiterID": recruiter_id})
if response.status_code == 200:
    profile = response.json()
    st.write(f"**Name:** {profile['name']}")
    st.write(f"**Email:** {profile['email']}")
    st.write(f"**Company:** {profile['company']}")
    st.write(f"**Posted Job Count:** {profile['positionPostedCount']}")
    st.write(f"**Recruiter Type:** {profile['recruiterType']}")
else:
    st.error("Failed to fetch profile information.")

# update recruiter profile
st.write("### Update Profile")
with st.form(key="update_profile_form"):
    name = st.text_input("Name", value=profile.get("name", ""))
    email = st.text_input("Email", value=profile.get("email", ""))
    company = st.text_input("Company", value=profile.get("company", ""))
    recruiter_type = st.selectbox("Recruiter Type", ["In-house", "Agency"], index=0 if profile.get("recruiterType") == "In-house" else 1)

    submitted = st.form_submit_button("Update Profile")
    if submitted:
        update_payload = {
            "name": name,
            "email": email,
            "company": company,
            "recruiterType": recruiter_type,
        }
        response = requests.put("http://api:4000/recruiter/profile", json=update_payload,  params={"recruiterID": recruiter_id})
        if response.status_code == 200:
            st.success("Profile updated successfully.")
        else:
            st.error("Failed to update profile.")
