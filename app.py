#create Server
#create 3 routes
#create 3 templates
##create layout for template
#create 2 form
#create a database model

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_behind_proxy import FlaskBehindProxy
from helper import get_movies, get_a_movie
from form import ReviewForm
from helper import get_movie_details, get_movies
from flask_sqlalchemy import SQLAlchemy

#create Flask App
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## needed for Codio

#create sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db’
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Displays movie search engine and movie results
    """
    #get data from search
    movie_search = request.form.get('search')
    print(request.form)

    #return movie results
    # todo: handle if no movies found
    if movie_search and request.method == 'POST':
        
        #print(movie_search)
        movie_results = get_movies(movie_search)
        ##print(movie_results)
        return render_template('index.html', title="Movie Search", subtitle="Movie Search Results", results=movie_results)

    return render_template('index.html', title="Movie Search")


@app.route('/movie/<id>', method=['GET', 'POST'])
def select_movie(id):
    """ Displays movies Details and Reviews
        Allows users to create reviews
    """
    print(id)

    #get all movie details
    movie_details = get_a_movie(str(id))
    print(movie_details)

    #get wtform from form.py
    review_form = ReviewForm()

    #get all revies
    all_reviews = Review.query.filter_by(id=id).all()

    #Check form is validated. Add form data to database
    if review_form.validate_on_submit():
        #Get form data values
        review_rating = request.form.get('rating')
        review_details = request.form.get('review_details')
        #Add to database
        review = Review(id=id, review_details=review_details, rating=review_rating)
        db.session.add(review)
        db.session.commit()
        
        #Flash message to uset
        flash(f'Thank you for your feedback. Your review has been submitted!', 'success')
        #return to 
        return redirect(url_for('select_movie', id=id, reviews=all_reviews))
    return render_template('results.html', title="Select Movie", details=movie_details)

#Database Model Objects
class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(255), nullable=False)

#Creates tables
with app.app_context():
    db.create_all()
#Runs apps with configs
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'the key you generated'
    app.run(debug=True, host='0.0.0.0')