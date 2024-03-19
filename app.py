from flask import Flask, render_template, Response, request, redirect, url_for
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
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
