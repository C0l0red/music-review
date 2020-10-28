from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from .utils import clean_data, SingleResource, db
from app.models import Album, Genre, Artist, Song

api = Namespace("albums", description="Endpoint to query a Albums")


serializer = api.model("album",{ 
    "id" : fields.String(description="Public ID of Album", attribute="public_id", readonly=True),
    "name" : fields.String(description="Name of Album"),
    "url" : fields.String(description="URL ID of Album"),
    "year" : fields.Integer(description="Year of Album", min=1960),

    "artist": fields.String(description="Artist of Album"),
    "tracks": fields.List(fields.String, description="Tracks on Album"),
    "genre": fields.String(description="Genre of Album"),
    "reviews": fields.List(fields.String, description="Reviews of Album", readonly=True),
})

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of Album", location="form")
parser.add_argument("url", type=str, help="URL of Album resource", location="form")
parser.add_argument("year", type=int, help="Year of Album's release", location="form")
parser.add_argument("artist", type=str, help="Artist of Album", location="form")
parser.add_argument("genre", type=str, help="Genre Album belongs to", location="form")
#parser.add_argument("tracks", type=list, help="List of tracks")
#parser.add_argument()

@api.route("/<id>")
@api.doc(params={"id": "ID of Album"})
@api.response(404, "Album not found")
class AlbumResource(Resource, SingleResource):
    ns = api
    Model = Album
    model = "Album"
    parser = parser
    serializer = serializer

    @api.doc(description="Fetch single Album with ID")
    @api.response(200, "Album fetched successfully", model=serializer)
    def get(self, id):
        return super(AlbumResource, self).get(id)


    @api.doc(description="Delete Album with ID")
    @api.response(200, "Album successfully deleted")
    def delete(self, id):
        return super(AlbumResource, self).delete(id)
 

    @api.doc(description="Edit Album with ID by passing a JSON object")
    @api.expect(parser, validate=True)
    @api.response(200, "Album successfully updated", model=serializer)
    @api.response(409, "Duplicate record")
    def put(self, id):
        return super(AlbumResource, self).put(id)


@api.route("/")
@api.response(404, "Album not found")
class AlbumListResource(Resource):

    @api.doc(params={"artist": "Artist Name", "album": "Album Name"}, description="Fetch single or multiple Albums using Artist and or Album parameters")
    @api.response(200, "Album fetched successfully", model=serializer)
    def get(self):
        artist = request.args.get("artist", None)
        album = request.args.get("album", None)

        if artist:
            artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
            if album:
                album = artist.albums.filter(Album.name.ilike(album)).first_or_404(f"Album '{album}' not found")
                return api.marshal(album, serializer, skip_none=True), 200
            
            albums = artist.albums.all()
        elif album:
            albums = Album.query.filter(Album.name.ilike(album)).all()
            if not albums:
                api.abort(404, f"No Album '{album}' found")
                #return {"error": f"No Album '{album}' found"}, 404
        else:
            albums = Album.query.all()

        return api.marshal(albums, serializer, skip_none=True), 200

    @api.expect(parser, validate=True)
    @api.response(201, "Album Created")
    @api.response(409, "Duplicate record")
    @api.doc(description="Create Albums using a JSON object", model=serializer)
    def post(self):
        data = parser.parse_args()
        required = ["name", "url", "year", "artist"]

        if any(val is None for key,val in data.items() if key in required):
            api.abort(400, "Value of a required key is missing", required=required)
            #return {"error": "name, url, year and artist are required"}, 400

        data = clean_data(data)

        try:
            album = Album(**data)
            db.session.add(album)
            db.session.commit()
        except:
            api.abort(409, "Album already exists")
            #return {"error": f"Album {data['name']} already exists"}, 409
        return api.marshal(album, serializer, skip_none=True, mask="id,name,artist,year,url,genre"), 201