import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

logger = logging.getLogger(__name__)

# Set the page layout to wide
st.set_page_config(layout='wide')

# Display the appropriate sidebar links for the role of the logged-in user
SideBarLinks()

# Display a welcome message with the Co-op Advisor's name
st.title(f"Welcome Co-Op Advisor, {st.session_state['first_name']}.")

# Display buttons to navigate to the relevant pages for Co-op Advisor
st.subheader("Co-op Advisor Dashboard")

# Button to navigate to "View Student Progress"
if st.button('View Student Progress', type='primary', use_container_width=True):
    st.switch_page('pages/21_Student_Progress.py')

# Button to navigate to "Update Co-op Placement"
if st.button('Update Co-op Placement', type='primary', use_container_width=True):
    st.switch_page('pages/22_Update_Placement.py')

# Button to navigate to "Manage Employers"
if st.button('Manage Employers', type='primary', use_container_width=True):
    st.switch_page('pages/23_Manage_Employer.py')


# Button to navigate to "View Advisor Profile"
if st.button('Advisor Profile', type='primary', use_container_width=True):
    st.switch_page('pages/24_Advisor_Profile.py')
