from flask import current_app as app, url_for, redirect, render_template, Blueprint
from flask_login import current_user
from app.models import Song, Artist, Album, Genre
from .forms import SongForm, AlbumForm, ArtistForm, GenreForm


metadata = Blueprint("metadata", __name__)

def add_router(Form, Model, route):
    form = Form()

    if form.validate_on_submit():
        obj = Model()
        form.populate_obj(obj)

        db.session.add(obj)
        db.session.commmit()

        return redirect(url_for(f'metadata.{route}s'))

    return render_template(f"add-{route}.html", form=form)

def edit_router(Form, obj, route, **kwargs):
    form = Form(data=obj)

    if form.validate_on_submit():
        form.populate_obj(obj)

        db.session.commit()

        return redirect(url_for(f"metadata.{route}", **kwargs))

    return render_template("add-{route}.html", form=form)



@metadata.route("/songs/<str:artist>-<str:name>")
@metadata.route("/songs")
def songs(artist=None, song=None):
    if song:
        artist = Artist.query.filter_by(name=artist).first_or_404()
        song = artist.songs.filter_by(name=song).first_or_404()

        return render_template("songs.html", song=song)

    songs = Song.query.all()

    return render_template("songs.html", songs=songs)

@metadata.route("/albums/<str:artist>-<str:name>")
@metadata.route("/albums")
def albums(artist=None, name=None):
    if artist:
        artist = Artist.query.filter_by(name=artist).first_or_404()

        song = artist.songs.filter_by(name=name).first_or_404()
        return render_template("albums.html", song=song)

    albums = Album.query.filter_by(name=name).all()

    return render_template("albums.html", albums=albums)

@metadata.route("/artists/<str:artist>")
@metadata.route("/artists")
def artists(name):
    if name:
        artist = Artist.query.filter_by(name=name).first_or_404()
        return render_template("artists.html", artist=artist)

    artists = Artist.query.all()
    
    return render_template("artists.html", artists=artists)

@metadata.route("/songs/add")
def add_song():
    return add_router(SongForm, Song, "song")


@metadata.route('/albums/add')
def add_album():
    return add_router(AlbumForm, Album, "album")
    

@metadata.route("/artists/add")
def add_artist():
    return add_router(ArtistForm, Artist, "artist")
    

@metadata.route("/genres/add")
def add_genre():
    return add_router(GenreForm, Genre, "genre")
    
@metadata.route('/songs/<str:artist>-<str-name>/edit')
def edit_song(artist, name):
    artist = Artist.query.filter_by(name=artist).first_or_404()
    song = artist.songs.filter_by(name=song).first_or_404()
    
    return edit_router(SongForm, song, "song", artist=artist.name, name=song.name)

@metadata.route("/albums/<str:artist>-<str:name>")
def edit_album(artist, name):
    artist = Artist.query.filter_by(name=artist).first_or_404()
    album = artist.albums.filter_by(name=name).first_or_404()

    return edit_router(AlbumForm, album, "album", artist=artist.name, name=album.name)

@metadata.route("/artists/<str:name>")
def edit_artist(name):
    artist = Artist.query.filter_by(name=name).first_or_404()

    return edit_router(ArtistForm, artist, "artist", name=artist.name)

@metadata.route('/genre/<str:name>')
def edit_genre(name):
    genre = Genre.query.filter_by(name=name).first_or_404()

    return edit_router(GenreForm, genre, "genre", name=genre.name)
