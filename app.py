from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import errno
import os
import nfc

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds',
      'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
#client = gspread.authorize(credentials)
#sheet = client.open('YourGoogleSheetName').sheet1  # Replace 'YourGoogleSheetName' with your actual sheet name

@app.route('/')
def index():
    return render_template('index.html')

def fetch_patient_data(credentials_file, spreadsheet_id, patient_id):
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

@app.route('/read_nfc')
def read_nfc():
    nfc_data = read_nfc_data()
    if nfc_data:
        # Store NFC data in Google Sheets
        store_data_in_google_sheets(nfc_data)
        return "NFC Data Read: {}".format(nfc_data)
    else:
        return "No NFC Card Detected"

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
    

def store_data_in_google_sheets(data):
    # Store data in Google Sheets
     row = [data]  # Assuming data is a single value, modify as needed
     #sheet.append_row(row)

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
