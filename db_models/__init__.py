from http import HTTPStatus
from unicodedata import name
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from os import path


DB_NAME = 'sql6501195'
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://sql6501195:G5mH4G4Ggq@sql6.freemysqlhosting.net/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    '''Swagger UI'''
    # Products UI
    SWAGGER_URL = "/swagger/products"
    SWAGGER_PATH = "/static/product.json"
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, SWAGGER_PATH)

    # Customer UI
    SWAGGER_URL1 = "/swagger/customers"
    SWAGGER_PATH1 = "/static/customer.json"
    SWAGGER_BLUEPRINT1 = get_swaggerui_blueprint(SWAGGER_URL1, SWAGGER_PATH1, blueprint_name=SWAGGER_URL1)

    # Orders UI
    SWAGGER_URL_2 = "/swagger/orders"
    SWAGGER_PATH_2 = "/static/order.json"
    SWAGGER_BLUEPRINT_2 = get_swaggerui_blueprint(SWAGGER_URL_2, SWAGGER_PATH_2, blueprint_name=SWAGGER_URL_2)


    # Error Handling
    @app.errorhandler(HTTPStatus.UNPROCESSABLE_ENTITY)
    def webargs_error_handler(err):
        headers = err.data.get('headers', None)
        messages = err.data.get("messages",["Invalid Request."])
  
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code
            
    
            
    # Register Blueprints
    from .views import bp
    app.register_blueprint(bp, url_prfix = '/')
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix= SWAGGER_URL)
    app.register_blueprint(SWAGGER_BLUEPRINT1, url_prefix= SWAGGER_URL1)
    app.register_blueprint(SWAGGER_BLUEPRINT_2, url_prefix= SWAGGER_URL_2)


    # Create Database
    create_database(app)

    return app


def create_database(app):
    if not path.exists('models' + DB_NAME):
        db.create_all(app=app)
