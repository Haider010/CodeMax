import sqlite3


class Database:
    def __init__(self, db_name="database.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        cursor = self.connection.cursor()


        # Create users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                verified bool NOT NULL
            )
        """
        )

        # Create verification code table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                verification_code TEXT NOT NULL
                )
        """
        )

        cursor.execute(
            """
            DROP TABLE IF EXISTS problems           
            """
        )
        # Create problems table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                difficulty VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                example_input_output TEXT NOT NULL
                )
        """
        )
        cursor.execute(
            """
            -- Insert data into Problems table
            INSERT INTO Problems (title, description, difficulty, example_input_output) 
            VALUES 
            ('Two Sum', 
            'Given an array of integers, return the indices of the two numbers that add up to a specific target.',
            'Easy',
            'Example: Given nums = [2, 7, 11, 15] and target = 9, the solution is the indices [0, 1] because 2 + 7 = 9.'),
            ('Reverse Integer', 
            'Given an integer, reverse its digits.',
            'Easy', 
            'Example: Given x = 123, the expected output is 321.'),
            ('Palindrome Number', 
            'Given an integer, determine if it is a palindrome.',
            'Easy', 
            'Example: Given x = 121, the expected output is True because 121 is a palindrome.'),
            ('Longest Substring Without Repeating Characters', 
            'Given a string, find the length of the longest substring without repeating characters.',
            'Medium',
            'Example: Given s = "abcabcbb", the longest substring without repeating characters is "abc" with a length of 3.'),
            ('Add Two Numbers', 
            'Add two numbers represented by linked lists.',
            'Medium', 
            'Example: Given l1 = [2, 4, 3] and l2 = [5, 6, 4], the output should be [7, 0, 8] as the sum of the two numbers represented by the linked lists.'),
            ('3Sum', 
            'Find all unique triplets in an array that sum up to a specific target.',
            'Medium', 
            'Example: Given nums = [-1, 0, 1, 2, -1, -4], the unique triplets that sum to zero are [-1, 0, 1] and [-1, -1, 2].'),
            ('Container With Most Water', 
            'Find the container with the most water, formed by two lines from the array.',
            'Medium', 
            'Example: Given height = [1, 8, 6, 2, 5, 4, 8, 3, 7], the maximum area is 49, formed by the lines at index 1 and 8.'),
            ('Longest Palindromic Substring', 
            'Given a string, find the longest palindromic substring.',
            'Medium', 
            'Example: Given s = "babad", the longest palindromic substring is "bab" or "aba".'),
            ('Median of Two Sorted Arrays', 
            'Find the median of two sorted arrays.',
            'Hard',
            'Example: Given nums1 = [1, 3] and nums2 = [2], the median of the two sorted arrays is 2.'),
            ('Regular Expression Matching', 
            'Implement regular expression matching with support for "?" and "*".',
            'Hard',
            'Example: Given s = "aab" and p = "c*a*b", the string s matches the pattern p, so the output is True.');
        """
        )
        cursor.execute("DROP TABLE IF EXISTS TestCases")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS TestCases (
                problem_id INT NOT NULL,
                input_data TEXT NOT NULL,
                expected_output TEXT NOT NULL,
                FOREIGN KEY (problem_id) REFERENCES Problems(id)
            );
        """)
        

        cursor.execute("""
            -- Test Cases for Easy Questions
            INSERT INTO TestCases (problem_id, input_data, expected_output) VALUES
            (1, '2 7 11 15\n9', '[0, 1]'),
            (2, '123', '321'),
            (3, '121', 'True'),

            -- Test Cases for Medium Questions
            (4, 'abcabcbb', '3'),
            (5, '2 4 3\n5 6 4', '[7, 0, 8]'),
            (6, '-1 0 1 2 -1 -4', '[[-1, 0, 1], [-1, -1, 2]]'),
            (7, '1 8 6 2 5 4 8 3 7', '49'),
            (8, 'babad', '"bab" or "aba"'),

            -- Test Cases for Hard Questions
            (9, '1 3\n2', '2'),
            (10, 'aab\nc*a*b', 'True');
        """)

        # Create contests table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        # Create submissions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                language TEXT NOT NULL,
                code TEXT NOT NULL,
                status TEXT NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            )
        """
        )

        # Create contest_problems
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS contest_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contest_id INTEGER NOT NULL,
                problem_id INTEGER NOT NULL,
                FOREIGN KEY (contest_id) REFERENCES contests (id),
                FOREIGN KEY (problem_id) REFERENCES problems (id)
            )
        """
        )
        self.connection.commit()
        cursor.close()

    def verify_user(self,email):
        cursor = self.connection.cursor()
        """
        Verifies a user by updating their 'verified' field to True based on their email.
        """
        try:
            # Update the 'verified' field to True for the user with the given email
            cursor.execute(
                """
                UPDATE users
                SET verified = 1
                WHERE email = ?
                """, (email,)
            )
            self.connection.commit()

            # Check if any rows were updated (meaning the user exists)
            if cursor.rowcount > 0:
                print(f"User with email {email} has been verified.")
            else:
                print(f"No user found with the email {email}.")
        except sqlite3.Error as e:
            print(f"Error verifying user: {e}")
        finally:
            cursor.close()

    def get_verification_code(self,email):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT verification_code FROM verification_codes WHERE email = ?""",(email,))
        code = cursor.fetchone()[0]
        return code
    
    def set_verification_code(self, email, code):
        """Sets the verification code for the given email in the database."""
        cursor = self.connection.cursor()
        
        # Check if the email already has a verification code
        cursor.execute("""
            SELECT * FROM verification_codes WHERE email = ?
        """, (email,))
        existing_code = cursor.fetchone()
        
        if existing_code:
            # If the code already exists, update it
            cursor.execute("""
                UPDATE verification_codes
                SET verification_code = ?
                WHERE email = ?
            """, (code, email))
        else:
            # If the email doesn't exist, insert the new verification code
            cursor.execute("""
                INSERT INTO verification_codes (email, verification_code)
                VALUES (?, ?)
            """, (email, code))
        
        # Commit the changes
        self.connection.commit()


    def get_test_cases(self,problem_id):
        # Establish a connection to your database
        cursor = self.connection.cursor()
        
        # SQL query to fetch test cases for a specific problem_id
        cursor.execute("""
            SELECT input_data, expected_output FROM TestCases
            WHERE problem_id = ?
        """, (problem_id,))
        
        # Fetch all rows and store them in a list of tuples
        test_cases = cursor.fetchall()

        # Close the connection
        cursor.close()

        # Convert the result to a list of dictionaries for better readability (optional)
        test_case_list = [{"input_data": case[0], "expected_output": case[1]} for case in test_cases]
        
        return test_case_list


    # Create user
    def create_user(self, name, email, password, verified):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO users (name, email, password, verified) VALUES (?, ?, ?, ?)",
                (name, email, password, verified),
            )
            self.connection.commit()
            cursor.close()
            return {"status": "success", "message": "User created successfully"}
        except sqlite3.IntegrityError as e:
            return {"status": "error", "message": str(e)}

    # Add to Database class
    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()

    # Read user
    def verified_read_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE verified = ?",(True,))
        users =  cursor.fetchall()
        users = [user[0] for user in users]
        return users
    
    # Read user
    def all_read_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users")
        users =  cursor.fetchall()
        users = [user[0] for user in users]
        return users

    # Get user by id
    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return user if user else {"message": "User not found"}

    # Update user
    def update_user(self, user_id, name, email):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id)
        )
        self.connection.commit()
        return {"status": "success", "message": "User updated successfully"}

    # Delete user
    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.connection.commit()
        return {"status": "success", "message": "User deleted successfully"}

    # Create problem
    def create_problem(self, title, difficulty, description):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO problems (title, difficulty, description) VALUES (?, ?, ?)",
                (title, difficulty, description),
            )
            self.connection.commit()
            return {"status": "success", "message": "Problem created successfully"}
        except sqlite3.Error as e:
            return {"status": "error", "message": str(e)}

    # Read problems
    def read_problems(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM problems")
        return cursor.fetchall()

    # Read problem by id
    def read_problem_by_id(self, problem_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
        return cursor.fetchone()

    # update problem
    def update_problem(self, problem_id, title, difficulty, description):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE problems SET title = ?, difficulty = ?, description = ? WHERE id = ?",
            (title, difficulty, description, problem_id),
        )
        self.connection.commit()
        return {"status": "success", "message": "Problem updated successfully"}

    # delete problem
    def delete_problem(self, problem_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM problems WHERE id = ?", (problem_id,))
        self.connection.commit()
        return {"status": "success", "message": "Problem deleted successfully"}

    # add contest
    def add_contest(self, title, description, start_time, end_time, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO contests (title, description, start_time, end_time, status)
               VALUES (?, ?, ?, ?, ?)""",
            (title, description, start_time, end_time, status),
        )
        self.connection.commit()
        return {"message": "Contest added successfully!"}

    # get contests
    def get_all_contests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contests")
        return cursor.fetchall()

    # Get contest by id
    def get_contest_by_id(self, contest_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM contests WHERE id = ?", (contest_id,))
        contest = cursor.fetchone()
        return contest if contest else {"message": "Contest not found"}

    # update contest
    def update_contest(
        self, contest_id, title, description, start_time, end_time, status
    ):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE contests
               SET title = ?, description = ?, start_time = ?, end_time = ?, status = ?
               WHERE id = ?""",
            (title, description, start_time, end_time, status, contest_id),
        )
        self.connection.commit()
        return {"message": "Contest updated successfully!"}

    # delete contest
    def delete_contest(self, contest_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM contests WHERE id = ?", (contest_id,))
        self.connection.commit()
        return {"message": "Contest deleted successfully!"}

    # add submission
    def add_submission(self, problem_id,  language, code, status):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO submissions (problem_id, language, code, status)
               VALUES (?, ?, ?, ?)""",
            (problem_id, language, code, status),
        )
        self.connection.commit()
        return {"message": "Submission added successfully!"}

    # get submissions
    def get_all_submissions(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM submissions")
        return cursor.fetchall()

    # get submission by id
    def get_submission_by_id(self, submission_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM submissions WHERE id = ?", (submission_id,))
        submission = cursor.fetchone()
        return submission if submission else {"message": "Submission not found"}

    # update submission
    def update_submission(
        self, submission_id, problem_id, user_id, language, code, status
    ):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE submissions
               SET problem_id = ?, user_id = ?, language = ?, code = ?, status = ?
               WHERE id = ?""",
            (problem_id, user_id, language, code, status, submission_id),
        )
        self.connection.commit()
        return {"message": "Submission updated successfully!"}

    # delete submission
    def delete_submission(self, submission_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
        self.connection.commit()
        return {"message": "Submission deleted successfully!"}

    # add contest problem
    def add_contest_problem(self, contest_id, problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO contest_problems (contest_id, problem_id)
               VALUES (?, ?)""",
            (contest_id, problem_id),
        )
        self.connection.commit()
        return {"message": "Problem added to contest successfully!"}

    # get all contest problems
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

    # get contest problem by id
    def get_contest_problem_by_id(self, contest_problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT cp.id, cp.contest_id, c.title as contest_title, 
                      cp.problem_id, p.title as problem_title
               FROM contest_problems cp
               JOIN contests c ON cp.contest_id = c.id
               JOIN problems p ON cp.problem_id = p.id
               WHERE cp.id = ?""",
            (contest_problem_id,),
        )
        result = cursor.fetchone()
        return result if result else {"message": "Contest problem not found"}

    # update contest problem
    def update_contest_problem(self, contest_problem_id, contest_id, problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            """UPDATE contest_problems
               SET contest_id = ?, problem_id = ?
               WHERE id = ?""",
            (contest_id, problem_id, contest_problem_id),
        )
        self.connection.commit()
        return {"message": "Contest problem updated successfully!"}

    # delete contest problem
    def delete_contest_problem(self, contest_problem_id):
        cursor = self.connection.cursor()
        cursor.execute(
            "DELETE FROM contest_problems WHERE id = ?", (contest_problem_id,)
        )
        self.connection.commit()
        return {"message": "Contest problem deleted successfully!"}
