import os
from flask import Flask
from flask_restful import Api, Resource
from application.database import db




app = None
api = None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libmang.sqlite3'
    db.init_app(app)
    api = Api(app)
    app.app_context().push()

    return app, api
app, api  = create_app()

from application.controllers import *

# api.add_resource(UserAPI, '/user/<string:username>')

if __name__ == '__main__':
    app.run()

    
