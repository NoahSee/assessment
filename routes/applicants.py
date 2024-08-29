from flask import Blueprint, jsonify, request
from db import get_db_connection
from flask_jwt_extended import jwt_required
import json

applicants_bp = Blueprint("applicants", __name__)


@applicants_bp.route("/", methods=["GET"])
@jwt_required()
def get_all_applicants():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applicants")
    applicants = cursor.fetchall()
    conn.close()
    return jsonify([dict(applicant) for applicant in applicants]), 200


@applicants_bp.route("/", methods=["POST"])
@jwt_required()
def add_applicant():
    new_applicant = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO applicants (id, name, email, date_of_birth, sex, marital_status, employment_status, household_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            new_applicant["id"],
            new_applicant["name"],
            new_applicant["email"],
            new_applicant["date_of_birth"],
            new_applicant["sex"],
            new_applicant["marital_status"],
            new_applicant["employment_status"],
            json.dumps(new_applicant["household_json"]),
        ),
    )
    conn.commit()
    return (
        jsonify(
            {"id": new_applicant["id"], "message": "Applicant added successfully!"}
        ),
        201,
    )
