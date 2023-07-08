from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class ReviewForm(FlaskForm):
    review_text = TextAreaField('Reveiw', validators=[DataRequired()])
    rating = RadioField('Rating', validators=[DataRequired()], choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5,'5 Stars')])
    submit = SubmitField('Sign Up')