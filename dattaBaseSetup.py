import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import random

DATABASE_FILE = 'quiz_bowl.db'
ADMIN_PASSWORDS = ['admin', 'Admin'] 
QUESTION_SCHEMA = """
(
    Question_ID INTEGER PRIMARY KEY,
    Question_Text TEXT NOT NULL,
    Option_A TEXT NOT NULL,
    Option_B TEXT NOT NULL,
    Option_C TEXT NOT NULL,
    Option_D TEXT,
    Correct_Answer TEXT NOT NULL
);
"""

# The four required course tables with at least 10 placeholder questions
COURSE_TABLES_DATA = {
    "Database_Management": [
        ("What is SQL?", "A structured query language", "A sequential query language", "A search query locator", None, "A"),
        ("What does CRUD stand for?", "Create, Retrieve, Update, Delete", "Count, Rebuild, Upload, Distribute", "Create, Read, Understand, Develop", None, "A"),
        ("Which is not a type of database model?", "Relational", "Hierarchical", "Sequential-Access", "Network", "C"),
        ("What is a Primary Key?", "A field that uniquely identifies a record", "A key that unlocks the database", "A field used for sorting", None, "A"),
        ("What is Normalization?", "Structuring a relational database to reduce data redundancy", "Making data columns the same size", "Sorting data alphabetically", None, "A"),
        ("What is a Foreign Key?", "A key used to link two tables together", "A primary key in another table", "A reference to a Primary Key in another table", "D"),
        ("What is a JOIN in SQL?", "A clause used to combine rows from two or more tables", "A command to permanently delete data", "A type of table constraint", None, "A"),
        ("What is an Index?", "A data structure that improves the speed of data retrieval operations", "A list of table columns", "The first row of a table", None, "A"),
        ("Which command removes a table and its data?", "DELETE", "REMOVE", "DROP TABLE", "TRUNCATE", "C"),
        ("Which clause filters results after aggregation?", "GROUP BY", "WHERE", "HAVING", "ORDER BY", "C"),
        ("What is a view in SQL?", "A virtual table based on the result-set of an SQL statement", "A graphical display of data", "A stored procedure", None, "A"),
    ],
    "Intro_to_Theater": [
        ("What is 'Blocking'?", "The planned stage movement of actors", "The process of memorizing lines", "The act of stopping another actor's performance", None, "A"),
        ("What is a 'Monologue'?", "A solo speech delivered by a character", "A short skit with two actors", "A dance number", None, "A"),
        ("What are 'Props'?", "Small items used by actors", "The scenery on stage", "The costumes worn", None, "A"),
        ("Who is often considered the 'Father of Drama'?", "Aristotle", "Shakespeare", "Thespis", "Socrates", "C"),
        ("What does 'Fourth Wall' refer to?", "The imaginary wall separating the stage from the audience", "The back wall of the theater", "The side walls of the set", None, "A"),
        ("A 'Tragedy' typically ends with:", "A catastrophic event and death", "A wedding", "A happy resolution", None, "A"),
        ("What is 'Improvisation'?", "Acting without a script", "Scripted dialogue", "Rehearsing lines", None, "A"),
        ("The 'Stage Left' is the actor's left when facing?", "The audience", "The back of the stage", "The wings", None, "A"),
        ("What is the main goal of a 'Chorus' in Greek theater?", "To comment on the action and provide background", "To provide musical entertainment", "To act as stagehands", None, "A"),
        ("What is 'Method Acting'?", "A technique where an actor tries to deeply understand a character's motives", "A style that uses only physical movement", "A quick way to memorize lines", None, "A"),
        ("What is the 'Dramaturg's' role?", "Assists the director with research and context", "Manages the budget", "Designs the lighting", None, "A"),
    ],
    "Organizational_Behavior": [
        ("What is 'Organizational Culture'?", "The shared values, beliefs, and norms of a group", "The building architecture", "The financial budget", None, "A"),
        ("What does the 'Big Five' model measure?", "Personality traits", "Company assets", "Project phases", None, "A"),
        ("What is 'Cognitive Dissonance'?", "The uncomfortable tension from having two conflicting thoughts or attitudes", "A type of leadership", "High employee turnover", None, "A"),
        ("What theory proposes that behavior is a function of its consequences?", "Reinforcement Theory", "Goal-Setting Theory", "Expectancy Theory", "Equity Theory", "A"),
        ("What is 'Groupthink'?", "A phenomenon where a group strives for conformity and consensus over critical evaluation", "When groups make better decisions than individuals", "A common office illness", None, "A"),
        ("What is a 'Halo Effect'?", "Drawing a general positive impression about an individual from a single characteristic", "A type of lighting design", "High employee morale", None, "A"),
        ("What is 'Job Satisfaction'?", "A positive feeling about one's job resulting from an evaluation of its characteristics", "The level of pay an employee receives", "The total benefits package", None, "A"),
        ("Which is a transactional leadership style?", "Contingent Reward", "Charisma", "Inspirational Motivation", "Individualized Consideration", "A"),
        ("What is 'Maslow's Hierarchy' concerned with?", "Employee needs", "Organizational structure", "Financial planning", None, "A"),
        ("What is 'Locus of Control'?", "The degree to which people believe they are masters of their own fate", "The company headquarters location", "A type of management control system", None, "A"),
        ("What is the 'Path-Goal' theory of leadership based on?", "Goal setting and motivation", "Follower readiness", "The leader's personality", None, "A"),
    ],
    "Applications_Development": [
        ("What does IDE stand for?", "Integrated Development Environment", "Internal Data Exchange", "Interface Design Engine", None, "A"),
        ("What is 'Object-Oriented Programming'?", "A programming paradigm based on the concept of 'objects'", "A style of programming without functions", "Programming that only uses graphics", None, "A"),
        ("What is 'Polymorphism'?", "The ability of a variable, function, or object to take on multiple forms", "A type of data encryption", "A bug in the code", None, "A"),
        ("What is 'Version Control'?", "A system that records changes to a file or set of files over time (e.g., Git)", "Checking the software's copyright date", "A security measure for login", None, "A"),
        ("What is 'Debugging'?", "The process of fixing errors in code", "Writing the initial code", "Deploying the finished application", None, "A"),
        ("What is an 'API'?", "Application Programming Interface", "Advanced Protocol Integration", "Automated Process Identifier", None, "A"),
        ("What is 'Encapsulation'?", "Bundling data and methods that work on that data within one unit", "Protecting data with a password", "Compiling code into a binary", None, "A"),
        ("Which language is often used for front-end web development?", "JavaScript", "Java", "Python", "C++", "A"),
        ("What is a 'Data Structure'?", "A specialized format for organizing and storing data", "A chart showing company hierarchy", "A file naming convention", None, "A"),
        ("What is a 'Framework'?", "A foundational, pre-written code structure that developers can build upon", "A type of coding error", "The final executable file", None, "A"),
        ("What is the primary function of a 'Compiler'?", "To convert high-level code into machine code", "To run code line by line", "To write documentation", None, "A"),
    ]
}

