import os
from pathlib import Path

from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

APP_MODE = os.getenv("APP_MODE", "local")

UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_RESUME_EXTENSIONS = {".pdf"}
MAX_RESUME_SIZE = 5 * 1024 * 1024

from db import get_db_connection
from flask import Flask, jsonify, request
from flask_cors import CORS
from copy import deepcopy
from datetime import date
from pathlib import Path
from werkzeug.utils import secure_filename

from services.candidate_service import (
    get_all_candidates,
    create_candidate as db_create_candidate,
    update_candidate as db_update_candidate
)
from services.job_service import create_job as db_create_job
from services.interview_service import create_interview as db_create_interview

app = Flask(__name__)
CORS(app)

DEMO_DATA = {
    "candidates": [
        {
            "id": 1,
            "name": "Aarav Mehta",
            "email": "aarav@example.com",
            "role": "Frontend Developer",
            "experience": "3 years",
            "score": 94,
            "stage": "Interview",
            "applied": "2026-09-25",
            "source": "LinkedIn"
        },
        {
            "id": 2,
            "name": "Priya Shah",
            "email": "priya@example.com",
            "role": "Python Developer",
            "experience": "2 years",
            "score": 91,
            "stage": "Screening",
            "applied": "2026-09-24",
            "source": "Referral"
        },
        {
            "id": 3,
            "name": "Rohan Patil",
            "email": "rohan@example.com",
            "role": "DevOps Engineer",
            "experience": "4 years",
            "score": 88,
            "stage": "Shortlisted",
            "applied": "2026-09-23",
            "source": "Indeed"
        },
        {
            "id": 4,
            "name": "Sneha Kulkarni",
            "email": "sneha@example.com",
            "role": "Data Analyst",
            "experience": "2 years",
            "score": 86,
            "stage": "Applied",
            "applied": "2026-09-22",
            "source": "Website"
        },
        {
            "id": 5,
            "name": "Vikram Joshi",
            "email": "vikram@example.com",
            "role": "Backend Developer",
            "experience": "5 years",
            "score": 82,
            "stage": "Offer",
            "applied": "2026-09-20",
            "source": "LinkedIn"
        }
    ],

    "jobs": [
        {
            "id": 1,
            "title": "Frontend Developer",
            "department": "Engineering",
            "location": "Mumbai / Hybrid",
            "type": "Full-time",
            "applicants": 18
        },
        {
            "id": 2,
            "title": "Python Developer",
            "department": "Engineering",
            "location": "Remote",
            "type": "Full-time",
            "applicants": 12
        },
        {
            "id": 3,
            "title": "Data Analyst",
            "department": "Analytics",
            "location": "Pune / Hybrid",
            "type": "Full-time",
            "applicants": 9
        }
    ],

    "interviews": [
        {
            "id": 1,
            "candidate": "Aarav Mehta",
            "role": "Frontend Developer",
            "date": "2026-09-28",
            "time": "10:30 AM",
            "interviewer": "Neha Sharma",
            "status": "Scheduled",
            "link": "https://meet.google.com/"
        },
        {
            "id": 2,
            "candidate": "Rohan Patil",
            "role": "DevOps Engineer",
            "date": "2026-09-29",
            "time": "2:00 PM",
            "interviewer": "Rahul Verma",
            "status": "Pending",
            "link": "https://meet.google.com/"
        },
        {
            "id": 3,
            "candidate": "Priya Shah",
            "role": "Python Developer",
            "date": "2026-09-30",
            "time": "11:00 AM",
            "interviewer": "Anita Rao",
            "status": "Scheduled",
            "link": "https://meet.google.com/"
        }
    ]
}


# Temporary in-memory application data.
# We will replace this with RDS MySQL in the next step.
APP_DATA = deepcopy(DEMO_DATA)


# =========================================================
# BASIC ROUTES
# =========================================================

@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "TalentFlow AI API"
    })


@app.get("/")
def home():
    return jsonify({
        "message": "TalentFlow AI API is running"
    })


# =========================================================
# APPLICATION STATE
# =========================================================

@app.get("/api/state")
def get_state():
    if APP_MODE != "database":
        return jsonify(APP_DATA)

    try:
        return jsonify({
            "candidates": get_all_candidates(),
            "jobs": get_all_jobs(),
            "interviews": get_all_interviews()
        })

    except Exception as e:
        return jsonify({
            "error": "Database connection failed",
            "details": str(e)
        }), 500


# =========================================================
# CANDIDATES
# =========================================================

@app.post("/api/candidates")
def create_candidate():
    payload = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "email",
        "role",
        "experience",
        "score"
    ]

    missing = [
        field
        for field in required_fields
        if field not in payload
    ]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    candidate = {
        "name": str(payload["name"]).strip(),
        "email": str(payload["email"]).strip(),
        "role": str(payload["role"]).strip(),
        "experience": str(payload["experience"]).strip(),
        "score": int(payload.get("score", 0)),
        "stage": payload.get("stage", "Applied"),
        "applied": payload.get(
            "applied",
            date.today().isoformat()
        ),
        "source": payload.get("source", "Website")
    }

    if APP_MODE == "database":
        db_candidate = {
            "name": candidate["name"],
            "email": candidate["email"],
            "position": candidate["role"],
            "experience": candidate["experience"],
            "score": candidate["score"],
            "stage": candidate["stage"],
            "applied_date": candidate["applied"]
        }

        created = db_create_candidate(db_candidate)

        candidate["id"] = created["id"]

        return jsonify({
            "message": "Candidate created successfully",
            "candidate": candidate
        }), 201

    # Local/in-memory mode
    candidate["id"] = (
        max(
            [c["id"] for c in APP_DATA["candidates"]],
            default=0
        ) + 1
    )

    APP_DATA["candidates"].insert(0, candidate)

    return jsonify({
        "message": "Candidate created successfully",
        "candidate": candidate
    }), 201


