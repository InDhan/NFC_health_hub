from flask import Flask, render_template, request, redirect, url_for
from templates.assets.logic.login import authenticate_user

app = Flask(__name__, static_folder='templates/', static_url_path='/')

@app.route('/')
def index():
    return render_template('index.html')

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
    
# @app.route('/add_patient', methods=['GET', 'POST'])
# def add_patient():
#     if request.method == 'POST':
#         return render_template('add_patient.html')
#     else:
#         return redirect(url_for('dashboard'))
    
@app.route('/add_patient')
def add_patient():
    return render_template('add_patient.html')

if __name__ == '__main__':
    app.run(debug=True)
