import hashlib


def hash_password(password: str) -> str:
    """
    Convert plain password into SHA256 hash.
    """
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify entered password.
    """
    return hash_password(password) == stored_hash