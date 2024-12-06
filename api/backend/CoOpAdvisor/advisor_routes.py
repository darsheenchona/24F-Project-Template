from datetime import datetime
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

coop_advisor = Blueprint('coop_advisor', __name__)

# ------------------------------------------------------------
# retrieve co-op advisor profile info
@coop_advisor.route('/coop_advisor/profile', methods=['GET'])
def get_coop_advisor_profile():
    advisor_id = request.args.get('advisorID')
    if not advisor_id:
        return make_response("Advisor ID is required", 400)

    query = f'''
        SELECT Users.name, Users.Email, Department, ActiveStudentCount
        FROM CoOpAdvisors 
        JOIN Users ON CoOpAdvisors.userID = Users.userID
        WHERE CoOpAdvisors.advisorID = {advisor_id}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    profile = cursor.fetchone()

    if not profile:
        return make_response("Co-op Advisor not found", 404)

    # Safely access 'email' using .get(), which won't raise KeyError if missing
    email = profile.get('email', 'No email available')
    
    return make_response(jsonify({
        "name": profile.get("name", "No name available"),
        "email": email,
        "department": profile.get("department", "No department available"),
        "advisingHistoryCount": profile.get("advisingHistoryCount", "N/A")
    }), 200)


@coop_advisor.route('/coop_advisor/profile', methods=['PUT'])
def update_coop_advisor_profile():
    advisor_id = request.args.get('advisorID')
    profile = request.json

    query = f'''
        UPDATE CoOpAdvisors
        SET department = '{profile["department"]}'
        WHERE advisorID = {advisor_id}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)

    query_users = f'''
        UPDATE Users
        SET name = '{profile["name"]}', email = '{profile["email"]}'
        WHERE userID = (SELECT userID FROM CoOpAdvisors WHERE advisorID = {advisor_id})
    '''
    cursor.execute(query_users)
    db.get_db().commit()

    return make_response("Co-op Advisor profile updated successfully", 200)

