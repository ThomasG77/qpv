import fiona
from rtree import index


def explode(coords):
    """Explode a GeoJSON geometry's coordinates object and yield coordinate
    tuples. As long as the input is conforming, the type of the geometry
    doesn't matter."""
    for e in coords:
        if isinstance(e, (float, int)):
            yield coords
            break
        else:
            for f in explode(e):
                yield f


def bbox(f):
    x, y = zip(*list(explode(f["geometry"]["coordinates"])))
    return min(x), min(y), max(x), max(y)


def generate_index_and_associated_features_info(path):
    features_keys = {}
    features = []
    idx = index.Index()
    # file_idx = index.Rtree("rtree")
    with fiona.open(path) as infile:
        for i, feature in enumerate(infile):
            left, bottom, right, top = bbox(feature)
            idx.insert(i, (left, bottom, right, top))
            features_keys[i] = feature
            features.append(feature)
    geojson = {"type": "FeatureCollection", "features": features}
    return idx, features_keys, geojson
