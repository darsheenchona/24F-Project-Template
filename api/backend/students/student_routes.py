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
@student_bp.route('/student/applications', methods=['GET'])
def get_applications():
    student_id = request.args.get('studentID')
    if not student_id or not student_id.isdigit():
        return make_response("Invalid or missing studentID parameter", 400)

    query = f'''
        SELECT A.ApplicationID,
               J.Title AS jobTitle,
               J.Company AS companyName,
               A.Status,
               A.DateApplied,
               A.ReviewScore,
               A.Feedback,
               J.Deadline,
               J.JobID
        FROM Applications A
        JOIN Jobs J ON A.JobID = J.JobID
        WHERE A.StudentID = {student_id}
    '''

    cursor = db.get_db().cursor()
    cursor.execute(query)
    applications = cursor.fetchall()

    return make_response(jsonify(applications), 200)


# Add a new application
@student_bp.route('/student/applications', methods=['POST'])
def add_application():
    data = request.json
    required_fields = ["StudentID", "JobID", "Status", "DateApplied", "ReviewScore", "Feedback"]
    for field in required_fields:
        if field not in data:
            return make_response(f"Missing field: {field}", 400)

    query = f'''
        INSERT INTO Applications (StudentID, JobID, Status, DateApplied, ReviewScore, Feedback)
        VALUES ({data["StudentID"]}, {data["JobID"]}, '{data["Status"]}', '{data["DateApplied"]}', {data["ReviewScore"]}, '{data["Feedback"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application added successfully", 201)


# Update an application
@student_bp.route('/student/applications/<application_id>', methods=['PUT'])
def update_application(application_id):
    data = request.json

    set_clauses = []
    if "Status" in data:
        set_clauses.append(f"Status = '{data['Status']}'")
    if "DateApplied" in data:
        set_clauses.append(f"DateApplied = '{data['DateApplied']}'")
    if "ReviewScore" in data:
        set_clauses.append(f"ReviewScore = {data['ReviewScore']}")
    if "Feedback" in data:
        set_clauses.append(f"Feedback = '{data['Feedback']}'")

    if not set_clauses:
        return make_response("No fields to update", 400)

    set_clause = ", ".join(set_clauses)
    query = f'''
        UPDATE Applications
        SET {set_clause}
        WHERE ApplicationID = {application_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application updated successfully", 200)


# Remove an application
@student_bp.route('/student/applications/<application_id>', methods=['DELETE'])
def delete_application(application_id):
    query = f'''
        DELETE FROM Applications WHERE ApplicationID = {application_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application removed successfully", 200)


# ------------------------------------------------------------
# Corrected get_job endpoint
@student_bp.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    if not job_id:
        return make_response("Missing job parameter", 400)

    query = f'''
        SELECT title AS Title,
               company AS Company,
               deadline AS Deadline,
               description AS Description,
               requirements AS Requirements,
               status AS Status
        FROM Jobs
        WHERE jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    job = cursor.fetchone()

    if not job:
        return make_response("Job not found", 404)

    return make_response(jsonify(job), 200)


# ------------------------------------------------------------
@student_bp.route('/student/savedjobs', methods=['GET'])
def get_saved_jobs():
    student_id = request.args.get('studentID')
    if not student_id or not student_id.isdigit():
        return make_response("Invalid or missing studentID parameter", 400)

    query = f'''
        SELECT S.SaveID, J.Title, J.Company, S.SaveDate
        FROM SavedJobs S
        JOIN Jobs J ON S.JobID = J.JobID
        WHERE S.StudentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    return make_response(jsonify(rows), 200)


@student_bp.route('/student/savedjobs', methods=['POST'])
def add_saved_job():
    data = request.json
    required_fields = ["StudentID", "JobID", "SaveDate"]
    for field in required_fields:
        if field not in data:
            return make_response(f"Missing field: {field}", 400)

    query = f'''
        INSERT INTO SavedJobs (StudentID, JobID, SaveDate)
        VALUES ({data["StudentID"]}, {data["JobID"]}, '{data["SaveDate"]}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Saved job added successfully", 201)


@student_bp.route('/student/savedjobs/<save_id>', methods=['DELETE'])
def delete_saved_job(save_id):
    query = f'''
        DELETE FROM SavedJobs WHERE SaveID = {save_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Saved job removed successfully", 200)


# ------------------------------------------------------------
# Fetch recommendations
@student_bp.route('/student/recommendations', methods=['GET'])
def get_recommendations():
    student_id = request.args.get('studentID')

    # Validate the input
    if not student_id or not student_id.isdigit():
        return make_response(jsonify({"error": "Invalid or missing studentID parameter"}), 400)

    # Query to fetch recommendations
    query = f'''
        SELECT recommendationID AS recommendation_id,
               PositionTitle AS job_title,
               Company AS company_name,
               matchScore AS match_score
        FROM RecommendedJobs
        JOIN Jobs ON Jobs.JobID = RecommendedJobs.JobID
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
    if not student_id or not student_id.isdigit():
        return make_response(jsonify({"error": "Invalid or missing studentID parameter"}), 400)

    query = f'''
        SELECT 
            MeetingID AS meeting_id,
            AdvisorID AS advisor_id,
            MeetingDateTime AS meeting_date_time,
            Purpose AS purpose,
            Notes AS notes
        FROM AdvisorMeetings
        WHERE StudentID = {student_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    meetings = cursor.fetchall()

    return make_response(jsonify(meetings), 200)


# Schedule a new meeting
@student_bp.route('/advisor-meetings', methods=['POST'])
def schedule_meeting():
    data = request.json
    required_fields = ["StudentID", "AdvisorID", "MeetingDateTime", "Purpose"]
    for field in required_fields:
        if field not in data or not data[field]:
            return make_response(jsonify({"error": f"Missing or invalid field: {field}"}), 400)

    query = f'''
        INSERT INTO AdvisorMeetings (StudentID, AdvisorID, MeetingDateTime, Purpose, Notes)
        VALUES ({data["StudentID"]}, {data["AdvisorID"]}, '{data["MeetingDateTime"]}', 
                '{data["Purpose"]}', '{data.get("Notes", "")}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Meeting scheduled successfully", 201)


# Update a meeting
@student_bp.route('/advisor-meetings/<meeting_id>', methods=['PUT'])
def update_meeting(meeting_id):
    data = request.json
    set_clauses = []
    if "meetingDateTime" in data:
        set_clauses.append(f"MeetingDateTime = '{data['meetingDateTime']}'")
    if "purpose" in data:
        set_clauses.append(f"Purpose = '{data['purpose']}'")
    if "notes" in data:
        set_clauses.append(f"Notes = '{data['notes']}'")

    if not set_clauses:
        return make_response(jsonify({"error": "No valid fields provided for update"}), 400)

    set_clause = ", ".join(set_clauses)
    query = f'''
        UPDATE AdvisorMeetings
        SET {set_clause}
        WHERE MeetingID = {meeting_id}
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
