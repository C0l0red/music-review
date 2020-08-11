from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired

class SongForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    year = IntegerField("Year", [DataRequired()])
    album = StringField("Album")
    artist = StringField("Artist", [DataRequired()])
    genre = StringField("Genre", [DataRequired()])
    features = StringField("Features")
    track_number = IntegerField("Track Number")
    disc_number = IntegerField("Disc Number")

class AlbumForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    artist = StringField("Artist", [DataRequired()])
    year = IntegerField("Year", [DataRequired()])
    genre = StringField("Genre", [DataRequired()])

class ArtistForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    genres = StringField("Genres", [DataRequired()])

class GenreForm(FlaskForm):
    name = StringField("Name", [DataRequired()])

