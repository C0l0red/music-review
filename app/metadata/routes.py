"""
from flask import current_app as app, url_for, redirect, render_template, Blueprint, request
from flask_login import current_user
from app.models import Song, Artist, Album, Genre
#from .forms import SongForm, AlbumForm, ArtistForm, GenreForm
from app.interface import Instance
from app import api, db
from flask_restplus import Resource, reqparse


metadata = Blueprint("metadata", __name__, url_prefix="/metadata")
"""
#songs = api.namespace("songs", description="Endpoint to query a Songs")
#songs = api.namespace("songs", description="Endpoint to query multiple Songs")
#albums = api.namespace("albums", description="Endpoint to query Albums")
#artists = api.namespace("artists", description="Endpoint to query Artists")
#genres = api.namespace("genres", description="Endpoint to query Genres")

#lastFM = Instance("lastFM")

#song_serializer = Song.serializer
#album_serializer = Album.serializer
#artist_serializer = Artist.serializer

"""
song_parser = reqparse.RequestParser()
song_parser.add_argument("name", type=str, help="Name of Song")
song_parser.add_argument("url", type=str, help="URL of Song resource")
song_parser.add_argument("year", type=int, help="Year Song was released")
song_parser.add_argument("track number", type=int, help="Track Number of Song if in an Album", dest="track_number")
song_parser.add_argument("album", type=str, help="Album name if Song is in an Album")
song_parser.add_argument("artist", type=str, help="Artist of Song")
song_parser.add_argument("genre", type=str, help="Genre Song belongs to")
song_parser.add_argument("featuring", type=str, help="List of Artists featured on Song", action="append")
#song_parser.add_argument()

album_parser = reqparse.RequestParser()
album_parser.add_argument("name", type=str, help="Name of Album")
album_parser.add_argument("url", type=str, help="URL of Album resource")
album_parser.add_argument("year", type=int, help="Year of Album's release")
#album_parser.add_argument("tracks", type=list, help="List of tracks")
album_parser.add_argument("artist", type=str, help="Artist of Album")
album_parser.add_argument("genre", type=str, help="Genre Album belongs to")
#album_parser.add_argument()

artist_parser = reqparse.RequestParser()
artist_parser.add_argument("name", type=str, help="Name of Artist")
artist_parser.add_argument("url", type=str, help="URL of Artist resource")
artist_parser.add_argument("genres", type=str, action="append", help="List of Genres Artist is into")
#artist_parser.add_argument()

genre_parser = reqparse.RequestParser()
genre_parser.add_argument("name", type=str, help="Name of Genre")
genre_parser.add_argument("url", type=str, help="URL of Genre resource")
#genre_parser.add_argument()

def clean_data(data):
    artist= data.get("artist")
    if artist:
        artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
        data['artist'] = artist

    album = data.get("album")
    if album:
        album = artist.albums.filter(Album.name.ilike(album)).first_or_404(f"Album '{album}' by '{artist}' not found")
        #print(album)
        data['album'] = album

    genre = data.get("genre")
    if genre:
        genre = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
        #print(genre)
        data['genre'] = genre

    featuring = data.get("featuring")
    if featuring:
        for i, artist in enumerate(featuring):
            result = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
            featuring[i] = result
        data["featuring"] = featuring

    genres = data.get("genres")        
    if genres:
        for i, genre in enumerate(genres):
            result = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
            genres[i] = result
        data["genres"] = genres
    
    return data

class SingleResource:

    def get(self, id):
        obj = self.Model.query.filter_by(public_id=id).first_or_404(f"{self.model} with ID '{id}' not found")
        return self.ns.marshal(obj, self.Model.serializer, skip_none=True), 200

    def delete(self, id):
        obj = self.Model.query.filter_by(public_id=id).first_or_404(f"{self.model} with ID '{id}' not found.")

        db.session.delete(obj)
        db.session.commit()

        return {"success": f"{self.model} '{obj}' successfully deleted"}, 200

    def put(self, id):
        data = self.parser.parse_args()
        print(data)
        data = {key:val for key,val in data.items() if val is not None}
        print(data)
        data = clean_data(data)
        print(data)
        #return
        result = self.Model.query.filter_by(public_id=id)

        obj = result.first_or_404(f"{self.model} with ID '{id}' not found")

        for key,val in data.items():
            if isinstance(val, list):
                for item in val:
                    getattr(obj, key).append(item)
            else:
                setattr(obj, key, val)

        try:
            db.session.commit()
        except:
            return {"error": f"Updated values already exist for another {self.model}"}

        return self.ns.marshal(obj, self.Model.serializer, skip_none=True), 200    


@songs.route("/<id>", endpoint="music")
@songs.doc(params={'id': 'ID of Song'})
@songs.response(404, "Resource not found")
class SongResource(Resource, SingleResource):
    ns = songs
    Model = Song
    model = "Song"
    parser = song_parser
    
    @ns.doc(description="Fetch single Song using ID")
    @ns.response(200, "Song fetched successfully")
    def get(self, id):
        return super(SongResource, self).get(id)


    @ns.doc(description="Delte Song using ID")
    @ns.response(200, "Song deleted successfully")
    def delete(self, id):
        return super(SongResource, self).delete(id)


    @ns.doc(description="Edit Song with ID by passing a JSON object")
    @ns.expect(parser, validate=True)
    @ns.response(200, "Song updated successfully")
    def put(self, id):
        return super(SongResource, self).put(id)


@songs.route("/")
@songs.response(404, "Resource not found")
class SongListResource(Resource):
    ns = songs
    parser = song_parser
    
    @ns.doc(params={"artist": "Artist Name", "song": "Song Name"}, description="Fetch single or multiple Songs using Artist and or Song name parameters")
    @ns.response(200, "Song fetched successfully")
    def get(self):
        artist = request.args.get("artist", None)
        song = request.args.get("song", None)
    

        if artist:
            artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found.")
            if song:
                song = artist.songs.filter(Song.name.ilike(song)).first_or_404(f"Song '{song}' not found.")
                return self.ns.marhsal(song, Song.serializer, skip_none=True), 200

            songs = artist.songs.query.all()
        elif song:
            songs = Song.query.filter(Song.name.ilike(song)).all()
            if not songs:
                return {"error": f"No Song '{song}' found"}, 404
        else:
            songs = Song.query.all()

        return self.ns.marshal(songs, Song.serializer, skip_none=True), 200

    @ns.doc(description="Create Song by sending a JSON object")
    @ns.expect(parser, validate=True)
    @ns.response(409, "Duplicate record")
    @ns.response(201, "Song Created", model=Song.serializer)
    def post(self):
        
        data = self.parser.parse_args()
        print(data)
        #return 
        if any(val is None for key,val in data.items() if key in ["name", "artist", "year"]):
            return {"error": "name, artist and year are required"}, 400
        print(data)
        #return {"okay":"okay"}
        #song = {key.replace(" ", "_"):val for key,val in song.items()}
        data = clean_data(data)
        

        print(data)
        song = Song(**data)
        #print(song)
        try:
            db.session.add(song)
            db.session.commit()
        except:
            return {"error": f"Song {data['name']} already exists"}, 409
        return self.ns.marshal(song, Song.serializer, mask="id, name, artist, features, album, year, url"), 201


@albums.route("/<id>")
@albums.doc(params={"id": "ID of Album"})
class AlbumResource(Resource, SingleResource):
    ns = albums
    Model = Album
    model = "Album"
    parser = album_parser

    @ns.doc(description="Fetch single Album with ID")
    @ns.response(200, "Album fetched successfully")
    def get(self, id):
        return super(AlbumResource, self).get(id)


    @ns.doc(description="Delete Album with ID")
    @ns.response(200, "Album successfully deleted")
    def delete(self, id):
        return super(AlbumResource, self).delete(id)
 

    @ns.doc(description="Edit Album with ID by passing a JSON object")
    @ns.expect(parser, validate=True)
    @ns.response(200, "Album successfully updated")
    @ns.response(409, "Duplicate record")
    def put(self, id):
        return super(AlbumResource, self).put(id)


@albums.route("/")
@albums.response(404, "Resource not found")
class AlbumListResource(Resource):
    ns = albums
    parser = album_parser

    @ns.doc(params={"artist": "Artist Name", "album": "Album Name"}, description="Fetch single or multiple Albums using Artist and or Album parameters")
    @ns.response(200, "Album fetched successfully")
    def get(self):
        artist = request.args.get("artist", None)
        album = request.args.get("album", None)

        if artist:
            artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
            if album:
                album = artist.albums.filter(Album.name.ilike(album)).first_or_404(f"Album '{album}' not found")
                return self.ns.marshal(album, Album.serializer, skip_none=True), 200
            
            albums = artist.albums.all()
        elif album:
            albums = Album.query.filter(Album.name.ilike(album)).all()
            if not albums:
                return {"error": f"No Album '{album}' found"}, 404
        else:
            albums = Album.query.all()

        return self.ns.marshal(albums, Album.serializer, skip_none=True), 200

    @ns.expect(parser, validate=True)
    @ns.response(201, "Album Created")
    @ns.response(409, "Duplicate record")
    @ns.doc(description="Create Albums using a JSON object")
    def post(self):
        data = self.parser.parse_args()
        if any(val is None for key,val in data.items() if key in ["name", "url", "year", "artist"]):
            return {"error": "name, url, year and artist are required"}, 400

        data = clean_data(data)
        album = Album(**data)

        try:
            db.session.add(album)
            db.session.commit()
        except:
            return {"error": f"Album {data['name']} already exists"}, 409
        return self.ns.marshal(album, Album.serializer, skip_none=True, mask="id,name,artist,year,url,genre"), 201

@artists.route("/<id>")
@artists.doc(params={"id": "ID of Artist"})
class ArtistResource(Resource, SingleResource):
    ns = artists
    Model = Artist
    model = "Artist"
    parser = artist_parser

    @ns.doc(description="Fetch single Artist with ID")
    @ns.response(200, "Artist fetched successfully")
    def get(self, id):
        return super(ArtistResource, self).get(id)

    @ns.doc(description="Delete Artist with ID")
    @ns.response(200, "Artist successfully deleted")
    def delete(self, id):
        return super(ArtistResource, self).delete(id)

    @ns.doc(description="Edit Artist with ID by passing a JSON object")
    @ns.expect(parser, validate=True)
    @ns.response(200, "Artist successfully updated")
    @ns.response(409, "Duplicate record")
    def put(self, id):
        return super(ArtistResource, self).put(id)

@artists.route("/")
@artists.response(404, "Resource not found")
class ArtistListResource(Resource):
    ns = artists
    parser = artist_parser

    @ns.doc(params={'genre': "Genre Name", "artist": "Artist Name"}, description="Fetch single or multiple Artists, optionally using Genre as a filter")
    @ns.response(200, "Artist fetched successfully")
    def get(self):
        genre = request.args.get("genre", None)
        artist = request.args.get("artist", None)

        if genre:
            genre = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
            if artist:
                artist = genre.artists.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' under Genre '{genre}' not found")
                return self.ns.marshal(artist, Artist.serializer, skip_none=True), 200

            artists = genre.artists.all()
            
        elif artist:
            artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
            return self.ns.marshal(artist, Artist.serializer, skip_none=True), 200
        else:
            artists = Artist.query.all()

        if not artists:
            return {"error": "No Artists found"}, 404
        return self.ns.marshal(artists, Artist.serializer, skip_none=True), 200

    @ns.expect(parser, validate=True)
    @ns.response(201, "Artist Created")
    @ns.response(409, "Duplicate record")
    @ns.doc(description="Create Artists using a JSON object")
    def post(self):
        data = self.parser.parse_args()
        if any(val is None for key,val in data.items() if key in ["name", "url"]):
            return {"error": "name and url are required"}, 400

        data = clean_data(data)
        artist = Artist(**data)

        try:
            db.session.add(artist)
            db.session.commit()
        except:
            return {"error": f"Artist {data['name']} already exists"}, 409
        return api.marshal(artist, Artist.serializer, skip_none=True, mask="id,name,url,genres"), 201

@genres.route("<id>")
@genres.doc(params={"id": "ID of Genre"})
class GenreResource(Resource, SingleResource):
    ns = genres
    Model = Genre
    model = "Genre"
    parser = genre_parser

    @ns.doc(description="Fetch single Genre with ID")
    @ns.response(200, "Genre fetched successfully")
    def get(self, id):
        return super(GenreResource, self).get(id)

    @ns.doc(description="Delete Genre with ID")
    @ns.response(200, "Genre successfully deleted")
    def delete(self, id):
        return super(GenreResource, self).delete(id)

    @ns.doc(description="Edit Genre with ID by passing a JSON object")
    @ns.expect(parser, validate=True)
    @ns.response(200, "Genre successfully updated")
    @ns.response(409, "Duplicate record")
    def put(self, id):
        return super(GenreResource, self).put(id)

@genres.route("/")
@genres.response(404, "Resource not found")
class GenreListResource(Resource):
    ns = genres
    Model = Genre
    model = "Genre"
    parser = genre_parser

    @ns.doc(params={"genre": "Genre Name"}, description="Fetch single or multiple Genres with an optional Genre name parameter")
    @ns.response(200, "Genre fetched successfully")
    def get(self):
        genre = request.args.get("genre", None)

        if genre:
            genre = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
            return self.ns.marshal(genre, Genre.serializer, skip_none=True), 200
        else:
            genres = Genre.query.all()
        return self.ns.marshal(genres, Genre.serializer, skip_none=True), 200

    @ns.expect(parser, validate=True)
    @ns.response(201, "Genre Created")
    @ns.response(409, "Duplicate record")
    @ns.doc(description="Create Genres using a JSON object")
    def post(self):
        data = self.parser.parse_args()
        if any(val is None for key,val in data.items() if key in ["name", "url"]):
            return {"error": "name and url are required"}, 400

        data = clean_data(data)
        genre = Genre(**data)

        try:
            db.session.add(genre)
            db.session.commit()
        except:
            return {"error": f"Genre {data['name']} already exists"}, 409
        return self.ns.marshal(genre, Genre.serializer, skip_none=True, mask="id,name,url"), 201
"""



