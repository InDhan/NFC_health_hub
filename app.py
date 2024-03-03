from flask import Flask, render_template, request, redirect, url_for
from templates.assets.logic.login import authenticate_user
from fetch_data import fetch_patient_data
from rfid import read_rfid,write_rfid

app = Flask(__name__, static_folder='templates/assets', static_url_path='/assets')

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST' and authenticate_user(request.form['username'], request.form['password']):
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if authenticate_user(request.form['username'], request.form['password']):
           return render_template('dashboard.html')
        else:
            return render_template('index.html', error="Invalid credentials. Please try again.")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    patient_id = read_rfid()
    

