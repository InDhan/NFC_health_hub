from flask import Flask, render_template
import nfcpy
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(credentials)
sheet = client.open('YourGoogleSheetName').sheet1  # Replace 'YourGoogleSheetName' with your actual sheet name

@app.route('/')
def index():
    return render_template('index.html')

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
    # Implement code to read NFC data using nfcpy
    # Example:
    # with nfc.ContactlessFrontend('usb') as clf:
    #     tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    #     data = tag.identifier.hex()
    #     return data
    pass

def store_data_in_google_sheets(data):
    # Store data in Google Sheets
    row = [data]  # Assuming data is a single value, modify as needed
    sheet.append_row(row)

if __name__ == '__main__':
    app.run(debug=True)
