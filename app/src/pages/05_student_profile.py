import streamlit as st
import requests

def display():
    st.title("Student Profile")

    # Sidebar input for Student ID
    student_id = st.sidebar.text_input("Enter Student ID", "1")

    # Validate Student ID
    if not student_id.isdigit():
        st.error("Please enter a valid numeric Student ID.")
        return

    # Fetch and display profile information
    st.write("Fetching your profile information...")
    try:
        # Corrected API URL with query parameter
        response = requests.get(f"http://api:4000/student/students/{student_id}")
        
        if response.status_code == 200:
            profile = response.json()
            if profile:
                st.subheader("Profile Details")
                st.write(f"**Name:** {profile.get('Name', 'N/A')}")
                st.write(f"**Email:** {profile.get('Email', 'N/A')}")
                st.write(f"**Major:** {profile.get('Major', 'N/A')}")
                st.write(f"**Year:** {profile.get('Year', 'N/A')}")
                st.write(f"**Skills:** {profile.get('Skills', 'N/A')}")
                st.write(f"**Interests:** {profile.get('Interests', 'N/A')}")
            else:
                st.warning("No profile data found for the provided Student ID.")
        else:
            st.error(f"Unable to fetch profile information. Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching profile information: {e}")

# Call the display function
if __name__ == "__main__":
    display()
