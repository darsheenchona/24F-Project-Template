import streamlit as st
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

if st.button('View Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_student_profile.py')

if st.button('Applications', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/06_Student_application.py')

if st.button('Bookmarks', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/07_student_bookmark.py')

if st.button('Recommendations', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/08_student_recommendation.py')

if st.button('Advisor Meetings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/09_student_meeting.py')
