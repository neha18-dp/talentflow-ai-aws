from db import get_db_connection


def get_all_candidates():
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    name,
                    email,
                    position,
                    experience,
                    score,
                    stage,
                    DATE_FORMAT(applied_date, '%%Y-%%m-%%d') AS applied_date
                FROM candidates
                ORDER BY applied_date DESC, id DESC
            """)
            return cursor.fetchall()
    finally:
        connection.close()


def create_candidate(candidate):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO candidates
                    (name, email, position, experience, score, stage, applied_date)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
            """, (
                candidate["name"],
                candidate["email"],
                candidate["position"],
                candidate.get("experience", ""),
                candidate.get("score", 0),
                candidate.get("stage", "Applied"),
                candidate["applied_date"],
            ))

            candidate_id = cursor.lastrowid

        return {
            **candidate,
            "id": candidate_id
        }

    finally:
        connection.close()


def update_candidate(candidate_id, updates):
    allowed_fields = {
        "name",
        "email",
        "position",
        "experience",
        "score",
        "stage",
        "applied_date",
    }

    fields = {
        key: value
        for key, value in updates.items()
        if key in allowed_fields
    }

    if not fields:
        return None

    connection = get_db_connection()

    try:
        set_clause = ", ".join(
            f"{field} = %s"
            for field in fields
        )

        values = list(fields.values())
        values.append(candidate_id)

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE candidates
                SET {set_clause}
                WHERE id = %s
                """,
                values
            )

        return True

    finally:
        connection.close()