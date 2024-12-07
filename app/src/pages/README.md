# `pages` Folder

This folder contains all the pages that will be part of the application. Details on required numbers will be provided in the Phase 3 documentation.

These pages are meant to show you an example of some of the features of Streamlit and the way we will limit functionality access by role/persona. It is not meant to represent a complete application.

TODO: Describe the pages folder and include link to documentation. Don't forget about ordering of pages.

# Pages Directory Overview

This folder contains all the Streamlit pages that are part of the application. These pages serve as examples of features available in the application and demonstrate how functionality is restricted based on role or persona. They are **not** meant to represent a full application but provide foundational components to showcase expected workflows and functionality.

The application is modularized into various pages for distinct user roles such as **Student**, **Co-op Advisor**, **Recruiter**, and **IT Service Head**, with routing and access logic configured accordingly.

---

## 🚀 Purpose

These pages demonstrate the following:

- **Streamlit Features:** Examples of UI workflows using Streamlit's interactive features.
- **Role-based Access:** How permissions and access are managed for different users (students, recruiters, co-op advisors, IT Service Heads).
- **Student Pages:** Profile management, application handling, and personalized recommendations.
- **Recruiter Pages:** Job postings, notifications, reports, and profile management for recruiters.
- **Co-op Advisor and IT Service Access:** Management workflows like progress tracking and asset handling.

Note that detailed feature descriptions and expected behaviors will be provided in the [Phase 3 documentation](#).

---

## 📄 Pages List and Functionality

Here is the ordered list of pages with their respective purposes:

### **Student Pages**
1. **00_student_Home.py**  
   Initial home page for student users. (Changes for Streamlit access.)
2. **05_student_profile.py**  
   Allows students to view and edit their profile information.
3. **06_Student_application.py**  
   Handles student application workflows and application history management.
4. **07_student_bookmark.py**  
   Enables bookmarking of relevant opportunities for students.
5. **08_student_recommendation.py**  
   Personalized job recommendations for students based on their interactions and history.
6. **09_student_meeting.py**  
   Manages meeting scheduling for student workflows.

### **Co-op Advisor Pages**
7. **20_Co-op_Advisor.py**  
   Entry point for Co-op Advisor dashboard-related tasks. Some fixed features and routing added.

8. **21_Student_Progress.py**  
   Displays student progress reports and tracks their placement data.

9. **22_Update_Placement.py**  
   Allows Co-op Advisors to make changes to placement data.

10. **23_Manage_Employer.py**  
    Interface for managing employer-related student opportunities and placement data.

11. **24_Advisor_Profile.py**  
    Advisor profile management functionalities.

---

### **Recruiter Pages**
12. **40_Recruiter_Home.py**  
    Entry UI for recruiters utilizing Flask and Streamlit integration.
13. **41_Dashboard.py**  
    Recruiter-specific dashboards for insights and quick views.
14. **41_Recruiter_Dashboard.py**  
    Expanded recruiter dashboards supporting deeper insights and reports.
15. **42_Recruiter_Jobs.py**  
    Job postings UI for recruiters to view, edit, and add jobs to the platform.
16. **42_Tickets.py**  
    Handles communication tickets for IT Service Head and recruiter support requests.
17. **43_Assets.py**  
    Asset management utilities for recruiter workflows.
18. **43_Recruiter_Job_Details.py**  
    Provides recruiters with detailed views of their posted opportunities.
19. **44_Recruiter_Notifications.py**  
    Notification center functionality for recruiter updates.
20. **45_Recruiter_Reports.py**  
    Allows recruiters to view performance, job opportunities, and data visualizations.
21. **46_Recruiter_Profile.py**  
    Profile page functionality for recruiters to manage their accounts.

---

### **IT Service Head Pages**
22. **40_ITService.py**  
    Landing page and initial routing for IT Service Head users.
23. **42_Tickets.py**  
    Ticket management functionalities for tracking communication workflows.

---

## 📚 Documentation

For a full understanding of the system design, expected features, access permissions, and workflows, refer to the [Phase 3 documentation](#).

---

## 🛠 How to Run These Pages

These pages are meant to be launched within a Streamlit environment. Instructions on running these pages will be included in the main repository `README.md`. For now:

1. Ensure Streamlit and all dependencies are installed.
2. Use the standard Streamlit launch workflow:

   ```bash
   streamlit run pages/00_student_Home.py
