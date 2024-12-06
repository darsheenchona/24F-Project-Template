import streamlit as st
from src.pages import student_profile, applications_page, bookmarks_page, recommendations_page, advisor_meetings_page

def display():
    st.title("Co-op Seeker Dashboard")
    st.write("Welcome! Select a feature to explore:")
    st.button("View Profile", on_click=student_profile.display)
    st.button("Applications", on_click=applications_page.display)
    st.button("Bookmarks", on_click=bookmarks_page.display)
    st.button("Recommendations", on_click=recommendations_page.display)
    st.button("Advisor Meetings", on_click=advisor_meetings_page.display)
