import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify
import serial.tools.list_ports
import time
from templates.assets.logic.login import authenticate_user
from flask_socketio import SocketIO
from prescription import update_prescription,fetch_prescriptions
from flask_socketio import SocketIO

# Initialize Flask app and SocketIO
app = Flask(__name__, static_folder='templates/', static_url_path='/')
socketio = SocketIO(app)

# Global variables
ser = None  # Serial port variable
rfid_uid = None  # RFID UID variable
prev_rfid_uid = None  # Previous RFID UID variable

def find_and_open_serial_port():
    global ser
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
            if data.startswith('Patient RFID: Card UID:'):
                rfid_uid = data.split(': ')[-1].strip()  # Extract the RFID UID from the data
                print("Patient RFID:", rfid_uid)
        time.sleep(0.1)  # Adjust delay as needed

@socketio.on('rfid_data')
def handle_rfid_data(data):
    global rfid_uid
    rfid_uid = data['tag_uid']  # Assuming 'tag_uid' is the key for RFID UID in the data
    socketio.emit('rfid_update', {'tag_uid': rfid_uid})

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
        print("RFID thread started.")  # Debug print

# Routes
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Handle login form submission
    if request.method == 'POST':
        # Add your login authentication logic here
        if authenticate_user(request.form['username'], request.form['password']):
            return redirect(url_for('dashboard'))  # Redirect to dashboard on successful login
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    global rfid_uid
    return render_template('dashboard.html', rfid_tag="RFID Tag UID:", rfid_value=rfid_uid)

# API endpoint to fetch RFID data
@app.route('/get_rfid_data', methods=['GET'])
def get_rfid_data():
    global prev_rfid_uid, rfid_uid
    if rfid_uid != prev_rfid_uid:
        prev_rfid_uid = rfid_uid
        return jsonify({"tag_uid": str(rfid_uid)})
    else:
        return jsonify({"tag_uid": None})

if __name__ == '__main__':
    start_rfid_thread()  # Start the RFID reading thread
    socketio.run(app, debug=True)  # Run the app with SocketIO support
