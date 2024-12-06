from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Create a Blueprint for tickets
tickets = Blueprint('tickets', __name__)

# ------------------------------------------------------------
# Get all tickets
@tickets.route('/tickets', methods=['GET'])
def get_all_tickets():
    query = '''
        SELECT ticket_id, title, description, status, created_at
        FROM tickets
    '''
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()
    
    # Send the data back as JSON
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Get ticket details by ID
@tickets.route('/ticket/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    query = f'''
        SELECT ticket_id, title, description, status, created_at
        FROM tickets
        WHERE ticket_id = {ticket_id}
    '''
    
    # Logging for debugging
    current_app.logger.info(f"GET /ticket/{ticket_id} query={query}")
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchone()
    
    # Send response
    if theData:
        response = make_response(jsonify(theData))
        response.status_code = 200
    else:
        response = make_response(jsonify({"error": "Ticket not found"}))
        response.status_code = 404
    return response

# ------------------------------------------------------------
# Add a new ticket
@tickets.route('/ticket', methods=['POST'])
def create_ticket():
    ticket_data = request.json
    current_app.logger.info(ticket_data)
    
    # Extract the data
    title = ticket_data.get('title')
    description = ticket_data.get('description')
    status = ticket_data.get('status', 'Open')  # Default to 'Open'

    query = f'''
        INSERT INTO tickets (title, description, status, created_at)
        VALUES ('{title}', '{description}', '{status}', NOW())
    '''
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Ticket created successfully")
    response.status_code = 201
    return response

# ------------------------------------------------------------
# Update an existing ticket
@tickets.route('/ticket/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket_data = request.json
    current_app.logger.info(ticket_data)
    
    # Extract the data
    title = ticket_data.get('title')
    description = ticket_data.get('description')
    status = ticket_data.get('status')

    query = f'''
        UPDATE tickets
        SET title = '{title}', description = '{description}', status = '{status}'
        WHERE ticket_id = {ticket_id}
    '''
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Ticket updated successfully")
    response.status_code = 200
    return response

# ------------------------------------------------------------
# Delete a ticket
@tickets.route('/ticket/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    query = f'''
        DELETE FROM tickets
        WHERE ticket_id = {ticket_id}
    '''
    
    # Execute the query
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Ticket deleted successfully")
    response.status_code = 200
    return response
