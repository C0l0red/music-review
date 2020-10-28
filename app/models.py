from . import db, login_manager
from flask import *
from uuid import uuid4
import jwt
#from flask_restplus import fields#, mask
#from flask_restplus.mask import Mask
from sqlalchemy.ext.declarative import declared_attr
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

make_uuid = (lambda: uuid4().hex.upper()[0:15])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

artist_features = db.Table("features", 
    db.Column("song_id", db.Integer,db.ForeignKey('song.id'), primary_key=True),
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.id"), primary_key=True)
)

artist_genre = db.Table("artist_genre", 
    db.Column("artist_id", db.Integer,db.ForeignKey('artist.id'), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
)

favorited_song_reviews = db.Table("favorited_song_reviews", 
    db.Column("song_review_id", db.Integer, db.ForeignKey("song_review.id"), primary_key=True),
    db.Column("profile", db.Integer, db.ForeignKey("profile.id"), primary_key=True)
)

favorited_album_reviews = db.Table("favorited_album_reviews", 
    db.Column("album_review_id", db.Integer, db.ForeignKey("album_review.id"), primary_key=True),
    db.Column("profile", db.Integer, db.ForeignKey("profile.id"), primary_key=True)
)

favorited_artist_reviews = db.Table("favorited_artist_reviews", 
    db.Column("artist_review_id", db.Integer, db.ForeignKey("artist_review.id"), primary_key=True),
    db.Column("profile", db.Integer, db.ForeignKey("profile.id"), primary_key=True)
)


# User Blueprint models

## User Model for the Users.
## It consists of an id, public id, username, email, password

class User(db.Model, UserMixin):
    """
    param str username: Username of User
    param str email: Email of User
    param str password: Password of User
    """
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80), nullable=False)#passwords are saved are encrypted at object creation
    
    profile = db.relationship("Profile", backref="user", uselist=False, lazy=False)

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        kwargs = {key:val for key,val in locals().items() if val is not None and key not in ["self", "__class__"]}

        if password:
            if len(password)<5:
                return {"error": "Password too short"}

        try:
            super(User, self).__init__(**kwargs)
            if password:
                self.set_password(password)
            else:
                self.set_password("password")
            
        except:
            return None

    """
    This method makes use of a dunder to change the represenation of the User Model to display the username as opposed 
    to the memory location
    """
    def __repr__(self):
        return self.username

    """
    This method sets the User's password to an encrypted version of the entered "password" string
    """
    def set_password(self, password):
        hash_ = generate_password_hash(password, method="sha256")
        self.password = hash_

    """
    This method verifies the User's password by comparing the "password" argument with the User object's password
    It returns a boolean
    """
    def check_password(self, password):
        return check_password_hash(self.password, password)

    """
    This method creates a token with JWT.
    The payload is the User object's username, it expires in 30 minutes.
    The return value is the token in UTF-8 encoding. 
    """
    def create_token(self):
        token = jwt.encode({"username":self.username, "exp": datetime.utcnow() + timedelta(minutes=30)}, app.config["SECRET_KEY"])
        return token.decode("UTF-8")

    """
    This method validates a token.
    It taken a "token" argument and tries to decode it using JWT.
    If the token is valid, it returns the User object's username,  otherwise it returns None.
    """
    @staticmethod
    def validate_token(token):
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return None
        
        return current_user  

#Profile Model for the User

##It consists of id, user id, favorite song, album and artist reviews

