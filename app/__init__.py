from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_restplus import Api
import os


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
#api = Api()

def create_app():
    app = Flask(__name__)
    #api.init_app(app, title="Music Review API", description="Make requests to the Music Review API",
                #version="0.1.0")

    db.init_app(app)
    login_manager.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE")
    app.config["SWAGGER_UI_JSONEDITOR"] = True
    #app.config['SQLALCHEMY_ECHO'] = True

    from .commands import create_db, drop_db, populate_db
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(populate_db)

    from .apiV1 import blueprint as apiV1

    app.register_blueprint(apiV1)

    #from .user.routes import user
    #from .auth.routes import auth
    #from .metadata.routes import metadata
    #from .review.routes import review

    #app.register_blueprint(auth)
    #app.register_blueprint(user)
    #app.register_blueprint(metadata)
    #app.register_blueprint(review)

    return app