@app.patch("/api/candidates/<int:candidate_id>")
def update_candidate(candidate_id):

    payload = request.get_json(silent=True) or {}

    allowed_fields = [
        "name",
        "email",
        "role",
        "experience",
        "score",
        "stage",
        "source"
    ]

    if APP_MODE == "database":
        updates = {
            field: payload[field]
            for field in allowed_fields
            if field in payload
        }

        db_updates = {}

        field_map = {
            "name": "name",
            "email": "email",
            "role": "position",
            "experience": "experience",
            "score": "score",
            "stage": "stage"
        }

        for field, value in updates.items():
            if field in field_map:
                db_updates[field_map[field]] = value

        if not db_updates:
            return jsonify({
                "error": "No valid fields to update"
            }), 400

        result = db_update_candidate(
            candidate_id,
            db_updates
        )

        if result is None:
            return jsonify({
                "error": "No valid fields to update"
            }), 400

        return jsonify({
            "message": "Candidate updated successfully",
            "candidate_id": candidate_id,
            "updates": updates
        })

    # Local/in-memory mode
    candidate = next(
        (
            c
            for c in APP_DATA["candidates"]
            if c["id"] == candidate_id
        ),
        None
    )

    if not candidate:
        return jsonify({
            "error": "Candidate not found"
        }), 404

    for field in allowed_fields:
        if field in payload:
            candidate[field] = payload[field]

    return jsonify({
        "message": "Candidate updated successfully",
        "candidate": candidate
    })


# =========================================================
# JOBS
# =========================================================

@app.post("/api/jobs")
def create_job():
    payload = request.get_json(silent=True) or {}

    required_fields = [
        "title",
        "department",
        "location",
        "type"
    ]

    missing = [
        field
        for field in required_fields
        if field not in payload
    ]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    job = {
        "title": str(payload["title"]).strip(),
        "department": str(payload["department"]).strip(),
        "location": str(payload["location"]).strip(),
        "type": str(payload["type"]).strip(),
        "applicants": int(payload.get("applicants", 0))
    }

    if APP_MODE == "database":
        db_job = {
            "title": job["title"],
            "department": job["department"],
            "location": job["location"],
            "type": job["type"]
        }

        created = db_create_job(db_job)

        job["id"] = created["id"]

        return jsonify({
            "message": "Job created successfully",
            "job": job
        }), 201

    # Local/in-memory mode
    job["id"] = (
        max(
            [j["id"] for j in APP_DATA["jobs"]],
            default=0
        ) + 1
    )

    APP_DATA["jobs"].insert(0, job)

    return jsonify({
        "message": "Job created successfully",
        "job": job
    }), 201


@app.get("/api/db-test")
def db_test():
    try:
        connection = get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 AS ok")
            result = cursor.fetchone()

        connection.close()

        return jsonify({
            "database": "connected",
            "result": result
        })

    except Exception as e:
        return jsonify({
            "database": "not_connected",
            "error": str(e)
        }), 500


        
# =========================================================
# JOBS
# =========================================================




@app.post("/api/interviews")
def create_interview():
    payload = request.get_json(silent=True) or {}

    required_fields = [
        "candidate",
        "role",
        "date",
        "time",
        "interviewer"
    ]

    missing = [
        field
        for field in required_fields
        if field not in payload
    ]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    interview = {
        "candidate": str(payload["candidate"]).strip(),
        "role": str(payload["role"]).strip(),
        "date": str(payload["date"]),
        "time": str(payload["time"]).strip(),
        "interviewer": str(payload["interviewer"]).strip(),
        "status": payload.get("status", "Scheduled"),
        "link": payload.get(
            "link",
            "https://meet.google.com/"
        )
    }

    if APP_MODE == "database":
        # Database mode will be connected to RDS after AWS setup.
        return jsonify({
            "error": "Database interview mode is not connected yet"
        }), 501

    # Local/in-memory mode
    interview["id"] = (
        max(
            [i["id"] for i in APP_DATA["interviews"]],
            default=0
        ) + 1
    )

    APP_DATA["interviews"].append(interview)

    return jsonify({
        "message": "Interview scheduled successfully",
        "interview": interview
    }), 201



# =========================================================
# RESUME UPLOAD
# =========================================================

@app.post("/api/candidates/<int:candidate_id>/resume")
def upload_resume(candidate_id):

    # Verify candidate exists in local mode
    if APP_MODE == "local":
        candidate = next(
            (
                c
                for c in APP_DATA["candidates"]
                if c["id"] == candidate_id
            ),
            None
        )

        if not candidate:
            return jsonify({
                "error": "Candidate not found"
            }), 404

    if "resume" not in request.files:
        return jsonify({
            "error": "No resume file provided"
        }), 400

    file = request.files["resume"]

    if not file.filename:
        return jsonify({
            "error": "No file selected"
        }), 400

    filename = secure_filename(file.filename)
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_RESUME_EXTENSIONS:
        return jsonify({
            "error": "Only PDF resumes are allowed"
        }), 400

    # Check file size
    file.seek(0, 2)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_RESUME_SIZE:
        return jsonify({
            "error": "Resume must be 5 MB or smaller"
        }), 400

    saved_name = f"candidate_{candidate_id}_{filename}"
    file_path = UPLOAD_FOLDER / saved_name

    file.save(file_path)

    return jsonify({
        "message": "Resume uploaded successfully",
        "candidate_id": candidate_id,
        "filename": filename,
        "size_bytes": file_size,
        "storage": "local"
    }), 201

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )