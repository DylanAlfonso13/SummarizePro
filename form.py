from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class ReviewForm(FlaskForm):
    id = IntegerField('movie_id', validators=[DataRequired(), Length(min=2, max=20)])
    review_text = TextAreaField('Reveiw', validators=[DataRequired(), Email()])
    rating = RadioField('Password', validators=[DataRequired()], choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5,'5 Stars')])

    submit = SubmitField('Sign Up')