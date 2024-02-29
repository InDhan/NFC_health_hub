from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/")
def login_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # Call the login script with subprocess
    result = subprocess.run(["python", "assets/js/login.py", username, password], capture_output=True, text=True)

    if result.returncode == 0:
        # Login successful
        return jsonify({"success": True}), 200
    else:
        # Login failed
        return jsonify({"success": False}), 401

if __name__ == "__main__":
    app.run(debug=True)
