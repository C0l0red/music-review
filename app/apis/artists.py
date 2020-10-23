from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from .utils import clean_data, SingleResource, db
from app.models import Artist, Album, Song, Genre

api = Namespace("artists", description="Endpoint to query a Artists")

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

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of Artist", location="form")
parser.add_argument("url", type=str, help="URL of Artist resource", location="form")
parser.add_argument("genres", type=str, action="append", help="List of Genres Artist is into", location="form")
#parser.add_argument()

@api.route("/<id>")
@api.doc(params={"id": "ID of Artist"})
@api.response(404, "Artist not found")
class ArtistResource(Resource, SingleResource):
    ns = api
    Model = Artist
    model = "Artist"
    parser = parser
    serializer = serializer

    @api.doc(description="Fetch single Artist with ID")
    @api.response(200, "Artist fetched successfully", model=serializer)
    def get(self, id):
        return super(ArtistResource, self).get(id)

    @api.doc(description="Delete Artist with ID")
    @api.response(200, "Artist successfully deleted")
    def delete(self, id):
        return super(ArtistResource, self).delete(id)

    @api.doc(description="Edit Artist with ID by passing a JSON object")
    @api.expect(parser, validate=True)
    @api.response(200, "Artist successfully updated", model=serializer)
    @api.response(409, "Duplicate record")
    def put(self, id):
        return super(ArtistResource, self).put(id)

@api.route("/")
@api.response(404, "Artist not found")
class ArtistListResource(Resource):

    @api.doc(params={'genre': "Genre Name", "artist": "Artist Name"}, description="Fetch single or multiple Artists, optionally using Genre as a filter")
    @api.response(200, "Artist fetched successfully", model=serializer)
    def get(self):
        genre = request.args.get("genre", None)
        artist = request.args.get("artist", None)

        if genre:
            genre = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
            if artist:
                artist = genre.artists.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' under Genre '{genre}' not found")
                return api.marshal(artist, serializer, skip_none=True), 200

            artists = genre.artists.all()
            
        elif artist:
            artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
            return api.marshal(artist, serializer, skip_none=True), 200
        else:
            artists = Artist.query.all()

        if not artists:
            api.abort(404, "No Artists found")
            #return {"error": "No Artists found"}, 404
        return api.marshal(artists, serializer, skip_none=True), 200

    @api.expect(parser, validate=True)
    @api.response(201, "Artist Created")
    @api.response(409, "Duplicate record", model=serializer)
    @api.doc(description="Create Artists using a JSON object")
    def post(self):
        data = parser.parse_args()
        required = ["name", "url"]

        if any(val is None for key,val in data.items() if key in required):
            api.abort(400, "Values for required keys are missing", required=required)
            #return {"error": "name and url are required"}, 400

        data = clean_data(data)

        try:
            artist = Artist(**data)
            db.session.add(artist)
            db.session.commit()
        except:
            api.abort(409, "Artist already exists")
            #return {"error": f"Artist {data['name']} already exists"}, 409
        return api.marshal(artist, serializer, skip_none=True, mask="id,name,url,genres"), 201