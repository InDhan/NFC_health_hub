import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request, render_template

# Initialize Flask app
app = Flask(__name__)

# Google Sheets API credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
client = gspread.authorize(creds)

# Google Spreadsheet ID
spreadsheet_id = '1FCoRib-XsrcSycRvHtEl8xYAV4KsbTXcr5ZkbkuabsY'

# Function to fetch prescription data for a specific patient ID
def fetch_prescriptions(patient_id):
    sheet = client.open_by_key(spreadsheet_id).sheet1
    data = sheet.get_all_records()
    prescriptions = [row['Prescription'] for row in data if row['Patient ID'] == patient_id]
    return prescriptions

# Routes
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/prescription', methods=['GET', 'POST'])
def prescription():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        prescriptions = fetch_prescriptions(patient_id)
        return render_template('prescription.html', prescriptions=prescriptions, patient_id=patient_id)
    else:
        return render_template('prescription.html')

if __name__ == '__main__':
    app.run(debug=True)
