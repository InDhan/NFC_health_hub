import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify
from templates.assets.logic.login import authenticate_user
import subprocess
import serial.tools.list_ports
import time
from prescription import fetch_prescriptions
app = Flask(__name__, static_folder='templates/', static_url_path='/')


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    global rfid_uid
    if request.method == 'POST':
        if authenticate_user(request.form['username'], request.form['password']):
            return render_template('dashboard.html', rfid_tag="RFID Tag UID:", rfid_value=rfid_uid)  # Pass rfid_uid to dashboard.html
        else:
            return render_template('index.html', error="Invalid credentials. Please try again.")
    else:
        return render_template('index.html')

@app.route('/get_rfid_data', methods=['GET'])
def get_rfid_data():
    global prev_rfid_uid, rfid_uid
    if rfid_uid != prev_rfid_uid:  # Check if the RFID UID has changed
        prev_rfid_uid = rfid_uid  # Update the previous RFID UID
        return jsonify(str(rfid_uid))  # Convert the RFID UID to a string and return
    else:
        return jsonify(None)  # Return None if the RFID UID has not changed 


@app.route('/add_patient')
def add_patient():
    return render_template('add_patient.html')

@app.route('/patient_info')
def patient_info():
    global rfid_uid
    return render_template('Patient_info.html', rfid_uid=rfid_uid)  # Pass rfid_uid to Patient_info.html

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        prescriptions = fetch_prescriptions(patient_id)
        return render_template('prescription.html', prescriptions=prescriptions, patient_id=patient_id)
    else:
        return render_template('prescription.html')

if __name__ == '__main__':
    start_rfid_thread()  # Start the RFID reading thread
    app.run(debug=True)
    patient_id = read_rfid()
    print([patient_id])
    

