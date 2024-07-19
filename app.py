from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load model
model = joblib.load('heart_disease_model.pkl')

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Simple check
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html')
    else:
        return redirect(url_for('login'))

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Extract features from form
            features = [float(request.form[feature]) for feature in [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]]
            logging.debug(f'Features: {features}')
            
            # Make prediction
            prediction = model.predict([features])[0]
            logging.debug(f'Prediction: {prediction}')
            
            # Determine result
            result = "Terdeteksi penyakit jantung" if prediction == 1 else "Terdeteksi bukan penyakit jantung"
            logging.debug(f'Result: {result}')
            
            return render_template('result.html', result=result)
        except Exception as e:
            logging.error(f'Error in diagnosis: {e}')
            return 'Error in diagnosis'
    
    return render_template('diagnose.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
