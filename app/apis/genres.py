from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from .utils import clean_data, SingleResource, db
from app.models import Artist, Album, Song, Genre

api = Namespace("genres", description="Endpoint to query a Genres")

serializer = api.model("genre", {
    "id" : fields.String(description="Public ID of Genre", attribute="public_id"),
    "name" : fields.String(description="Name of Genre"),
    "url" : fields.String(description="URL ID of Genre"),
    "songs": fields.List(fields.String, description="Songs in Genre"),
    "albums": fields.List(fields.String, description="Albums in Genre"),
})

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="Name of Genre", location="form")
parser.add_argument("url", type=str, help="URL of Genre resource", location="form")
#parser.add_argument()

@api.route("<id>")
@api.doc(params={"id": "ID of Genre"})
@api.response(404, "Genre not found")
class GenreResource(Resource, SingleResource):
    ns = api
    Model = Genre
    model = "Genre"
    parser = parser
    serializer = serializer

    @api.doc(description="Fetch single Genre with ID")
    @api.response(200, "Genre fetched successfully", model=serializer)
    def get(self, id):
        return super(GenreResource, self).get(id)

    @api.doc(description="Delete Genre with ID")
    @api.response(200, "Genre successfully deleted")
    def delete(self, id):
        return super(GenreResource, self).delete(id)

    @api.doc(description="Edit Genre with ID by passing a JSON object")
    @api.expect(parser, validate=True)
    @api.response(200, "Genre successfully updated", model=serializer)
    @api.response(409, "Duplicate record")
    def put(self, id):
        return super(GenreResource, self).put(id)

@api.route("/")
@api.response(404, "Genre not found")
class GenreListResource(Resource):

    @api.doc(params={"genre": "Genre Name"}, description="Fetch single or multiple Genres with an optional Genre name parameter")
    @api.response(200, "Genre fetched successfully", model=serializer)
    def get(self):
        genre = request.args.get("genre", None)

        if genre:
            genre = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
            return api.marshal(genre, serializer, skip_none=True), 200
        else:
            genres = Genre.query.all()
        return api.marshal(genres, serializer, skip_none=True), 200

    @api.expect(parser, validate=True)
    @api.response(201, "Genre Created", model=serializer)
    @api.response(409, "Duplicate record")
    @api.doc(description="Create Genres using a JSON object")
    def post(self):
        data = parser.parse_args()
        required = ["name", "url"]
        if any(val is None for key,val in data.items() if key in required):
            api.abort(400, "Values of required keys are missing", required=required)
            #return {"error": "name and url are required"}, 400

        data = clean_data(data)

        try:
            genre = Genre(**data)
            db.session.add(genre)
            db.session.commit()
        except:
            api.abort(409, "Genre already exists")
            #return {"error": f"Genre {data['name']} already exists"}, 409
        return api.marshal(genre, serializer, skip_none=True, mask="id,name,url"), 201