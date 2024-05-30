from flask import jsonify, request, Response
from ..models.user import User, db 
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint

user_bp = Blueprint('user', __name__)

def to_dict(x):
    return {
        'id': x.id,
        'email': x.email,
        'name': x.name,
    }

# route pour recuperer un utilisateur par son ID - GET  (id)
@user_bp.route('/users/<int:id>', methods=["GET"])
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        output = jsonify(to_dict(user))
        return output

# route pour recuperer tous les  utilisateurs
@user_bp.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    output = jsonify([to_dict(user) for user in users])
    return output
    
# recevoir un user pour le créer - PUT (email, password, name) 
@user_bp.route('/users', methods=["PUT"])
def create_user():
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if not user:
        # New User Object
        password_hash = generate_password_hash(data["password"], method="sha256")
        new_user = User(email=email, name=data["name"], password=password_hash)
        
        # Add user
        db.session.add(new_user)
        db.session.commit()
        

# recevoir une user pour vérifier - POST (email, password)
@user_bp.route('/users', methods=["POST"])
def is_user():
    print("="*20)
    print("="*20)
    print("="*20)
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, data["password"]):
            return Response("{'mot de passe':'bon'}", status=200, mimetype='application/json')
        
        return Response("{'mot de passe':'pas bon'}", status=400, mimetype='application/json')
    
    return Response("{'user':'pas bon'}", status=404, mimetype='application/json')

        