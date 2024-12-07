-- Drop database if it already exists and create a new one
DROP DATABASE IF EXISTS CoopProjectDB;
CREATE DATABASE CoopProjectDB;
USE CoopProjectDB;

-- Drop all tables if they exist

DROP TABLE IF EXISTS SystemAlerts;
DROP TABLE IF EXISTS ITServices;
DROP TABLE IF EXISTS PlatformAnalytics;
DROP TABLE IF EXISTS Notifications;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS AdvisorMeetings;
DROP TABLE IF EXISTS RecommendedJobs;
DROP TABLE IF EXISTS SavedJobs;
DROP TABLE IF EXISTS Applications;
DROP TABLE IF EXISTS Placement;
DROP TABLE IF EXISTS Jobs;
DROP TABLE IF EXISTS Employers
DROP TABLE IF EXISTS CoOpAdvisors;
DROP TABLE IF EXISTS Alumni;
DROP TABLE IF EXISTS Recruiters;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Reports;
DROP TABLE IF EXISTS Interviews;
DROP TABLE IF EXISTS ITEmployee;
DROP TABLE IF EXISTS ITAssets;
DROP TABLE IF EXISTS Tickets;



-- Create the Users table
CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Role ENUM('Student', 'Recruiter', 'Advisor', 'IT Head') NOT NULL,
    Password VARCHAR(255) NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdatedAt DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the CoOpAdvisors table
