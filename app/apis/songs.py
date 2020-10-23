from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from .utils import clean_data, SingleResource, db
from app.models import Song, Album, Artist, Genre

api = Namespace("songs", description="Endpoint to query a Songs")

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

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of Song", location="form")
parser.add_argument("url", type=str, help="URL of Song resource", location="form")
parser.add_argument("year", type=int, help="Year Song was released", location="form")
parser.add_argument("track number", type=int, help="Track Number of Song if in an Album", dest="track_number", location="form")
parser.add_argument("album", type=str, help="Album name if Song is in an Album", location="form")
parser.add_argument("artist", type=str, help="Artist of Song", location="form")
parser.add_argument("genre", type=str, help="Genre Song belongs to", location="form")
parser.add_argument("featuring", type=str, help="List of Artists featured on Song", action="append", location="form")


@api.route("/<id>")
@api.doc(params={'id': 'ID of Song'})
@api.response(404, "Song not found")
class SongResource(Resource, SingleResource):
    ns = api
    parser = parser
    Model = Song
    serializer = serializer
    model = "Song"
    
    @api.doc(description="Fetch single Song using ID")
    @api.response(200, "Song fetched successfully", model=serializer)
    def get(self, id):
        return super(SongResource, self).get(id)


    @api.doc(description="Delte Song using ID")
    @api.response(200, "Song deleted successfully")
    def delete(self, id):
        return super(SongResource, self).delete(id)


    @api.doc(description="Edit Song with ID by passing a JSON object")
    @api.expect(parser, validate=True)
    @api.response(200, "Song updated successfully", model=serializer)
    def put(self, id):
        return super(SongResource, self).put(id)


@api.route("/")
@api.response(404, "Song not found")
class SongListResource(Resource):
    
    @api.doc(params={"artist": "Artist Name", "song": "Song Name"}, description="Fetch single or multiple Songs using Artist and or Song name parameters")
    @api.response(200, "Song fetched successfully", model=serializer)
    def get(self):
        artist = request.args.get("artist", None)
        song = request.args.get("song", None)
    
        if artist:
            artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found.")
            if song:
                song = artist.songs.filter(Song.name.ilike(song)).first_or_404(f"Song '{song}' not found.")
                return api.marhsal(song, serializer, skip_none=True), 200

            songs = artist.songs.query.all()
        elif song:
            songs = Song.query.filter(Song.name.ilike(song)).all()
            if not songs:
                api.abort(404, f"No Song '{song}' found")
                #return {"error": f"No Song '{song}' found"}, 404
        else:
            songs = Song.query.all()

        return api.marshal(songs, serializer, skip_none=True), 200

    @api.doc(description="Create Song by sending a JSON object")
    @api.expect(parser, validate=True)
    @api.response(409, "Duplicate record")
    @api.response(201, "Song Created", model=serializer)
    def post(self):
        
        data = parser.parse_args()
        required = ["name", "artist", "year"]

        if any(val is None for key,val in data.items() if key in required):
            #return {"error": "name, artist and year are required"}, 400
            api.abort(400, "Value for a required key is missing", required=required)
        data = clean_data(data)
        
        song = Song(**data)
        try:
            db.session.add(song)
            db.session.commit()
        except:
            #return {"error": f"Song {data['name']} already exists"}, 409
            api.abort(409, "Song already exists")
        return api.marshal(song, serializer, mask="id, name, artist, features, album, year, url"), 201