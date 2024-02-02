from flask import Flask, render_template, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import nfc
import os
import errno
import hid

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('Patient_Dataset').sheet1  # Replace 'Patient_Dataset' with your actual sheet name

# HID Omnikey 5321 V2 device setup
vendor_id = 0x076b
product_id = 0x5321
device = hid.device()
device.open(vendor_id, product_id)

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
    return "No NFC Data Found"

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
            while True:
                target = clf.sense()
                if target is not None:
                    return bytes(target.uid)
    except OSError as e:
        if e.errno == errno.ENODEV:
            print("NFC reader is not connected.")
        else:
            print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def fetch_patient_data(identifier):
    # Fetch patient data based on NFC tag or manually entered ID
    try:
        # Authenticate with Google Sheets API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        gc = gspread.authorize(credentials)

        # Open the Google Spreadsheet
        sheet = gc.open_by_key(spreadsheet_id).get_worksheet(0)

        # Find row index of the patient ID
        row_index = None
        for index, row in enumerate(sheet.get_all_values()):
            if row and row[0] == patient_id:
                row_index = index + 1
                break

        # If patient ID found, return corresponding data as dictionary
        if row_index:
            headers = sheet.row_values(1)
            patient_values = sheet.row_values(row_index)
            patient_data = dict(zip(headers, patient_values))
            return patient_data
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    credentials_file = 'keys.json'  
    spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'  
     # Read patient ID from NFC card
    patient_id_bytes = read_nfc_data()
    if patient_id_bytes is None:
        exit()  # Exit the program if NFC reader is not connected
    patient_id = patient_id_bytes.decode('utf-8')

    print("Patient ID from NFC card:", patient_id)

    # Fetch patient data using the retrieved patient ID
    patient_data = fetch_patient_data(credentials_file, spreadsheet_id, patient_id)
    
    if patient_data:
        print("Patient Data:")
        for key, value in patient_data.items():
            print(f"{key}: {value}")
    else:
        print("Patient ID not found or error occurred.")
    app.run(debug=True)
