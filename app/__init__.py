from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
    
    CORS(app)
    JWTManager(app)
    
    from app.routes.projects import projects_bp
    from app.routes.blog import blog_bp
    from app.routes.contact import contact_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(projects_bp, url_prefix='/api')
    app.register_blueprint(blog_bp, url_prefix='/api')
    app.register_blueprint(contact_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    
    return app