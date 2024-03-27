import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from rfid import read_rfid

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

if __name__ == "__main__":
    credentials_file = 'keys.json'
    spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'

    patient_id = input("Enter patient ID manually: ")

    #patient_id = read_data()
    print(f'The patient id you provided is {patient_id}')

    time.sleep(0)

    if patient_id:
        print("Patient ID:", patient_id)
        # Fetch patient data using the retrieved patient ID
        patient_data = fetch_patient_data(credentials_file, spreadsheet_id, patient_id)
        if patient_data:
            print("Patient Data:")
            for key, value in patient_data.items():
                print(f"{key}: {value}")
        else:
            print("Patient ID not found or error occurred.")
    else:
        print("No patient ID detected.")
