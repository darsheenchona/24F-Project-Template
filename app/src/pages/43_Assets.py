import streamlit as st
from modules.nav import SideBarLinks
from datetime import datetime
import requests

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Manage IT Assets")

# Function to fetch IT assets
def fetch_assets():
    try:
        response = requests.get("http://api:4000/it/assets")
        response.raise_for_status()  # Raise an error for non-200 status codes
        assets = response.json()  # Convert JSON response to Python dict
        st.session_state.assets = assets  # Cache the assets in session state
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching assets: {e}")
        st.session_state.assets = []


# Initialize session state for assets
if "assets" not in st.session_state:
    st.session_state.assets = []

# Initialize the asset being edited
if "asset_to_update" not in st.session_state:
    st.session_state.asset_to_update = None

# Function to update an asset
def update_asset(asset_id, update_payload):
    try:
        response = requests.put(f"http://api:4000/it/assets/{asset_id}", json=update_payload)
        if response.status_code == 200:
            st.success("Asset updated successfully.")
            st.session_state.asset_to_update = None  # Reset edit state
            fetch_assets()  # Refresh assets
        else:
            st.error("Failed to update asset.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating asset: {e}")

# Fetch assets if not already loaded
if not st.session_state.assets:
    fetch_assets()

# Display assets
st.write("### Existing IT Assets")
for asset in st.session_state.assets:
    # Display asset information
    st.write(
        f"**Asset ID:** {asset['assetID']} | **Name:** {asset['assetName']} | "
        f"**Status:** {asset['ITStatus']} | **Type:** {asset['assetType']}"
    )
    st.write(f"Details: {asset['assetDetails']}")

    # Editing asset
    if st.session_state.asset_to_update == asset["assetID"]:
        with st.form(key=f"edit_asset_{asset['assetID']}"):
            updated_name = st.text_input("Asset Name", value=asset["assetName"])
            updated_status = st.selectbox(
                "Status",
                ["Active", "Inactive"],
                index=["Active", "Inactive"].index(asset["ITStatus"]),
            )
            updated_type = st.text_input("Type", value=asset["assetType"])
            updated_details = st.text_area("Details", value=asset["assetDetails"])

            submitted = st.form_submit_button("Submit Update")
            if submitted:
                update_payload = {
                    "assetName": updated_name,
                    "ITStatus": updated_status,
                    "assetType": updated_type,
                    "assetDetails": updated_details,
                }
                update_asset(asset["assetID"], update_payload)

    elif st.session_state.asset_to_update is None:
        if st.button(f"Update Asset {asset['assetID']}", key=f"update_btn_{asset['assetID']}"):
            st.session_state.asset_to_update = asset["assetID"]

# Add new asset
st.write("### Add New IT Asset")
with st.form(key="add_asset_form"):
    asset_name = st.text_input("Asset Name")
    asset_status = st.selectbox("Status", ["Active", "Inactive"])
    asset_type = st.text_input("Type")
    asset_details = st.text_area("Details")
    submitted = st.form_submit_button("Add Asset")
    if submitted:
        new_asset = {
            "assetName": asset_name,
            "ITStatus": asset_status,
            "assetType": asset_type,
            "assetDetails": asset_details,
        }
        try:
            response = requests.post("http://api:4000/it/assets", json=new_asset)
            if response.status_code == 201:
                st.success("IT Asset added successfully.")
                fetch_assets()  # Refresh assets
            else:
                st.error("Failed to add IT asset.")
                st.write("Response Content:", response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Error adding IT asset: {e}")
