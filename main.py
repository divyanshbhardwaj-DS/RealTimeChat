from modules.database import initialize_database
from client.login import start_login


def main():

    initialize_database()

    start_login()


if __name__ == "__main__":
    main()