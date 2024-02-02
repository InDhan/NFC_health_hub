from flask import Flask, render_template
import hid
import sqlite3

app = Flask(__name__)

# Database setup
conn = sqlite3.connect('health_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS health_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, data TEXT)''')
conn.commit()

# HID Omnikey device setup
vendor_id = 0x076b
product_id = 0x5321
device = hid.device()
device.open(vendor_id, product_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read_nfc')
def read_nfc():
    nfc_data = read_nfc_data()
    if nfc_data:
        # Store NFC data in database
        store_data_in_db(nfc_data)
        return "NFC Data Read: {}".format(nfc_data)
    else:
        return "No NFC Card Detected"

def read_nfc_data():
    # Implement code to read NFC data from the HID Omnikey device
    # Example: 
    # data = device.read(16)
    # return data
    pass

def store_data_in_db(data):
    # Store data in SQLite database
    c.execute("INSERT INTO health_data (user_id, data) VALUES (?, ?)", ("user_id_here", data))
    conn.commit()

if __name__ == '__main__':
    app.run(debug=True)
