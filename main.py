import os
from flask import Flask
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV','development') == "production":
        raise Exception('Currently no production config is set up')
    else:
        print("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app()

# Import all the controllers so they are loaded
from application.controllers import *




# Add all restful controllers
from application.api import ListAPI, CardAPI, UserAPI
api.add_resource(UserAPI, "/api/user", "/api/user/<int:UserID>")
api.add_resource(ListAPI, "/api/list", "/api/list/<int:ListID>")
api.add_resource(CardAPI, "/api/card", "/api/card/<int:CardID>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