# --- Database Management Functions ---

def db_execute(query, params=()):
    """A general utility function for database connection and execution."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def db_fetch(query, params=()):
    """A general utility function for fetching data."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def initialize_database():
    """Connects to the database and ensures all required tables are created and populated."""
    for table_name, questions in COURSE_TABLES_DATA.items():
        # Create table if it doesn't exist
        db_execute(f"CREATE TABLE IF NOT EXISTS {table_name} {QUESTION_SCHEMA}")
        
        # Check if table has enough content
        count = db_fetch(f"SELECT COUNT(*) FROM {table_name}")
        count = count[0][0] if count else 0
        
        if count < 10:
            print(f"Populating table: {table_name}")
            # Insert placeholder questions
            insert_query = f"""
            INSERT INTO {table_name} 
            (Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer) 
            VALUES (?, ?, ?, ?, ?, ?);
            """
            conn = sqlite3.connect(DATABASE_FILE)
            cursor = conn.cursor()
            cursor.executemany(insert_query, questions)
            conn.commit()
            conn.close()
    print("Database initialization complete.")

def get_all_course_tables():
    """Retrieves the list of all quiz tables (courses) from the database."""
    return [row[0] for row in db_fetch("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")]

def get_questions_for_course(course_name):
    """Retrieves all questions from a specified course table."""
    query = f"SELECT Question_ID, Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer FROM {course_name}"
    return db_fetch(query)

