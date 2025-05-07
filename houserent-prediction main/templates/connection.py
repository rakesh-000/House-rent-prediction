from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/sabarish'
db = SQLAlchemy(app)

class LoginPage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

@app.route('/connection', methods=['POST'])
def connection():
    username = request.form['username']
    password = request.form['password']

    login_page = LoginPage(username=username, password=password)
    db.session.add(login_page)
    db.session.commit()

    return "Registration Successful"