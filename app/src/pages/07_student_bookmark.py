import streamlit as st
import requests

def display():
    st.title("Bookmarks")
    st.write("Your bookmarked co-op listings:")

    response = requests.get("http://localhost:5000/api/student/bookmarks")
    if response.status_code == 200:
        bookmarks = response.json()
        for bookmark in bookmarks:
            st.subheader(f"{bookmark['job_title']} at {bookmark['company_name']}")
            st.button("Remove Bookmark", key=bookmark['id'], on_click=remove_bookmark, args=(bookmark['id'],))
    else:
        st.error("Unable to fetch bookmarks.")

    st.write("---")
    st.subheader("Add a Bookmark")
    job_title = st.text_input("Job Title")
    company_name = st.text_input("Company Name")
    if st.button("Add Bookmark"):
        add_bookmark(job_title, company_name)

def add_bookmark(job_title, company_name):
    payload = {"job_title": job_title, "company_name": company_name}
    response = requests.post("http://localhost:5000/api/student/bookmarks", json=payload)
    if response.status_code == 201:
        st.success("Bookmark added successfully!")
    else:
        st.error("Failed to add bookmark.")

def remove_bookmark(bookmark_id):
    response = requests.delete(f"http://localhost:5000/api/student/bookmarks/{bookmark_id}")
    if response.status_code == 200:
        st.success("Bookmark removed successfully!")
    else:
        st.error("Failed to remove bookmark.")
