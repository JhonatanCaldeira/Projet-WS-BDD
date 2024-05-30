from flask import Flask
from .models.user import db
from .routes.user_routes import user_bp

def create_app():
    
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"

    db.init_app(app)
    
    
    app.register_blueprint(user_bp, url_prefix="/api")
    
    with app.app_context():
        db.create_all()
        print("Database created!")    
    
    return app
