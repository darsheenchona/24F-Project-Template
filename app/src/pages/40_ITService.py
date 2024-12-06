import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome to the IT Service Portal, {st.session_state['first_name']}.")
st.write('')
st.write('')

if st.button('Main Dashboard', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/41_Dashboard.py')

if st.button('View All Tickets', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/42_Tickets.py')

if st.button('View All Assets', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/43_Assets.py')