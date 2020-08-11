from . import db
from flask import *
from uuid import uuid4
import jwt

make_uuid = (lambda: uuid4().hex.upper()[0:15])

features = db.Table("features", 
    db.Column("song_id", db.Integer,db.ForeignKey('song.id'), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id"), primary_key=True)
    )

artist_genre = db.Table("artist_genre", 
    db.Column("artist_id", db.Integer,db.ForeignKey('artist.id'), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
    )

"""
album_genre = db.Table("album_genre", 
    db.Column("album_id", db.Integer,db.ForeignKey('album.id'), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
    )
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return self.username

    def set_password(self, password):
        hash_ = generate_password_hash(password, method="sha256")
        self.password = hash_

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_token(self):
        token = jwt.encode({"username":self.username, "exp": datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET_KEY"])
        return token.decode("UTF-8")

    @staticmethod
    def validate_token(token):
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return None
        
        return current_user  

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    favorite_song_reviews = db.relationship("SongReview", secondary="favorited_song_reviews", backref="favorited_users", lazy=True)
    favorite_album_reviews = db.relationship("AlbumReview", secondary="favorited_album_reviews", backref="favorited_albums", lazy=True)
    favorite_artist_reviews = db.relationship("ArtistReview", secondary="favorited_artist_reviews", backref="favorited_artists", lazy=True)

    song_reviews = db.relationship("SongReview", backref="profile", lazy=True)
    album_reviews = db.relationship("AlbumReview", backref="profile", lazy=True)
    artist_reviews = db.relationship("ArtistReview", backref="profile", lazy=True)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer)
    
    reviews = db.relationship("Review", backref="artist", lazy=True)
    features_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __repr__(self):
        return self.name 


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    
    year = db.Column(db.Integer)
    tracks = db.relationship("Song", backref="album", lazy=False)
    reviews = db.relationship("Review", backref="artist", lazy=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __repr__(self):
        return self.name


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(50), nullable=False)

    reviews = db.relationship("Review", backref="artist", lazy=True)
    songs = db.relationship("Song", backref="artist", lazy=True)
    features = db.relationship("Song", secondary='features', backref="featuring", lazy=True)
    albums = db.relationship("Album", backref="artist", lazy=True)
    genres = db.relationship("Genre", secondary="artist_genre", backref="artists", lazy=True)

    def __repr__(self):
        return self.name


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    albums = db.relationship("Album", backref="genre", lazy=True)

    def __repr__(self):
        return self.name


class SongReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    song_id = db.Column(db.String(200))
    song_offline_id = db.Column(db.Integer, db.ForeignKey("song.id"))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False)


class AlbumReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    album_id = db.Column(db.String(200))
    album_offline_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False)

class ArtistReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.String(200))
    artist_offline_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False)

    

