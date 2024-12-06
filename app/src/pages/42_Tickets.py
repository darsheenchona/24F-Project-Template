import streamlit as st
import requests
import pandas as pd

# Flask API base URL
API_URL = "http://127.0.0.1:5000/api"

st.title("All Tickets")

# Fetch tickets from the backend
@st.cache_data
def fetch_tickets():
    try:
        response = requests.get(f"{API_URL}/tickets")
        response.raise_for_status()  # Raise an error for bad status codes
        tickets = response.json()  # Convert JSON response to Python dict
        return tickets
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tickets: {e}")
        return []

# Display tickets in a table
def display_tickets():
    tickets = fetch_tickets()
    if tickets:
        tickets_df = pd.DataFrame(tickets)
        tickets_df.columns = ["Ticket ID", "Time", "Status", "Details", "Fulfilled By"]
        st.dataframe(tickets_df, use_container_width=True)
    else:
        st.write("No tickets available.")

st.write("### Existing Tickets")
display_tickets()

# Add a form to create a new ticket
st.write("### Add a New Ticket")

with st.form(key="new_ticket_form"):
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    details = st.text_area("Details")
    fulfilled_by = st.number_input("Fulfilled By (Employee ID)", min_value=1, step=1)
    submit_button = st.form_submit_button("Add Ticket")

if submit_button:
    # Send POST request to create a new ticket
    try:
        response = requests.post(
            f"{API_URL}/tickets",
            json={"TicketStatus": status, "TicketDetails": details, "FufilledBy": int(fulfilled_by)},
        )
        if response.status_code == 201:
            st.success("Ticket added successfully!")
            # Refresh the ticket list after adding a new ticket
            display_tickets()
        else:
            st.error(f"Failed to add ticket: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
