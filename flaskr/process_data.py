import os
import subprocess
import zipfile

from osgeo import gdal
import requests

url_zip_data = "https://sig.ville.gouv.fr/Atlas/qp-politiquedelaville-shp.zip"


def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def download_and_extract_command(instance_path):
    print("download_and_extract")
    # zip file handler
    file_name = url_zip_data.split("/")[-1]
    destination_zip_path = os.path.join(instance_path, file_name)
    download_url(url_zip_data, destination_zip_path, chunk_size=128)
    zip = zipfile.ZipFile(destination_zip_path)

    # list available files in the container
    files = zip.namelist()

    # extract a specific file from the zip container
    basename = "QP_METROPOLEOUTREMER_WGS84_EPSG4326"
    for f in [s for s in files if basename in s]:
        zip.extract(f, path=instance_path)
        """print(f"{os.path.join(instance_path, 'qpv.geojson')}",
            f'{os.path.join(instance_path, basename)}.shp')
        """
        gdal.VectorTranslate(
            f"{os.path.join(instance_path, 'qpv.geojson')}",
            f"{os.path.join(instance_path, basename)}.shp",
            layerCreationOptions=["WRITE_NAME=NO", "RFC7946=YES"],
            format="GeoJSON",
        )
        cmd = [
            "tippecanoe",
            "--layer",
            "qpv",
            "--generate-ids",
            "--no-tile-stats",
            "--drop-densest-as-needed",
            "--detect-shared-borders",
            "-Z2",
            "-z14",
            "--force",
            "--output",
            f"{os.path.join(instance_path, 'qpv.mbtiles')}",
            f"{os.path.join(instance_path, 'qpv.geojson')}",
        ]
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        std_out, std_err = process.communicate()
        print(std_out.strip(), std_err)
        # tippecanoe -l qpv --generate-ids --no-tile-stats \
        # --drop-densest-as-needed --detect-shared-borders -Z2 -z14 -f \
        # -o qpv.mbtiles qpv.geojson


destination_dir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "instance")
)
download_and_extract_command(destination_dir)
