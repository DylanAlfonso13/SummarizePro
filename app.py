from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager, login_required, current_user, login_user, logout_user)
from forms import RegistrationForm, LoginForm
from pdf import grab_pdf, pdf_summary
from url import grabText, gen_summary
from video import get_transcript, summarize_transcript, get_video_title
import git
from dotenv import load_dotenv
import openai
import os


# create Flask App
app = Flask(__name__)
# Load in API Key
load_dotenv()
openai.api_key = os.environ.get('OPENAI_API_KEY')
# create sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    if request.method == "POST":
        link = request.form['url']
        try:
            text = get_transcript(link)
            title = get_video_title(link)
            summary = summarize_transcript(text)
            if (current_user.is_authenticated):
                new_summary = Summary(DBurl=title,
                                      DBsummary=summary,
                                      user_id=current_user.id
                                      )
                db.session.add(new_summary)
                db.session.commit()
            return render_template('video_page.html', summary=summary)
        except Exception as e:
            error_message = str(e)
            return render_template(
                'video_page.html',
                error_message=error_message
            )
    return render_template('video_page.html')


@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
    if request.method == 'POST':
        try:
            pdf_file = request.files['pdfFile']
            filename = pdf_file.filename
            text = grab_pdf(pdf_file)
            summary = pdf_summary(text)
            if (current_user.is_authenticated):
                new_summary = Summary(
                    DBurl=filename, DBsummary=summary, user_id=current_user.id)
                db.session.add(new_summary)
                db.session.commit()
            return render_template('pdf_page.html', summary=summary)
        except Exception as e:
            error_message = str(e)
            return render_template(
                'pdf_page.html',
                error_message=error_message
            )

    return render_template('pdf_page.html')


@app.route('/article', methods=['GET', 'POST'])
def article():
    if request.method == "POST":
        url = request.form['url']
        try:
            text = grabText(url)
            summary = gen_summary(text)
            if (current_user.is_authenticated):
                new_summary = Summary(
                    DBurl=url, DBsummary=summary, user_id=current_user.id)
                db.session.add(new_summary)
                db.session.commit()
            return render_template('article_page.html', summary=summary)
        except Exception as e:
            error_message = str(e)
            return render_template(
                'article_page.html',
                error_message=error_message
            )
    return render_template('article_page.html')


@app.route('/summaries')
@login_required
def summaries():
    print(current_user)
    summaries = Summary.query.filter_by(user_id=current_user.id).all()
    return render_template('summaries.html', summaries=summaries)


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user:
        response = {'message': 'Username already exists'}
        return jsonify(response), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    response = {'message': 'Registration successful'}
    return jsonify(response)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        response = {'message': 'Login successful'}
        return jsonify(response)

    response = {'message': 'Invalid username or password'}
    return jsonify(response), 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unAuthorized():
    return "Unauthorized. Please log in to access this page.", 401


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DBurl = db.Column(db.String(200), nullable=False)
    DBsummary = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)


with app.app_context():
    db.create_all()


# Runs apps with configs
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'the key you generated'
    app.run(debug=True, host='0.0.0.0', port='8080')
