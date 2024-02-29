import sys

def main():
    # Simulated user database
    users = {
        "user1": "password1",
        "user2": "password2"
    }

    # Get username and password from command-line arguments
    username = sys.argv[1]
    password = sys.argv[2]

    # Check if the username exists and the password matches
    if username in users and users[username] == password:
        sys.exit(0)  # Exit with success status code
    else:
        sys.exit(1)  # Exit with error status code

if __name__ == "__main__":
    main()
