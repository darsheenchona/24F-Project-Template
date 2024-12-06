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
    query = '''
        SELECT Students.studentID, Users.name AS student_name, Students.major
        FROM Students
        JOIN Users ON Students.userID = Users.userID
        WHERE Students.advisorID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (advisor_id,))
    students = cursor.fetchall()

    return make_response(jsonify(students), 200)


# retrieve specific student advised by a co-op advisor
@coop_advisor.route('/students/<student_id>', methods=['GET'])
def get_student_details(student_id):
    query = '''
        SELECT Users.name, Students.major, Students.gpa, Students.email
        FROM Students
        JOIN Users ON Students.userID = Users.userID
        WHERE Students.studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (student_id,))
    student = cursor.fetchone()

    if not student:
        return make_response("Student not found", 404)

    return make_response(jsonify(student), 200)


# update student details
@coop_advisor.route('/students/<student_id>', methods=['PUT'])
def update_student_details(student_id):
    data = request.json
    query = '''
        UPDATE Students
        SET major = %s, gpa = %s, email = %s
        WHERE studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data["major"], data["gpa"], data["email"], student_id))
    db.get_db().commit()

    return make_response("Student details updated successfully", 200)


# ------------------------------------------------------------
# retrieve the student's co-op placement history
@coop_advisor.route('/students/<student_id>/placements', methods=['GET'])
def get_student_placements(student_id):
    query = '''
        SELECT Placement.placementID, Placement.company, Placement.position, Placement.startDate, Placement.endDate, Placement.status
        FROM Placement
        WHERE Placement.studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (student_id,))
    placements = cursor.fetchall()

    return make_response(jsonify(placements), 200)


# add a new placement for a student
@coop_advisor.route('/students/<student_id>/placements', methods=['POST'])
def add_student_placement(student_id):
    data = request.json
    query = '''
        INSERT INTO Placement (studentID, company, position, startDate, endDate, status)
        VALUES (%s, %s, %s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (student_id, data["company"], data["position"], data["startDate"], data["endDate"], data["status"]))
    db.get_db().commit()

    return make_response("Placement added successfully", 201)


# update placement details
@coop_advisor.route('/students/<student_id>/placements/<placement_id>', methods=['PUT'])
def update_placement(student_id, placement_id):
    data = request.json
    query = '''
        UPDATE Placement
        SET company = %s, position = %s, startDate = %s, endDate = %s, status = %s
        WHERE placementID = %s AND studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data["company"], data["position"], data["startDate"], data["endDate"], data["status"], placement_id, student_id))
    db.get_db().commit()

    return make_response("Placement updated successfully", 200)


# delete placement
@coop_advisor.route('/students/<student_id>/placements/<placement_id>', methods=['DELETE'])
def delete_placement(student_id, placement_id):
    query = '''
        DELETE FROM Placement
        WHERE placementID = %s AND studentID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (placement_id, student_id))
    db.get_db().commit()

    return make_response("Placement deleted successfully", 200)


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

