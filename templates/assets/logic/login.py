# login.py

def authenticate_user(username, password):
    # Simulated user database
    users = {
        "user1": "password1",
        "user2": "password2",
        "utkarsh": "utkarsh"  # Added user
    }

    # Check if the username exists and the password matches
    if username in users and users[username] == password:
        return True
    else:
        return False
    

    