# --- Main Application Class ---

class QuizBowlApp:
    def __init__(self, master):
        self.master = master
        master.title("Quiz Bowl Application")
        self.current_q_index = 0
        self.score = 0
        self.questions = []
        self.course_name = ""

        # Start with the login screen
        self.login_screen()

    # --- GUI Utility Methods ---
    def clear_frame(self):
        """Destroys all widgets in the master window."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def set_title(self, title):
        """Sets the window title and geometry based on context."""
        self.master.title(title)
        if "Login" in title or "Dashboard" in title:
            self.master.geometry("450x300")
        else:
            self.master.geometry("600x550")

    # --- Login/Admin Dashboard ---
    def login_screen(self):
        """Creates the initial screen with Administrator and Student paths."""
        self.clear_frame()
        self.set_title("Quiz Bowl Application - Login")

        tk.Label(self.master, text="Welcome to the Quiz Bowl!", font=('Arial', 16, 'bold')).pack(pady=10)

        # Administrator Path Widgets
        tk.Label(self.master, text="-- Administrator Login --", font=('Arial', 12)).pack(pady=(15, 5))
        
        tk.Label(self.master, text="Password:").pack()
        self.admin_pass_entry = tk.Entry(self.master, show="*", width=30)
        self.admin_pass_entry.pack()

        tk.Button(self.master, text="Login as Administrator", command=self.attempt_admin_login, bg='#E84A5F', fg='white').pack(pady=10)

        # Student Path (Updated button label)
        tk.Label(self.master, text="-- OR --", font=('Arial', 10)).pack(pady=10)
        # ------------------------------------------------------------------
        # --- THE CHANGE IS HERE: 'Student' instead of 'Start Quiz as Student' ---
        tk.Button(self.master, text="Student", command=self.student_interface, bg='#3BBF72', fg='white').pack(pady=5, ipadx=20)
        # ------------------------------------------------------------------

    def attempt_admin_login(self):
        entered_password = self.admin_pass_entry.get()
        if entered_password in ADMIN_PASSWORDS:
            messagebox.showinfo("Login Success", "Welcome Administrator!")
            self.admin_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid password. Please try again.")
            self.admin_pass_entry.delete(0, tk.END)

    def admin_dashboard(self):
        self.clear_frame()
        self.set_title("Administrator Dashboard")
        
        tk.Label(self.master, text="Admin Control Panel", font=('Arial', 18, 'bold')).pack(pady=15)

        tk.Button(self.master, text="1. Add New Questions/Courses", command=self.admin_add_content, bg='#2A9FD6', fg='white').pack(fill='x', padx=50, pady=5, ipady=5)
        tk.Button(self.master, text="2. View/Edit Questions", command=self.admin_select_course_for_edit, bg='#EBB95C', fg='black').pack(fill='x', padx=50, pady=5, ipady=5)
        tk.Button(self.master, text="3. Delete Questions", command=self.admin_select_course_for_delete, bg='#DE7E48', fg='white').pack(fill='x', padx=50, pady=5, ipady=5)
        
        tk.Button(self.master, text="Logout", command=self.login_screen, bg='gray').pack(pady=20)

    # --- 1. Admin: Add New Questions/Courses Implementation ---
    def admin_add_content(self):
        self.clear_frame()
        self.set_title("Admin: Add New Question")

        tk.Label(self.master, text="Add New Question", font=('Arial', 16, 'bold')).pack(pady=10)

        # Frame for input fields
        input_frame = tk.Frame(self.master)
        input_frame.pack(padx=20, pady=10, fill='x')

        # Course Selection Dropdown
        tk.Label(input_frame, text="Select Course:").grid(row=0, column=0, sticky='w', pady=2)
        courses = get_all_course_tables()
        self.course_var = tk.StringVar(self.master)
        self.course_var.set(courses[0] if courses else "No Courses")
        course_dropdown = tk.OptionMenu(input_frame, self.course_var, *courses)
        course_dropdown.config(width=25)
        course_dropdown.grid(row=0, column=1, sticky='ew', padx=10, pady=2)

        # Question Text Input
        tk.Label(input_frame, text="Question Text:").grid(row=1, column=0, sticky='w', pady=2)
        self.q_text_entry = tk.Entry(input_frame, width=50)
        self.q_text_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=2)

        # Option Inputs
        self.options_entries = {}
        for i, opt_label in enumerate(['A', 'B', 'C', 'D']):
            tk.Label(input_frame, text=f"Option {opt_label}:").grid(row=i+2, column=0, sticky='w', pady=2)
            entry = tk.Entry(input_frame, width=50)
            entry.grid(row=i+2, column=1, sticky='ew', padx=10, pady=2)
            self.options_entries[opt_label] = entry

        # Correct Answer Selection
        tk.Label(input_frame, text="Correct Answer:").grid(row=6, column=0, sticky='w', pady=2)
        self.correct_ans_var = tk.StringVar(self.master)
        self.correct_ans_var.set("A")
        correct_ans_dropdown = tk.OptionMenu(input_frame, self.correct_ans_var, 'A', 'B', 'C', 'D')
        correct_ans_dropdown.config(width=5)
        correct_ans_dropdown.grid(row=6, column=1, sticky='w', padx=10, pady=2)

        input_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        tk.Button(self.master, text="Save New Question", command=self._save_new_question, bg='#3BBF72', fg='white').pack(pady=15, ipadx=10)
        tk.Button(self.master, text="Back to Dashboard", command=self.admin_dashboard, bg='gray').pack()

    def _save_new_question(self):
        """Logic to insert the new question into the selected course table."""
        course = self.course_var.get()
        q_text = self.q_text_entry.get().strip()
        opt_a = self.options_entries['A'].get().strip()
        opt_b = self.options_entries['B'].get().strip()
        opt_c = self.options_entries['C'].get().strip()
        opt_d = self.options_entries['D'].get().strip() or None # Allow D to be optional
        correct_ans = self.correct_ans_var.get()

        if not (course and q_text and opt_a and opt_b and opt_c and correct_ans):
            messagebox.showwarning("Validation Error", "Please fill in the Question Text and at least options A, B, and C.")
            return

        query = f"""
        INSERT INTO {course} 
        (Question_Text, Option_A, Option_B, Option_C, Option_D, Correct_Answer) 
        VALUES (?, ?, ?, ?, ?, ?);
        """
        params = (q_text, opt_a, opt_b, opt_c, opt_d, correct_ans)
        
        if db_execute(query, params):
            messagebox.showinfo("Success", f"New question added to {course.replace('_', ' ')}.")
            # Clear fields for next entry
            self.q_text_entry.delete(0, tk.END)
            for entry in self.options_entries.values():
                entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add question to database.")


    # --- 2. Admin: View/Edit Questions Implementation ---
    def admin_select_course_for_edit(self):
        """Initial screen to select a course before viewing/editing questions."""
        self.clear_frame()
        self.set_title("Admin: Select Course to View/Edit")
        
        tk.Label(self.master, text="Select a Course to View/Edit Questions", font=('Arial', 14, 'bold')).pack(pady=15)
        
        courses = get_all_course_tables()
        
        for course in courses:
            tk.Button(self.master, 
                      text=f"Edit {course.replace('_', ' ')} Questions", 
                      command=lambda c=course: self.admin_view_edit_questions(c),
                      width=40).pack(pady=5)
            
        tk.Button(self.master, text="Back to Dashboard", command=self.admin_dashboard, bg='gray').pack(pady=20)


    def admin_view_edit_questions(self, course_name):
        """Displays questions in a course and allows the admin to select one for editing."""
        self.clear_frame()
        self.set_title(f"Admin: View/Edit Questions in {course_name.replace('_', ' ')}")
        
        questions = get_questions_for_course(course_name)
        if not questions:
            tk.Label(self.master, text="No questions in this course.", fg='red').pack(pady=10)
            tk.Button(self.master, text="Back to Course Select", command=self.admin_select_course_for_edit).pack(pady=20)
            return

        tk.Label(self.master, text="Select a question to edit:", font=('Arial', 12)).pack(pady=10)

        # Use Treeview for a cleaner list display
        tree_frame = tk.Frame(self.master)
        tree_frame.pack(padx=10, pady=5, fill='both', expand=True)

        tree = ttk.Treeview(tree_frame, columns=('ID', 'Question', 'Answer'), show='headings')
        tree.heading('ID', text='ID', anchor='w')
        tree.heading('Question', text='Question Text', anchor='w')
        tree.heading('Answer', text='Correct', anchor='w')
        tree.column('ID', width=50, stretch=tk.NO)
        tree.column('Question', width=400)
        tree.column('Answer', width=80, stretch=tk.NO)
        
        for q_data in questions:
            q_id, q_text, _, _, _, _, correct_ans = q_data
            tree.insert('', tk.END, values=(q_id, q_text[:60] + '...' if len(q_text) > 60 else q_text, correct_ans))

        tree.bind('<Double-1>', lambda event: self._open_edit_window(event, tree, course_name))
        tree.pack(fill='both', expand=True)
        
        tk.Button(self.master, text="Back to Dashboard", command=self.admin_dashboard, bg='gray').pack(pady=10)

    def _open_edit_window(self, event, tree, course_name):
        """Opens a new window to edit the selected question."""
        try:
            selected_item = tree.selection()[0]
            q_id = tree.item(selected_item, 'values')[0]
        except IndexError:
            messagebox.showwarning("Selection Error", "Please double-click a question to edit.")
            return

        # Fetch the full question data again
        question_data = db_fetch(f"SELECT * FROM {course_name} WHERE Question_ID=?", (q_id,))[0]
        
        # New Toplevel window for editing
        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Edit Question ID: {q_id}")
        edit_window.geometry("500x500")

        tk.Label(edit_window, text=f"Editing Question {q_id} in {course_name.replace('_', ' ')}", font=('Arial', 14)).pack(pady=10)

        # Question Text Input
        tk.Label(edit_window, text="Question Text:").pack(pady=2)
        q_text_entry = tk.Text(edit_window, height=4, width=45)
        q_text_entry.insert(tk.END, question_data[1])
        q_text_entry.pack(padx=10)

        # Option and Answer Inputs
        options_entries = {}
        correct_ans_var = tk.StringVar(edit_window)
        correct_ans_var.set(question_data[6])

        options_frame = tk.Frame(edit_window)
        options_frame.pack(pady=10, padx=10, fill='x')

        for i, opt_label in enumerate(['A', 'B', 'C', 'D']):
            tk.Label(options_frame, text=f"Option {opt_label}:").grid(row=i, column=0, sticky='w', padx=5)
            entry = tk.Entry(options_frame, width=40)
            entry.insert(tk.END, question_data[i+2] if question_data[i+2] else "")
            entry.grid(row=i, column=1, padx=5)
            
            tk.Radiobutton(options_frame, text="Correct", variable=correct_ans_var, value=opt_label).grid(row=i, column=2)
            options_entries[opt_label] = entry
            
        def save_changes():
            new_q_text = q_text_entry.get("1.0", tk.END).strip()
            new_opt_a = options_entries['A'].get().strip()
            new_opt_b = options_entries['B'].get().strip()
            new_opt_c = options_entries['C'].get().strip()
            new_opt_d = options_entries['D'].get().strip() or None
            new_correct_ans = correct_ans_var.get()

            if not (new_q_text and new_opt_a and new_opt_b and new_opt_c and new_correct_ans):
                messagebox.showwarning("Validation", "Question and options A, B, C cannot be empty.")
                return

            update_query = f"""
            UPDATE {course_name} SET 
            Question_Text=?, Option_A=?, Option_B=?, Option_C=?, Option_D=?, Correct_Answer=?
            WHERE Question_ID=?
            """
            params = (new_q_text, new_opt_a, new_opt_b, new_opt_c, new_opt_d, new_correct_ans, q_id)

            if db_execute(update_query, params):
                messagebox.showinfo("Success", "Question updated successfully!")
                edit_window.destroy()
                self.admin_view_edit_questions(course_name) # Refresh the list view
            else:
                messagebox.showerror("Error", "Failed to update question.")

        tk.Button(edit_window, text="Save Changes", command=save_changes, bg='#2A9FD6', fg='white').pack(pady=15, ipadx=10)
        tk.Button(edit_window, text="Cancel", command=edit_window.destroy, bg='gray').pack()


    # --- 3. Admin: Delete Questions Implementation ---
    def admin_select_course_for_delete(self):
        """Initial screen to select a course before deleting questions."""
        self.clear_frame()
        self.set_title("Admin: Select Course to Delete Questions From")
        
        tk.Label(self.master, text="Select a Course to Delete Questions From", font=('Arial', 14, 'bold')).pack(pady=15)
        
        courses = get_all_course_tables()
        
        for course in courses:
            tk.Button(self.master, 
                      text=f"Delete Questions in {course.replace('_', ' ')}", 
                      command=lambda c=course: self.admin_delete_questions(c),
                      width=40).pack(pady=5)
            
        tk.Button(self.master, text="Back to Dashboard", command=self.admin_dashboard, bg='gray').pack(pady=20)


    def admin_delete_questions(self, course_name):
        """Displays questions in a course and allows the admin to select one for deletion."""
        self.clear_frame()
        self.set_title(f"Admin: Delete Questions in {course_name.replace('_', ' ')}")
        
        questions = get_questions_for_course(course_name)
        if not questions:
            tk.Label(self.master, text="No questions in this course.", fg='red').pack(pady=10)
            tk.Button(self.master, text="Back to Course Select", command=self.admin_select_course_for_delete).pack(pady=20)
            return

        tk.Label(self.master, text="Select a question (double-click or select and click Delete) to delete:", font=('Arial', 12)).pack(pady=10)

        # Use Treeview for question display
        tree_frame = tk.Frame(self.master)
        tree_frame.pack(padx=10, pady=5, fill='both', expand=True)

        tree = ttk.Treeview(tree_frame, columns=('ID', 'Question'), show='headings')
        tree.heading('ID', text='ID', anchor='w')
        tree.heading('Question', text='Question Text', anchor='w')
        tree.column('ID', width=50, stretch=tk.NO)
        tree.column('Question', width=500)
        
        for q_data in questions:
            q_id, q_text = q_data[0], q_data[1]
            tree.insert('', tk.END, values=(q_id, q_text[:80] + '...' if len(q_text) > 80 else q_text))

        tree.pack(fill='both', expand=True)

        def delete_selected():
            try:
                selected_item = tree.selection()[0]
                q_id = tree.item(selected_item, 'values')[0]
                q_text_preview = tree.item(selected_item, 'values')[1]
                
                if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Question ID {q_id}:\n'{q_text_preview}'?"):
                    query = f"DELETE FROM {course_name} WHERE Question_ID=?"
                    if db_execute(query, (q_id,)):
                        messagebox.showinfo("Success", f"Question ID {q_id} deleted successfully.")
                        self.admin_delete_questions(course_name) # Refresh the list
                    else:
                        messagebox.showerror("Error", "Failed to delete question.")
            except IndexError:
                messagebox.showwarning("Selection Error", "Please select a question to delete.")

        tk.Button(self.master, text="Delete Selected Question", command=delete_selected, bg='#DE7E48', fg='white').pack(pady=15, ipadx=10)
        tk.Button(self.master, text="Back to Dashboard", command=self.admin_dashboard, bg='gray').pack()


    # --- Student Interface Methods ---
    def student_interface(self):
        self.clear_frame()
        self.set_title("Student Quiz - Select Course")
        tk.Label(self.master, text="Welcome Student! Select a Course Category", font=('Arial', 16, 'bold')).pack(pady=15)
        courses = get_all_course_tables()
        if not courses:
            tk.Label(self.master, text="No courses available. Check database setup.", fg='red').pack(pady=10)
        for course in courses:
            tk.Button(self.master, 
                      text=course.replace('_', ' '),
                      command=lambda c=course: self.quiz_start(c),
                      width=40, height=2).pack(pady=5)
        tk.Button(self.master, text="Back to Login", command=self.login_screen, bg='gray').pack(pady=20)

    def quiz_start(self, course_name):
        self.course_name = course_name
        self.questions = get_questions_for_course(course_name)
        if not self.questions:
            messagebox.showerror("Error", f"No questions found for {course_name}.")
            return self.student_interface()
        
        random.shuffle(self.questions) 
        self.current_q_index = 0
        self.score = 0
        self.total_questions = len(self.questions)
        self.display_quiz_question()

    def display_quiz_question(self):
        self.clear_frame()
        self.set_title(f"Quiz: {self.course_name.replace('_', ' ')}")
        if self.current_q_index >= self.total_questions:
            self.show_quiz_results()
            return
        q_data = self.questions[self.current_q_index]
        q_text = q_data[1]
        option_texts = [q_data[2], q_data[3], q_data[4], q_data[5]]
        options = [(label, text) for label, text in zip(['A', 'B', 'C', 'D'], option_texts) if text]

        progress_text = f"Question {self.current_q_index + 1} of {self.total_questions}"
        tk.Label(self.master, text=progress_text, font=('Arial', 10, 'italic')).pack(pady=(10, 0), anchor='w', padx=20)
        
        tk.Label(self.master, text=q_text, font=('Arial', 13, 'bold'), wraplength=550, justify=tk.LEFT, bg='#F0F0F0', padx=10, pady=10).pack(pady=(5, 20), anchor='w', fill='x', padx=10)

        self.selected_answer = tk.StringVar(self.master)
        self.selected_answer.set("")

        for label, option_text in options:
            radio_btn = tk.Radiobutton(
                self.master, 
                text=f"{label}. {option_text}", 
                variable=self.selected_answer, 
                value=label,
                font=('Arial', 11),
                justify=tk.LEFT,
                anchor='w',
                width=500
            )
            radio_btn.pack(anchor='w', padx=30, pady=2)

        tk.Button(self.master, text="Submit Answer", command=self.submit_answer, bg='#3BBF72', fg='white', width=20).pack(pady=20)
        tk.Button(self.master, text="End Quiz Early", command=self.student_interface).pack()

    def submit_answer(self):
        user_choice = self.selected_answer.get()
        if not user_choice:
            messagebox.showwarning("Warning", "Please select an answer before submitting.")
            return

        q_data = self.questions[self.current_q_index]
        correct_answer = q_data[6]
        
        is_correct = (user_choice == correct_answer)

        feedback_text = ""
        if is_correct:
            self.score += 1
            feedback_text = "✅ Correct! Well done."
        else:
            feedback_text = f"❌ Incorrect. The correct answer was **{correct_answer}**."

        messagebox.showinfo("Feedback", feedback_text)
        
        self.current_q_index += 1
        self.display_quiz_question()

    def show_quiz_results(self):
        self.clear_frame()
        self.set_title("Quiz Results")

        score_percent = (self.score / self.total_questions) * 100
        
        tk.Label(self.master, text="Quiz Completed!", font=('Arial', 18, 'bold')).pack(pady=20)
        
        tk.Label(self.master, text=f"Your Score for {self.course_name.replace('_', ' ')}:", font=('Arial', 12)).pack(pady=5)
                 
        tk.Label(self.master, text=f"{self.score} out of {self.total_questions}\n({score_percent:.2f}%)", 
                 font=('Arial', 24, 'bold'), fg='#2A9FD6', pady=10).pack()
        
        tk.Button(self.master, text="Take Another Quiz", command=self.student_interface, bg='#EBB95C').pack(pady=15, ipadx=10)
        tk.Button(self.master, text="Back to Login", command=self.login_screen, bg='gray').pack(pady=5)

# --- Main Execution Block ---
if __name__ == "__main__":
    initialize_database() 
    root = tk.Tk()
    app = QuizBowlApp(root)
    root.mainloop()