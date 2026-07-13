from modules.auth import register_user, login_user

print(register_user(
    "Divyansh Sharma",
    "divyansh",
    "Password123"
))

print(login_user(
    "divyansh",
    "Password123"
))