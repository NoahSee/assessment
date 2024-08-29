from flask import Blueprint, jsonify, request
from db import get_db_connection
import subprocess
import json

schemes_bp = Blueprint("schemes", __name__)


@schemes_bp.route("/", methods=["GET"])
@jwt_required()
def get_schemes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()
    return jsonify([dict(scheme) for scheme in schemes])


@schemes_bp.route("/eligible", methods=["GET"])
@jwt_required()
def get_eligible_schemes():
    applicant_id = request.args.get("applicant")
    if not applicant_id:
        return jsonify({"message": "Applicant ID is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT household_json FROM applicants WHERE id = ?", (applicant_id,)
    )
    applicant = cursor.fetchone()
    if not applicant:
        return jsonify({"message": "Applicant not found"}), 404

    household_json = applicant["household_json"]

    cursor.execute("SELECT * FROM schemes")
    schemes = cursor.fetchall()

    eligible_schemes = []
    for scheme in schemes:
        criteria_jq = scheme["criteria_jq"]
        if evaluate_criteria(household_json, criteria_jq):
            eligible_schemes.append(scheme)

    return jsonify([dict(scheme) for scheme in eligible_schemes])


def evaluate_criteria(applicant, criteria_jq):
    try:
        json_data = json.dumps(json.loads(applicant))
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False

    try:
        result = subprocess.run(
            ["jq", "-c", criteria_jq], input=json_data, text=True, capture_output=True
        )
        return result.returncode == 0 and result.stdout.startswith("true")
    except FileNotFoundError:
        raise RuntimeError("JQ command not found. Install JQ to proceed.")
    except Exception as e:
        print(f"Error evaluating criteria: {e}")
        return False
