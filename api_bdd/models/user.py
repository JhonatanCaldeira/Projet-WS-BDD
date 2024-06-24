from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
        }

    @staticmethod
    def get_user(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def get_login(data):
        if 'email' not in data and 'password' not in data:
            raise ValueError("Missing parameter")

        user = User.query.filter_by(email=data['email']).first()
        if not user:
            raise ValueError("Email doesn't exist")

        if check_password_hash(user.password, data["password"]):        
            return user

        raise ValueError("bad password")

    @staticmethod
    def get_users():
        return User.query.all()

    @staticmethod
    def create_user(data):
        if 'email' not in data and 'name' not in data and 'password' not in data:
            raise ValueError("Missing parameter")

        if User.query.filter_by(email=data['email']).first():
            raise ValueError("Email already exists")

        password_hash = generate_password_hash(data["password"])
        new_user = User(email=data["email"],
                        name=data["name"],
                        password=password_hash)

        # Add user
        db.session.add(new_user)
        db.session.commit()

        return new_user
