import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Manage Tickets")
# Function to fetch tickets
def fetch_tickets():
    try:
        response = requests.get("http://api:4000/it/tickets")
        response.raise_for_status()  # Raise an error for non-200 status codes
        tickets = response.json()  # Convert JSON response to Python dict
        st.session_state.tickets = tickets  # Cache the tickets in session state
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tickets: {e}")
        st.session_state.tickets = []

# Initialize session state for tickets
if "tickets" not in st.session_state:
    st.session_state.tickets = []

# Initialize the ticket being edited
if "ticket_to_update" not in st.session_state:
    st.session_state.ticket_to_update = None


# Function to update a ticket
def update_ticket(ticket_id, update_payload):
    try:
        response = requests.put(f"http://api:4000/it/tickets/{ticket_id}", json=update_payload)
        if response.status_code == 200:
            st.success("Ticket updated successfully.")
            st.session_state.ticket_to_update = None  # Reset edit state
            fetch_tickets()  # Refresh tickets
        else:
            st.error("Failed to update ticket.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating ticket: {e}")


# Fetch tickets if not already loaded
if not st.session_state.tickets:
    fetch_tickets()

# Display tickets
st.write("### Existing Tickets")
for ticket in st.session_state.tickets:
    # Display ticket information
    st.write(
        f"**Ticket ID:** {ticket['TicketID']} | **Status:** {ticket['TicketStatus']} | "
        f"**Submitted At:** {ticket['TicketTime']}"
    )
    st.write(f"Details: {ticket['TicketDetails']}")
    st.write(f"Fulfilled By: {ticket['FufilledBy']}")

    # Editing ticket
    if st.session_state.ticket_to_update == ticket["TicketID"]:
        with st.form(key=f"edit_ticket_{ticket['TicketID']}"):
            updated_status = st.selectbox(
                "Status",
                ["Open", "In Progress", "Closed"],
                index=["Open", "In Progress", "Closed"].index(ticket["TicketStatus"]),
            )
            updated_details = st.text_area("Details", value=ticket["TicketDetails"])

            submitted = st.form_submit_button("Submit Update")
            if submitted:
                update_payload = {
                    "TicketStatus": updated_status,
                    "TicketDetails": updated_details,
                }
                update_ticket(ticket["TicketID"], update_payload)

    elif st.session_state.ticket_to_update is None:
        if st.button(f"Update Ticket {ticket['TicketID']}", key=f"update_btn_{ticket['TicketID']}"):
            st.session_state.ticket_to_update = ticket["TicketID"]


