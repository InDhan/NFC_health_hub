from flask import Flask, render_template, request
from task import read_rfid_data,read_rfid,fetch_patient_data


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/read_rfid')


@app.route('/fetch_data_manually', methods=['POST'])

def run():
    pass

if __name__ == '__main__':
    # Read patient ID from RFID card
    patient_id_bytes = read_rfid_data()
    if patient_id_bytes is None:
        exit()  # Exit the program if RFID reader is not connected
    patient_id = patient_id_bytes.decode('utf-8')

    print("Patient ID from RFID card:", patient_id)

    # Fetch patient data using the retrieved patient ID
    patient_data = fetch_patient_data(patient_id)

    if patient_data:
        print("Patient Data:")
        for key, value in patient_data.items():
            print(f"{key}: {value}")
    else:
        print("Patient ID not found or error occurred.")

    app.run(debug=True)
