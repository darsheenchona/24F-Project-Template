import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime
import requests

st.set_page_config(layout="wide")
SideBarLinks()
st.title("IT Management Dashboard")

# Function to fetch tickets
def fetch_tickets():
    try:
        response = requests.get("http://api:4000/it/tickets")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tickets: {e}")
        return []

# Function to fetch employees
def fetch_employees():
    try:
        response = requests.get("http://api:4000/it/employees")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching employees: {e}")
        return []

# Function to fetch assets
def fetch_assets():
    try:
        response = requests.get("http://api:4000/it/assets")
        response.raise_for_status()
        assets = response.json()
        return assets
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching assets: {e}")
        return []


# Function to fetch uncompleted tickets
def get_uncompleted_tickets(tickets):
    return [ticket for ticket in tickets if ticket["TicketStatus"] == "Open"]

# Function to fetch active assets
def get_active_assets(assets):
    return [asset for asset in assets if asset["ITStatus"] == "Operational"]

# Layout
tickets = fetch_tickets()
employees = fetch_employees()
assets = fetch_assets()

# Top Row: Uncompleted Tickets and Create New Ticket
col1, col2 = st.columns(2)

# Top Left: Uncompleted Tickets
with col1:
    st.subheader("Uncompleted Tickets")
    uncompleted_tickets = get_uncompleted_tickets(tickets)
    if uncompleted_tickets:
        for ticket in uncompleted_tickets:
            st.write(
                f"**ID:** {ticket['TicketID']} | **Details:** {ticket['TicketDetails']} | **Submitted:** {ticket['TicketTime']}"
            )
    else:
        st.write("No uncompleted tickets found.")

# Top Right: Create New Ticket
with col2:
    st.subheader("Create New Ticket")
    with st.form(key="create_ticket_form"):
        details = st.text_area("Details")
        status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
        fulfilled_by = st.selectbox(
            "Fulfilled By (Employee ID)",
            options=[emp["ITEmpID"] for emp in employees],
            format_func=lambda emp_id: f"{emp_id} - {next((emp['EmpFirstName'] + ' ' + emp['EmpLastName'] for emp in employees if emp['ITEmpID'] == emp_id), 'Unknown')}"
        )
        submitted = st.form_submit_button("Create Ticket")
        if submitted:
            new_ticket = {
                "TicketDetails": details,
                "TicketStatus": status,
                "TicketTime": datetime.now().isoformat(),
                "FufilledBy": fulfilled_by,
            }
            try:
                response = requests.post("http://api:4000/it/tickets", json=new_ticket)
                if response.status_code == 201:
                    st.success("Ticket created successfully.")
                else:
                    st.error("Failed to create ticket.")
                    st.write("Response Content:", response.text)
            except requests.exceptions.RequestException as e:
                st.error(f"Error creating ticket: {e}")

# Bottom Row: Employee List and Metrics
col3, col4 = st.columns(2)

# Bottom Left: Employee Names and Emails
with col3:
    st.subheader("Employees")
    if employees:
        for employee in employees:
            st.write(
                f"**ID:** {employee['ITEmpID']} | **Name:** {employee['EmpFirstName']} {employee['EmpLastName']} | **Email:** {employee['Email']}"
            )
    else:
        st.write("No employees found.")

# Bottom Right: Metrics and Active Assets
with col4:
    st.subheader("Active Assets")
    active_assets = get_active_assets(assets)
    if active_assets:
        for asset in active_assets:
            st.write(f"**ID:** {asset['assetID']} | **Name:** {asset['assetName']} | **Status:** {asset['ITStatus']}")
    else:
        st.write("No active assets found.")
