from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse
from .utils import db
from app.models import User

api = Namespace("users", description="Endpoint to query a Users")

serializer = api.model("user", {
    "id": fields.String(description="ID of User", attribute="public_id", readonly=True),
    "username": fields.String(description="Username of User"),
    "email": fields.String(description="Email Address of User"),
})

parser = reqparse.RequestParser()
parser.add_argument("username", type=str, help="Username of User", location="form")
parser.add_argument("email", type=str, help="Email of User", location="form")
parser.add_argument("password", type=str, help="Password of User", location="form")
#parser.add_argument()

@api.route("/<id>")
@api.param("id", "User ID")
@api.response(404, "User not found")
class UserResource(Resource):

    @api.response(200, "User fetched successfully", model=serializer)
    @api.doc(description="Fetch single User using User ID")
    def get(self, id):

        user = User.query.filter_by(public_id=id).first_or_404(f"User with ID '{id}' not found")
        return api.marshal(user, serializer, skip_none=True), 200

    @api.response(200, "User deleted successfully")
    @api.doc(description="Delete User with ID")
    def delete(self, id):
        user = User.query.filter_by(public_id=id).first_or_404(f"User with ID '{id}' not found")

        db.session.delete(user)
        db.session.commit()

        return {"success": f"User '{user}' deleted"}, 200

    @api.doc(description="Update User with ID")
    @api.expect(parser, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(409, "Duplicate record")
    def put(self, id):
        data = parser.parse_args()
        user = User.query.filter_by(public_id=id).first_or_404(f"User with ID '{id}' not found")
        
        username = data.get("username", None)
        email = data.get("email", None)
        password = data.get("password", None)

        if username:
            if User.query.filter(User.username.ilike(username)).first():
                api.abort(409, f"Username '{username}' taken")
            user.username = username
        if email:
            if User.query.filter(User.email.ilike(email)).first():
                api.abort(409, f"Email '{email}' already taken")
            user.email = email
        if password:
            if user.check_password(password):
                api.abort(403, f"Cannot use same password")
            if len(password) < 5:
                api.abort(403, "Password too short. It must be at least 5 characters long")
            user.set_password(password)

        if not any(data.values()):
            api.abort(400, "Enter at least one key to update, along with a value", keys=["username", "email", "password"])
        db.session.commit()

        return api.marshal(user, serializer, skip_none=True), 200 

@api.route("/")
@api.response(404, "User not found")
class UserListResource(Resource):

    @api.response(200, "User fetched successfully", model=serializer)
    @api.doc(params={"username": "Username of User", "email": "Email of User"}, description="Fetch a single User using Email or Username parameters, or multiple Users")
    def get(self):
        username = request.args.get("username", None)
        email = request.args.get("email", None)

        if username:
            user = User.query.filter(User.username.ilike(username)).first_or_404(f"User '{username}' not found")
        elif email:
            user = User.query.filter(User.email.ilike(email)).first_or_404(f"User with email '{email}' not found")
        else:
            users = User.query.all()
            return api.marshal(users, serializer, skip_none=True), 200
        
        return api.marshal(user, serializer, skip_none=True), 200

    @api.expect(parser, validate=True)
    @api.response(201, "User successfully created")
    @api.response(409, "Duplicate error")
    def post(self):
        data = parser.parse_args()
        required = ['username', "email", 'password']

        if any(x is None for x in data.values()):
            api.abort(400, "Value for a required key is missing", required=required)
        user = User(**data)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            api.abort(409, "User already exists")

        print(data)
        return api.marshal(user, serializer, skip_none=True), 201