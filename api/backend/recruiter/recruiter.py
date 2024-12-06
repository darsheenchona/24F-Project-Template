from datetime import date, time, datetime

from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

# Blueprint for recruiter endpoints
recruiter = Blueprint('recruiter', __name__)


# ------------------------------------------------------------
# retrieve recruiter profile info
@recruiter.route('/recruiter/profile', methods=['GET'])
def get_recruiter_profile():
    recruiter_id = request.args.get('recruiterID')
    query = f'''
        SELECT Users.name, Users.email, Recruiters.company, Recruiters.positionPostedCount, Recruiters.recruiterType
        FROM Recruiters
        JOIN Users ON Recruiters.userID = Users.userID
        WHERE Recruiters.recruiterID = {recruiter_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    profile = cursor.fetchone()

    if not profile:
        return make_response("Recruiter not found", 404)

    return make_response(jsonify(profile), 200)


# update profile
@recruiter.route('/recruiter/profile', methods=['PUT'])
def update_recruiter_profile():
    recruiter_id = request.args.get('recruiterID')
    profile = request.json

    query = f'''
        UPDATE Recruiters
        SET company = '{profile["company"]}', recruiterType = '{profile["recruiterType"]}'
        WHERE recruiterID = {recruiter_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    # need to also update our users table if we have new name or email
    query_users = f'''
        UPDATE Users
        SET name = '{profile["name"]}', email = '{profile["email"]}'
        WHERE userID = (SELECT userID FROM Recruiters WHERE recruiterID = {recruiter_id})
    '''
    cursor.execute(query_users)
    db.get_db().commit()

    return make_response("Profile update successful", 200)


# ------------------------------------------------------------
# retrieve list of jobs given recruiterID
@recruiter.route('/jobs', methods=['GET'])
def get_jobs():
    recruiter_id = request.args.get('recruiterID')
    query = f'''
        SELECT jobID, title, company, description, requirements, status, deadline, progress
        FROM Jobs
        WHERE postedBy = {recruiter_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    jobs = cursor.fetchall()
    return make_response(jsonify(jobs), 200)


# create new job post given recruiterID
@recruiter.route('/jobs', methods=['POST'])
def create_job():
    data = request.json
    recruiter_id = request.args.get('recruiterID')
    query = f'''
        INSERT INTO Jobs (title, company, description, requirements, status, deadline, postedBy)
        VALUES ('{data["title"]}', '{data["company"]}', '{data["description"]}', '{data["requirements"]}', '{data["status"]}', '{data["deadline"]}', '{recruiter_id}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Job created successfully", 201)


# update job post
@recruiter.route('/jobs/<job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.json
    query = f'''
        UPDATE Jobs
        SET title = '{data["title"]}', company = '{data["company"]}', description = '{data["description"]}', 
            requirements = '{data["requirements"]}', status = '{data["status"]}', deadline = '{data["deadline"]}'
        WHERE jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Job updated successfully", 200)


# delete job post
@recruiter.route('/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    query = f'''
        DELETE FROM Jobs WHERE jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Job deleted successfully", 200)


# ------------------------------------------------------------
# retrieve candidates for a specific job
@recruiter.route('/jobs/<job_id>/candidates', methods=['GET'])
def get_candidates(job_id):
    # fetch query parameters; this will be for filter and sorting functionality
    skill_filter = request.args.get("skill")  # filter by skill (optional)
    sort_by = request.args.get("sort")  # sort parameter (optional)

    # query to fetch candidates and their application info
    query = f'''
        SELECT 
            Students.studentID, 
            Users.name AS candidate_name, 
            Students.skills, 
            Applications.applicationID, 
            Applications.status, 
            Applications.reviewScore, 
            Applications.feedback
        FROM Applications
        JOIN Students ON Applications.studentID = Students.studentID
        JOIN Users ON Students.userID = Users.userID
        WHERE Applications.jobID = {job_id}
    '''

    # apply skill filter if provided
    if skill_filter:
        query += f" AND LOWER(Students.skills) LIKE LOWER('%{skill_filter}%')"

    # apply sorting if specified
    if sort_by == "name":
        query += " ORDER BY Users.name ASC"
    elif sort_by == "status":
        query += " ORDER BY Applications.status ASC"
    elif sort_by == "reviewScore":
        query += " ORDER BY Applications.reviewScore DESC"

    cursor = db.get_db().cursor()
    cursor.execute(query)
    candidates = cursor.fetchall()

    # Return results as JSON
    return make_response(jsonify(candidates), 200)


# retrieve details about a specific candidate for a given job
@recruiter.route('/jobs/<job_id>/candidates/<candidate_id>', methods=['GET'])
def get_candidate_details(job_id, candidate_id):
    query = f'''
        SELECT Applications.applicationID, Users.name, Students.skills, Applications.status, Applications.feedback
        FROM Applications
        JOIN Students ON Applications.studentID = Students.studentID
        JOIN Users ON Students.userID = Users.userID
        WHERE Applications.jobID = {job_id} AND Students.studentID = {candidate_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    candidate = cursor.fetchone()

    # if candidate not in database, then return error response
    if not candidate:
        return make_response("Candidate not found", 404)

    return make_response(jsonify(candidate), 200)


# update candidate application status or add a note
@recruiter.route('/jobs/<job_id>/candidates/<candidate_id>', methods=['PUT'])
def update_candidate_status(job_id, candidate_id):
    data = request.json
    query = f'''
        UPDATE Applications
        SET status = '{data["status"]}', feedback = '{data["feedback"]}'
        WHERE jobID = {job_id} AND studentID = {candidate_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Candidate status update successful", 200)


# get all candidates given a recruiter
@recruiter.route('/recruiter/<recruiter_id>/candidates', methods=['GET'])
def get_all_candidates(recruiter_id):
    query = f'''
        SELECT DISTINCT Students.studentID, Users.name AS candidate_name
        FROM Applications
        JOIN Jobs ON Applications.jobID = Jobs.jobID
        JOIN Students ON Applications.studentID = Students.studentID
        JOIN Users ON Students.userID = Users.userID
        WHERE Jobs.postedBy = {recruiter_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    candidates = cursor.fetchall()

    return make_response(jsonify(candidates), 200)


# ------------------------------------------------------------
# retrieve applications given a specific job
@recruiter.route('/jobs/<job_id>/applications', methods=['GET'])
def get_applications(job_id):
    query = f'''
        SELECT applicationID, studentID, status, reviewScore, feedback
        FROM Applications
        WHERE jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    applications = cursor.fetchall()

    return make_response(jsonify(applications), 200)


# update application status
@recruiter.route('/jobs/<job_id>/applications/<application_id>', methods=['PUT'])
def update_application_status(job_id, application_id):
    data = request.json
    query = f'''
        UPDATE Applications
        SET status = '{data["status"]}'
        WHERE applicationID = {application_id} AND jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Application status update successful", 200)


# ------------------------------------------------------------
# retrieve notifications given recruiterID
@recruiter.route('/notifications', methods=['GET'])
def get_notifications():
    recruiter_id = request.args.get('recruiterID')
    if not recruiter_id:
        return make_response("Recruiter ID is required", 400)

    query = f'''
        SELECT notificationID, content, dateSent, notificationType
        FROM Notifications
        WHERE userID = {recruiter_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    notifications = cursor.fetchall()

    return make_response(jsonify(notifications), 200)


# send a notification
@recruiter.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    user_id = data.get("userID")
    content = data.get("content")
    notification_type = data.get("notificationType")

    # require non null fields
    if not user_id or not content or not notification_type:
        return make_response("Missing required fields", 400)

    query = f'''
        INSERT INTO Notifications (userID, content, notificationType)
        VALUES ({user_id}, '{content}', '{notification_type}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Notification sent successfully", 201)


# mark a notification as read
@recruiter.route('/notifications/<notification_id>', methods=['PUT'])
def mark_notification_as_read(notification_id):
    query = f'''
        UPDATE Notifications
        SET IsRead = TRUE
        WHERE NotificationID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (notification_id,))
    db.get_db().commit()

    return make_response("Notification marked as read successfully", 200)


# ------------------------------------------------------------
# retrieve reports
@recruiter.route('/reports', methods=['GET'])
def get_reports():
    query = f'''
        SELECT reportID, title, description, dateGenerated
        FROM Reports
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    reports = cursor.fetchall()

    return make_response(jsonify(reports), 200)


# generate a report given a recruiterID
@recruiter.route('/reports', methods=['POST'])
def generate_report():
    data = request.json
    recruiter_id = request.args.get('recruiterID')
    query = f'''
        INSERT INTO Reports (title, description, dateGenerated, GeneratedBy)
        VALUES ('{data["title"]}', '{data["description"]}', NOW(), '{recruiter_id}')
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Report generated successfully", 201)


# delete a report
@recruiter.route('/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    query = f'''
        DELETE FROM Reports WHERE reportID = {report_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Report delete successful", 200)


# get interviews for a given job
@recruiter.route('/jobs/<job_id>/interviews', methods=['GET'])
def get_interviews(job_id):
    query = f'''
        SELECT 
            interviewID, 
            Students.studentID, 
            Users.name AS candidate_name, 
            InterviewDateTime, 
            notes
        FROM Interviews
        JOIN Students ON Interviews.studentID = Students.studentID
        JOIN Users ON Students.userID = Users.userID
        WHERE Interviews.jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    interviews = cursor.fetchall()

    return make_response(jsonify(interviews), 200)


# schedule new interview for specific job
@recruiter.route('/jobs/<job_id>/interviews', methods=['POST'])
def create_interview(job_id):
    interview = request.json
    student_id = interview.get('studentID')
    interview_datetime = interview.get('InterviewDateTime')
    notes = interview.get('notes')
    if not student_id or not interview_datetime or not notes:
        return make_response("Missing required fields", 400)

    query = f'''
        INSERT INTO Interviews (jobID, studentID, InterviewDateTime, notes)
        VALUES ({job_id}, {student_id}, {interview_datetime}, {notes})
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (job_id, student_id, interview_datetime, notes))
    db.get_db().commit()

    return make_response("Interview scheduled successfully", 201)


# update an interview (reschedule) for a specific job
@recruiter.route('/jobs/<job_id>/interviews/<interview_id>', methods=['PUT'])
def update_interview(job_id, interview_id):
    interview = request.json
    interview_datetime = interview.get('InterviewDateTime')
    notes = interview.get('notes')

    if not interview_datetime or not notes:
        return make_response("Missing required fields", 400)

    query = f'''
        UPDATE Interviews
        SET InterviewDateTime = %s, notes = %s
        WHERE interviewID = %s AND jobID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (interview["InterviewDateTime"], interview["notes"], interview_id, job_id))
    db.get_db().commit()

    return make_response("Interview updated successfully", 200)


# delete specific interview for specific job
@recruiter.route('/jobs/<job_id>/interviews/<interview_id>', methods=['DELETE'])
def delete_interview(job_id, interview_id):
    query = f'''
        DELETE FROM Interviews
        WHERE interviewID = {interview_id} AND jobID = {job_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (interview_id, job_id))
    db.get_db().commit()

    return make_response("Interview deleted successfully", 200)
