from flask import Blueprint, jsonify, request
from db import get_db_connection
from .schemes import evaluate_criteria

applications_bp = Blueprint('applications', __name__)


@applications_bp.route("/", methods=["GET"])
@jwt_required()
def get_applications():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM applications")
    applications = cursor.fetchall()
    return jsonify([dict(application) for application in applications])


@applications_bp.route("/", methods=["POST"])
@jwt_required()
def add_application():
    new_application = request.json

    applicant_id = new_application.get("applicant_id")
    scheme_id = new_application.get("scheme_id")

    if not applicant_id or not scheme_id:
        return jsonify({"message": "Applicant ID and Scheme ID are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM applicants WHERE id = ?", (applicant_id,))
    applicant = cursor.fetchone()
    if not applicant:
        return jsonify({"message": "Applicant not found"}), 404

    cursor.execute("SELECT * FROM schemes WHERE id = ?", (scheme_id,))
    scheme = cursor.fetchone()
    if not scheme:
        return jsonify({"message": "Scheme not found"}), 404

    criteria_jq = scheme['criteria_jq']

    if not evaluate_criteria(applicant["household_json"], criteria_jq):
        return jsonify({"message": "Applicant does not meet the criteria for this scheme"}), 400

    cursor.execute(
        "INSERT INTO applications (applicant_id, scheme_id) VALUES (?, ?)",
        (applicant_id, scheme_id),
    )
    conn.commit()

    return (
        jsonify({"id": cursor.lastrowid,
                "message": "Application added successfully!"}),
        201,
    )


@applications_bp.route("/<int:application_id>/outcome", methods=["PUT"])
@jwt_required()
def update_application_outcome(application_id):
    data = request.json
    new_outcome = data.get("outcome")

    if new_outcome not in ["Approved", "Denied"]:
        return jsonify({"message": "Invalid outcome. Valid outcomes are 'Approved' or 'Denied'."}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET outcome = ? WHERE id = ?",
        (new_outcome, application_id)
    )

    if cursor.rowcount == 0:
        return jsonify({"message": "Application not found or no changes made."}), 404

    conn.commit()
    conn.close()

    return jsonify({"message": f"Application {application_id} updated to {new_outcome}."}), 200
