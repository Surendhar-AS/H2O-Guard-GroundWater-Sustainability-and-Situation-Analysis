from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_mail import Mail, Message
import random
import string
from . import app
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'surendharas1402@gmail.com'
app.config['MAIL_PASSWORD'] = 'oazt xxxc vnyp rgni'  # you have to give your password of gmail account
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Function to generate OTP
def generate_otp():
    numbers = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    return numbers + letters

# Function to send OTP via email
def send_email_otp(email, otp):
    msg = Message('OTP for Password Reset', sender='surendharas1402@gmail.com', recipients=[email])
    msg.body = f'Your OTP is: {otp}'
    mail.send(msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        otp = generate_otp()  # Generate OTP for each login attempt
        send_email_otp(email, otp)
        flash('OTP has been sent to your email.')
        # Store email and OTP in session
        session['email'] = email
        session['otp'] = otp
        return render_template('enter_otp.html')
    return render_template('login.html')

@app.route('/validate-otp', methods=['POST'])
def validate_otp():
    if 'email' not in session:
        flash('Please log in to validate OTP.')
        return redirect(url_for('login'))  # Redirect to the login route

    entered_otp = request.form['otp']
    email = session.get('email')  # Retrieve email from session
    otp = session.get('otp')  # Retrieve OTP from session

    if entered_otp == otp:
        flash('OTP is correct. You are now logged in.')
        return redirect('/home')
    else:
        flash('Wrong OTP entered. Please try again.')
        return redirect('/login')


