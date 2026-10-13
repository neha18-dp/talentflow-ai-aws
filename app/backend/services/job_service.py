from db import get_db_connection


def get_all_jobs():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    title,
                    department,
                    location,
                    type,
                    DATE_FORMAT(created_at, '%%Y-%%m-%%d') AS created_at
                FROM jobs
                ORDER BY id DESC
            """)
            return cursor.fetchall()
    finally:
        connection.close()


def create_job(job):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO jobs
                    (title, department, location, type)
                VALUES
                    (%s, %s, %s, %s)
            """, (
                job["title"],
                job.get("department", ""),
                job.get("location", ""),
                job.get("type", "Full-time"),
            ))

            return {
                **job,
                "id": cursor.lastrowid
            }

    finally:
        connection.close()