from flask import Flask, render_template, redirect, url_for, request, flash
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import PyPDF2
import json
from pdf import pdf_to_json


#create Flask App
app = Flask(__name__)


#create sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
    print(request.form)
    if request.method == 'POST':
        value = request.form.get('fileupload')
        return value
        # pdf_to_text(value)
    return render_template('pdf_page.html')

@app.route('/convert', methods=['POST'])
def convert():
    pdf_file = request.files['pdfFile']
    return pdf_to_json(pdf_file)

@app.route('/article', methods=['GET','POST'])
def article():
    return render_template('article_page.html')

#Database Model Objects
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    with app.app_context():
        db.create_all()

#Creates tables
with app.app_context():
    db.create_all()

#Runs apps with configs
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'the key you generated'
    app.run(debug=True, host='0.0.0.0', port='8080')