from modules.database import connect


# ---------------- SAVE MESSAGE ---------------- #

def save_message(sender, receiver, message):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages
        (sender, receiver, message)
        VALUES (?, ?, ?)
        """,
        (sender, receiver, message)
    )

    conn.commit()
    conn.close()


# ---------------- LOAD HISTORY ---------------- #

def load_history(user1, user2):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sender, message, timestamp
        FROM messages

        WHERE

        (sender=? AND receiver=?)

        OR

        (sender=? AND receiver=?)

        ORDER BY timestamp ASC
        """,
        (
            user1,
            user2,
            user2,
            user1
        )
    )

    data = cursor.fetchall()

    conn.close()

    return data


# ---------------- LOAD GLOBAL CHAT ---------------- #

def load_global_chat():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sender, message, timestamp
        FROM messages
        ORDER BY timestamp ASC
        """
    )

    data = cursor.fetchall()

    conn.close()

    return data


# ---------------- DELETE CHAT ---------------- #

def delete_chat():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM messages"
    )

    conn.commit()
    conn.close()


# ---------------- LAST MESSAGE ---------------- #

def last_message():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT sender, message
        FROM messages
        ORDER BY id DESC
        LIMIT 1
        """
    )

    row = cursor.fetchone()

    conn.close()

    return row