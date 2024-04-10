import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import threading
from rfid import rfid_uid

def fetch_patient_data(credentials_file, spreadsheet_id, patient_id):
    try:
        # Authenticate with Google Sheets API
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        gc = gspread.authorize(credentials)

        # Open the Google Spreadsheet
        sheet = gc.open_by_key(spreadsheet_id).sheet1

        # Find the cell containing the patient ID
        cell = sheet.find(patient_id)

        if cell:
            # Get the row and column of the cell
            row_index = cell.row
            column_index = cell.col

            # Get the headers (first row)
            headers = sheet.row_values(1)

            # Get the patient data from the row
            patient_values = sheet.row_values(row_index)
            patient_data = dict(zip(headers, patient_values))
            return patient_data
        else:
            print(f"Patient ID {patient_id} not found.")
            return None

    except gspread.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Patient ID {patient_id} not found.")
        else:
            print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def read_rfid_and_fetch_data():
    global rfid_uid
    try:
        while True:
            if rfid_uid:
                print("RFID Tag UID:", rfid_uid)
                # Fetch patient data using the retrieved RFID UID
                patient_data = fetch_patient_data(credentials_file, spreadsheet_id, rfid_uid)
                if patient_data:
                    print("Patient Data:")
                    for key, value in patient_data.items():
                        print(f"{key}: {value}")
                else:
                    print("Patient ID not found or error occurred.")
                rfid_uid = None  # Reset RFID UID after processing
            time.sleep(1)  # Delay for readability
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    credentials_file = 'keys.json'
    spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'

    # Start a new thread to read RFID and fetch data simultaneously
    rfid_thread = threading.Thread(target=read_rfid_and_fetch_data)
    rfid_thread.daemon = True
    rfid_thread.start()

    try:
        while True:
            time.sleep(1)  # Main thread sleeps while other threads run
    except KeyboardInterrupt:
        print("\nExiting...")
