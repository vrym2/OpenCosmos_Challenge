"""
    Download Sentinel 2 images
"""
import os
import click
import numpy as np
from typing import Tuple
from dotenv import load_dotenv
from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    bbox_to_dimensions,
    SentinelHubRequest,
    DataCollection,
    MimeType,
    MosaickingOrder)
from opencosmos.utils import Loader
from sentinelhub.geometry import BBox
import logging
from logging import config
config.fileConfig("logger.ini")

# Loading the environment variables
load_dotenv()

class sentinel2_image:
    """Functions related to SentinelHub"""

    evalscript_true_color = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: ["B02", "B03", "B04"]
                }],
                output: {
                    bands: 3
                }
            };
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    def __init__(
            self,
            log: isinstance = None) -> None:
        """Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log

        sh_client_id = os.environ["SH_CLIENT_ID"]
        sh_client_secret = os.environ["SH_CLIENT_SECRET"]

        try:
            assert sh_client_id is not None
            assert sh_client_secret is not None
        except AssertionError:
            self.log.debug(f"Make sure to add Sentinel OAuth IDs to the env variables")
        else:
            self.config = SHConfig()
            self.config.instance_id = "open-cosmos"
            self.config.sh_client_id = sh_client_id
            self.config.sh_client_secret = sh_client_secret
            self.config.save("open-cosmos-profile")
            
    def aoi(
            self, 
            coords_wgs84: Tuple = (46.16, -16.15, 46.51, -15.58), 
            resolution: np.int16 = 60):
        """Define an area of interest
        
        Args:\n
            coords_wgs84: WGS84 bounding box coordinates (left, bottom, right, top)
            resolution: Resolution of the desired image.
        """
        try:
            assert coords_wgs84 is not None
        except AssertionError:
            self.log.debug("Provide the bbox coordinates ina tuple")
            return None
        else:
            bbox = BBox(bbox=coords_wgs84, crs=CRS.WGS84)
            bbox_size = bbox_to_dimensions(bbox, resolution = resolution) 
            self.log.info(f"Image shape at {resolution} m resolution: {bbox_size} pixels")
            return bbox, bbox_size
    
    def true_color(
            self, 
            bbox: BBox = None, 
            resolution: np.int16 = 60,
            time_interval: Tuple = ("2020-06-01", "2020-06-30")):
        """Downloading True color mosaic
        
        Args:\n
            bbox: A SentinelHub BBox object.
            resolution: Resolution of the desired data download.
        """
        # Create the folder to download
        download_folder = os.path.join("data", "sentinel")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        
        bbox_size = bbox_to_dimensions(bbox, resolution = resolution)
        if not self.config.sh_client_id or not self.config.sh_client_secret:
            self.log.debug("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")
        else:
            loading = Loader("Downloading the True color Mosaic...", "Well, That was fast", 0.05).start()
            request_true_color = SentinelHubRequest(
                data_folder = download_folder,
                evalscript = self.evalscript_true_color,
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.SENTINEL2_L1C,
                        time_interval=time_interval,
                        mosaicking_order=MosaickingOrder.LEAST_CC,
                    )
                ],
                responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
                bbox=bbox,
                size=bbox_size,
                config = self.config)
            imgs = request_true_color.get_data(save_data=True)
            loading.stop()

            self.log.info("The downloaded files are in the following directories")
            for folder, _, filenames in os.walk(request_true_color.data_folder):
                for filename in filenames:
                    self.log.info(f"{os.path.join(folder, filename)}")

@click.command()
@click.option("--coords_wgs84", type = str, help = "WGS84 bbox coords, separated by a comma")
@click.option("--time_interval", type = str, help = "Enter the time interval separated by a comma")
def main(coords_wgs84, time_interval):
    try:
        coords = [float(x) for x in coords_wgs84.split(',')]
        interval = [interval for interval in time_interval.split(',')]
        print(coords)
        print(interval)
    except AttributeError:
        pass

    image = sentinel2_image(log = logging)
    bbox, _ = image.aoi()
    image.true_color(bbox = bbox)



if __name__ == "__main__":
    main()