from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# RESTful API Home
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask RESTful API with validations!"})

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "age": u.age} for u in users])

# GET single user
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "age": user.age})
    return jsonify({"error": "User not found"}), 404

# CREATE user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    try:
        new_user = User(name=data['name'], email=data['email'], age=data['age'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"id": new_user.id, "name": new_user.name, "email": new_user.email, "age": new_user.age}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# UPDATE user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    try:
        user.name = data['name']
        user.email = data['email']
        user.age = data['age']
        db.session.commit()
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "age": user.age})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
