from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from db import get_db_connection
from flask_jwt_extended import jwt_required

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO administrators (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists!"}), 409
    finally:
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM administrators WHERE username = ?", (username,))
    admin = cursor.fetchone()

    if admin and bcrypt.check_password_hash(admin["password"], password):
        access_token = create_access_token(identity={"username": admin["username"]})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
