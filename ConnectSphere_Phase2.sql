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
DROP TABLE IF EXISTS Jobs;
DROP TABLE IF EXISTS CoOpAdvisors;
DROP TABLE IF EXISTS Alumni;
DROP TABLE IF EXISTS Recruiters;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Users;

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
    MeetingDate DATE,
    MeetingTime TIME,
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
    assetDetails TEXT,

);
-- Create the Tickets table 
CREATE TABLE Tickets (
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    TicketTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    TicketStatus TEXT,
    TicketDetails TEXT,
    FufilledBy INT NOT NULL,
    FOREIGN KEY (FufilledBy) REFERENCES ITEmployee(ITEmpID) 
);

-- Create the SystemAlerts table
CREATE TABLE SystemAlerts (
    AlertID INT AUTO_INCREMENT PRIMARY KEY,
    TicketID INT NOT NULL,
    AlertType VARCHAR(50),
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ResolutionStatus VARCHAR(50),
    Severity ENUM('Low', 'Medium', 'High'),
    FOREIGN KEY (TicketID) REFERENCES Tickets(TicketID) ON DELETE CASCADE
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

-- Insert sample data for Users
INSERT INTO Users (Name, Email, Role, Password) VALUES
('Alice Smith', 'alice.smith@example.com', 'Student', 'password1'),
('Bob Johnson', 'bob.johnson@example.com', 'Recruiter', 'password2'),
('Charlie Brown', 'charlie.brown@example.com', 'Advisor', 'password3');

-- Insert sample data for Students
INSERT INTO Students (UserID, Major, Year, Skills) VALUES
(1, 'Computer Science', 3, 'Python, SQL'),
(1, 'Data Science', 2, 'Machine Learning, R');

-- Insert sample data for Recruiters
INSERT INTO Recruiters (UserID, Company, PositionPostedCount) VALUES
(2, 'TechCorp', 10),
(2, 'Innovate Inc.', 5);

-- Insert sample data for Jobs
INSERT INTO Jobs (Title, Company, Description, Status, PostedBy, DatePosted) VALUES
('Software Engineer Intern', 'TechCorp', 'Develop and test software', 'Open', 1, '2024-01-15'),
('Data Analyst Intern', 'Innovate Inc.', 'Analyze datasets', 'Open', 2, '2024-02-01');
