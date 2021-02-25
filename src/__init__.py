from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_restful import Api, marshal_with
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_searchable import make_searchable

app = Flask(__name__)
app.config.from_object("src.config.Config")
# cors
CORS(app, supports_credentials=True)
# db
db = SQLAlchemy(app)
make_searchable(db.metadata)
# ma
ma = Marshmallow()
# routes
api = Api(app)
# seeder
seeder = FlaskSeeder(app, db)

# logging
import logging.config

logging.config.dictConfig(app.config['LOGGING_CONFIG'])

# import models
from .models import *
# import routes
from .routes import *
# import services
from .services import *
# import libs
from .libs import *

# import common
from .common import (
    ManualException,
    ErrorResponse
)


# error handling
@app.errorhandler(Exception)
@marshal_with(ErrorResponse.marshallable())
def handle_error(error):
    logging.error(f'Error: {error}')
    return ErrorResponse(), 500


@app.errorhandler(ManualException)
@marshal_with(ErrorResponse.marshallable())
def handle_manual_error(error):
    logging.error(f'Error: {error}')
    return ErrorResponse(code=error.code, msg=error.msg, err=error.err), error.code
