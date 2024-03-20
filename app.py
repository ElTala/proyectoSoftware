from flask import Flask, render_template, Response, request, redirect, url_for
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests
import smtplib
import email.utils
from email.message import EmailMessage
from email.mime.text import MIMEText
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#Autenticación
def authenticate(username, password):
    with open('users.txt', 'r') as f:
        for line in f:
            user, passw = line.strip().split(',')
            if user == username and passw == password:
                return True
    return False

#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authenticate(username, password):
            return redirect(url_for('home'))
        else:
            error = "Login incorrecto"
    return render_template('login.html', error=error)
    
#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        with open('users.txt', 'r') as f:
            users = [line.strip().split(',')[0] for line in f]
            if username in users:
                error = "El nombre de usuario ya existe"
            else:
                with open('users.txt', 'a') as f:
                    f.write(f'{username},{password}\n')
                remitente = "aperez71@uabc.edu.mx"
                destinatario = request.form.get('email')
                mensaje = "Hola, le damos la bienvenida a nuestro sistema de VR"
                email = EmailMessage()
                email["From"] = remitente
                email["To"] = destinatario
                email["Subject"] = "Bienvenid@"
                email.set_content(mensaje)
                smtp = smtplib.SMTP_SSL("smtp.gmail.com")
                smtp.login(remitente)
                smtp.sendmail(remitente, destinatario, email.as_string())
                smtp.quit()
                return redirect(url_for('login'))
            


    return render_template('register.html', error=error)

#Contraseña olvidada
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        with open('users.txt', 'r') as f:
            users = [line.strip().split(',')[0] for line in f]
            if username not in users:
                error = "El nombre de usuario no existe"
                return render_template('forgot-password.html', error=error)
        return redirect(url_for('reset_password', username=username))
    return render_template('forgot-password.html')

#Contraseña recuperada
@app.route('/reset-password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        with open('users.txt', 'r') as f:
            users = [line.strip().split(',') for line in f]
        with open('users.txt', 'w') as f:
            for user in users:
                if user[0] == username:
                    f.write(f'{username},{new_password}\n')
                else:
                    f.write(f'{user[0]},{user[1]}\n')
        return redirect(url_for('login'))
    return render_template('reset-password.html', username=username)

#Cámara
@app.route('/camara',methods=['GET'])
def test():
    return render_template('camara.html')

@app.route('/submit',methods=['POST'])
def submit():
    image = request.args.get('image')
    print(type(image))
    return "Hola"
if __name__ == '__main__':
    app.run(debug=True)