CREATE TABLE CoOpAdvisors (
    AdvisorID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Department VARCHAR(50),
    MeetingAvailability TEXT,
    ActiveStudentCount INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create the Placement table
CREATE TABLE Placement (
    placementID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    company VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    status ENUM('Active', 'Completed', 'Pending') NOT NULL,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE
);



-- Create the Students table
CREATE TABLE Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Major VARCHAR(50),
    Year INT,
    Skills TEXT,
    Interests TEXT,
    DashboardPreferences TEXT,
    ResumeLink VARCHAR(255),
    PortfolioLink VARCHAR(255),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create the Recruiters table
CREATE TABLE Recruiters (
    RecruiterID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Company VARCHAR(100),
    PositionPostedCount INT,
    FiltersPreferences TEXT,
    RecruiterType ENUM('In-house', 'Agency'),
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create the Jobs table
CREATE TABLE Jobs (
    JobID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100),
    Company VARCHAR(100),
    Description TEXT,
    Requirements TEXT,
    Status ENUM('Open', 'Closed'),
    PostedBy INT NOT NULL,
    DatePosted DATE,
    Deadline DATE,
    Location VARCHAR(100),
    SalaryRange VARCHAR(50),
    Progress INT DEFAULT 0,
    FOREIGN KEY (PostedBy) REFERENCES Recruiters(RecruiterID) ON DELETE CASCADE
);



-- Create the Applications table
CREATE TABLE Applications (
    ApplicationID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    JobID INT NOT NULL,
    Status ENUM('Pending', 'Accepted', 'Rejected'),
    DateApplied DATE,
    ReviewScore INT,
    Feedback TEXT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (JobID) REFERENCES Jobs(JobID) ON DELETE CASCADE
);

-- Create the SavedJobs table
CREATE TABLE SavedJobs (
    SaveID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    JobID INT NOT NULL,
    SaveDate DATE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (JobID) REFERENCES Jobs(JobID) ON DELETE CASCADE
);

-- Create the RecommendedJobs table
CREATE TABLE RecommendedJobs (
    RecommendationID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    JobID INT NOT NULL,
    MatchScore INT,
    PositionTitle VARCHAR(100),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (JobID) REFERENCES Jobs(JobID) ON DELETE CASCADE
);

-- Create the AdvisorMeetings table
CREATE TABLE AdvisorMeetings (
    MeetingID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    AdvisorID INT NOT NULL,
    MeetingDateTime DATETIME NOT NULL,
    Purpose TEXT,
    Notes TEXT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE,
    FOREIGN KEY (AdvisorID) REFERENCES CoOpAdvisors(AdvisorID) ON DELETE CASCADE
);

-- Create the Events table
CREATE TABLE Events (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    StudentID INT NOT NULL,
    EventName VARCHAR(100),
    CompanyName VARCHAR(100),
    EventDate DATE,
    EventType VARCHAR(50),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE
);

-- Create the Notifications table
CREATE TABLE Notifications (
    NotificationID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Content TEXT,
    DateSent DATETIME DEFAULT CURRENT_TIMESTAMP,
    NotificationType ENUM('Reminder', 'Alert', 'Update'),
    IsRead BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create the PlatformAnalytics table
CREATE TABLE PlatformAnalytics (
    AnalyticsID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    UsageDuration INT,
    ActivityType VARCHAR(50),
    DeviceType VARCHAR(50),
    Date DATE,
    FOREIGN KEY (UserID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Create the ITServices table
CREATE TABLE ITServices (
    ITID INT AUTO_INCREMENT PRIMARY KEY,
    PlatformUsageMetrics TEXT,
    SystemHealthLogs TEXT,
    IssueTicketsCount INT
);

-- Create the SystemAlerts table
CREATE TABLE SystemAlerts (
    AlertID INT AUTO_INCREMENT PRIMARY KEY,
    ITID INT NOT NULL,
    AlertType VARCHAR(50),
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ResolutionStatus VARCHAR(50),
    Severity ENUM('Low', 'Medium', 'High'),
    FOREIGN KEY (ITID) REFERENCES ITServices(ITID) ON DELETE CASCADE
);

-- Create the Alumni table
CREATE TABLE Alumni (
    AlumniID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    GraduationYear INT,
    CoOpExperienceDetails TEXT,
    CurrentPosition VARCHAR(100),
    Company VARCHAR(100),
    LinkedInProfile VARCHAR(255)
);

-- Create the Reports table
CREATE TABLE Reports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(100),
    Description TEXT,
    DateGenerated DATETIME DEFAULT CURRENT_TIMESTAMP,
    GeneratedBy INT NOT NULL,
    FOREIGN KEY (GeneratedBy) REFERENCES Recruiters(RecruiterID) ON DELETE CASCADE
);

-- Create the Interviews table
CREATE TABLE Interviews (
    InterviewID INT AUTO_INCREMENT PRIMARY KEY,
    JobID INT NOT NULL,
    StudentID INT NOT NULL,
    InterviewDateTime DATETIME NOT NULL,
    Notes TEXT,
    FOREIGN KEY (JobID) REFERENCES Jobs(JobID) ON DELETE CASCADE,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID) ON DELETE CASCADE
);

-- Create the ITEmployee table
CREATE TABLE ITEmployee (
    ITEmpID INT AUTO_INCREMENT PRIMARY KEY,
    PlatformUsageMetrics TEXT,
    SystemHealthLogs TEXT,
    Email TEXT,
    EmpFirstName TEXT,
    EmpLastName TEXT
);

-- Create the ITAssets table
CREATE TABLE ITAssets (
    assetID INT AUTO_INCREMENT PRIMARY KEY,
    assetName TEXT,
    ITStatus TEXT,
    assetType TEXT,
    assetDetails TEXT
);

-- Create the Tickets table 
CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    TicketTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    TicketStatus TEXT,
    TicketDetails TEXT,
    FufilledBy INT DEFAULT 1,
    FOREIGN KEY (FufilledBy) REFERENCES ITEmployee(ITEmpID) 
);


INSERT INTO Users (Name, Email, Role, Password) VALUES
('Emily Watson', 'emily.watson@advisors.com', 'Advisor', 'EmilyAdvisor123#'),
('Michael Brown', 'michael.brown@advisors.com', 'Advisor', 'MichaelAdvisor@456'),
('Sarah Johnson', 'sarah.johnson@advisors.com', 'Advisor', 'SarahSecure#2024'),
('David Wilson', 'david.wilson@advisors.com', 'Advisor', 'DavidAdvises#789'),
('Jessica Thomas', 'jessica.thomas@advisors.com', 'Advisor', 'Jessica#Advisor2024'),
('Christopher Taylor', 'christopher.taylor@advisors.com', 'Advisor', 'Chris@Advisor123'),
('Amanda White', 'amanda.white@advisors.com', 'Advisor', 'AmandaAdvisorSecure#'),
('Joshua Harris', 'joshua.harris@advisors.com', 'Advisor', 'JoshH#2024'),
('Rachel Miller', 'rachel.miller@advisors.com', 'Advisor', 'RachelMAdvisor#'),
('Andrew Moore', 'andrew.moore@advisors.com', 'Advisor', 'AndrewSecure2024#'),
('Samantha Clark', 'samantha.clark@advisors.com', 'Advisor', 'Samantha@123Advisor'),
('Ethan Lewis', 'ethan.lewis@advisors.com', 'Advisor', 'EthanAdvisor@Secure'),
('Victoria Lee', 'victoria.lee@advisors.com', 'Advisor', 'Victoria#Advises'),
('Daniel Anderson', 'daniel.anderson@advisors.com', 'Advisor', 'DanielAdvisor#Secure'),
('Megan Young', 'megan.young@advisors.com', 'Advisor', 'MeganSecure2024#'),
('Matthew Scott', 'matthew.scott@advisors.com', 'Advisor', 'MattAdvisor@2024'),
('Sophia King', 'sophia.king@advisors.com', 'Advisor', 'Sophia#AdvisorSecure'),
('James Hall', 'james.hall@advisors.com', 'Advisor', 'JamesH@Advisor123'),
('Olivia Wright', 'olivia.wright@advisors.com', 'Advisor', 'OliviaSecure#'),
('Benjamin Adams', 'benjamin.adams@advisors.com', 'Advisor', 'BenAdvisor@789'),
('Natalie Evans', 'natalie.evans@advisors.com', 'Advisor', 'NatalieAdvises#2024'),
('William Baker', 'william.baker@advisors.com', 'Advisor', 'Will@AdvisorSecure'),
('Chloe Roberts', 'chloe.roberts@advisors.com', 'Advisor', 'ChloeAdvisor123#'),
('Alexander Carter', 'alexander.carter@advisors.com', 'Advisor', 'AlexCAdvisor#'),
('Hannah Turner', 'hannah.turner@advisors.com', 'Advisor', 'HannahAdvisor@Secure'),
('Noah Green', 'noah.green@advisors.com', 'Advisor', 'NoahSecureAdvisor#'),
('Ella Edwards', 'ella.edwards@advisors.com', 'Advisor', 'EllaAdvisor@Secure'),
('Mason Ramirez', 'mason.ramirez@advisors.com', 'Advisor', 'MasonRAdvises#'),
('Grace Collins', 'grace.collins@advisors.com', 'Advisor', 'GraceAdvisorSecure@'),
('Lucas Bell', 'lucas.bell@advisors.com', 'Advisor', 'LucasAdvises#2024');




INSERT INTO CoOpAdvisors (UserID, Department, MeetingAvailability, ActiveStudentCount) VALUES
(1, 'Computer Science', 'Monday, Wednesday', 25),
(2, 'Electrical Engineering', 'Tuesday, Friday', 20),
(3, 'Mechanical Engineering', 'Monday, Friday', 22),
(4, 'Civil Engineering', 'Tuesday, Thursday', 18),
(5, 'Data Science', 'Wednesday, Friday', 30),
(6, 'Marketing', 'Monday, Wednesday', 15),
(7, 'Business Administration', 'Tuesday, Thursday', 28),
(8, 'Cybersecurity', 'Monday, Friday', 26),
(9, 'Artificial Intelligence', 'Wednesday, Friday', 32),
(10, 'Biotechnology', 'Tuesday, Thursday', 20),
(11, 'Finance', 'Monday, Wednesday', 19),
(12, 'Human Resources', 'Tuesday, Thursday', 12),
(13, 'Environmental Science', 'Wednesday, Friday', 18),
(14, 'Robotics', 'Monday, Thursday', 30),
(15, 'Mathematics', 'Tuesday, Friday', 17),
(16, 'Physics', 'Monday, Wednesday', 22),
(17, 'Education', 'Wednesday, Thursday', 10),
(18, 'Psychology', 'Monday, Friday', 25),
(19, 'Law', 'Tuesday, Thursday', 14),
(20, 'Nursing', 'Monday, Wednesday', 24),
(21, 'Film Production', 'Wednesday, Friday', 12),
(22, 'Architecture', 'Tuesday, Thursday', 18),
(23, 'Public Health', 'Monday, Friday', 19),
(24, 'Media Studies', 'Wednesday, Friday', 15),
(25, 'Information Technology', 'Tuesday, Thursday', 33),
(26, 'Accounting', 'Monday, Friday', 21),
(27, 'Sociology', 'Wednesday, Thursday', 14),
(28, 'Physics', 'Monday, Wednesday', 16),
(29, 'Economics', 'Tuesday, Thursday', 20),
(30, 'Agriculture', 'Monday, Friday', 22);

INSERT INTO Placement (StudentID, company, position, startDate, endDate, status) VALUES
(1, 'Google', 'Software Engineer', '2023-06-01', '2023-12-01', 'Active'),
(1, 'Facebook', 'Data Analyst', '2024-01-01', '2024-06-01', 'Pending'),
(2, 'Microsoft', 'UX Designer', '2023-07-01', '2023-12-01', 'Completed'),
(2, 'Amazon', 'Cloud Engineer', '2024-02-01', '2024-08-01', 'Active'),
(3, 'Apple', 'iOS Developer', '2023-09-01', '2024-03-01', 'Pending'),
(3, 'Intel', 'Hardware Engineer', '2023-10-15', '2024-04-15', 'Active'),
(4, 'IBM', 'AI Research Intern', '2023-06-01', '2023-12-15', 'Completed'),
(4, 'Oracle', 'Business Analyst', '2024-01-15', '2024-07-15', 'Pending'),
(5, 'Netflix', 'Software Tester', '2023-08-01', '2024-01-01', 'Completed'),
(5, 'Spotify', 'Data Scientist', '2024-03-01', '2024-09-01', 'Active'),
(6, 'Adobe', 'Graphic Designer', '2023-11-01', '2024-04-01', 'Pending'),
(6, 'Salesforce', 'CRM Consultant', '2023-12-01', '2024-06-01', 'Active'),
(7, 'Twitter', 'Product Manager', '2023-05-01', '2023-10-01', 'Completed'),
(7, 'TikTok', 'Social Media Strategist', '2023-12-01', '2024-06-01', 'Active'),
(8, 'Adobe', 'Web Developer', '2023-06-15', '2023-12-15', 'Active'),
(8, 'Cisco', 'Network Engineer', '2023-07-01', '2024-01-01', 'Pending'),
(9, 'Dell', 'Systems Administrator', '2023-08-01', '2024-01-01', 'Completed'),
(9, 'HP', 'DevOps Engineer', '2024-02-01', '2024-07-01', 'Active'),
(10, 'Uber', 'Operations Manager', '2023-09-01', '2024-03-01', 'Pending'),
(10, 'Lyft', 'Operations Analyst', '2023-11-15', '2024-05-15', 'Active'),
(11, 'Snapchat', 'Marketing Intern', '2023-12-01', '2024-06-01', 'Completed'),
(11, 'Pinterest', 'UX Research Intern', '2023-09-01', '2024-03-01', 'Pending'),
(12, 'Airbnb', 'Hospitality Coordinator', '2024-01-01', '2024-07-01', 'Active'),
(12, 'Expedia', 'Travel Analyst', '2024-02-01', '2024-08-01', 'Completed'),
(13, 'LinkedIn', 'HR Intern', '2023-06-01', '2023-12-01', 'Pending'),
(13, 'Indeed', 'Talent Acquisition Analyst', '2023-07-15', '2024-01-15', 'Active'),
(14, 'Dropbox', 'Software Engineer Intern', '2023-08-01', '2024-02-01', 'Completed'),
(14, 'Box', 'Cloud Support Engineer', '2023-10-01', '2024-04-01', 'Active'),
(15, 'PayPal', 'Finance Analyst', '2023-09-15', '2024-03-15', 'Pending'),
(15, 'Venmo', 'Transaction Coordinator', '2023-11-01', '2024-05-01', 'Active'),
(16, 'Square', 'Product Designer', '2023-07-01', '2023-12-01', 'Completed'),
(16, 'Stripe', 'Frontend Developer', '2024-01-01', '2024-06-01', 'Active'),
(17, 'Yahoo', 'Data Analyst Intern', '2023-09-15', '2024-03-15', 'Pending'),
(17, 'Reddit', 'Content Strategist', '2023-10-01', '2024-04-01', 'Active'),
(18, 'Microsoft', 'Cybersecurity Analyst', '2023-11-01', '2024-05-01', 'Pending'),
(18, 'Amazon', 'Security Consultant', '2024-01-01', '2024-07-01', 'Active'),
(19, 'Spotify', 'Machine Learning Intern', '2023-06-01', '2023-12-01', 'Completed'),
(19, 'Netflix', 'AI Research Assistant', '2023-08-01', '2024-02-01', 'Active'),
(20, 'Oracle', 'IT Systems Analyst', '2023-07-15', '2023-12-15', 'Pending'),
(20, 'IBM', 'System Analyst', '2023-10-01', '2024-04-01', 'Active');


INSERT INTO Users (Name, Email, Role, Password) VALUES
-- Students
('John Doe', 'john.doe@university.edu', 'Student', 'JohnSecure123'),
('Jane Smith', 'jane.smith@university.edu', 'Student', 'JaneSecure123'),
('Alice Brown', 'alice.brown@university.edu', 'Student', 'Alice123@Secure'),
('Tom Wilson', 'tom.wilson@university.edu', 'Student', 'TomWilson#2024'),
('Diana Prince', 'diana.prince@university.edu', 'Student', 'DianaSecure@2024'),
('Mark Green', 'mark.green@university.edu', 'Student', 'MarkG@Secure'),
('Eva White', 'eva.white@university.edu', 'Student', 'Eva2024@Uni'),
('Sam Lee', 'sam.lee@university.edu', 'Student', 'SamLee123#'),
('Nina Black', 'nina.black@university.edu', 'Student', 'NinaBlack2024'),
('Paul Harris', 'paul.harris@university.edu', 'Student', 'PaulH@Uni2024'),
-- Recruiters
('Recruiter A', 'recruiter.a@company.com', 'Recruiter', 'RecruitA123'),
('Recruiter B', 'recruiter.b@agency.com', 'Recruiter', 'RecruitB2024'),
('Recruiter C', 'recruiter.c@company.com', 'Recruiter', 'RecruitC@Secure'),
('Recruiter D', 'recruiter.d@agency.com', 'Recruiter', 'RecruitD#Secure'),
('Recruiter E', 'recruiter.e@company.com', 'Recruiter', 'RecruitE@2024'),
('Recruiter F', 'recruiter.f@agency.com', 'Recruiter', 'RecruitF123'),
('Recruiter G', 'recruiter.g@company.com', 'Recruiter', 'RecruitG@Secure'),
('Recruiter H', 'recruiter.h@agency.com', 'Recruiter', 'RecruitH#Secure'),
('Recruiter I', 'recruiter.i@company.com', 'Recruiter', 'RecruitI2024'),
('Recruiter J', 'recruiter.j@agency.com', 'Recruiter', 'RecruitJ123'),
('Yomayra', 'yomayra@example.com', 'Recruiter', 'password123');


INSERT INTO Students (UserID, Major, Year, Skills, Interests, DashboardPreferences, ResumeLink, PortfolioLink) VALUES
(1, 'Computer Science', 4, 'Java, Python, C++', 'AI, Robotics', 'Compact', 'https://resume.example.com/student1', 'https://portfolio.example.com/student1'),
(2, 'Mechanical Engineering', 3, 'SolidWorks, MATLAB, AutoCAD', 'Automotive Design, CAD', 'Detailed', 'https://resume.example.com/student2', 'https://portfolio.example.com/student2'),
(3, 'Civil Engineering', 2, 'AutoCAD, STAAD Pro', 'Structural Design, Green Architecture', 'Compact', 'https://resume.example.com/student3', 'https://portfolio.example.com/student3'),
(4, 'Electrical Engineering', 4, 'Embedded Systems, Circuit Design, MATLAB', 'IoT, Power Systems', 'Detailed', 'https://resume.example.com/student4', 'https://portfolio.example.com/student4'),
(5, 'Data Science', 2, 'Python, R, SQL', 'Machine Learning, Analytics', 'Compact', 'https://resume.example.com/student5', 'https://portfolio.example.com/student5'),
(6, 'Information Technology', 3, 'HTML, CSS, JavaScript', 'Web Development, Networking', 'Detailed', 'https://resume.example.com/student6', 'https://portfolio.example.com/student6'),
(7, 'Chemical Engineering', 4, 'Aspen Plus, MATLAB', 'Process Engineering, Sustainability', 'Compact', 'https://resume.example.com/student7', 'https://portfolio.example.com/student7'),
(8, 'Business Administration', 2, 'Leadership, Strategy, MS Office', 'Consulting, Startups', 'Compact', 'https://resume.example.com/student8', 'https://portfolio.example.com/student8'),
(9, 'Marketing', 3, 'Digital Marketing, SEO, Analytics', 'Social Media, Branding', 'Detailed', 'https://resume.example.com/student9', 'https://portfolio.example.com/student9'),
(10, 'Finance', 4, 'Accounting, Budgeting, Excel', 'Investing, Stock Market', 'Compact', 'https://resume.example.com/student10', 'https://portfolio.example.com/student10'),
(11, 'Psychology', 3, 'SPSS, Research Methods', 'Behavioral Studies, Therapy', 'Detailed', 'https://resume.example.com/student11', 'https://portfolio.example.com/student11'),
(12, 'Cybersecurity', 4, 'Network Security, Ethical Hacking', 'Cryptography, Data Privacy', 'Compact', 'https://resume.example.com/student12', 'https://portfolio.example.com/student12'),
(13, 'Robotics', 3, 'ROS, Python, Machine Vision', 'Automation, Embedded Systems', 'Detailed', 'https://resume.example.com/student13', 'https://portfolio.example.com/student13'),
(14, 'Environmental Science', 2, 'GIS, Remote Sensing', 'Climate Change, Policy Analysis', 'Compact', 'https://resume.example.com/student14', 'https://portfolio.example.com/student14'),
(15, 'Mathematics', 4, 'Linear Algebra, MATLAB', 'Topology, Numerical Analysis', 'Detailed', 'https://resume.example.com/student15', 'https://portfolio.example.com/student15'),
(31, 'English Literature', 4, 'Creative Writing, Storytelling', 'Writing, Editing', 'Compact', 'https://resume.example.com/student21', 'https://portfolio.example.com/student21'),
(32, 'Journalism', 3, 'SEO Writing, Editing', 'Digital Media, Marketing', 'Detailed', 'https://resume.example.com/student22', 'https://portfolio.example.com/student22'),
(33, 'Marketing', 2, 'Content Creation, Copywriting', 'Social Media, Branding', 'Compact', 'https://resume.example.com/student23', 'https://portfolio.example.com/student23'),
(34, 'Computer Science', 4, 'React, Node.js, SQL', 'Web Development, Databases', 'Detailed', 'https://resume.example.com/student24', 'https://portfolio.example.com/student24'),
(35, 'Software Engineering', 3, 'Full Stack Development, Agile', 'Cloud Computing, AI', 'Compact', 'https://resume.example.com/student25', 'https://portfolio.example.com/student25'),
(36, 'Data Science', 4, 'Python, R, Machine Learning', 'Big Data, Analytics', 'Detailed', 'https://resume.example.com/student26', 'https://portfolio.example.com/student26');



INSERT INTO Recruiters (UserID, Company, PositionPostedCount, FiltersPreferences, RecruiterType) VALUES
(11, 'GreenTech Innovations', 12, 'Skills=Renewable Energy, Location=California', 'In-house'),
(12, 'NextWave Solutions', 10, 'Experience=Mid, Industry=Finance', 'Agency'),
(13, 'BioMed Inc.', 8, 'Skills=Biotech, Location=Boston', 'In-house'),
(14, 'Skyline Builders', 15, 'Experience=Entry, Industry=Civil Engineering', 'Agency'),
(15, 'QuantumAI Labs', 20, 'Skills=AI, Experience=Senior', 'In-house'),
(16, 'Bright Future Education', 7, 'Industry=Education, Location=Remote', 'Agency'),
(17, 'CyberShield Security', 18, 'Skills=Cybersecurity, Location=New York', 'In-house'),
(18, 'PixelPerfect Studios', 10, 'Skills=Animation, Industry=Media', 'Agency'),
(19, 'AgroFuture', 9, 'Skills=AgriTech, Experience=Entry', 'In-house'),
(20, 'BlueSky Aerospace', 16, 'Skills=Aerospace Engineering, Location=Texas', 'Agency');
INSERT INTO Recruiters (UserID, Company, PositionPostedCount, FiltersPreferences, RecruiterType) VALUES
(21, 'CodeWave', 25, 'Skills=Full Stack, Location=San Francisco', 'Agency'),
(22, 'GigaTech', 30, 'Skills=Cloud Computing, Experience=Senior', 'In-house'),
(14, 'CyberShield Security', 18, 'Skills=Cybersecurity, Location=New York', 'In-house'),
(12, 'QuantumAI Labs', 20, 'Skills=AI, Experience=Senior', 'In-house'),
(35, 'BrightMedia Group', 15, 'Skills=Social Media, Industry=Marketing', 'Agency'),
(11, 'Skyline Builders', 15, 'Experience=Entry, Industry=Civil Engineering', 'Agency'),
(26, 'UrbanDesigners', 8, 'Skills=Architecture, Location=Los Angeles', 'In-house'),
(34, 'AI Insights', 12, 'Skills=Machine Learning, Location=Remote', 'In-house'),
(15, 'PixelPerfect Studios', 10, 'Skills=Animation, Industry=Media', 'Agency'),
(9, 'NextWave Solutions', 10, 'Experience=Mid, Industry=Finance', 'Agency'),
(19, 'EcoLife Innovations', 12, 'Skills=Sustainability, Location=Seattle', 'Agency'),
(24, 'Visionary Films', 10, 'Skills=Editing, Industry=Media', 'In-house'),
(28, 'NextGen Health', 20, 'Skills=Public Health, Experience=Entry', 'In-house'),
(51, 'TechCorp', 30, 'Skills=React, Location=Remote', 'In-house'),
(2, 'Innovate Inc.', 15, 'Skills=Project Management, Agile', 'Agency'),
(17, 'BlueSky Aerospace', 16, 'Skills=Aerospace Engineering, Location=Texas', 'Agency'),
(20, 'HealthPlus Systems', 14, 'Industry=Healthcare, Location=Remote', 'In-house'),
(23, 'FinancePro Consultants', 18, 'Skills=Finance, Location=Chicago', 'Agency'),
(37, 'EcoUrban Planners', 14, 'Skills=Environmental Science, Location=Seattle', 'Agency'),
(18, 'DataHaven', 22, 'Skills=Data Analytics, Experience=Mid', 'In-house'),
(31, 'SafeNet Systems', 16, 'Skills=Cybersecurity, Experience=Mid', 'Agency'),
(27, 'InnovateEd', 12, 'Industry=Education, Location=Boston', 'Agency'),
(25, 'NeuroTech Labs', 14, 'Skills=Neuroscience, Experience=Senior', 'Agency'),
(33, 'FreshStart Farms', 10, 'Skills=AgriTech, Location=Iowa', 'Agency'),
(30, 'AlphaRobotics', 22, 'Skills=Robotics, Location=New York', 'In-house'),
(39, 'Orbit Solutions', 20, 'Skills=Space Science, Location=Texas', 'Agency'),
(40, 'GlobalLingua', 10, 'Skills=Linguistics, Experience=Entry', 'In-house');

INSERT INTO Employers (name, industry, location, status) VALUES
('Tech Innovations Ltd.', 'Technology', 'San Francisco, CA', 'active'),
('GreenBuild Corp.', 'Construction', 'Los Angeles, CA', 'active'),
('DataMinds Analytics', 'Data Science', 'New York, NY', 'active'),
('HealthPlus Medical', 'Healthcare', 'Chicago, IL', 'inactive'),
('AutoTech Solutions', 'Automotive', 'Detroit, MI', 'active'),
('Creative Minds Agency', 'Marketing', 'Miami, FL', 'inactive'),
('EcoGreen Enterprises', 'Environmental', 'Seattle, WA', 'active'),
('FinTech Partners', 'Finance', 'Boston, MA', 'active'),
('Smart Systems Inc.', 'Electronics', 'Austin, TX', 'inactive'),
('Global Retailers', 'Retail', 'Dallas, TX', 'active');

INSERT INTO Jobs (Title, Company, Description, Requirements, Status, PostedBy, DatePosted, Deadline, Location, SalaryRange) VALUES
('Frontend Developer Intern', 'CodeWave', 'Develop and maintain UI components', 'HTML, CSS, JavaScript', 'Open', 21, '2024-01-16', '2024-02-16', 'San Francisco', '$20/hr'),
('Backend Developer Intern', 'GigaTech', 'Work on server-side logic and database management', 'Python, Django, SQL', 'Open', 22, '2024-01-18', '2024-02-18', 'Remote', '$25/hr'),
('Cybersecurity Analyst', 'CyberShield Security', 'Monitor and secure networks', 'Network Security, Kali Linux', 'Open', 14, '2024-01-19', '2024-02-19', 'New York', '$30/hr'),
('Data Scientist', 'QuantumAI Labs', 'Analyze large datasets and build ML models', 'Python, R, Machine Learning', 'Open', 12, '2024-01-20', '2024-02-20', 'Boston', '$35/hr'),
('Marketing Specialist Intern', 'BrightMedia Group', 'Assist in marketing campaigns', 'SEO, Social Media', 'Open', 35, '2024-01-21', '2024-02-21', 'Remote', '$18/hr'),
('Mechanical Engineer Intern', 'Skyline Builders', 'Design and analyze mechanical systems', 'SolidWorks, AutoCAD', 'Open', 11, '2024-01-22', '2024-02-22', 'Texas', '$22/hr'),
('Civil Engineer Intern', 'UrbanDesigners', 'Support structural and civil projects', 'STAAD Pro, AutoCAD', 'Open', 26, '2024-01-23', '2024-02-23', 'Los Angeles', '$20/hr'),
('AI Research Assistant', 'AI Insights', 'Support AI research projects', 'Deep Learning, TensorFlow', 'Open', 34, '2024-01-24', '2024-02-24', 'Remote', '$28/hr'),
('Graphic Designer Intern', 'PixelPerfect Studios', 'Create graphics and visuals for marketing', 'Photoshop, Illustrator', 'Open', 15, '2024-01-25', '2024-02-25', 'New York', '$18/hr'),
('Business Analyst Intern', 'NextWave Solutions', 'Analyze business processes', 'Excel, SQL', 'Open', 9, '2024-01-26', '2024-02-26', 'Chicago', '$24/hr'),
('Supply Chain Analyst', 'EcoLife Innovations', 'Optimize supply chain processes', 'Logistics, ERP Software', 'Open', 19, '2024-01-27', '2024-02-27', 'Seattle', '$28/hr'),
('Senior Content Writer', 'TechCorp', 'Write scripts and promotional content', 'Creative Writing, Storytelling', 'Open', 24, '2024-01-28', '2024-02-28', 'Remote', '$20/hr');
INSERT INTO Jobs (Title, Company, Description, Requirements, Status, PostedBy, DatePosted, Deadline, Location, SalaryRange) VALUES
('Frontend Developer Intern', 'CodeWave', 'Develop and maintain UI components', 'HTML, CSS, JavaScript', 'Open', 21, '2024-01-16', '2024-02-16', 'San Francisco', '$20/hr'),
('Backend Developer Intern', 'GigaTech', 'Work on server-side logic and database management', 'Python, Django, SQL', 'Open', 22, '2024-01-18', '2024-02-18', 'Remote', '$25/hr'),
('Cybersecurity Analyst', 'CyberShield Security', 'Monitor and secure networks', 'Network Security, Kali Linux', 'Open', 14, '2024-01-19', '2024-02-19', 'New York', '$30/hr'),
('Data Scientist', 'QuantumAI Labs', 'Analyze large datasets and build ML models', 'Python, R, Machine Learning', 'Open', 12, '2024-01-20', '2024-02-20', 'Boston', '$35/hr'),
('Marketing Specialist Intern', 'BrightMedia Group', 'Assist in marketing campaigns', 'SEO, Social Media', 'Open', 35, '2024-01-21', '2024-02-21', 'Remote', '$18/hr'),
('Mechanical Engineer Intern', 'Skyline Builders', 'Design and analyze mechanical systems', 'SolidWorks, AutoCAD', 'Open', 11, '2024-01-22', '2024-02-22', 'Texas', '$22/hr'),
('Civil Engineer Intern', 'UrbanDesigners', 'Support structural and civil projects', 'STAAD Pro, AutoCAD', 'Open', 26, '2024-01-23', '2024-02-23', 'Los Angeles', '$20/hr'),
('AI Research Assistant', 'AI Insights', 'Support AI research projects', 'Deep Learning, TensorFlow', 'Open', 34, '2024-01-24', '2024-02-24', 'Remote', '$28/hr'),
('Graphic Designer Intern', 'PixelPerfect Studios', 'Create graphics and visuals for marketing', 'Photoshop, Illustrator', 'Open', 15, '2024-01-25', '2024-02-25', 'New York', '$18/hr'),
('Business Analyst Intern', 'NextWave Solutions', 'Analyze business processes', 'Excel, SQL', 'Open', 9, '2024-01-26', '2024-02-26', 'Chicago', '$24/hr'),
('Supply Chain Analyst', 'EcoLife Innovations', 'Optimize supply chain processes', 'Logistics, ERP Software', 'Open', 19, '2024-01-27', '2024-02-27', 'Seattle', '$28/hr'),
('Content Writer', 'TechCorp', 'Write scripts and promotional content', 'Creative Writing, Storytelling', 'Open', 24, '2024-01-28', '2024-02-28', 'Remote', '$20/hr'),
('Health Informatics Specialist', 'NextGen Health', 'Manage health data systems', 'SQL, Healthcare IT', 'Open', 28, '2024-01-29', '2024-02-29', 'Remote', '$26/hr'),
('Full Stack Developer', 'TechCorp', 'Develop and manage web applications', 'React, Node.js, SQL', 'Open', 24, '2024-01-30', '2024-03-01', 'Remote', '$30/hr'),
('Product Manager Intern', 'Innovate Inc.', 'Assist in product lifecycle management', 'Project Management, Agile', 'Open', 2, '2024-02-01', '2024-03-01', 'New York', '$25/hr');
INSERT INTO Jobs (Title, Company, Description, Requirements, Status, PostedBy, DatePosted, Deadline, Location, SalaryRange) VALUES
('Software Engineer Intern', 'TechCorp', 'Develop and test software', 'Python, SQL, Teamwork', 'Open', 24, '2024-01-15', '2024-02-15', 'Remote', '$25/hr'),
('Data Analyst Intern', 'Innovate Inc.', 'Analyze datasets and prepare reports', 'SQL, R, Excel', 'Open', 2, '2024-01-20', '2024-02-20', 'New York', '$22/hr'),
('Frontend Developer Intern', 'CodeWave', 'Develop and maintain UI components', 'HTML, CSS, JavaScript', 'Open', 21, '2024-01-16', '2024-02-16', 'San Francisco', '$20/hr'),
('Backend Developer Intern', 'GigaTech', 'Work on server-side logic and database management', 'Python, Django, SQL', 'Open', 22, '2024-01-18', '2024-02-18', 'Remote', '$25/hr'),
('Cybersecurity Analyst', 'CyberShield Security', 'Monitor and secure networks', 'Network Security, Kali Linux', 'Open', 14, '2024-01-19', '2024-02-19', 'New York', '$30/hr'),
('Data Scientist', 'QuantumAI Labs', 'Analyze large datasets and build ML models', 'Python, R, Machine Learning', 'Open', 12, '2024-01-20', '2024-02-20', 'Boston', '$35/hr');



INSERT INTO Applications (StudentID, JobID, Status, DateApplied, ReviewScore, Feedback) VALUES
(1, 1, 'Pending', '2024-01-20', NULL, NULL),
(2, 2, 'Accepted', '2024-01-22', 85, 'Great match for the role'),
(3, 3, 'Rejected', '2024-01-25', 65, 'Needs more technical experience'),
(4, 4, 'Pending', '2024-01-28', NULL, NULL),
(5, 5, 'Accepted', '2024-01-30', 90, 'Impressive skills and background'),
(6, 6, 'Rejected', '2024-02-01', 72, 'Overqualified for the position'),
(7, 7, 'Accepted', '2024-02-03', 88, 'Excellent cultural fit'),
(8, 8, 'Pending', '2024-02-05', NULL, NULL),
(9, 9, 'Rejected', '2024-02-07', 50, 'Lacks required certifications'),
(10, 10, 'Accepted', '2024-02-09', 82, 'Good potential with some training'),
(11, 11, 'Pending', '2024-02-10', NULL, NULL),
(12, 12, 'Accepted', '2024-02-11', 91, 'Outstanding performance in interview'),
(13, 13, 'Rejected', '2024-02-12', 60, 'Skills mismatch for the role'),
(14, 14, 'Pending', '2024-02-13', NULL, NULL),
(15, 15, 'Accepted', '2024-02-14', 87, 'Proven track record of success');

INSERT INTO Applications (StudentID, JobID, Status, DateApplied, ReviewScore, Feedback) VALUES
-- Applications for Content Writer Job
(16, 24, 'Pending', '2024-01-30', NULL, NULL),  -- John Doe applied for Content Writer
(17, 24, 'Accepted', '2024-01-29', 90, 'Excellent writing samples'),  -- Jane Smith applied for Content Writer
(18, 24, 'Rejected', '2024-01-28', 65, 'Not a good fit'),  -- Alice Brown applied for Content Writer

-- Applications for Full Stack Developer Job
(19, 26, 'Pending', '2024-01-25', NULL, NULL),  -- Tom Wilson applied for Full Stack Developer
(20, 26, 'Accepted', '2024-01-26', 88, 'Great technical skills'),  -- Diana Prince applied for Full Stack Developer
(21, 26, 'Rejected', '2024-01-24', 70, 'Needs more experience');  -- Mark Green applied for Full Stack Developer

-- Insert sample data into Interviews table
INSERT INTO Interviews (JobID, StudentID, InterviewDateTime, Notes) VALUES
-- Interviews for Content Writer Job
(24, 16, '2024-02-05 10:00:00', 'Discuss writing samples and creativity test.'),
(24, 17, '2024-02-06 14:00:00', 'Review portfolio and previous projects.'),
-- Interviews for Full Stack Developer Job
(26, 19, '2024-02-07 11:30:00', 'Technical round focusing on React and Node.js.'),
(26, 20, '2024-02-08 09:00:00', 'Assess full-stack development skills.');


INSERT INTO SavedJobs (StudentID, JobID, SaveDate) VALUES
(1, 1, '2024-01-20'),
(2, 2, '2024-01-21'),
(3, 3, '2024-01-22'),
(4, 4, '2024-01-23'),
(5, 5, '2024-01-24'),
(6, 6, '2024-01-25'),
(7, 7, '2024-01-26'),
(8, 8, '2024-01-27'),
(9, 9, '2024-01-28'),
(10, 10, '2024-01-29'),
(1, 11, '2024-01-30'),
(2, 12, '2024-01-31'),
(3, 13, '2024-02-01'),
(4, 14, '2024-02-02'),
(5, 15, '2024-02-03'),
(6, 16, '2024-02-04'),
(7, 17, '2024-02-05'),
(8, 18, '2024-02-06'),
(9, 19, '2024-02-07'),
(10, 20, '2024-02-08');


INSERT INTO RecommendedJobs (StudentID, JobID, MatchScore, PositionTitle) VALUES
(1, 1, 95, 'Software Engineer Intern'),
(2, 2, 90, 'Data Analyst Intern'),
(3, 3, 88, 'Frontend Developer Intern'),
(4, 4, 92, 'Backend Developer Intern'),
(5, 5, 85, 'Cybersecurity Analyst'),
(6, 6, 87, 'Data Scientist'),
(7, 7, 80, 'Marketing Specialist Intern'),
(8, 8, 84, 'Mechanical Engineer Intern'),
(9, 9, 89, 'Civil Engineer Intern'),
(10, 10, 93, 'AI Research Assistant'),
(11, 11, 86, 'Graphic Designer Intern'),
(12, 12, 94, 'Business Analyst Intern'),
(13, 13, 91, 'Supply Chain Analyst'),
(14, 14, 83, 'Content Writer'),
(15, 15, 88, 'Health Informatics Specialist');



-- Insert sample data for AdvisorMeetings (Weak Entity)
INSERT INTO AdvisorMeetings (StudentID, AdvisorID, MeetingDateTime, Purpose, Notes) VALUES
(1, 3, '2024-02-01', 'Career Planning', 'Discussed resume improvement'),
(2, 4, '2024-02-02', 'Internship Search', 'Suggested networking events'),
(3, 5, '2024-02-03', 'Skill Development', 'Recommended online courses'),
(4, 6, '2024-02-04', 'Project Guidance', 'Reviewed project scope'),
(5, 7, '2024-02-05', 'Research Opportunities', 'Provided insights on available labs'),
(6, 8, '2024-02-06', 'Course Selection', 'Discussed course prerequisites'),
(7, 9, '2024-02-07', 'Industry Trends', 'Shared recent industry updates'),
(8, 10, '2024-02-08', 'Mock Interview', 'Conducted behavioral interview'),
(9, 3, '2024-02-09', 'Job Applications', 'Reviewed application strategy'),
(10, 4, '2024-02-10', 'Networking Tips', 'Suggested LinkedIn optimizations'),
(11, 5, '2024-02-11', 'Research Proposal', 'Provided feedback on proposal draft'),
(12, 6, '2024-02-12', 'Leadership Skills', 'Discussed effective team management'),
(13, 7, '2024-02-13', 'Career Development', 'Helped identify professional mentors'),
(14, 8, '2024-02-14', 'Resume Writing', 'Aligned with industry standards'),
(15, 9, '2024-02-15', 'Networking Events', 'Recommended local meetups'),
(1, 10, '2024-02-16', 'Skill Enhancement', 'Focused on improving soft skills'),
(2, 3, '2024-02-17', 'Job Interview Prep', 'Practiced with mock scenarios'),
(3, 4, '2024-02-18', 'Career Goals', 'Explored research-oriented roles'),
(4, 5, '2024-02-19', 'Course Advice', 'Discussed electives for career growth'),
(5, 6, '2024-02-20', 'Professional Development', 'Advised on certification programs'),
(6, 7, '2024-02-21', 'Internship Review', 'Analyzed past internship experiences'),
(7, 8, '2024-02-22', 'Research Collaboration', 'Discussed potential research projects'),
(8, 9, '2024-02-23', 'Industry Research', 'Explored recent developments in AI'),
(9, 10, '2024-02-24', 'Portfolio Review', 'Evaluated online portfolio design'),
(10, 3, '2024-02-25', 'Conference Prep', 'Advised on networking strategies'),
(11, 4, '2024-02-26', 'Mock Presentations', 'Reviewed presentation skills'),
(12, 5, '2024-02-27', 'Job Offers', 'Compared multiple offers and benefits'),
(13, 6, '2024-02-28', 'Thesis Planning', 'Brainstormed thesis topics and ideas'),
(14, 7, '2024-02-29', 'Internship Opportunities', 'Suggested targeted applications'),
(15, 8, '2024-03-01', 'Alumni Network', 'Introduced to key alumni mentors'),
(1, 9, '2024-03-02', 'Career Exploration', 'Explored cross-domain opportunities'),
(2, 10, '2024-03-03', 'Resume Analysis', 'Provided in-depth resume feedback'),
(3, 3, '2024-03-04', 'Mock Coding Interviews', 'Practiced with live scenarios'),
(4, 4, '2024-03-05', 'Skill Assessment', 'Reviewed technical skill gaps'),
(5, 5, '2024-03-06', 'Leadership Guidance', 'Discussed soft skill improvement'),
(6, 6, '2024-03-07', 'Course Selection', 'Advised on selecting advanced courses'),
(7, 7, '2024-03-08', 'Thesis Discussion', 'Explored research objectives'),
(8, 8, '2024-03-09', 'Team Management', 'Focused on team project collaboration'),
(9, 9, '2024-03-10', 'Internship Strategies', 'Suggested industry networking events'),
(10, 10, '2024-03-11', 'Industry Overview', 'Discussed latest market trends'),
(11, 3, '2024-03-12', 'Career Transition', 'Explored alternate career paths'),
(12, 4, '2024-03-13', 'Presentation Skills', 'Reviewed public speaking strategies'),
(13, 5, '2024-03-14', 'Networking Preparation', 'Suggested ideal LinkedIn optimizations'),
(14, 6, '2024-03-15', 'Career Development', 'Focused on resume improvement'),
(15, 7, '2024-03-16', 'Job Opportunities', 'Discussed advanced positions in IT');

INSERT INTO Events (StudentID, EventName, CompanyName, EventDate, EventType) VALUES
-- Initial Entries
(1, 'Tech Networking Night', 'TechCorp', '2024-02-10', 'Networking'),
(2, 'Data Science Workshop', 'Innovate Inc.', '2024-02-15', 'Workshop'),
-- Additional Entries
(3, 'AI Symposium', 'QuantumAI Labs', '2024-02-20', 'Conference'),
(4, 'Mechanical Engineering Fair', 'Skyline Builders', '2024-02-25', 'Career Fair'),
(5, 'Cybersecurity Bootcamp', 'CyberShield Security', '2024-03-01', 'Workshop'),
(6, 'Marketing Summit', 'BrightMedia Group', '2024-03-05', 'Seminar'),
(7, 'Chemical Engineering Expo', 'EcoLife Innovations', '2024-03-10', 'Expo'),
(8, 'Business Leadership Talk', 'NextWave Solutions', '2024-03-15', 'Seminar'),
(9, 'Digital Marketing Webinar', 'PixelPerfect Studios', '2024-03-20', 'Webinar'),
(10, 'Finance Networking Event', 'FinancePro Consultants', '2024-03-25', 'Networking'),
(11, 'Psychology Research Forum', 'HealthPlus Systems', '2024-03-30', 'Conference'),
(12, 'Cybersecurity Hackathon', 'SafeNet Systems', '2024-04-05', 'Hackathon'),
(13, 'Robotics Competition', 'AlphaRobotics', '2024-04-10', 'Competition'),
(14, 'Environmental Awareness Day', 'EcoUrban Planners', '2024-04-15', 'Workshop'),
(15, 'Mathematics Colloquium', 'GigaTech', '2024-04-20', 'Seminar'),
(1, 'Software Development Meetup', 'CodeWave', '2024-04-25', 'Meetup'),
(2, 'Engineering Internship Panel', 'UrbanDesigners', '2024-04-30', 'Panel'),
(3, 'Civil Engineering Site Visit', 'Skyline Builders', '2024-05-05', 'Site Visit'),
(4, 'Electrical Engineering Workshop', 'BlueSky Aerospace', '2024-05-10', 'Workshop'),
(5, 'Data Science Seminar', 'DataHaven', '2024-05-15', 'Seminar'),
(6, 'IT Career Fair', 'TechCorp', '2024-05-20', 'Career Fair'),
(7, 'Chemical Processes Lecture', 'BioMed Inc.', '2024-05-25', 'Lecture'),
(8, 'Business Startups Workshop', 'Innovate Inc.', '2024-05-30', 'Workshop'),
(9, 'Social Media Marketing Webinar', 'BrightMedia Group', '2024-06-05', 'Webinar'),
(10, 'Finance Industry Insights', 'FinancePro Consultants', '2024-06-10', 'Seminar'),
(11, 'Mental Health Awareness Event', 'NextGen Health', '2024-06-15', 'Seminar'),
(12, 'Ethical Hacking Workshop', 'CyberShield Security', '2024-06-20', 'Workshop'),
(13, 'Automation Conference', 'AlphaRobotics', '2024-06-25', 'Conference'),
(14, 'Climate Change Symposium', 'EcoLife Innovations', '2024-06-30', 'Symposium'),
(15, 'Math Puzzle Challenge', 'GigaTech', '2024-07-05', 'Competition'),
(1, 'AI and Machine Learning Forum', 'QuantumAI Labs', '2024-07-10', 'Conference'),
(2, 'Mechanical Design Competition', 'Skyline Builders', '2024-07-15', 'Competition'),
(3, 'Structural Engineering Seminar', 'UrbanDesigners', '2024-07-20', 'Seminar'),
(4, 'Electrical Systems Expo', 'BlueSky Aerospace', '2024-07-25', 'Expo'),
(5, 'Data Analytics Workshop', 'DataHaven', '2024-07-30', 'Workshop'),
(6, 'IT Security Meetup', 'SafeNet Systems', '2024-08-05', 'Meetup'),
(7, 'Sustainability Summit', 'EcoUrban Planners', '2024-08-10', 'Summit'),
(8, 'Entrepreneurship Talk', 'NextWave Solutions', '2024-08-15', 'Seminar'),
(9, 'Graphic Design Contest', 'PixelPerfect Studios', '2024-08-20', 'Competition'),
(10, 'Investment Strategies Workshop', 'FinancePro Consultants', '2024-08-25', 'Workshop'),
(11, 'Psychology Symposium', 'HealthPlus Systems', '2024-08-30', 'Symposium'),
(12, 'Cyber Defense Expo', 'CyberShield Security', '2024-09-05', 'Expo'),
(13, 'Robotics Hackathon', 'AlphaRobotics', '2024-09-10', 'Hackathon'),
(14, 'Environmental Policy Discussion', 'EcoLife Innovations', '2024-09-15', 'Discussion'),
(15, 'Mathematics Research Conference', 'GigaTech', '2024-09-20', 'Conference'),
(1, 'Software Engineering Workshop', 'CodeWave', '2024-09-25', 'Workshop'),
(2, 'Engineering Design Fair', 'Skyline Builders', '2024-09-30', 'Fair'),
(3, 'Infrastructure Development Seminar', 'UrbanDesigners', '2024-10-05', 'Seminar'),
(4, 'Aerospace Technology Expo', 'BlueSky Aerospace', '2024-10-10', 'Expo'),
(5, 'Big Data Conference', 'DataHaven', '2024-10-15', 'Conference');


INSERT INTO Notifications (UserID, Content, NotificationType, IsRead) VALUES
-- 'Reminder' Notifications
(1, 'Don’t forget to submit your application for the Software Engineer Intern position.', 'Reminder', FALSE),
(2, 'Your scheduled interview for Data Analyst Intern is tomorrow.', 'Reminder', FALSE),
(3, 'Deadline approaching for AI Symposium registration.', 'Reminder', FALSE),
(4, 'Update your profile to enhance job matches.', 'Reminder', TRUE),
(5, 'The job posting for Frontend Developer Intern closes in 3 days.', 'Reminder', FALSE),
(6, 'Complete your application for the Cybersecurity Analyst role.', 'Reminder', FALSE),
(7, 'Finalize your resume for the upcoming career fair.', 'Reminder', FALSE),
(8, 'Register for the Robotics Workshop before the deadline.', 'Reminder', TRUE),
(9, 'Prepare for the mock interview session this weekend.', 'Reminder', FALSE),
(10, 'Your meeting with Co-op Advisor is tomorrow at 10:00 AM.', 'Reminder', FALSE),

-- 'Alert' Notifications
(11, 'Your interview for Backend Developer Intern is starting in 30 minutes.', 'Alert', FALSE),
(12, 'New login detected from a different device.', 'Alert', TRUE),
(13, 'Changes were made to your application status.', 'Alert', FALSE),
(14, 'Your resume has been viewed by GigaTech.', 'Alert', TRUE),
(15, 'Important: The AI Symposium venue has changed.', 'Alert', FALSE),
(16, 'Your event registration has been confirmed.', 'Alert', TRUE),
(17, 'A new job posting matches your profile.', 'Alert', FALSE),
(18, 'Your account password was recently changed.', 'Alert', TRUE),
(19, 'Application review complete for Business Analyst Intern.', 'Alert', FALSE),
(20, 'Security alert: Unusual activity detected on your account.', 'Alert', FALSE),

-- 'Update' Notifications
(21, 'Your application for Cybersecurity Analyst has been accepted.', 'Update', TRUE),
(22, 'The workshop “Introduction to Machine Learning” has been added to your events.', 'Update', FALSE),
(23, 'Your account settings have been successfully updated.', 'Update', TRUE),
(24, 'You have a new connection request on the platform.', 'Update', FALSE),
(25, 'Your application for Data Science Intern is under review.', 'Update', FALSE),
(26, 'New feature: Customize your job alerts based on preferences.', 'Update', TRUE),
(27, 'A recruiter has sent you a message.', 'Update', FALSE),
(28, 'New networking event added: AI and Ethics Symposium.', 'Update', FALSE),
(29, 'Your attendance has been marked for the Robotics Workshop.', 'Update', TRUE),
(30, 'Career tips updated: How to ace your technical interviews.', 'Update', TRUE);




INSERT INTO PlatformAnalytics (UserID, UsageDuration, ActivityType, DeviceType, Date) VALUES
(1, 120, 'Job Search', 'Mobile', '2024-01-15'),
(2, 90, 'Profile Update', 'Desktop', '2024-01-16'),
(3, 75, 'Resume Upload', 'Mobile', '2024-01-17'),
(4, 60, 'Job Search', 'Tablet', '2024-01-18'),
(5, 45, 'Event Registration', 'Desktop', '2024-01-19'),
(6, 150, 'Job Application', 'Mobile', '2024-01-20'),
(7, 80, 'Profile Update', 'Desktop', '2024-01-21'),
(8, 100, 'Job Search', 'Tablet', '2024-01-22'),
(9, 200, 'Job Application', 'Mobile', '2024-01-23'),
(10, 50, 'Resume Upload', 'Desktop', '2024-01-24'),
(11, 90, 'Event Registration', 'Mobile', '2024-01-25'),
(12, 140, 'Job Search', 'Tablet', '2024-01-26'),
(13, 60, 'Profile Update', 'Mobile', '2024-01-27'),
(14, 170, 'Job Application', 'Desktop', '2024-01-28'),
(15, 30, 'Resume Upload', 'Tablet', '2024-01-29'),
(16, 85, 'Job Search', 'Mobile', '2024-01-30'),
(17, 120, 'Event Registration', 'Desktop', '2024-01-31'),
(18, 95, 'Job Application', 'Tablet', '2024-02-01'),
(19, 110, 'Profile Update', 'Mobile', '2024-02-02'),
(20, 45, 'Resume Upload', 'Desktop', '2024-02-03'),
(21, 75, 'Job Search', 'Tablet', '2024-02-04'),
(22, 130, 'Job Application', 'Mobile', '2024-02-05'),
(23, 65, 'Event Registration', 'Desktop', '2024-02-06'),
(24, 180, 'Profile Update', 'Mobile', '2024-02-07'),
(25, 90, 'Job Search', 'Tablet', '2024-02-08'),
(26, 50, 'Resume Upload', 'Desktop', '2024-02-09'),
(27, 60, 'Job Application', 'Mobile', '2024-02-10'),
(28, 75, 'Event Registration', 'Tablet', '2024-02-11'),
(29, 150, 'Job Search', 'Mobile', '2024-02-12'),
(30, 120, 'Resume Upload', 'Desktop', '2024-02-13'),
(31, 45, 'Job Application', 'Tablet', '2024-02-14'),
(32, 80, 'Profile Update', 'Mobile', '2024-02-15'),
(33, 170, 'Job Search', 'Desktop', '2024-02-16'),
(34, 100, 'Event Registration', 'Mobile', '2024-02-17'),
(35, 140, 'Resume Upload', 'Tablet', '2024-02-18'),
(36, 65, 'Job Application', 'Mobile', '2024-02-19'),
(37, 95, 'Profile Update', 'Desktop', '2024-02-20'),
(38, 60, 'Job Search', 'Tablet', '2024-02-21'),
(39, 75, 'Event Registration', 'Mobile', '2024-02-22'),
(40, 150, 'Resume Upload', 'Desktop', '2024-02-23'),
(41, 85, 'Job Application', 'Tablet', '2024-02-24'),
(42, 130, 'Profile Update', 'Mobile', '2024-02-25'),
(43, 45, 'Job Search', 'Desktop', '2024-02-26'),
(44, 95, 'Event Registration', 'Tablet', '2024-02-27'),
(45, 170, 'Resume Upload', 'Mobile', '2024-02-28'),
(46, 50, 'Job Application', 'Desktop', '2024-02-29'),
(47, 120, 'Job Search', 'Tablet', '2024-03-01'),
(48, 65, 'Event Registration', 'Mobile', '2024-03-02'),
(49, 75, 'Profile Update', 'Desktop', '2024-03-03'),
(50, 180, 'Resume Upload', 'Tablet', '2024-03-04');


INSERT INTO ITServices (PlatformUsageMetrics, SystemHealthLogs, IssueTicketsCount) VALUES
('High activity from 9 AM - 5 PM', 'No critical errors', 5),
('Moderate activity from 8 AM - 4 PM', 'Minor warning logs', 3),
('Low activity after 6 PM', 'Routine maintenance logs', 2),
('High activity from 10 AM - 6 PM', 'No major issues', 4),
('Peak activity from 11 AM - 3 PM', 'Database optimization alerts', 6),
('Moderate activity from 7 AM - 3 PM', 'Patch deployment logs', 3),
('High activity from 12 PM - 8 PM', 'No warnings', 1),
('Low activity from 6 PM onwards', 'Server reboot logs', 2),
('Moderate activity from 9 AM - 1 PM', 'Scheduled backup logs', 2),
('Peak activity from 10 AM - 2 PM', 'Memory usage spikes', 7),
('High activity from 11 AM - 7 PM', 'Disk space alerts', 5),
('Moderate activity from 8 AM - 2 PM', 'Minor service interruptions', 3),
('Peak activity from 12 PM - 4 PM', 'System overload logs', 8),
('Low activity after 5 PM', 'Routine checks', 1),
('High activity from 9 AM - 6 PM', 'CPU usage warnings', 4),
('Moderate activity from 10 AM - 5 PM', 'No critical issues', 2),
('Low activity from 7 PM onwards', 'Scheduled downtime', 3),
('High activity from 11 AM - 4 PM', 'System error recovery logs', 6),
('Peak activity from 10 AM - 3 PM', 'Cache clearing alerts', 4),
('Moderate activity from 8 AM - 6 PM', 'No logged errors', 1),
('High activity from 10 AM - 5 PM', 'Database tuning logs', 7),
('Moderate activity from 9 AM - 3 PM', 'Routine maintenance', 2),
('Peak activity from 12 PM - 6 PM', 'Disk usage warnings', 6),
('Low activity after 6 PM', 'Routine updates', 1),
('High activity from 11 AM - 7 PM', 'No warnings', 3),
('Moderate activity from 10 AM - 4 PM', 'Patch installation logs', 5),
('Peak activity from 9 AM - 2 PM', 'System reboot logs', 4),
('High activity from 12 PM - 5 PM', 'Memory optimization logs', 6),
('Low activity from 8 PM onwards', 'Scheduled maintenance', 2),
('Moderate activity from 7 AM - 2 PM', 'No anomalies detected', 1),
('High activity from 8 AM - 4 PM', 'System update logs', 4),
('Low activity after 7 PM', 'Routine alerts', 2),
('Peak activity from 10 AM - 1 PM', 'Disk optimization alerts', 6),
('Moderate activity from 6 AM - 12 PM', 'No warnings', 3),
('High activity from 9 AM - 6 PM', 'Critical error logs', 7),
('Low activity from 8 PM - 11 PM', 'System backup logs', 1),
('Moderate activity from 10 AM - 2 PM', 'Performance tuning logs', 4),
('High activity from 7 AM - 3 PM', 'Routine checks', 5),
('Peak activity from 12 PM - 8 PM', 'Minor issues logged', 2),
('Moderate activity from 9 AM - 5 PM', 'System stability reports', 3),
('High activity from 8 AM - 5 PM', 'No anomalies detected', 6),
('Low activity from 6 PM - 10 PM', 'Routine maintenance logs', 2),
('Moderate activity from 10 AM - 4 PM', 'Minor warning logs', 1),
('Peak activity from 9 AM - 3 PM', 'Critical disk warnings', 7),
('High activity from 11 AM - 7 PM', 'Routine service checks', 3),
('Moderate activity from 10 AM - 6 PM', 'Patch updates', 4),
('Low activity from 8 PM onwards', 'Routine maintenance alerts', 2);

INSERT INTO ITServices (PlatformUsageMetrics, SystemHealthLogs, IssueTicketsCount) VALUES
('Moderate activity from 8 AM - 4 PM', 'Routine server checks completed', 3),
('Peak activity from 10 AM - 3 PM', 'Memory optimization warnings', 4),
('Low activity from 6 PM onwards', 'Scheduled server maintenance logs', 2),
('High activity from 9 AM - 6 PM', 'Critical error reports resolved', 5),
('Moderate activity from 7 AM - 3 PM', 'No significant warnings logged', 1),
('Peak activity from 12 PM - 5 PM', 'Cache clearing operations', 2),
('High activity from 10 AM - 4 PM', 'Database tuning completed successfully', 4),
('Moderate activity from 9 AM - 1 PM', 'Minor disk space alerts', 3),
('Peak activity from 11 AM - 7 PM', 'Routine checks and performance updates', 6),
('Low activity after 8 PM', 'Scheduled security updates', 1),
('High activity from 10 AM - 6 PM', 'Routine error handling logs', 5),
('Moderate activity from 8 AM - 2 PM', 'Backup procedures completed', 2),
('Peak activity from 11 AM - 4 PM', 'Disk optimization reports', 4),
('Moderate activity from 9 AM - 5 PM', 'Performance monitoring logs', 3),
('Low activity after 7 PM', 'Routine downtime notifications', 2),
('High activity from 8 AM - 4 PM', 'Error recovery tasks executed', 4),
('Moderate activity from 10 AM - 3 PM', 'Security scan reports', 3),
('Peak activity from 9 AM - 1 PM', 'Critical disk warnings addressed', 6),
('High activity from 11 AM - 5 PM', 'System stability maintained', 2),
('Low activity from 8 PM onwards', 'Routine update logs', 5);





INSERT INTO SystemAlerts (ITID, AlertType, ResolutionStatus, Severity) VALUES
(1, 'Database Connectivity', 'Resolved', 'Medium'),
(2, 'Unauthorized Access Attempt', 'Pending', 'High'),
(3, 'Server Overload', 'Resolved', 'High'),
(4, 'Memory Usage Spike', 'Pending', 'Low'),
(5, 'Disk Space Warning', 'Resolved', 'Medium'),
(6, 'Software Update Failure', 'Resolved', 'High'),
(7, 'Network Latency', 'Pending', 'Medium'),
(8, 'Unauthorized API Call', 'Resolved', 'High'),
(9, 'Firewall Configuration Issue', 'Pending', 'High'),
(10, 'Backup Failure', 'Resolved', 'High'),
(11, 'Cache Overflow', 'Resolved', 'Low'),
(12, 'CPU Usage Spike', 'Pending', 'Medium'),
(13, 'Unauthorized Login', 'Resolved', 'High'),
(14, 'Patch Installation Error', 'Resolved', 'Medium'),
(15, 'Scheduled Downtime Alert', 'Resolved', 'Low'),
(16, 'SSL Certificate Expiry', 'Pending', 'High'),
(17, 'System Overload', 'Resolved', 'High'),
(18, 'Database Locking', 'Pending', 'Medium'),
(19, 'DNS Failure', 'Resolved', 'High'),
(20, 'Login Failure', 'Resolved', 'Medium'),
(21, 'Unauthorized Data Export', 'Pending', 'High'),
(22, 'Email Notification Failure', 'Resolved', 'Low'),
(23, 'Firewall Rule Conflict', 'Pending', 'High'),
(24, 'Disk IO Latency', 'Resolved', 'Medium'),
(25, 'Network Congestion', 'Resolved', 'Medium'),
(26, 'Unauthorized File Access', 'Resolved', 'High'),
(27, 'API Gateway Timeout', 'Pending', 'High'),
(28, 'Power Outage Alert', 'Resolved', 'High'),
(29, 'Software Crash', 'Pending', 'Medium'),
(30, 'Memory Allocation Error', 'Resolved', 'Low'),
(31, 'System Log Overflow', 'Resolved', 'Medium'),
(32, 'Malware Detected', 'Pending', 'High'),
(33, 'Unexpected System Reboot', 'Resolved', 'High'),
(34, 'Database Query Timeout', 'Resolved', 'Medium'),
(35, 'Data Inconsistency Detected', 'Pending', 'High'),
(36, 'DNS Lookup Error', 'Resolved', 'Low'),
(37, 'Firewall Port Misconfiguration', 'Pending', 'High'),
(38, 'High Latency Detected', 'Resolved', 'Medium'),
(39, 'Resource Allocation Failure', 'Resolved', 'High'),
(40, 'Unauthorized Network Probe', 'Pending', 'High'),
(41, 'Load Balancer Failure', 'Resolved', 'High'),
(42, 'Backup Corruption', 'Resolved', 'High'),
(43, 'Unexpected System Shutdown', 'Pending', 'Medium'),
(44, 'User Session Timeout', 'Resolved', 'Low'),
(45, 'Malware Activity Suspicion', 'Pending', 'High'),
(46, 'API Rate Limit Exceeded', 'Resolved', 'Medium'),
(47, 'Unauthorized Remote Access', 'Pending', 'High'),
(48, 'Critical Service Failure', 'Resolved', 'High'),
(49, 'Login Anomaly Detected', 'Resolved', 'High'),
(50, 'Data Breach Attempt', 'Pending', 'High');


INSERT INTO Alumni (Name, GraduationYear, CoOpExperienceDetails, CurrentPosition, Company, LinkedInProfile) VALUES
('Michael Smith', 2020, 'Software Engineer Intern at TechCorp', 'Software Engineer', 'TechCorp', 'https://linkedin.com/in/michaelsmith'),
('Emily Johnson', 2019, 'Data Analyst Intern at Innovate Inc.', 'Data Scientist', 'Innovate Inc.', 'https://linkedin.com/in/emilyjohnson'),
('Christopher Brown', 2021, 'Cybersecurity Intern at CyberShield', 'Cybersecurity Analyst', 'CyberShield', 'https://linkedin.com/in/christopherbrown'),
('Sophia Davis', 2020, 'Machine Learning Intern at QuantumAI Labs', 'Machine Learning Engineer', 'QuantumAI Labs', 'https://linkedin.com/in/sophiadavis'),
('Matthew Martinez', 2018, 'Marketing Intern at BrightMedia Group', 'Marketing Specialist', 'BrightMedia Group', 'https://linkedin.com/in/matthewmartinez'),
('Olivia Garcia', 2022, 'Mechanical Engineer Intern at Skyline Builders', 'Mechanical Engineer', 'Skyline Builders', 'https://linkedin.com/in/oliviagarcia'),
('Daniel Wilson', 2020, 'Civil Engineer Intern at UrbanDesigners', 'Civil Engineer', 'UrbanDesigners', 'https://linkedin.com/in/danielwilson'),
('Ava Anderson', 2019, 'AI Research Assistant at AI Insights', 'AI Research Scientist', 'AI Insights', 'https://linkedin.com/in/avaanderson'),
('Ethan Thomas', 2021, 'Graphic Designer Intern at PixelPerfect Studios', 'Graphic Designer', 'PixelPerfect Studios', 'https://linkedin.com/in/ethanthomas'),
('Isabella Moore', 2020, 'Business Analyst Intern at NextWave Solutions', 'Business Analyst', 'NextWave Solutions', 'https://linkedin.com/in/isabellamoore'),
('James Taylor', 2018, 'Supply Chain Analyst Intern at EcoLife Innovations', 'Supply Chain Manager', 'EcoLife Innovations', 'https://linkedin.com/in/jamestaylor'),
('Mia Harris', 2021, 'Content Writer Intern at Visionary Films', 'Content Strategist', 'Visionary Films', 'https://linkedin.com/in/miaharris'),
('Alexander Clark', 2019, 'Health Informatics Intern at NextGen Health', 'Health Informatics Specialist', 'NextGen Health', 'https://linkedin.com/in/alexanderclark'),
('Charlotte Walker', 2022, 'Full Stack Developer Intern at TechCorp', 'Full Stack Developer', 'TechCorp', 'https://linkedin.com/in/charlottewalker'),
('Henry Lewis', 2018, 'Product Manager Intern at Innovate Inc.', 'Product Manager', 'Innovate Inc.', 'https://linkedin.com/in/henrylewis'),
('Amelia Young', 2020, 'Electrical Engineer Intern at BlueSky Aerospace', 'Electrical Engineer', 'BlueSky Aerospace', 'https://linkedin.com/in/ameliayoung'),
('Benjamin King', 2019, 'Public Health Coordinator Intern at HealthPlus Systems', 'Public Health Specialist', 'HealthPlus Systems', 'https://linkedin.com/in/benjaminking'),
('Harper Scott', 2021, 'Account Manager Intern at FinancePro Consultants', 'Account Manager', 'FinancePro Consultants', 'https://linkedin.com/in/harperscott'),
('Sebastian White', 2020, 'Software Tester Intern at CodeWave', 'Quality Assurance Engineer', 'CodeWave', 'https://linkedin.com/in/sebastianwhite'),
('Evelyn Hall', 2018, 'Machine Learning Engineer Intern at QuantumAI Labs', 'Data Scientist', 'QuantumAI Labs', 'https://linkedin.com/in/evelynhall'),
('Logan Allen', 2021, 'Architectural Intern at EcoUrban Planners', 'Architect', 'EcoUrban Planners', 'https://linkedin.com/in/loganallen'),
('Abigail Green', 2020, 'HR Coordinator Intern at Bright Future Education', 'HR Specialist', 'Bright Future Education', 'https://linkedin.com/in/abigailgreen'),
('Lucas Adams', 2019, 'DevOps Engineer Intern at GigaTech', 'DevOps Engineer', 'GigaTech', 'https://linkedin.com/in/lucasadams'),
('Ella Nelson', 2021, 'Environmental Analyst Intern at EcoLife Innovations', 'Environmental Scientist', 'EcoLife Innovations', 'https://linkedin.com/in/ellanelson'),
('Mason Perez', 2018, 'Data Engineer Intern at DataHaven', 'Data Engineer', 'DataHaven', 'https://linkedin.com/in/masonperez'),
('Aria Baker', 2020, 'Videographer Intern at Visionary Films', 'Video Producer', 'Visionary Films', 'https://linkedin.com/in/ariabaker'),
('Liam Mitchell', 2021, 'Accountant Intern at FinancePro Consultants', 'Accountant', 'FinancePro Consultants', 'https://linkedin.com/in/liammitchell'),
('Chloe Rodriguez', 2019, 'IT Support Specialist Intern at SafeNet Systems', 'IT Support Engineer', 'SafeNet Systems', 'https://linkedin.com/in/chloerodriguez'),
('Noah Rivera', 2020, 'Education Consultant Intern at InnovateEd', 'Education Consultant', 'InnovateEd', 'https://linkedin.com/in/noahrivera'),
('Grace Campbell', 2021, 'Research Assistant Intern at NeuroTech Labs', 'Research Scientist', 'NeuroTech Labs', 'https://linkedin.com/in/gracecampbell');

INSERT INTO ITEmployee (Email, EmpFirstName, EmpLastName) VALUES
('temp@company.com','Temp','Name'),
('jdoe@company.com', 'John', 'Doe'),
('asmith@company.com', 'Alice', 'Smith'),
('mbrown@company.com', 'Michael', 'Brown');

INSERT INTO ITAssets (assetName, ITStatus, assetType, assetDetails)
VALUES
('Firewall', 'Operational', 'Hardware', 'Secures the company network from external threats'),
('Load Balancer', 'Operational', 'Hardware', 'Distributes incoming traffic to servers'),
('Database Server', 'Needs Maintenance', 'Hardware', 'Stores transactional and analytics data'),
('Cloud Storage', 'Operational', 'Service', 'AWS S3 for backups and archives'),
('Endpoint Security Software', 'Needs Update', 'Software', 'Antivirus and malware protection for user endpoints'),
('Laptop', 'Operational', 'Hardware', 'Dell Latitude for remote work'),
('Printer', 'Operational', 'Hardware', 'HP LaserJet for office printing'),
('Email Server', 'Needs Maintenance', 'Hardware', 'Handles all company email traffic'),
('Switch', 'Operational', 'Hardware', 'Cisco Catalyst for LAN connectivity'),
('Router', 'Operational', 'Hardware', 'Handles all outgoing internet traffic'),
('Virtual Machine', 'Operational', 'Software', 'Windows Server 2019 for app hosting'),
('Antivirus Software', 'Operational', 'Software', 'McAfee Enterprise Security Suite'),
('Patch Management Software', 'Operational', 'Software', 'Automates software patching across the network'),
('Backup Server', 'Needs Maintenance', 'Hardware', 'Stores daily backups for disaster recovery'),
('Firewall Software', 'Operational', 'Software', 'Sophos for network security'),
('File Server', 'Operational', 'Hardware', 'Shared storage for company files'),
('CRM Software', 'Operational', 'Software', 'Manages customer relationships and interactions'),
('DNS Server', 'Operational', 'Hardware', 'Resolves domain names to IP addresses'),
('Patch Panel', 'Operational', 'Hardware', 'Connects network cables in server racks'),
('Network Analyzer', 'Operational', 'Software', 'Monitors network performance and detects anomalies');


INSERT INTO Tickets (TicketStatus, TicketDetails, FufilledBy) VALUES
('Open', 'Resolve slow database queries', 1),
('In Progress', 'Fix network latency issues', 2),
('Closed', 'Update endpoint security software', 4),
('Open', 'Install new patches on servers', 1),
('Closed', 'Configure new firewall rules', 2),
('In Progress', 'Replace failed hard drive on database server', 4),
('Open', 'Investigate high CPU usage on email server', 1),
('Closed', 'Update antivirus definitions on all endpoints', 3),
('Open', 'Reboot file server after maintenance', 1),
('Closed', 'Fix network switch connectivity issues', 2),
('Open', 'Troubleshoot VPN connection for remote employees', 1),
('In Progress', 'Analyze traffic for possible DDoS attack', 2),
('Closed', 'Implement new group policies for user access', 4),
('Open', 'Replace aging printer hardware', 1),
('In Progress', 'Test new backup server configuration', 2),
('Open', 'Deploy patch management software update', 1),
('Closed', 'Resolve user login issues on CRM software', 4),
('Open', 'Optimize network performance for cloud storage', 1),
('In Progress', 'Audit DNS server for configuration errors', 3),
('Closed', 'Fix broken patch panel in server room', 2);
