from datetime import datetime
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Blueprint for co-op advisor endpoints
coop_advisor = Blueprint('coop_advisor', __name__)

# ------------------------------------------------------------
# retrieve co-op advisor profile info
@coop_advisor.route('/coop_advisor/profile', methods=['GET'])
def get_coop_advisor_profile():
    advisor_id = request.args.get('advisorID')
    if not advisor_id:
        return make_response("Advisor ID is required", 400)

    query = '''
        SELECT Users.name, Users.email, CoOpAdvisors.department, CoOpAdvisors.advisingHistoryCount
        FROM CoOpAdvisors 
        JOIN Users ON CoOpAdvisors.userID = Users.userID
        WHERE CoOpAdvisors.advisorID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (advisor_id,))
    profile = cursor.fetchone()

    if not profile:
        return make_response("Co-op Advisor not found", 404)

    return make_response(jsonify(profile), 200)


# update co-op advisor profile
@coop_advisor.route('/coop_advisor/profile', methods=['PUT'])
def update_coop_advisor_profile():
    advisor_id = request.args.get('advisorID')
    profile = request.json

    query = '''
        UPDATE CoOpAdvisors
        SET department = %s
        WHERE advisorID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (profile["department"], advisor_id))

    query_users = '''
        UPDATE Users
        SET name = %s, email = %s
        WHERE userID = (SELECT userID FROM CoOpAdvisors WHERE advisorID = %s)
    '''
    cursor.execute(query_users, (profile["name"], profile["email"], advisor_id))
    db.get_db().commit()

    return make_response("Co-op Advisor profile updated successfully", 200)


# ------------------------------------------------------------
# retrieve list of students advised by a co-op advisor
@coop_advisor.route('/Students', methods=['GET'])
def get_advised_students():
    advisor_id = request.args.get('advisorID')
    if not advisor_id:
        return make_response("Advisor ID is required", 400)

    query = '''
        SELECT Students.studentID, Users.name AS student_name, Students.major
        FROM Students
        JOIN Users ON Students.userID = Users.userID
        WHERE Students.advisorID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (advisor_id,))
    students = cursor.fetchall()

    if not students:
        return make_response("No students found for the specified advisor", 404)

    return make_response(jsonify(students), 200)



# retrieve specific student advised by a co-op advisor
@coop_advisor.route('/students/<StudentID>', methods=['GET'])
def get_student_details(StudentID):
    query = '''
        SELECT Users.name, Students.major, Students.gpa, Students.email
        FROM Students
        JOIN Users ON Students.userID = Users.userID
        WHERE Students.studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (StudentID,))
    student = cursor.fetchone()

    if not student:
        return make_response("Student not found", 404)

    return make_response(jsonify(student), 200)



# update student details
@coop_advisor.route('/students/<StudentID>', methods=['PUT'])
def update_student_details(StudentID):
    data = request.json
    query = '''
        UPDATE Students
        SET major = %s, gpa = %s, email = %s
        WHERE studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data["major"], data["gpa"], data["email"], StudentID))
    db.get_db().commit()

    return make_response("Student details updated successfully", 200)


# ------------------------------------------------------------
@coop_advisor.route('/students/<int:studentID>/placements', methods=['GET'])
def get_student_placements(studentID):
    query = f'''
        SELECT placementID, company, position, startDate, endDate, status
        FROM Placement
        WHERE StudentID = {studentID}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    placements = cursor.fetchall()
    
    # Log the result of the query
    logger.info(f"Query result: {placements}")

    if not placements:
        return make_response(jsonify({"error": "No placements found for this student."}), 404)

    return make_response(jsonify(placements), 200)

# Add a new placement for a student
@coop_advisor.route('/students/<StudentID>/placements', methods=['POST'])
def add_student_placement(StudentID):
    data = request.json
    
    # Validate required fields
    if not all(field in data for field in ['company', 'position', 'startDate', 'endDate', 'status']):
        return make_response(jsonify({"error": "Missing required fields"}), 400)
    
    # Using string interpolation
    query = f'''
        INSERT INTO Placement (studentID, company, position, startDate, endDate, status)
        VALUES ({StudentID}, '{data["company"]}', '{data["position"]}', '{data["startDate"]}', '{data["endDate"]}', '{data["status"]}')
    '''
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute(query)
        db.get_db().commit()
        return make_response(jsonify({"message": "Placement added successfully."}), 201)
    except Exception as e:
        logger.error(f"Error inserting placement: {e}")
        return make_response(jsonify({"error": "Failed to add placement."}), 500)


# Update placement details
@coop_advisor.route('/students/<StudentID>/placements/<placementID>', methods=['PUT'])
def update_placement(StudentID, placementID):
    data = request.json
    
    # Validate required fields
    if not all(field in data for field in ['company', 'position', 'startDate', 'endDate', 'status']):
        return make_response(jsonify({"error": "Missing required fields"}), 400)
    
    # Using string interpolation
    query = f'''
        UPDATE Placement
        SET company = '{data["company"]}', position = '{data["position"]}', startDate = '{data["startDate"]}', endDate = '{data["endDate"]}', status = '{data["status"]}'
        WHERE placementID = {placementID} AND studentID = {StudentID}
    '''
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute(query)
        db.get_db().commit()
        return make_response(jsonify({"message": "Placement updated successfully."}), 200)
    except Exception as e:
        logger.error(f"Error updating placement: {e}")
        return make_response(jsonify({"error": "Failed to update placement."}), 500)



# Delete placement
@coop_advisor.route('/students/<StudentID>/placements/<placementID>', methods=['DELETE'])
def delete_placement(StudentID, placementID):
    # Using string interpolation
    query = f'''
        DELETE FROM Placement
        WHERE placementID = {placementID} AND StudentID = {StudentID}
    '''
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute(query)
        db.get_db().commit()
        return make_response(jsonify({"message": "Placement deleted successfully."}), 200)
    except Exception as e:
        logger.error(f"Error deleting placement: {e}")
        return make_response(jsonify({"error": "Failed to delete placement."}), 500)



# ------------------------------------------------------------
# retrieve reports for co-op advisor
@coop_advisor.route('/reports', methods=['GET'])
def get_reports():
    query = '''
        SELECT reportID, title, description, dateGenerated
        FROM Reports
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    reports = cursor.fetchall()

    return make_response(jsonify(reports), 200)


# generate a new report for co-op advisor
@coop_advisor.route('/reports', methods=['POST'])
def generate_report():
    data = request.json
    advisor_id = request.args.get('advisorID')
    query = '''
        INSERT INTO Reports (title, description, dateGenerated, GeneratedBy)
        VALUES (%s, %s, NOW(), %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data["title"], data["description"], advisor_id))
    db.get_db().commit()

    return make_response("Report generated successfully", 201)


# delete a specific report
@coop_advisor.route('/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    query = '''
        DELETE FROM Reports WHERE reportID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (report_id,))
    db.get_db().commit()

    return make_response("Report deleted successfully", 200)


# Blueprint for recruiter-related endpoints
@coop_advisor.route('/employers', methods=['GET'])
def get_employers():
    query = '''
        SELECT employerID, name, industry, location
        FROM Employers
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    employers = cursor.fetchall()

    if not employers:
        return make_response("No employers found", 404)

    return make_response(jsonify(employers), 200)

