from flask import Flask, render_template, redirect, url_for, request, flash
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_required
from pdf import pdf_summary
from url import grabText, gen_summary
from forms import RegistrationForm, LoginForm
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


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/pdf', methods=['GET', 'POST'])
def pdf():
    if request.method == 'POST':
        try:
            pdf_file = request.files['pdfFile']
            filename = pdf_file.filename
            summary = pdf_summary(pdf_file)
            new_summary = Summary(DBurl=filename, DBsummary=summary)
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
            new_summary = Summary(DBurl=url, DBsummary=summary)
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
# @login_required
def summaries():
    summaries = Summary.query.all()
    return render_template('summaries.html', summaries=summaries)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(
            user.password,
            form.password.data
        ):
            # Log in the user (You can use Flask-Login for this)
            return redirect(url_for('index'))  # Redirect to the user dashboard
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DBurl = db.Column(db.String(200), nullable=False)
    DBsummary = db.Column(db.Text, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


with app.app_context():
    db.create_all()


# Runs apps with configs
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'the key you generated'
    app.run(debug=True, host='0.0.0.0', port='8080')
