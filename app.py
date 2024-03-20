import threading
from flask import Flask, render_template, request, redirect, url_for
from templates.assets.logic.login import authenticate_user
import subprocess

# Import the RFID reader script
from rfid import read_rfid

app = Flask(__name__, static_folder='templates/', static_url_path='/')

# Define a global variable to store the RFID tag UID
rfid_uid = None

# Function to continuously read RFID tags
def read_rfid_tags():
    global rfid_uid
    while True:
        rfid_uid = read_rfid()

# Start a new thread to run the RFID reader function
rfid_thread = threading.Thread(target=read_rfid_tags)
rfid_thread.daemon = True
rfid_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST' and authenticate_user(request.form['username'], request.form['password']):
        subprocess.run(['python', '../rfid.py'])  # Replace 'path/to/rfid.py' with the actual path
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if authenticate_user(request.form['username'], request.form['password']):
           return render_template('dashboard.html')
        else:
            return render_template('index.html', error="Invalid credentials. Please try again.")
    else:
        return render_template('index.html')
    
@app.route('/add_patient')
def add_patient():
    return render_template('add_patient.html')

@app.route('/patient_info')
def patient_info():
    return render_template('Patient_info.html')

if __name__ == '__main__':
    app.run(debug=True)
