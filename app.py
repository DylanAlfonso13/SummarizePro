from flask import Flask, render_template, redirect, url_for, request, flash
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
from pdf import pdf_summary



#create Flask App
app = Flask(__name__)
#create sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Note: make sure later we have summary add to DB
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
        except Exception:
            error_message = "Try inputting a different file, it's likely the wrong type"
            return render_template('pdf_page.html', error_message=error_message)
        # value = request.form.get('fileupload')
        # print(value)
        # return value
        # pdf_to_text(value)

    return render_template('pdf_page.html')

# @app.route('/convert', methods=['POST'])
# def convert():
    # pdf_file = request.files['pdfFile']
    # return pdf_summary(pdf_file)

@app.route('/article', methods=['GET','POST'])
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
            return render_template('article_page.html', error_message=error_message)
    return render_template('article_page.html')

@app.route('/summaries')
def summaries():
    summaries = Summary.query.all()
    return render_template('summaries.html', summaries=summaries)

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

class Summary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    DBurl = db.Column(db.String(200), nullable=False)
    DBsummary = db.Column(db.Text, nullable=False)

#Creates tables
with app.app_context():
    db.create_all()

#Runs apps with configs
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'the key you generated'
    app.run(debug=True, host='0.0.0.0', port='8080')