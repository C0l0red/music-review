"""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length

class SongReviewForm(FlaskForm):
    song = StringField("Song")
    review = TextAreaField("Review", [Length(min=30)])
    rating = IntegerField("Rating")
    user = StringField("User")

class AlbumReviewForm(FlaskForm):
    album = StringField("Album")
    tracks = TextAreaField("Tracks")
    review = TextAreaField("Review", [Length(min=30)])
    rating = IntegerField("Rating")
    user = StringField("User")

class ArtistReviewForm(FlaskForm):
    review = TextAreaField("Review", [Length(min=30)])
    rating = IntegerField("Rating")
"""