# ------------------------------------------------------------
# retrieve list of students advised by a co-op advisor
@coop_advisor.route('/Students', methods=['GET'])
def get_advised_students():
    advisor_id = request.args.get('advisorID')
    if not advisor_id:
        return make_response("Advisor ID is required", 400)

    query = f'''
        SELECT Students.studentID, Users.name AS student_name, Students.major
        FROM Students
        JOIN Users ON Students.userID = Users.userID
        WHERE Students.advisorID = {advisor_id}
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    students = cursor.fetchall()

    if not students:
        return make_response("No students found for the specified advisor", 404)

    return make_response(jsonify(students), 200)



# retrieve specific student advised by a co-op advisor
@coop_advisor.route('/students/<StudentID>', methods=['GET'])
def get_student_details(StudentID):
    query = f'''
        SELECT Users.name, Students.major, Students.gpa, Students.email
        FROM Students
        JOIN Users ON Students.userID = Users.userID
        WHERE Students.studentID = {StudentID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    student = cursor.fetchone()

    if not student:
        return make_response("Student not found", 404)

    return make_response(jsonify(student), 200)


# update student details
@coop_advisor.route('/students/<StudentID>', methods=['PUT'])
def update_student_details(StudentID):
    data = request.json
    if not data:
        return make_response("Student data is required", 400)

    query = f'''
        UPDATE Students
        SET Major = '{data["major"]}', GPA = {data["gpa"]}, Email = '{data["email"]}'
        WHERE StudentID = {StudentID}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
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
# Retrieve reports for co-op advisor
@coop_advisor.route('/reports', methods=['GET'])
def get_reports():
    query = '''
        SELECT ReportID, Title, Description, DateGenerated
        FROM Reports
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    reports = cursor.fetchall()

    return make_response(jsonify(reports), 200)


# Generate a new report for co-op advisor
@coop_advisor.route('/reports', methods=['POST'])
def generate_report():
    data = request.json
    advisor_id = request.args.get('advisorID')

    # Check if advisor_id is provided
    if not advisor_id:
        return make_response("Advisor ID is required", 400)

    # Use direct string formatting instead of %s
    query = f'''
        INSERT INTO Reports (Title, Description, DateGenerated, GeneratedBy)
        VALUES ("{data['Title']}", "{data['description']}", NOW(), {advisor_id})
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Report generated successfully", 201)


# Delete a specific report
@coop_advisor.route('/reports/<report_id>', methods=['DELETE'])
def delete_report(report_id):
    query = f'''
        DELETE FROM Reports WHERE ReportID = {report_id}
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    return make_response("Report deleted successfully", 200)


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



# ---------------------------------------------
# Add a new employer
@coop_advisor.route('/employers', methods=['POST'])
def add_employer():
    data = request.json
    name = data.get("name")
    industry = data.get("industry")
    location = data.get("location")
    status = data.get("status", "active")  # Default status is 'active'

    # Validate input
    if not name or not industry or not location:
        return make_response("All fields (name, industry, location) are required", 400)

    query = f'''
        INSERT INTO Employers (name, industry, location, status)
        VALUES ("{name}", "{industry}", "{location}", "{status}")
    '''
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()
        return make_response("Employer added successfully", 201)
    except Exception as e:
        logger.error(f"Error adding employer: {e}")
        return make_response("Error adding employer", 500)


# ---------------------------------------------
# Deactivate an employer (change status to inactive)
@coop_advisor.route('/employers/<int:employer_id>', methods=['PUT'])
def deactivate_employer(employer_id):
    data = request.json
    status = data.get("status", "inactive")

    # Update the employer's status
    query = f'''
        UPDATE Employers
        SET status = "{status}"
        WHERE employerID = {employer_id}
    '''
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response("Employer not found", 404)

        return make_response(f"Employer {employer_id} updated successfully", 200)
    except Exception as e:
        logger.error(f"Error updating employer: {e}")
        return make_response("Error updating employer", 500)


# ---------------------------------------------
# Update employer details
@coop_advisor.route('/employers/<int:employer_id>', methods=['PATCH'])
def update_employer(employer_id):
    data = request.json
    name = data.get("name")
    industry = data.get("industry")
    location = data.get("location")

    # Update only provided fields
    updates = []
    if name:
        updates.append(f'name = "{name}"')
    if industry:
        updates.append(f'industry = "{industry}"')
    if location:
        updates.append(f'location = "{location}"')

    if updates:
        query = f'''
            UPDATE Employers
            SET {", ".join(updates)}
            WHERE employerID = {employer_id}
        '''
        try:
            cursor = db.get_db().cursor()
            cursor.execute(query)
            db.get_db().commit()

            if cursor.rowcount == 0:
                return make_response("Employer not found", 404)

            return make_response("Employer updated successfully", 200)
        except Exception as e:
            logger.error(f"Error updating employer: {e}")
            return make_response("Error updating employer", 500)

    return make_response("No fields provided for update", 400)


# ---------------------------------------------
# Delete an employer
@coop_advisor.route('/employers/<int:employer_id>', methods=['DELETE'])
def delete_employer(employer_id):
    query = f'''
        DELETE FROM Employers WHERE employerID = {employer_id}
    '''
    try:
        cursor = db.get_db().cursor()
        cursor.execute(query)
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response("Employer not found", 404)

        return make_response("Employer deleted successfully", 200)
    except Exception as e:
        logger.error(f"Error deleting employer: {e}")
        return make_response("Error deleting employer", 500)




# Retrieve student progress and profile information (Skills, Interests, etc.)
@coop_advisor.route('/student_progress/<int:student_id>', methods=['GET'])
def get_student_progress(student_id):
    # Query to get student profile (major, skills, interests, etc.) using direct string interpolation
    query = f'''
        SELECT Major, Skills, Interests, DashboardPreferences, ResumeLink, PortfolioLink
        FROM Students
        WHERE StudentID = {student_id}
    '''  # Use direct string interpolation for student_id
    
    cursor = db.get_db().cursor()
    cursor.execute(query)  # Execute query without parameters
    student_data = cursor.fetchone()

    if not student_data:
        return make_response("Student not found", 404)

    student_profile = {
        "major": student_data[0] or "N/A",  # If no data, return "N/A"
        "skills": student_data[1] or "No skills listed",  # If no skills, return default message
        "interests": student_data[2] or "No interests listed",  # If no interests, return default message
        "dashboard_preferences": student_data[3] or "No preferences set",  # If no preferences, return default message
        "resume_link": student_data[4] or "No resume link provided",  # If no resume, return default message
        "portfolio_link": student_data[5] or "No portfolio link provided"  # If no portfolio, return default message
    }

    return make_response(jsonify(student_profile), 200)


# ------------------------------------------------------------
# Update student progress or profile (Skills, Interests, etc.)
@coop_advisor.route('/student_progress/<int:student_id>', methods=['PUT'])
def update_student_progress(student_id):
    # Get the new data from the request
    data = request.json

    # Collect updated values from the request (skills, interests, etc.)
    skills = data.get("skills")
    interests = data.get("interests")
    dashboard_preferences = data.get("dashboard_preferences")
    resume_link = data.get("resume_link")
    portfolio_link = data.get("portfolio_link")

    # Query to update student profile data using direct string interpolation
    query = f'''
        UPDATE Students
        SET Skills = '{skills}', Interests = '{interests}', DashboardPreferences = '{dashboard_preferences}',
            ResumeLink = '{resume_link}', PortfolioLink = '{portfolio_link}'
        WHERE StudentID = {student_id}
    '''  # Use direct string interpolation for fields and student_id
    
    cursor = db.get_db().cursor()
    cursor.execute(query)  # Execute query without parameters
    db.get_db().commit()

    return make_response("Student profile updated successfully", 200)
