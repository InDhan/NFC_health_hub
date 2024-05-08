import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify
import serial.tools.list_ports
import time
from flask_socketio import SocketIO
from templates.assets.logic.login import authenticate_user  # Import authenticate_user if needed
from prescription import fetch_prescriptions, update_prescription
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize Flask app and SocketIO
app = Flask(__name__, static_folder='templates/', static_url_path='/')
socketio = SocketIO(app)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json", scope)
client = gspread.authorize(creds)

# Replace "YOUR_GOOGLE_SHEET_ID" with the actual ID of your Google Sheet
sheet = client.open_by_key("1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY").sheet1

# Global variables
ser = None  # Serial port variable
nfc_uid = None  # NFC UID variable
prev_nfc_uid = None  # Previous NFC UID variable

# Function to find and open the serial port
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

# Function to read NFC data from the Arduino
def read_nfc():
    global ser, nfc_uid
    while True:
        if ser is not None and ser.is_open:
            # Read data from the Arduino
            data = ser.readline().strip().decode('utf-8')
            print("Raw data:", data)  # Debug print to see the raw data received
            if data.startswith('Patient NFC: Card UID:'):
                nfc_uid = data.split(': ')[-1].strip()  # Extract the NFC UID from the data
                print("Patient NFC:", nfc_uid)  # Debug print NFC UID to the terminal
                # Emit the NFC UID via SocketIO
                socketio.emit('nfc_update', {'tag_uid': nfc_uid})
        else:
            print("Serial port is not open.")  # Debug print if serial port is not open
        time.sleep(0.1)  # Adjust delay as needed


# SocketIO event handler for NFC data
@socketio.on('nfc_data')
def handle_nfc_data(data):
    global nfc_uid
    nfc_uid = data['tag_uid']  # Assuming 'tag_uid' is the key for NFC UID in the data
    socketio.emit('nfc_update', {'tag_uid': nfc_uid})

# Function to start the NFC reading thread
def start_nfc_thread():
    global ser
    ser = find_and_open_serial_port()
    if ser is None:
        print("Error: No available serial port found!")
    else:
        print("Serial port opened successfully.")
        # Start a new thread to run the NFC reader function
        nfc_thread = threading.Thread(target=read_nfc)
        nfc_thread.daemon = True
        nfc_thread.start()
        print("NFC thread started.")  # Debug print

# Routes

# Index route
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if authenticate_user(request.form['username'], request.form['password']):
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")
    else:
        return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    global nfc_uid
    return render_template('dashboard.html', nfc_tag="NFC Tag UID:", nfc_value=nfc_uid)

def nfc_data():
    global nfc_uid
    return render_template('nfc_data.html', nfc_uid=nfc_uid)
    
# API endpoint to fetch NFC data
@app.route('/get_nfc_data', methods=['GET'])
def get_nfc_data():
    global prev_nfc_uid, nfc_uid
    if nfc_uid != prev_nfc_uid:
        prev_nfc_uid = nfc_uid
        return jsonify({"tag_uid": str(nfc_uid)})
    else:
        return jsonify({"tag_uid": None})

# Route to display patient information and update prescription
@app.route('/patient_info', methods=['GET', 'POST'])
def patient_info():
    if request.method == 'POST':
        # Check if 'patientID' is in the form data
        if 'patientID' not in request.form:
            return jsonify({"error": "Patient ID not provided."}), 400

        # Get patient ID from the form data
        patient_id = request.form['patientID']

        # Fetch prescriptions for the patient from Google Sheets
        prescriptions = fetch_prescriptions(patient_id)

        # Render the patient_info.html template with prescriptions data
        return render_template('patient_info.html', patientID=patient_id, prescriptions=prescriptions)
    else:
        # Render the patient_info.html template for GET requests
        return render_template('patient_info.html', patientID=None, prescriptions=None)

# Route to update patient prescription
@app.route('/update_prescription', methods=['POST'])
def update_prescription():
    data = request.get_json()
    patientID = data.get('patientID')
    new_prescription = data.get('new_prescription')

    # Update Google Sheet logic
    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
        data = sheet.get_all_values()
        headers = data[0]  # Assuming the first row contains headers
        for row in data:
            if row[2] == patientID or row[14] == patientID:  # Assuming Patient ID is in column B (index 1) and UID is in column C (index 2)
                row[13] = new_prescription  # Assuming "last_prescription" is at index 13
                sheet.update_row(row, index=row.row_number)  # Update the row in the Google Sheet
                return jsonify({'success': True}), 200
        return jsonify({'success': False, 'error': 'Patient ID not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def get_row_index(sheet, patientID):
    values_list = sheet.col_values(1)  # Assuming patient IDs are in column 1
    if patientID in values_list:
        return values_list.index(patientID) + 1  # Adding 1 as Google Sheets index starts from 1
    else:
        return None

                    
if __name__ == '__main__':
    start_nfc_thread()
    socketio.run(app, debug=True)
