import io
import os
from flask import (
    Flask,
    jsonify,
    make_response,
    request,
    send_file,
    render_template,
)
import requests
from shapely.geometry import Point, shape
from pymbtiles import MBtiles

delta = 0.0000001
api_adresse_url = "https://api-adresse.data.gouv.fr/search"


def register_routes(app: Flask):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/api/v1/search_qpv")
    def search_qpv():
        """ """
        adresse = request.args.get("adresse", None)
        longitude = request.args.get("longitude", None)
        latitude = request.args.get("latitude", None)
        props = None
        # mypoint = (2.405850,48.916150)
        if (longitude is None or latitude is None) and adresse is None:
            return jsonify({})
        if adresse is not None:
            response = requests.get(f"{api_adresse_url}?q={adresse}")
            json_content = response.json()
            if len(json_content.get("features")) > 0:
                feature = json_content.get("features")[0]
                props = feature.get("properties")
                props["lon"], props["lat"] = x_point, y_point = feature.get(
                    "geometry"
                ).get("coordinates")
            else:
                return jsonify(
                    {
                        "type": "FeatureCollection",
                        "message": "Adress not found",
                        "features": [],
                    }
                )
        else:
            x_point, y_point = float(longitude), float(latitude)
        left_point, bottom_point, right_point, top_point = [
            x_point - delta,
            y_point - delta,
            x_point + delta,
            y_point + delta,
        ]
        intersected = list(
            app.config["idx_qpv"].intersection(
                (left_point, bottom_point, right_point, top_point)
            )
        )
        pt = Point(x_point, y_point)
        # print(intersected)
        result = [
            i
            for i in intersected
            if pt.within(shape(app.config["features_keys"][i].get("geometry")))
        ]
        if len(result) == 1:
            content = {
                "type": "FeatureCollection",
                "message": "In a QPV",
                "features": [app.config["features_keys"][result[0]]],
            }
        else:
            content = {
                "type": "FeatureCollection",
                "message": "Not in a QPV",
                "features": [],
            }
        if props is not None:
            content["deduced_adress"] = props
        return jsonify(content)

    @app.route("/api/v1/qpv/tiles/<int:z>/<int:x>/<int:y>.pbf")
    def tiles(z, x, y):
        new_y = (2**z) - 1 - y
        mbtiles_path = f"{os.path.join(app.instance_path, 'qpv.mbtiles')}"
        with MBtiles(mbtiles_path) as src:
            response = make_response(
                send_file(
                    io.BytesIO(src.read_tile(z=z, x=x, y=new_y)),
                    mimetype="application/x-protobuf",
                )
            )
            response.headers["Content-Type"] = "application/x-protobuf"
            response.headers["Content-Encoding"] = "gzip"
            return response

    """
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)


    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        # links is now a list of url, endpoint tuples
        return f"<ul>{''.join([f'<li>{i}</li>' for i in links])}</ul>"
    """
