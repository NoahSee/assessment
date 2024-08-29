# app.py
from routes.auth import auth_bp
from routes.applications import applications_bp
from routes.schemes import schemes_bp
from routes.applicants import applicants_bp
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from db import init_db

# Initialize Flask app and extensions
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "somekey"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Initialize database
with app.app_context():
    init_db()

# Register Blueprints
app.register_blueprint(applicants_bp, url_prefix="/api/applicants")
app.register_blueprint(schemes_bp, url_prefix="/api/schemes")
app.register_blueprint(applications_bp, url_prefix="/api/applications")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
