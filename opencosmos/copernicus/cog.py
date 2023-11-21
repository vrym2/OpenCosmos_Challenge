"""
Convert GeoTIFFs to Cloud Optimised GeoTIFFs
"""
import os
import click
import rasterio as rio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles
from opencosmos.utils import Loader
import logging
from logging import config
config.fileConfig("logger.ini")

class cloud_optimised_geotiff:

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log
    
    def cog_convert(self, input_tiff_path: str = None):
        r"""Convert Geotiff to COG
        
        Args:\n
            input_tiff_path: Path to the untilled Geotiff image.
        """
        # File paths
        output_cog_tiff = os.path.basename(input_tiff_path).split('.')[0]
        output_folder = os.path.dirname(os.path.realpath(input_tiff_path))
        output_cog_tiff = os.path.join(output_folder, f"{output_cog_tiff}_cog.tiff")
        
        # Read Geotiff data
        tiff = rio.open(input_tiff_path)
        bounds = tiff.bounds
        width = tiff.width
        height = tiff.height
        nbands = 3
        img_array = tiff.read(1)
        src_transform = from_bounds(*bounds, width=width, height=height)
        src_profile = dict(
            driver="GTiff",
            dtype=tiff.dtypes[0],
            count=nbands,
            height=height,
            width=width,
            crs="epsg:4326",
            transform=src_transform)
        
        # Convert to COG
        loading = Loader("Converting GeoTIFF to Cloud Optimised GeoTIFF...", "That was fast", 0.05).start()
        with MemoryFile() as memfile:
            with memfile.open(**src_profile) as mem:
                mem.write(img_array, indexes=3)
                dst_profile = cog_profiles.get("deflate")
                cog_translate(
                    mem,
                    output_cog_tiff,
                    dst_profile,
                    in_memory=True,
                    quiet=True,)
        loading.stop()    
            

@click.command()
@click.option("--input_tiff_path", type = str, help = "Path to the untilled GeoTiff file")
def main(input_tiff_path):
    sentinel_data = cloud_optimised_geotiff(log = logging)
    sentinel_data.cog_convert(input_tiff_path = input_tiff_path)

if __name__ == "__main__":
    main()