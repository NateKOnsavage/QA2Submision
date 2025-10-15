Getting Started
Prerequisites
You need Python 3.x installed on your system. No external libraries are strictly required as this application uses standard libraries included with Python.

Installation and Setup
Save the Code: Save the entire Python code block you provided into a single file named quiz_bowl_app.py.

Run the Application: Open your terminal or command prompt, navigate to the directory where you saved the file, and run the application:

Bash
python quiz_bowl_app.py

Database Initialization: The first time you run the application, it will automatically create the SQLite database file named quiz_bowl.db and populate it with the initial placeholder questions for the four required courses (Database_Management, Intro_to_Theater, Organizational_Behavior, Applications_Development).

Usage Instructions
The application starts at the Login Screen, offering two paths: Student and Administrator.

Student Interface
The student interface is designed for taking quizzes.

Start Quiz: Click the Student button on the Login Screen.

Select Course: Choose a course category (e.g., Database Management).

Take Quiz: The quiz begins immediately with questions drawn randomly from the selected course.

Submit: Select an option and click Submit Answer. The application provides instant feedback and calculates a final score upon completion.

Administrator Interface
The administrator can manage the entire question bank.

Login: Click Login as Administrator and enter an approved password.

Default Passwords: admin or Admin

Dashboard Functions:

Option	Functionality
1. Add New Questions/Courses:	Allows you to add new questions to an existing course or automatically create a new course table by selecting its name.
2. View/Edit Questions:	Allows you to select a course and double-click a question in the list to open an edit window for modifying its text, options, or correct answer.
3. Delete Questions:	Allows you to select a course and delete individual questions using their ID.

Export to Sheets
Logout: Click Logout to return to the main login screen.

Application Structure
The code is organized into three main sections:

Database Management Functions: (db_execute, db_fetch, initialize_database, etc.) handle all interactions with the sqlite3 database.

Data Structure: The COURSE_TABLES_DATA dictionary holds the initial schema and placeholder content.

Main Application Class (QuizBowlApp): This is the core class that manages the GUI, state, and routing between the login, admin, and student screens.

Database Details
File: quiz_bowl.db

Tables: One table is created for each course (e.g., Database_Management).

Schema (for all tables):

Column	Type	Description
Question_ID	INTEGER	Primary Key, auto-incrementing.
Question_Text	TEXT	The full question text.
Option_A to Option_D	TEXT	The multiple-choice options (D is optional).
Correct_Answer	TEXT	Stores the letter of the correct option (e.g., 'A', 'B', 'C').
