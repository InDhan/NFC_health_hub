import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# Google Spreadsheet ID
spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'


def fetch_prescriptions(id_value):
    try:
        sheet = client.open_by_key(spreadsheet_id).sheet1
        data = sheet.get_all_values()
        prescriptions = []
        headers = data[0]  # Assuming the first row contains headers
        for row in data:
            if row[2] == id_value or row[14] == id_value:  # Assuming Patient ID is in column B (index 1) and UID is in column C (index 2)
                patient_data = dict(zip(headers[1:14], row[1:14]))  # Exclude the UID from headers and row
                patient_data['patient_name'] = row[2]
                patient_data['doc_name'] = row[3]
                patient_data['last_date_visit'] = row[4]
                patient_data['age'] = row[5]
                patient_data['blood_group'] = row[6]
                patient_data['gender'] = row[7]
                patient_data['glucose'] = row[8]
                patient_data['bp'] = row[9]
                patient_data['insulin'] = row[10]
                patient_data['bmi'] = row[11]
                patient_data['diagnosed_disease'] = row[12]
                patient_data['last_prescription'] = row[13]
                prescriptions.append(patient_data)
        return prescriptions
    except Exception as e:
        print(f"Error fetching prescriptions: {e}")
        return []



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