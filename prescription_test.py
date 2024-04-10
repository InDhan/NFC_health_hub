import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# Google Spreadsheet ID
spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'

# Function to fetch prescription data for a specific patient ID or UID from columns B (index 1) and C (index 2)
def fetch_prescriptions(id_value):
    sheet = client.open_by_key(spreadsheet_id).sheet1
    data = sheet.get_all_values()
    prescriptions = []
    for row in data:
        if row[1] == id_value:  # Assuming Patient ID is in column B (index 1)
            prescriptions.append(row[13])  # Assuming prescriptions are in column L (index 11)
            break
        elif row[2] == id_value:  # Assuming UID is in column C (index 2)
            prescriptions.append(row[13])  # Assuming prescriptions are in column L (index 11)
            break
    return prescriptions

# Function to update prescription for a specific patient ID or UID in column 12
def update_prescription(id_value, new_prescription):
    sheet = client.open_by_key(spreadsheet_id).sheet1
    data = sheet.get_all_values()
    updated_prescription = None
    for i, row in enumerate(data):
        if row[1] == id_value or row[2] == id_value:  # Assuming Patient ID is in column B (index 1) and UID is in column C (index 2)
            sheet.update_cell(i + 1, 14, new_prescription)  # Update prescription in column L (index 12)
            updated_prescription = new_prescription
            break
    return updated_prescription

def main():
    id_value = input("Enter Patient ID or UID: ")
    prescriptions = fetch_prescriptions(id_value)
    if prescriptions:
        print("Prescriptions for Patient ID or UID:", id_value)
        for prescription in prescriptions:
            print("-", prescription)
        new_prescription = input("Enter new prescription: ")
        updated_prescription = update_prescription(id_value, new_prescription)
        if updated_prescription:
            print("Updated Prescription:", updated_prescription)
            print("Prescription updated successfully.")
        else:
            print("Failed to update prescription.")
    else:
        print("No prescriptions found for the Patient ID or UID.")

if __name__ == "__main__":
    main()
