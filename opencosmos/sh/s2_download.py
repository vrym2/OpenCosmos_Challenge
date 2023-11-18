"""
Download Sentinel 2 images
"""
import logging
import os
from logging import config
from typing import Tuple

import click
import numpy as np
from dotenv import load_dotenv
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    MimeType,
    MosaickingOrder,
    SentinelHubRequest,
    bbox_to_dimensions,
)

from opencosmos.sh import sentinelhub_config, sentinelhub_eval_scripts
from opencosmos.utils import Loader

config.fileConfig("logger.ini")

# Loading the environment variables
load_dotenv()


class sentinel2_image:
    """Functions related to SentinelHub"""

    mime_type = {"png": MimeType.PNG, "tiff": MimeType.TIFF}

    @staticmethod
    def sh_request_config(download_file_type: str = "png", eval_script: str = "true_color"):
        """Configuring the SH request"""
        mime_type = sentinel2_image.mime_type[download_file_type]
        if eval_script == "true_color":
            eval_script = sentinelhub_eval_scripts.true_color
        elif eval_script == "cloud_mask":
            eval_script == sentinelhub_eval_scripts.cloud_mask
        elif eval_script == "all_bands":
            eval_script == sentinelhub_eval_scripts.all_bands
        elif eval_script == "dem":
            eval_script == sentinelhub_eval_scripts.dem
        else:
            eval_script is None
        return mime_type, eval_script

    def __init__(self, log: isinstance = None, instance_id: str = "open-cosmos") -> None:
        """Defining variables

        Args:\n
            log: custom logger ini file.
        """
        self.log = log
        # Sentinel hub configuration
        sh = sentinelhub_config(log=log)
        self.sh_config = sh.save(instance_id=instance_id)

    def aoi(self, coords_wgs84: Tuple = (46.16, -16.15, 46.51, -15.58), resolution: np.int16 = 10):
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
            self.bbox = BBox(bbox=coords_wgs84, crs=CRS.WGS84)
            self.bbox_size = bbox_to_dimensions(self.bbox, resolution=resolution)
            self.log.info(f"Image shape at {resolution} m resolution: {self.bbox_size} pixels")
            return self.bbox, self.bbox_size

    def download(
        self,
        time_interval: Tuple = ("2020-06-01", "2020-06-30"),
        download_file_type: str = "png",
        eval_script: str = "true_color",
    ):
        """Downloading True color mosaic

        Args:\n
            time_interval: self explanatory
            download_file_type: "PNG" or "TIFF"
            eval_script: Different evaluation scripts, found in "eval_scripts.py"
        """
        # Sentinel Hub request configuration
        mime_type, eval_script = self.sh_request_config(download_file_type, eval_script)

        # Create the folder to download
        download_folder = os.path.join("data", f"{download_file_type}")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Sanity check
        if not self.sh_config.sh_client_id or not self.sh_config.sh_client_secret:
            self.log.debug(
                "Warning! To use Process API, please provide the credentials (OAuth client ID and client secret)."
            )
        else:
            loading = Loader(
                f"Downloading the {download_file_type.upper()} True color Mosaic...",
                "Well, That was fast",
                0.05,
            ).start()
            request_true_color = SentinelHubRequest(
                data_folder=download_folder,
                evalscript=eval_script,
                input_data=[
                    SentinelHubRequest.input_data(
                        data_collection=DataCollection.SENTINEL2_L1C,
                        time_interval=time_interval,
                        mosaicking_order=MosaickingOrder.LEAST_CC,
                    )
                ],
                responses=[SentinelHubRequest.output_response("default", mime_type)],
                bbox=self.bbox,
                size=self.bbox_size,
                config=self.sh_config,
            )
            request_true_color.get_data(save_data=True)
            loading.stop()

            self.log.info("The downloaded files are in the following directories")
            for folder, _, filenames in os.walk(request_true_color.data_folder):
                for filename in filenames:
                    self.log.info(f"{os.path.join(folder, filename)}")


@click.command()
@click.option(
    "--coords_wgs84",
    type=str,
    default="-0.18,51.46,-0.03,51.53",
    help="WGS84 bbox coords, separated by a comma",
)  # London coordinates
@click.option(
    "--resolution",
    type=np.int16,
    default=10,
    help="Resolution of the downloading bounding box image",
)
@click.option(
    "--time_interval",
    type=str,
    default="2020-06-01, 2020-06-30",
    help="Enter the time interval separated by a comma",
)
def main(coords_wgs84, time_interval, resolution):
    coords = [float(x) for x in coords_wgs84.split(",")]
    interval = [interval for interval in time_interval.split(",")]

    for file_type, _ in sentinel2_image.mime_type.items():
        image = sentinel2_image(log=logging)
        image.aoi(coords_wgs84=coords, resolution=resolution)
        image.download(
            time_interval=interval, download_file_type=file_type, eval_script="true_color"
        )


if __name__ == "__main__":
    main()
