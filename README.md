# QPV API with demo


## Dependencies

Create virtualenv

```bash
python3.7 -m venv venv
source venv/bin/activate
./venv/bin/pip3.7 install flask fiona shapely requests flask_cors numpy rtree pymbtiles flask-swagger-ui
./venv/bin/pip3.7 install gdal==2.4
```

## Data

Get data and process it (need gdal lib and tippecanoe utility)

```bash
python3.7 flaskr/process_data.py
```

## Run local server

```bash
./run_local.sh
```

There is a `wsgi.py` for production deployment

## Entries/endpoints

There is a front at

https://qpv.webgeodatavore.com

We also offer an API

- longitude,latitude within a QPV https://qpv.webgeodatavore.com/api/v1/search_qpv?longitude=2.405850&latitude=48.916150
- longitude, latitude not within a QPV https://qpv.webgeodatavore.com/api/v1/search_qpv?longitude=2.405850&latitude=44.916150
- address valid and within a QPV https://qpv.webgeodatavore.com/api/v1/search_qpv?adresse=20%20Rue%20Honor%C3%A9%20Daumier%2044100%20Nantes
- address valid but not within a QPV https://qpv.webgeodatavore.com/api/v1/search_qpv?adresse=28%20rue%20paul%20bellamy,%2044000%20Nantes
- invalid address, so no QPV https://qpv.webgeodatavore.com/api/v1/search_qpv?adresse=20RueHonoDaumierNantes

An alternate API could be https://sig.ville.gouv.fr/wsa.php but you need to be a public actor. It could be richer but we do not really know if it goes further than our API.

## Dev infos

You can set a precommit using `requirements-dev.txt` and `pre-commit install`