class Profile(db.Model):
    """
    param str user_id: User ID of Profile 
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    public_id = db.Column(db.String(15), default=make_uuid)

    song_reviews = db.relationship("SongReview", backref="profile", lazy="dynamic")
    album_reviews = db.relationship("AlbumReview", backref="profile", lazy="dynamic")
    artist_reviews = db.relationship("ArtistReview", backref="profile", lazy="dynamic")

    favorited_song_reviews = db.relationship("SongReview", secondary="favorited_song_reviews", 
                                            backref="users_favorited", lazy="dynamic")
    favorited_album_reviews = db.relationship("AlbumReview", secondary="favorited_album_reviews", 
                                            backref="users_favorited", lazy="dynamic")
    favorited_artist_reviews = db.relationship("ArtistReview", secondary="favorited_artist_reviews", 
                                            backref="users_favorited", lazy="dynamic")


    def __init__(self, **kwargs):
        try:
            super(Profile, self).__init__(**kwargs)
        except:
            return None

    def __repr__(self):
        return f"{self.user.username}'s Profile'"

class Song(db.Model):
    """
    param str name: Name of Song
    param str url: URL of Song
    param int year: Year of Song
    param Artist artist: Artist of song
    param Artist featuring: Artists featured on Song
    param Album album: Album Song belongs to
    param int artist_id: ID of Artist
    param int album_id: ID of Album
    """
    """
    serializer = api.model("song",{
        "id" : fields.String(description="Public ID of Song", attribute="public_id", readonly=True),
        "name" : fields.String(description="Name of Song"),
        "url" : fields.String(description="URL ID of Song"),
        "year" : fields.Integer(description="Year of Song", min=1960),
        "track number": fields.Integer(description="Number of Track in Album", attribute="track_number"),

        "featuring": fields.List(fields.String, description="Artists featured on Song"),
        "album": fields.String(description="Album song belongs to"),
        "genre": fields.String(description="Genre song belongs to"),
        "artist": fields.String(description="Artists of Song"),
        "reviews": fields.List(fields.String, description="Reviews of Song", readonly=True),
    })
    """
    

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid, unique=True)
    name = db.Column(db.String(60), nullable=False)
    url = db.Column(db.String(100), unique=True)
    year = db.Column(db.Integer)
    track_number = db.Column(db.Integer)
    
    reviews = db.relationship("SongReview", backref="artist", lazy="dynamic")
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))


    def __init__(self, name=None, url=None, artist=None, year=None, featuring=None, album=None, track_number=None, genre=None):
        if album:
            if Song.query.join(Song.album, Song.artist).filter(Song.name.ilike(name)).filter((Artist.id==artist.id)| (Album.id==album.id)).first():
                return None
        else:
            if Song.query.join(Song.artist).filter(Song.name.ilike(name),Artist.id==artist.id).first():
                return None
        #if album:
           #if Song.query.filter_by(album=album, name=name).first():
                #return None

        self.name = name
        kwargs = {key:val for key,val in locals().items() if val is not None and key not in ["self", "__class__"]}
    
        try:
            super(Song, self).__init__(**kwargs)

        except:
            return None

    def __repr__(self):
        return self.name


class Album(db.Model):
    """
    param str name: Name of Album
    param str url: URL of Album
    param int year: Year of Album
    param Artist artist: Artist of Album
    param Genre genre: Genre of Album
    """
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(60), nullable=False)
    url = db.Column(db.String(100), unique=True)
    year = db.Column(db.Integer)

    tracks = db.relationship("Song", backref=db.backref("album", lazy="joined"), lazy="dynamic")
    reviews = db.relationship("AlbumReview", backref="artist", lazy=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __init__(self, name=None, url=None, artist=None, year=None, genre=None, artist_id=None, genre_id=None):
        if Album.query.join(Album.artist).filter(Album.name.ilike(name), Artist.id==artist.id).first():
            return None
        self.name = name
        kwargs = {key:val for key,val in locals().items() if val is not None and key not in ["self", "__class__"]}

        try:
            super(Album, self).__init__(**kwargs)
        except:
            return None

    def __repr__(self):
        return self.name


class Artist(db.Model):
    """
    param str name: Name of Artist
    param str url: URL of Artist
    param Song songs: Songs by Artist
    param Artist features: Features by Artist
    param Album albums: Albums by Artist
    param Genre genres: Genres by Artist
    """
    """
    serializer = api.model("artist",{
        "id" : fields.String(description="Public ID of Artist", attribute="public_id"),
        "name" : fields.String(description="Name of Artist"),
        "url" : fields.String(description="URL ID of Artist"),
        
        "songs": fields.List(fields.String, description="Songs by Artist"),
        "features": fields.List(fields.String, description="Songs Artist was featured on"),
        "albums": fields.List(fields.String, descripton="Albums by Artist"),
        "genres": fields.List(fields.String, description="Genres of Artist"),
        "reviews": fields.List(fields.String, description="Reviews of Artist"),
    })
    """


    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid)
    name = db.Column(db.String(50), nullable=False, unique=True)
    url = db.Column(db.String(100), unique=True)

    reviews = db.relationship("ArtistReview", backref="artist", lazy="dynamic")
    songs = db.relationship("Song", backref="artist", lazy="dynamic")
    features = db.relationship("Song", secondary='features', backref=db.backref("featuring", lazy="joined"), lazy="dynamic")
    albums = db.relationship("Album", backref="artist", lazy="dynamic", collection_class=set)
    genres = db.relationship("Genre", secondary="artist_genre", backref=db.backref("artists", lazy="dynamic"), lazy="joined")

    def __init__(self, name=None, url=None, songs=None, features=None, albums=None, genres=None):
        self.name = name
        kwargs = {key:val for key,val in locals().items() if val is not None and key not in ["self", "__class__"]}

        try:
            super(Artist, self).__init__(**kwargs)
        except:
            return None

    def __repr__(self):
        return self.name


class Genre(db.Model):
    """
    param str name: Name of Genre
    param str url: URL of Genre
    param list songs: Songs in Genre
    param list albums: Albums in Genre
    """
    """
    serializer = api.model("genre", {
        "id" : fields.String(description="Public ID of Genre", attribute="public_id"),
        "name" : fields.String(description="Name of Genre"),
        "url" : fields.String(description="URL ID of Genre"),
        "songs": fields.List(fields.String, description="Songs in Genre"),
        "albums": fields.List(fields.String, description="Albums in Genre"),
    })
    """

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(15), default=make_uuid, unique=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    url = db.Column(db.String(100), unique=True)

    songs = db.relationship("Song", backref="genre", lazy="dynamic")
    albums = db.relationship("Album", backref="genre", lazy="dynamic")

    def __init__(self, name=None, url=None, songs=None, albums=None):
        self.name = name
        kwargs = {key:val for key,val in locals().items() if val is not None and key not in ["self", "__class__"]}

        try:
            super(Genre, self).__init__(**kwargs)
        except:
            return None

    def __repr__(self):
        return self.name

class BaseReview:
    """
    mask = Mask("name", skip=True)
    serializer = api.model("review", {
        "id": fields.String(description="ID of Song Review"),
        "review": fields.String(description="Body of Song Review"),
        "users favorited": fields.List(fields.String, description="ID of Profile reviewing Song", attribute="users_favorited")
    })
    """
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text, nullable=False)
    metadata_id = db.Column(db.String(200))

    @declared_attr
    def offline_metadata_id(cls):
        return 

    @declared_attr
    def profile_id(cls): 
        return db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False)


class SongReview(db.Model, BaseReview):
    #_type = db.Column(db.String(15), default="Song Review")
    song_id = db.Column(db.Integer, db.ForeignKey("song.id"))
    album_review_id = db.Column(db.Integer, db.ForeignKey("album_review.id"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        serializer = self.serializer.update(
            {"song": fields.Nested(Song.serializer, mask=self.mask)}
        )
    

    def __repr__(self):
        return f"{self.profile}'s Review of {self.song}"

class AlbumReview(db.Model, BaseReview):
    #_type = db.Column(db.String(15), default="Album Review")
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))
    track_reviews = db.relationship("SongReview", backref="album_review", lazy='joined')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        serializer = self.serializer.update(
            {"album": fields.Nested(Album.serializer, mask=self.mask)}
        )

    def __repr__(self):
        return f"{self.profile}'s Review of {self.album}"


class ArtistReview(db.Model, BaseReview):
    #_type = db.Column(db.String(15), default="Artist Review")
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        serializer = self.serializer.update(
            {"artist": fields.Nested(Artist.serializer, mask=self.mask)}
        )

    def __repr__(self):
        return f"{self.profile}'s Review of {self.artist}"

    

