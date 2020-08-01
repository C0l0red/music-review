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

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(50), nullable=False)
    songs = db.relationship("Song", backref="artist", lazy=True)
    features = db.relationship("Song", secondary='features', backref="featuring", lazy=True)
    albums = db.relationship("Album", backref="artist", lazy=True)
    genres = db.relationship("Genre", secondary="artist_genre", backref="artists", lazy=True)

    def __repr__(self):
        return self.name

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer)
    tracks = db.relationship("Song", backref="album", lazy=False)

    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __repr__(self):
        return self.name

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer)
    
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __repr__(self):
        return self.name

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    albums = db.relationship("Album", backref="genre", lazy=True)

    def __repr__(self):
        return self.name

