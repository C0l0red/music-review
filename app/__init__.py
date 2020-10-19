from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restplus import Api


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
api = Api()

def create_app():
    app = Flask(__name__)
    api.init_app(app, title="Music Review API", description="Make requests to the Music Review API",
                version="1.0")

    db.init_app(app)
    login_manager.init_app(app)
    #print(app.config)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SWAGGER_UI_JSONEDITOR"] = True
    #app.config['SQLALCHEMY_ECHO'] = True

    from .commands import create_db, drop_db, populate_db
    app.cli.add_command(create_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(populate_db)

    from .user.routes import user
    from .auth.routes import auth
    from .metadata.routes import metadata
    from .review.routes import review

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(metadata)
    app.register_blueprint(review)

    return app