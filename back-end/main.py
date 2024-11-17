from flask import Flask, jsonify, request
from utility import Database
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db = Database()  

@app.route("/")
def home():
    return "Home Page"


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
        "description": problem[3]
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

# Add a Contest
@app.route('/contests', methods=['POST'])
def add_contest():
    data = request.json
    result = db.add_contest(
        data["title"], data["description"], data["start_time"], data["end_time"], data["status"]
    )
    return jsonify(result)

# Get Contests
@app.route('/contests', methods=['GET'])
def get_contests():
    contests = db.get_all_contests()
    print(contests)
    response = {"contests": [{"id": contest[0], "title": contest[1], "description": contest[2],"start_time":contest[3],"end_time":contest[4],"status":contest[5],"created_at":contest[6]} for contest in contests]}
    return response

# Get a contest by id
@app.route('/contests/<int:contest_id>', methods=['GET'])
def get_contest_by_id(contest_id):
    contest = db.get_contest_by_id(contest_id)
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
@app.route('/submissions/<int:submission_id>', methods=['GET'])
def get_submission_by_id(submission_id):
    submission = db.get_submission_by_id(submission_id)
    return jsonify({"submission": submission})

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
    contest_problem = db.get_contest_problem_by_id(contest_problem_id)
    return jsonify({"contest_problem": contest_problem})

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
