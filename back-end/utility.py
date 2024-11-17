import sqlite3

class Database:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        cursor = self.connection.cursor()

        #Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password NOT NULL
            )
        """)
        #Create problems table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                difficulty VARCHAR(255) NOT NULL,
                description TEXT NOT NULL
                )
        """)
        #Create contests table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        #Create submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                language TEXT NOT NULL,
                code TEXT NOT NULL,
                status TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (problem_id) REFERENCES problems (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        #Create contest_problems
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contest_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contest_id INTEGER NOT NULL,
                problem_id INTEGER NOT NULL,
                FOREIGN KEY (contest_id) REFERENCES contests (id),
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            )
        """) 
        self.connection.commit()
        cursor.close()

    #Create user
    def create_user(self, name, email):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.connection.commit()
            cursor.close()
            return {"status": "success", "message": "User created successfully"}
        except sqlite3.IntegrityError as e:
            return {"status": "error", "message": str(e)}
        
    #Read user
    def read_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    #Get user by id
    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user if user else {"message": "User not found"}
    
    #Update user
    def update_user(self, user_id, name, email):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        self.connection.commit()
        return {"status": "success", "message": "User updated successfully"}
    
    #Delete user
    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.connection.commit()
        return {"status": "success", "message": "User deleted successfully"}
    
    #Create problem
    def create_problem(self, title, difficulty, description):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO problems (title, difficulty, description) VALUES (?, ?, ?)",
                (title, difficulty, description)
            )
            self.connection.commit()
            return {"status": "success", "message": "Problem created successfully"}
        except sqlite3.Error as e:
            return {"status": "error", "message": str(e)}

    #Read problems
    def read_problems(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM problems")
        return cursor.fetchall()

    #Read problem by id
    def read_problem_by_id(self, problem_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
        return cursor.fetchone()

    #update problem
    def update_problem(self, problem_id, title, difficulty, description):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE problems SET title = ?, difficulty = ?, description = ? WHERE id = ?",
            (title, difficulty, description, problem_id)
        )
        self.connection.commit()
        return {"status": "success", "message": "Problem updated successfully"}

    #delete problem
    def delete_problem(self, problem_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
        self.connection.commit()
        return {"status": "success", "message": "Problem deleted successfully"}
    
    #add contest
    def add_contest(self, title, description, start_time, end_time, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO contests (title, description, start_time, end_time, status)
               VALUES (?, ?, ?, ?, ?)""",
            (title, description, start_time, end_time, status)
        )
        self.connection.commit()
        return {"message": "Contest added successfully!"}
    
    #get contests
    def get_all_contests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contests")
        return cursor.fetchall()
    
    #Get contest by id
    def get_contest_by_id(self, contest_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contests WHERE id = ?", (contest_id,))
        contest = cursor.fetchone()
        return contest if contest else {"message": "Contest not found"}

    #update contest
    def update_contest(self, contest_id, title, description, start_time, end_time, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE contests
               SET title = ?, description = ?, start_time = ?, end_time = ?, status = ?
               WHERE id = ?""",
            (title, description, start_time, end_time, status, contest_id)
        )
        self.connection.commit()
        return {"message": "Contest updated successfully!"}

    #delete contest
    def delete_contest(self, contest_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM contests WHERE id = ?", (contest_id,))
        self.connection.commit()
        return {"message": "Contest deleted successfully!"}

    #add submission
    def add_submission(self, problem_id, user_id, language, code, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO submissions (problem_id, user_id, language, code, status)
               VALUES (?, ?, ?, ?, ?)""",
            (problem_id, user_id, language, code, status)
        )
        self.connection.commit()
        return {"message": "Submission added successfully!"}
    
    #get submissions
    def get_all_submissions(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM submissions")
        return cursor.fetchall()
    
    #get submission by id
    def get_submission_by_id(self, submission_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,))
        submission = cursor.fetchone()
        return submission if submission else {"message": "Submission not found"}
    
    #update submission
    def update_submission(self, submission_id, problem_id, user_id, language, code, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE submissions
               SET problem_id = ?, user_id = ?, language = ?, code = ?, status = ?
               WHERE id = ?""",
            (problem_id, user_id, language, code, status, submission_id)
        )
        self.connection.commit()
        return {"message": "Submission updated successfully!"}
    
    #delete submission
    def delete_submission(self, submission_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
        self.connection.commit()
        return {"message": "Submission deleted successfully!"}

     #add contest problem
    def add_contest_problem(self, contest_id, problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO contest_problems (contest_id, problem_id)
               VALUES (?, ?)""",
            (contest_id, problem_id)
        )
        self.connection.commit()
        return {"message": "Problem added to contest successfully!"}

    #get all contest problems
    def get_all_contest_problems(self):
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT cp.id, cp.contest_id, c.title as contest_title, 
                      cp.problem_id, p.title as problem_title
               FROM contest_problems cp
               JOIN contests c ON cp.contest_id = c.id
               JOIN problems p ON cp.problem_id = p.id"""
        )
        return cursor.fetchall()

    #get contest problem by id
    def get_contest_problem_by_id(self, contest_problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT cp.id, cp.contest_id, c.title as contest_title, 
                      cp.problem_id, p.title as problem_title
               FROM contest_problems cp
               JOIN contests c ON cp.contest_id = c.id
               JOIN problems p ON cp.problem_id = p.id
               WHERE cp.id = ?""",
            (contest_problem_id,)
        )
        result = cursor.fetchone()
        return result if result else {"message": "Contest problem not found"}

    #update contest problem
    def update_contest_problem(self, contest_problem_id, contest_id, problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE contest_problems
               SET contest_id = ?, problem_id = ?
               WHERE id = ?""",
            (contest_id, problem_id, contest_problem_id)
        )
        self.connection.commit()
        return {"message": "Contest problem updated successfully!"}

    #delete contest problem
    def delete_contest_problem(self, contest_problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM contest_problems WHERE id = ?",
            (contest_problem_id,)
        )
        self.connection.commit()
        return {"message": "Contest problem deleted successfully!"}


