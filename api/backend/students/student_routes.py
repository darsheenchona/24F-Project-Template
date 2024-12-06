from flask import Blueprint, request, jsonify, make_response
from backend.db_connection import db

# Define the Blueprint
student_bp = Blueprint('student_bp', __name__)


# ------------------------------------------------------------
# Retrieve student profile
@student_bp.route('/student/students/<studentID>', methods=['GET'])
def get_student_profile(studentID):
    if not studentID:
        return make_response("Missing studentID parameter", 400)

    query = f'''
        SELECT Users.Name, Users.Email, Students.Major, Students.Year, Students.Skills, Students.Interests
        FROM Students
        JOIN Users ON Students.UserID = Users.UserID
        WHERE Students.StudentID = {studentID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    profile = cursor.fetchone()

    if not profile:
        return make_response("Student not found", 404)

    return make_response(jsonify(profile), 200)


# ------------------------------------------------------------
# Retrieve applications
@student_bp.route('/applications', methods=['GET'])
def get_applications():
    student_id = request.args.get('studentID')
    query = f'''
        SELECT applicationID, jobTitle, companyName, status, deadline
        FROM Applications
        WHERE studentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    applications = cursor.fetchall()

    return make_response(jsonify(applications), 200)


# Add a new application
@student_bp.route('/applications', methods=['POST'])
def add_application():
    data = request.json
    query = f'''
        INSERT INTO Applications (studentID, jobTitle, companyName, status, deadline)
        VALUES ({data["studentID"]}, '{data["jobTitle"]}', '{data["companyName"]}', '{data["status"]}', '{data["deadline"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application added successfully", 201)


# Update an application
@student_bp.route('/applications/<application_id>', methods=['PUT'])
def update_application(application_id):
    data = request.json
    query = f'''
        UPDATE Applications
        SET status = '{data["status"]}', jobTitle = '{data["jobTitle"]}'
        WHERE applicationID = {application_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application updated successfully", 200)


# Remove an application
@student_bp.route('/applications/<application_id>', methods=['DELETE'])
def delete_application(application_id):
    query = f'''
        DELETE FROM Applications WHERE applicationID = {application_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application removed successfully", 200)


# ------------------------------------------------------------
# Retrieve bookmarks
@student_bp.route('/bookmarks', methods=['GET'])
def get_bookmarks():
    student_id = request.args.get('studentID')
    query = f'''
        SELECT bookmarkID, jobTitle, companyName
        FROM Bookmarks
        WHERE studentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    bookmarks = cursor.fetchall()

    return make_response(jsonify(bookmarks), 200)


# Add a new bookmark
@student_bp.route('/bookmarks', methods=['POST'])
def add_bookmark():
    data = request.json
    query = f'''
        INSERT INTO Bookmarks (studentID, jobTitle, companyName)
        VALUES ({data["studentID"]}, '{data["jobTitle"]}', '{data["companyName"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Bookmark added successfully", 201)


# Remove a bookmark
@student_bp.route('/bookmarks/<bookmark_id>', methods=['DELETE'])
def delete_bookmark(bookmark_id):
    query = f'''
        DELETE FROM Bookmarks WHERE bookmarkID = {bookmark_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Bookmark removed successfully", 200)


# ------------------------------------------------------------
# Fetch recommendations
@student_bp.route('/recommendations', methods=['GET'])
def get_recommendations():
    student_id = request.args.get('studentID')
    query = f'''
        SELECT recommendationID, jobTitle, companyName, matchScore
        FROM Recommendations
        WHERE studentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    recommendations = cursor.fetchall()

    return make_response(jsonify(recommendations), 200)


# ------------------------------------------------------------
# Fetch advisor meetings
@student_bp.route('/advisor-meetings', methods=['GET'])
def get_advisor_meetings():
    student_id = request.args.get('studentID')
    query = f'''
        SELECT meetingID, advisorName, meetingDate, meetingTime, purpose, notes
        FROM AdvisorMeetings
        WHERE studentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    meetings = cursor.fetchall()

    return make_response(jsonify(meetings), 200)


# Schedule a new meeting
@student_bp.route('/advisor-meetings', methods=['POST'])
def schedule_meeting():
    data = request.json
    query = f'''
        INSERT INTO AdvisorMeetings (studentID, advisorName, meetingDate, meetingTime, purpose, notes)
        VALUES ({data["studentID"]}, '{data["advisorName"]}', '{data["meetingDate"]}', '{data["meetingTime"]}', '{data["purpose"]}', '{data["notes"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Meeting scheduled successfully", 201)


# Update a meeting
@student_bp.route('/advisor-meetings/<meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    data = request.json
    query = f'''
        UPDATE AdvisorMeetings
        SET purpose = '{data["purpose"]}', notes = '{data["notes"]}'
        WHERE meetingID = {meeting_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Meeting updated successfully", 200)


# Cancel a meeting
@student_bp.route('/advisor-meetings/<meeting_id>', methods=['DELETE'])
def delete_meeting(meeting_id):
    query = f'''
        DELETE FROM AdvisorMeetings WHERE meetingID = {meeting_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Meeting canceled successfully", 200)
