from flask import Blueprint
from flask_restplus import Api

from .apis.albums import api as albums
from .apis.artists import api as artists
from .apis.genres import api as genres
from .apis.songs import api as songs
from .apis.users import api as users
#from .apis.


blueprint = Blueprint('alphaV2', __name__, url_prefix='/api/alphaV2')
api = Api(blueprint,
    title='Music Review API',
    version='0.1.2',
    description='"Make requests to the Music Review API"',
    # All API metadatas
)

api.add_namespace(albums)
api.add_namespace(artists)
api.add_namespace(genres)
api.add_namespace(songs)
api.add_namespace(users)
#api.add_namespace()