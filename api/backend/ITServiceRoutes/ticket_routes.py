from flask import Blueprint, jsonify, request, make_response, current_app
from backend.db_connection import db

# Create the Blueprint
it_admins = Blueprint('it_admins', __name__)

# ------------------------------------------------------------
# GET: Fetch all tickets
@it_admins.route('/it/tickets', methods=['GET'])
def get_tickets():
    query = "SELECT * FROM Tickets"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    the_data = cursor.fetchall()
    return jsonify(the_data), 200

# POST: Create a new ticket
@it_admins.route('/it/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    query = f"""
        INSERT INTO Tickets (TicketStatus, TicketDetails, FufilledBy)
        VALUES ('{data['TicketStatus']}', '{data['TicketDetails']}', {data['FufilledBy']})
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Ticket created successfully", 201)

# PUT: Update a ticket status
@it_admins.route('/it/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket_status(ticket_id):
    data = request.json
    query = f"""
        UPDATE Tickets
        SET TicketStatus = '{data['TicketStatus']}'
        WHERE TicketID = {ticket_id}
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Ticket updated successfully", 200)

# DELETE: Delete a ticket
@it_admins.route('/it/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    query = f"DELETE FROM Tickets WHERE TicketID = {ticket_id}"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("Ticket deleted successfully", 200)

# GET: Fetch all IT employees
@it_admins.route('/it/employees', methods=['GET'])
def get_it_employees():
    query = "SELECT * FROM ITEmployee"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    the_data = cursor.fetchall()
    return jsonify(the_data), 200

# POST: Add a new IT employee
@it_admins.route('/it/employees', methods=['POST'])
def add_it_employee():
    data = request.json
    query = f"""
        INSERT INTO ITEmployee (PlatformUsageMetrics, SystemHealthLogs, Email, EmpFirstName, EmpLastName)
        VALUES ('{data['PlatformUsageMetrics']}', '{data['SystemHealthLogs']}', '{data['Email']}', '{data['EmpFirstName']}', '{data['EmpLastName']}')
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("IT employee added successfully", 201)

# GET: Fetch all IT assets
@it_admins.route('/it/assets', methods=['GET'])
def get_it_assets():
    query = "SELECT * FROM ITAssets"
    cursor = db.get_db().cursor()
    cursor.execute(query)
    the_data = cursor.fetchall()
    return jsonify(the_data), 200

# POST: Add a new IT asset
@it_admins.route('/it/assets', methods=['POST'])
def add_it_asset():
    data = request.json
    query = f"""
        INSERT INTO ITAssets (assetName, ITStatus, assetType, assetDetails)
        VALUES ('{data['assetName']}', '{data['ITStatus']}', '{data['assetType']}', '{data['assetDetails']}')
    """
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    return make_response("IT asset added successfully", 201)
