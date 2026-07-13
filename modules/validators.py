def validate_registration(full_name, username, password, confirm_password):
    if not full_name.strip():
        return False, "Full name is required."

    if not username.strip():
        return False, "Username is required."

    if len(username) < 4:
        return False, "Username must be at least 4 characters."

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if password != confirm_password:
        return False, "Passwords do not match."

    return True, "Valid"