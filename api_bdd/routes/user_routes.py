from flask import jsonify, request
from ..models.user import User
from flask import Blueprint

user_bp = Blueprint('user', __name__)


# route pour recuperer un utilisateur par son ID - GET  (id)
@user_bp.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    user = User.get_user(id)
    if user:
        return jsonify(user.to_dict())
    message = {"message": "User not found"}
    return jsonify(message), 404


# route pour recuperer tous les  utilisateurs
@user_bp.route('/users', methods=["GET"])
def get_users():
    users = User.get_users()
    output = jsonify([user.to_dict() for user in users])
    return output


# recevoir un user pour le créer - PUT (email, password, name)
@user_bp.route('/users', methods=["PUT"])
def create_user():
    data = request.get_json()
    try:
        new_user = User.create_user(data)
        return jsonify(new_user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# recevoir une user pour vérifier - POST (email, password)
@user_bp.route('/users', methods=["POST"])
def is_user():
    data = request.get_json()
    try:
        user = User.get_login(data)
        return jsonify(user.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
