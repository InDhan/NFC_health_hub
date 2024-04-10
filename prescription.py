import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'

def fetch_prescriptions(id_value):
    sheet = client.open_by_key(spreadsheet_id).sheet1
    data = sheet.get_all_values()
    prescriptions = []
    for row in data:
        if row[1] == id_value or row[2] == id_value:
            prescriptions.append(row[13])
            break
    return prescriptions

def update_prescription(id_value, new_prescription):
    sheet = client.open_by_key(spreadsheet_id).sheet1
    data = sheet.get_all_values()
    for i, row in enumerate(data):
        if row[1] == id_value or row[2] == id_value:
            sheet.update_cell(i + 1, 14, new_prescription)
            return new_prescription
    return None
