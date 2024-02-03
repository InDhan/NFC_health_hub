from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import nfc

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('Patient_Dataset').sheet1  # Replace 'Patient_Dataset' with your actual sheet name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read_nfc')
def read_nfc():
    nfc_data = read_nfc_data()
    if nfc_data:
        patient_data = fetch_patient_data(nfc_data)
        if patient_data:
            return render_template('patient_info.html', data=patient_data)
    return "No NFC Data Found HID PRoblem "

@app.route('/fetch_data_manually', methods=['POST'])
def fetch_data_manually():
    patient_id = request.form['patient_id']
    if patient_id:
        patient_data = fetch_patient_data(patient_id)
        if patient_data:
            return render_template('patient_info.html', data=patient_data)
    return "No Data Found for Provided ID"

def read_nfc_data():
    print("Waiting for NFC card...")
    try:
        with nfc.ContactlessFrontend('usb') as clf:
            target = clf.sense()
            if target is not None:
                return bytes(target.uid)
            else:
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_patient_data(identifier):
    # Fetch patient data based on NFC tag or manually entered ID
    try:
        row = sheet.find(identifier).row
        patient_data = sheet.row_values(row)
        return patient_data
    except gspread.exceptions.CellNotFound:
        return None

if __name__ == '__main__':
    app.run(debug=True)
