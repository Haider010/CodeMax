from flask import Flask, jsonify, request
from utility import Database
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import requests
import yagmail
import random
import string
from email_validator import validate_email, EmailNotValidError
from huggingface_hub import InferenceClient


app = Flask(__name__)
CORS(app)
db = Database()  

# RapidAPI Judge0 Credentials
RAPIDAPI_HOST = "judge0-ce.p.rapidapi.com"
RAPIDAPI_KEY = "b66cb0edd6msh7b3858557c7a863p1a33d5jsn2ed6283ff643"

# Endpoint to execute code on test cases
@app.route('/submitCode/<int:problem_id>', methods=['POST'])
def submit_code(problem_id):
    try:
        # Get code and language from frontend
        print("Hang Submit Code")
        data = request.json
        code = data.get('code')
        language = data.get('language')

        # Map language names to Judge0 language IDs
        language_map = {
            "python": 71,
            "javascript": 63,
            "java": 62,
            "cpp": 54,
            "csharp": 51
        }
        language_id = language_map.get(language)
        if not language_id:
            return jsonify({"error": f"Unsupported language: {language}"}), 400

        test_cases = db.get_test_cases(problem_id)

        if not test_cases:
            return jsonify({"error": "No test cases found for this problem"}), 404

        # Run code for each test case
        results = []
        for test_case in test_cases:
            input_data = test_case['input_data']
            expected_output = test_case['expected_output']

            # Prepare payload for Judge0
            payload = {
                "source_code": code,
                "language_id": language_id,
                "stdin": input_data
            }

            # Submit code to Judge0
            headers = {
                'x-rapidapi-key': RAPIDAPI_KEY,
                'x-rapidapi-host': RAPIDAPI_HOST,
                'content-type': 'application/json'
            }
            response = requests.post(f"https://{RAPIDAPI_HOST}/submissions?base64_encoded=false", 
                                     json=payload, headers=headers)
            submission_response = response.json()

            if "token" not in submission_response:
                results.append({"input": input_data, "error": "Failed to create submission"})
                continue

            # Fetch result using token
            token = submission_response["token"]
            result_response = requests.get(f"https://{RAPIDAPI_HOST}/submissions/{token}?base64_encoded=false", 
                                        headers=headers)
            result_data = result_response.json()

            # Append results
            results.append({
                "input": input_data,
                "expected_output": expected_output,
                "actual_output": result_data.get("stdout", "").strip(),
                "status": result_data.get("status", {}).get("description"),
                "execution_time": result_data.get("time"),
                "memory": result_data.get("memory"),
            })
            if results[-1]["status"] == "Accepted" and results[-1]["expected_output"] != results[-1]["actual_output"]:
                results[-1]["status"] = "Rejected"
            db.add_submission(
                problem_id, language, code, results[-1]["status"]
            )

        return jsonify({"test_case_results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


API_KEY = "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"  # Replace with your token

# Initialize the InferenceClient
client = InferenceClient(api_key=API_KEY)

@app.route('/api/get-response', methods=['POST'])
def get_response():
    try:
        # Extract user input and conversation history from the request
        user_input = request.json.get('message', '')
        conversation_history = request.json.get('conversation_history', [])

        if not user_input:
            return jsonify({"success": False, "error": "Message is required"}), 400

        # Prepare the messages for the Hugging Face API
        messages = [{"role": "user", "content": msg} for msg in conversation_history]
        messages.append({"role": "user", "content": user_input})

        # Call the Hugging Face API
        completion = client.chat.completions.create(
            model="microsoft/DialoGPT-medium",
            messages=messages,
            max_tokens=500
        )

        # Extract AI's reply
        ai_reply = completion.choices[0].message["content"]
        print(completion)

        return jsonify({"success": True, "reply": ai_reply})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/")
def home():
    return "Home Page"

def generate_verification_code():
    """Generate a 6-digit verification code"""
    return ''.join(random.choices(string.digits, k=6))

def send_verification_email(email, code):
    """Send the verification code to the user's email"""
    yag = yagmail.SMTP('bsai23057@itu.edu.pk', 'arfm duyc gyyw btml')
    yag.send(
        to=email,
        subject="CodeMax Registration - Email Verification",
        contents=f"You're registering for CodeMax. Your verification code is: {code}"
    )

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')  # Changed to pbkdf2:sha256 for stronger hashing
    print(data)
    
    # Validate email
    try:
        validate_email(email)
    except EmailNotValidError as e:
        return jsonify({"error": "Invalid email format"}), 400

    users = db.verified_read_users()

    # Check if the email already exists
    if email in users:
        return jsonify({"error": "Email is already registered"}), 400

    # Generate and send verification code
    verification_code = generate_verification_code()
    send_verification_email(email, verification_code)

    # Store user data temporarily (pending verification)
    db.create_user(name, email, password, False)

    db.set_verification_code(email, verification_code)

    return jsonify({"message": "Verification email sent. Please check your inbox."}), 200
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    email = data['email']
    code = data['code']
    users = db.all_read_users()
    print(users)
    if email not in users:
        return jsonify({"error": "Email not found"}), 404

    # Check if the verification code matches
    if db.get_verification_code(email) == code:
        db.verify_user(email)
        return jsonify({"message": "Email verified successfully!"}), 200
    else:
        return jsonify({"error": "Invalid verification code"}), 400

@app.route('/get_name', methods=['GET'])
def get_name():
    email = request.args.get('email')  # Get email from query parameters
    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Fetch name from the database based on the email
    name = db.get_name(email)
    
    if name:
        return jsonify({"name": name})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/finishContest', methods=['POST'])
def finish_contest():
    data = request.get_json()
    contest_id = data.get('contestId')
    total_time_taken = data.get('totalTimeTaken')
    accepted_submissions = data.get('acceptedSubmissions')
    user_name = data.get('userName')  # Get the user's name from the payload
    db.save_contest_result(contest_id, user_name, total_time_taken,accepted_submissions)

    return jsonify({"success": True})  # Return a success message or error based on your logic

@app.route('/has_finished_contest', methods=['GET'])
def has_finished_contest():
    # Get contest_id and user_name from the query parameters
    contest_id = request.args.get('contestId')
    user_name = request.args.get('userName')

    result = db.is_contest_finished(contest_id,user_name)
    print(result)
    if result:
        return jsonify({"finished": True}), 200  # User has already finished the contest
    else:
        return jsonify({"finished": False}), 200  # User has not finished the contest


# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = db.get_user_by_email(email)  # Add a new method in your Database class
    print(user)
    if not user:
        return jsonify({"error": "User not found!"}), 404

    if check_password_hash(user[3], password):  # Assuming `password` is in the 4th column
        return jsonify({"message": "Login successful!", "user_id": user[0]}), 200
    else:
        return jsonify({"error": "Incorrect password!"}), 401
# Get Users
@app.route('/users', methods=['GET'])
def get_users():
    users = db.read_users()
    return jsonify({"users": [{"id": u[0], "name": u[1], "email": u[2]} for u in users]})

# Get user by id
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = db.get_user_by_id(user_id)
    return jsonify({"user": user})

# Add User
@app.route('/users', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 415
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Request body cannot be empty"}), 400
        if not data.get("name") or not data.get("email"):
            return jsonify({"status": "error", "message": "Name and email are required"}), 400
        result = db.create_user(data["name"], data["email"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid JSON: {str(e)}"}), 400

# Update User
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"status": "error", "message": "Name and email are required"}), 400
    result = db.update_user(user_id, data["name"], data["email"])
    return jsonify(result)

# Delete User
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = db.delete_user(user_id)
    return jsonify(result)

# Create a new problem
@app.route('/Problems', methods=['POST'])
def add_problem():
    data = request.json
    if not data or not data.get("title") or not data.get("difficulty") or not data.get("description"):
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    result = db.create_problem(data["title"], data["difficulty"], data["description"])
    return jsonify(result)

# Get all problems
@app.route('/Problems', methods=['GET'])
def get_problems():
    problems = db.read_problems()
    return jsonify({"problems": [
        {"id": p[0], "title": p[1], "difficulty": p[2], "description": p[3]} for p in problems
    ]})

# Get a problem by ID
@app.route('/Problems/<int:problem_id>', methods=['GET'])
def get_problem(problem_id):
    problem = db.read_problem_by_id(problem_id)
    if not problem:
        return jsonify({"status": "error", "message": "Problem not found"}), 404
    return jsonify({
        "id": problem[0],
        "title": problem[1],
        "difficulty": problem[2],
        "description": problem[3],
        "example_input_output": problem[4]
    })

# Update a problem
@app.route('/Problems/<int:problem_id>', methods=['PUT'])
def update_problem(problem_id):
    data = request.json
    if not data or not data.get("title") or not data.get("difficulty") or not data.get("description"):
        return jsonify({"status": "error", "message": "All fields are required"}), 400
    result = db.update_problem(problem_id, data["title"], data["difficulty"], data["description"])
    return jsonify(result)

# Delete a problem
@app.route('/Problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    result = db.delete_problem(problem_id)
    return jsonify(result)

# Add Contest
@app.route('/contests', methods=['POST'])
def add_contest():
    data = request.json

    # Validation: Start time must be before End time, and Start time must be in the future.
    created_at = datetime.now()
    start_time = datetime.fromisoformat(data["start_time"])
    end_time = datetime.fromisoformat(data["end_time"])
    
    if start_time <= created_at:
        return jsonify({"error": "Start time must be in the future."}), 400
    if start_time >= end_time:
        return jsonify({"error": "Start time must be before End time."}), 400

    # Add contest to the database
    result = db.add_contest(
        data["title"], data["description"], data["start_time"], data["end_time"], "Pending"
    )
    return jsonify(result)


# Get Contests
@app.route('/contests', methods=['GET'])
def get_contests():
    contests = db.get_all_contests()
    now = datetime.now()

    # Update statuses dynamically
    contests = [
        {
            "id": c[0],
            "title": c[1],
            "description": c[2],
            "start_time": datetime.fromisoformat(c[3]).strftime('%Y-%m-%d %H:%M'),
            "end_time": datetime.fromisoformat(c[4]).strftime('%Y-%m-%d %H:%M'),
            "status": (
                "Running" if datetime.fromisoformat(c[3]) <= now <= datetime.fromisoformat(c[4])
                else "Completed" if now > datetime.fromisoformat(c[4])
                else "Pending"
            ),
            "created_at": datetime.strptime(c[6], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
        }
        for c in contests
    ]

    return jsonify({"contests": contests})


# Get a contest by id
@app.route('/contests/<int:contest_id>', methods=['GET'])
def get_contest_by_id(contest_id):
    contest = db.get_contest_by_id(contest_id)
    start_time = datetime.fromisoformat(contest[3])  # Convert string to datetime object
    end_time = datetime.fromisoformat(contest[4])  # Similarly for end_time
    contest = {
        "ID": contest[0],
        "Title": contest[1],
        "Description": contest[2],
        "Start-Time": start_time.isoformat(),  # Return in ISO format
        "End-Time": end_time.isoformat(),    # Return in ISO format
        "Status": contest[5],
        "Created-at": contest[6]
    }
    return jsonify({"contest": contest})

# Update Contest
@app.route('/contests/<int:contest_id>', methods=['PUT'])
def update_contest(contest_id):
    data = request.json
    result = db.update_contest(
        contest_id, data["title"], data["description"],
        data["start_time"], data["end_time"], data["status"]
    )
    return jsonify(result)

# Delete Contest
@app.route('/contests/<int:contest_id>', methods=['DELETE'])
def delete_contest(contest_id):
    result = db.delete_contest(contest_id)
    return jsonify(result)

# Add Submission
@app.route('/submissions', methods=['POST'])
def add_submission():
    data = request.json
    result = db.add_submission(
        data["problem_id"], data["user_id"], data["language"], data["code"], data["status"]
    )
    return jsonify(result)

# Get Submissions
@app.route('/submissions', methods=['GET'])
def get_submissions():
    submissions = db.get_all_submissions()
    return jsonify({"submissions": submissions})

# Get a submission by id
@app.route('/submissions/<int:problem_id>', methods=['GET'])
def get_submission_by_id(problem_id):
    submissions = db.get_submission_by_id(problem_id)
    # Assuming your submission data is a list of tuples, you can map it to a dictionary
    formatted_submissions = [
        {
            "id": submission[0],
            "problem_id": submission[1],
            "language": submission[2],
            "code": submission[3],
            "status": submission[4],
            "submitted_at": submission[5]
        }
        for submission in submissions
    ]
    return jsonify({"submissions": formatted_submissions})


# Update Submission
@app.route('/submissions/<int:submission_id>', methods=['PUT'])
def update_submission(submission_id):
    data = request.json
    result = db.update_submission(
        submission_id, data["problem_id"], data["user_id"],
        data["language"], data["code"], data["status"]
    )
    return jsonify(result)

# Delete Submission
@app.route('/submissions/<int:submission_id>', methods=['DELETE'])
def delete_submission(submission_id):
    result = db.delete_submission(submission_id)
    return jsonify(result)

# Add Contest problem
@app.route('/contest_problems', methods=['POST'])
def add_contest_problem():
    data = request.json
    result = db.add_contest_problem(data["contest_id"], data["problem_id"])
    return jsonify(result)

# Get Contest Problems
@app.route('/contest_problems', methods=['GET'])
def get_contest_problems():
    contest_problems = db.get_all_contest_problems()
    return jsonify({"contest_problems": contest_problems})

# Get Contest Problem by id
@app.route('/contest_problems/<int:contest_problem_id>', methods=['GET'])
def get_contest_problem_by_id(contest_problem_id):
    contest_problems = db.get_contest_problem_by_id(contest_problem_id)
    
    # Check if the result is a single problem (tuple) or multiple problems (list of tuples)
    if isinstance(contest_problems, tuple):
        contest_problems = [contest_problems]  # Convert to a list if it's a single problem
    
    problems = [
        {
            "id": problem[0],
            "title": problem[1],
            "difficulty": problem[2],
            "description": problem[3],
            "example": problem[4]
        }
        for problem in contest_problems
    ]
    return jsonify({"contest_problems": problems})


# Update Contest Problem
@app.route('/contest_problems/<int:contest_problem_id>', methods=['PUT'])
def update_contest_problem(contest_problem_id):
    data = request.json
    result = db.update_contest_problem(
        contest_problem_id, data["contest_id"], data["problem_id"]
    )
    return jsonify(result)

# Delete Contest Problem
@app.route('/contest_problems/<int:contest_problem_id>', methods=['DELETE'])
def delete_contest_problem(contest_problem_id):
    result = db.delete_contest_problem(contest_problem_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
