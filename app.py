import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify
from templates.assets.logic.login import authenticate_user
import subprocess
import serial.tools.list_ports
import time
from prescription import update_prescription,fetch_prescriptions
#from flask_socketio import SocketIO

app = Flask(__name__, static_folder='templates/', static_url_path='/')

ser = None  # Initialize serial port variable
rfid_uid = None  # Initialize RFID UID variable
#socketio = SocketIO(app)

def find_and_open_serial_port():
    # Get a list of available serial ports
    ports = serial.tools.list_ports.comports()

    # Iterate through the ports to find a suitable one
    for port in ports:
        if 'COM' in port.device:  # Adjust this condition as needed for your system
            try:
                # Attempt to open the serial port
                ser = serial.Serial(port.device, 9600)
                print(f"Opened serial port: {port.device}")
                return ser
            except serial.SerialException:
                continue
    
    # Return None if no suitable port is found
    return None

def read_rfid():
    global ser, rfid_uid
    while True:
        if ser is not None and ser.is_open:
            # Read data from the Arduino
            data = ser.readline().strip().decode('utf-8')
            if data:
                rfid_uid = data
                print("Patient RFID:", rfid_uid)
        time.sleep(0.1)  # Adjust delay as needed

def start_rfid_thread():
    global ser
    ser = find_and_open_serial_port()
    if ser is None:
        print("Error: No available serial port found!")
    else:
        print("Serial port opened successfully.")
        # Start a new thread to run the RFID reader function
        rfid_thread = threading.Thread(target=read_rfid)
        rfid_thread.daemon = True
        rfid_thread.start()

# Variable to store the previous RFID UID
prev_rfid_uid = None

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
    
# def get_rfid_data():
#     global prev_rfid_uid, rfid_uid
#     if rfid_uid != prev_rfid_uid:  # Check if the RFID UID has changed
#         prev_rfid_uid = rfid_uid  # Update the previous RFID UID
#         return jsonify(str(rfid_uid))  # Convert the RFID UID to a string and return
#     else:
#         return jsonify(None)  # Return None if the RFID UID has not changed 

# def rfid_display():
#     tag_uid = get_rfid_data()
#     return render_template('index.html', tag_uid=tag_uid)

@app.route('/get_rfid_data', methods=['GET'])
def get_rfid_data():
    global prev_rfid_uid, rfid_uid
    if rfid_uid != prev_rfid_uid:
        prev_rfid_uid = rfid_uid
        return jsonify({"tag_uid": str(rfid_uid)})
    else:
        return jsonify({"tag_uid": None})


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

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/patient_info', methods=['GET', 'POST'])
def patient_info():
    if request.method == 'POST':
        id_value = request.form['id_value']
        return render_template('patient_info.html', id_value=id_value)
    return render_template('patient_info.html')

@app.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    id_value = request.args.get('id_value')
    prescriptions = fetch_prescriptions(id_value)
    return jsonify({'prescriptions': prescriptions})

@app.route('/update_prescription', methods=['POST'])
def update_prescription_route():
    data = request.json
    id_value = data.get('id_value')
    new_prescription = data.get('new_prescription')
    updated_prescription = update_prescription(id_value, new_prescription)
    if updated_prescription:
        return jsonify({'message': 'Prescription updated successfully', 'success': True}), 200
    else:
        return jsonify({'message': 'Failed to update prescription', 'success': False}), 404
    
if __name__ == '__main__':
    start_rfid_thread()  # Start the RFID reading thread
    app.run(debug=True)
    patient_id = read_rfid()
    print([patient_id])
    

