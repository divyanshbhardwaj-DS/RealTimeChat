from modules.database import connect
from modules.security import hash_password, verify_password


def register_user(full_name, username, password):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))

    if cursor.fetchone():
        conn.close()
        return False, "Username already exists"

    hashed = hash_password(password)

    cursor.execute(
        """
        INSERT INTO users(full_name,username,password_hash)
        VALUES(?,?,?)
        """,
        (full_name, username, hashed)
    )

    conn.commit()
    conn.close()

    return True, "Registration Successful"


def login_user(username, password):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return False

    return verify_password(password, user[0])