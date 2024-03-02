from flask import render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyrfid   
import nfc 
# Import the appropriate RFID library
import os
import errno
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
gc = gspread.authorize(credentials)
sheet = gc.open_by_key('1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY').get_worksheet(0)

def fetch_patient_data(patient_id):
    try:
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

def read_rfid():
    rfid_data = read_rfid_data()
    if rfid_data:
        patient_id = rfid_data.decode('utf-8')  # Assuming patient ID is stored as a string
        patient_data = fetch_patient_data(patient_id)
        if patient_data:
            return render_template('patient_info.html', data=patient_data)
    return "No RFID Data Found"


def read_rfid_data():
    print("Waiting for RFID card...")
    try:
        with pyrfid.RFIDReader(port='/dev/ttyUSB0', baudrate=9600) as reader:  # Initialize RFID reader
            tag_id = reader.read_tag()  # Read RFID tag
            return tag_id
    except Exception as e:
        print(f"Error: {e}")
    return None

def store_data_in_google_sheets(data):
    # Store data in Google Sheets
    row = [data]  # Assuming data is a single value, modify as needed
    # sheet.append_row(row)

def check_attr():
    attribute = dir(pyrfid)
    print(attribute)

