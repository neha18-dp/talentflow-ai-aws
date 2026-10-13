from db import get_db_connection


def get_all_interviews():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    i.id,
                    i.candidate_id,
                    c.name AS candidate_name,
                    c.position,
                    i.interview_date,
                    i.interview_time,
                    i.interviewer
                FROM interviews i
                JOIN candidates c
                    ON c.id = i.candidate_id
                ORDER BY i.interview_date, i.interview_time
            """)
            return cursor.fetchall()
    finally:
        connection.close()


def create_interview(interview):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO interviews
                    (candidate_id, interview_date, interview_time, interviewer)
                VALUES
                    (%s, %s, %s, %s)
            """, (
                interview["candidate_id"],
                interview["interview_date"],
                interview["interview_time"],
                interview["interviewer"],
            ))

            return {
                **interview,
                "id": cursor.lastrowid
            }

    finally:
        connection.close()
        