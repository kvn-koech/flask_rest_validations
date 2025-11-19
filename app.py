from flask import Flask, request, jsonify
from models import db, User
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app) 

# RESTful API Home
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Flask RESTful API with validations!",
        "endpoints": {
            "GET /users": "Get all users",
            "GET /users/<id>": "Get single user",
            "POST /users": "Create new user",
            "PUT /users/<id>": "Update user",
            "DELETE /users/<id>": "Delete user"
        }
    })

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    except Exception as e:
        return jsonify({"error": "Failed to fetch users", "details": str(e)}), 500

# GET single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user:
            return jsonify(user.to_dict())
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": "Failed to fetch user", "details": str(e)}), 500

# CREATE user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        
        # Check if JSON data exists
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Check required fields
        required_fields = ['name', 'email', 'age']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            age=data['age']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify(new_user.to_dict()), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Validation error", "details": str(e)}), 400
    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed: users.email" in str(e):
            return jsonify({"error": "Email already exists"}), 400
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create user", "details": str(e)}), 500

# UPDATE user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'age' in data:
            user.age = data['age']
        
        db.session.commit()
        return jsonify(user.to_dict())
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": "Validation error", "details": str(e)}), 400
    except IntegrityError as e:
        db.session.rollback()
        if "UNIQUE constraint failed: users.email" in str(e):
            return jsonify({"error": "Email already exists"}), 400
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update user", "details": str(e)}), 500

# DELETE user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete user", "details": str(e)}), 500

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "database": "connected"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)