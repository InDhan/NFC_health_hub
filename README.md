NFC_health_hub/
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── patient_info.html
│   └── assets/
│       ├── css/
│       │   └── style.css
│       └── logic/
│           └── login.py
│
├── task.py
├── rfid.py
└── app.py


import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# Google Spreadsheet ID
spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'

# Function to fetch prescription data for a specific patient ID or UID
def fetch_prescriptions(id_value):
    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
        data = sheet.get_all_values()
        patient_data = {}
        
        # Get the header row to use as keys in the patient_data dictionary
        headers = data[0]
        
        for row in data[1:]:  # Start from index 1 to skip the header row
            if row[1] == id_value or row[14] == id_value:  # Assuming Patient ID is in column B (index 1) and UID is in column O (index 14)
                # Populate the patient_data dictionary with headers as keys and corresponding row data as values
                patient_data = {headers[i]: row[i] for i in range(len(headers))}
                break
        
        return patient_data
    except Exception as e:
        print(f"Error fetching patient data: {e}")
        return None





# Function to update prescription for a specific patient ID or UID
def update_prescription(id_value, new_prescription):
    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
        data = sheet.get_all_values()
        for i, row in enumerate(data):
            if row[1] == id_value or row[2] == id_value:  # Assuming Patient ID is in column B (index 1) and UID is in column C (index 2)
                sheet.update_cell(i + 1, 13, new_prescription)  # Update prescription in column M (index 13)
                return new_prescription
        return None  # If ID/UID not found
    except Exception as e:
        print(f"Error updating prescription: {e}")
        return None

def main():
    id_value = input("Enter Patient ID or UID: ").strip()
    if not id_value:
        print("Patient ID or UID cannot be empty.")
        return
    
    prescriptions = fetch_prescriptions(id_value)
    if prescriptions:
        print(f"Prescriptions for Patient ID or UID: {id_value}")
        for prescription in prescriptions:
            print("-", prescription)
        new_prescription = input("Enter new prescription: ").strip()
        if new_prescription:
            updated_prescription = update_prescription(id_value, new_prescription)
            if updated_prescription:
                print("Updated Prescription:", updated_prescription)
                print("Prescription updated successfully.")
            else:
                print("Failed to update prescription.")
        else:
            print("New prescription cannot be empty.")
    else:
        print("No prescriptions found for the Patient ID or UID.")

if __name__ == "__main__":
    main()
