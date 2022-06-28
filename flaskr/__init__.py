import os

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from .lib_intersection_qpv import generate_index_and_associated_features_info
from .cli import register_cli
from .routes import register_routes

# from .process_data import download_and_extract_command


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="dev",
        FILEPATH=os.path.join(
            app.instance_path, "QP_METROPOLEOUTREMER_WGS84_EPSG4326.shp"
        ),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    register_cli(app)
    register_routes(app)

    # URL for exposing Swagger UI (without trailing '/')
    SWAGGER_URL = "/api/docs"
    # Our API url (can of course be a local resource)
    API_URL = "/static/swagger.json"

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={"app_name": "Test application"},  # Swagger UI config overrides
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix="/api/docs")

    (
        app.config["idx_qpv"],
        app.config["features_keys"],
        app.config["geojson"],
    ) = generate_index_and_associated_features_info(app.config["FILEPATH"])

    return app