"""
def add_metadata(data, Model):
    obj = Model(data)

    if obj:
        db.session.add(obj)
        db.session.commit()
        return obj, 201
    
    return {"Error": "Object already exists in database"}, 400

def edit_metadata(data, obj):
    obj.update(data, False)

    db.session.commit()
    return obj


@metadata.route("/songs/<str:artist>/<str:song>")
@metadata.route("/songs/<str:song>")
@metadata.route("/songs")
def songs(artist=None, song=None):
    if song:
        try:
            if artist:
                _artist = Artist.query.filter_by(name=artist).first()
                result = _artist.songs.filter_by(name=song).first()
            else:
                result = Song.query.filter_by(name=song).all()

            assert result is not None
        except:
            result = lastFM.track.info(track=song, artist=artist)
        finally:
            return render_template("songs.html", song=result)

    result = Song.query.all()

    return render_template("songs.html", songs=result)

@metadata.route("/albums/<str:artist>/<str:album>")
@metadata.route("/albums/<str:album>")
@metadata.route("/albums")
def albums(artist=None, album=None):
    if album:
        try:
            if artist:
                _artist = Artist.query.filter_by(name=artist).first()
                result = _artist.albums.filter_by(name=album).first()
            else:
                result = Album.query.filter_by(name=album).all()

            assert result is not None
        except:
            result = lastFM.album.info(album=album, artist=artist)
        finally:
            return render_template("albums.html", album=result)

    result = Album.query.all()
    return render_template("albums.html", albums=result)


@metadata.route("/artists/<str:artist>")
@metadata.route("/artists")
def artists(artist):
    try:
        if artist:
            result = Artist.query.filter_by(name=name).first_or_404()
        else:
            result = Artist.query.all()
    except:
        result = Artists.get_info(artist=artist)
    finally:
        return render_template("artists.html", artists=result)

    result = Artist.query.all()
    
    return render_template("artists.html", artists=result)

@metadata.route("/songs/add")
def add_song():
    return add_metadata(SongForm, Song, "song")


@metadata.route('/albums/add')
def add_album():
    return add_metadata(AlbumForm, Album, "album")
    

@metadata.route("/artists/add")
def add_artist():
    return add_metadata(ArtistForm, Artist, "artist")
    

@metadata.route("/genres/add")
def add_genre():
    return add_metadata(GenreForm, Genre, "genre")
    
@metadata.route('/songs/<str:artist>-<str-name>/edit')
def edit_song(artist, name):
    artist = Artist.query.filter_by(name=artist).first_or_404()
    song = artist.songs.filter_by(name=song).first_or_404()
    
    return edit_metadata(SongForm, song, "song", artist=artist.name, name=song.name)

@metadata.route("/albums/<str:artist>-<str:name>")
def edit_album(artist, name):
    artist = Artist.query.filter_by(name=artist).first_or_404()
    album = artist.albums.filter_by(name=name).first_or_404()

    return edit_metadata(AlbumForm, album, "album", artist=artist.name, name=album.name)

@metadata.route("/artists/<str:name>")
def edit_artist(name):
    artist = Artist.query.filter_by(name=name).first_or_404()

    return edit_metadata(ArtistForm, artist, "artist", name=artist.name)

@metadata.route('/genre/<str:name>')
def edit_genre(name):
    genre = Genre.query.filter_by(name=name).first_or_404()

    return edit_metadata(GenreForm, genre, "genre", name=genre.name)
"""


"""
def add_metadata(form, Model, route):

    if form.validate_on_submit():
        obj = Model()
        form.populate_obj(obj)

        db.session.add(obj)
        db.session.commmit()

        return redirect(url_for(f'metadata.{route}s'))

    return render_template(f"add-{route}.html", form=form)

def edit_metadata(Form, obj, route, **kwargs):
    form = Form(data=obj)

    if form.validate_on_submit():
        form.populate_obj(obj)

        db.session.commit()

        return redirect(url_for(f"metadata.{route}", **kwargs))

    return render_template("add-{route}.html", form=form)
"""
