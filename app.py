from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import nfc
import hid
import sys

app = Flask(__name__)

# Google Sheets setup
try:
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open('Patient_Dataset').sheet1  # Replace 'YourGoogleSheetName' with your actual sheet name
except Exception as e:
    print("Error initializing Google Sheets:", e)
    sys.exit(1)

# HID Omnikey 5321 V2 device setup
try:
    vendor_id = 0x076b
    product_id = 0x5321
    device = hid.device()
    device.open(vendor_id, product_id)
except Exception as e:
    print("Error initializing HID device:", e)
    sys.exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read_nfc')
def read_nfc():
    if check_nfc_device_status():
        nfc_data = read_nfc_data()
        if nfc_data:
            # Store NFC data in Google Sheets
            store_data_in_google_sheets(nfc_data)
            return "NFC Data Read: {}".format(nfc_data)
    return "No NFC Card Detected"

def check_nfc_device_status():
    # Check if NFC device is connected and operational
    return device.is_plugged() and device.is_alive()

def read_nfc_data():
    with nfc.ContactlessFrontend('usb') as clf:
        print("Waiting for NFC tag...")
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        data = tag.identifier.hex()
        return data

def store_data_in_google_sheets(data):
    try:
        # Store data in Google Sheets
        row = [data]  # Assuming data is a single value, modify as needed
        sheet.append_row(row)
    except Exception as e:
        print("Error storing data in Google Sheets:", e)

if __name__ == '__main__':
    app.run(debug=True)
