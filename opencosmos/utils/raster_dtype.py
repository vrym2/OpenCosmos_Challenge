import click
from osgeo import gdal
import numpy as np
from skimage import exposure
from PIL import Image
from opencosmos.utils import Loader
import logging
from logging import config
config.fileConfig("logger.ini")

class raster_convert:
    """Convert raster data type"""

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log

    def dtype_to_uint8(self, input_tiff_path, output_tiff_path):
        r"""Convert he dtype from unit16 ro uint8
        
        Args:\n
            input_tiff_path: An input tiff with dtype of unit16
            output_tiff_path: Path to an output tiff file. 
        """
        # Load the GeoTIFF raster
        loading = Loader("Converting the data type of raster...", "That was fast", 0.05).start()
        dataset = gdal.Open(input_tiff_path)
        raster_data_uint16 = dataset.GetRasterBand(1).ReadAsArray()

        # Perform the conversion from uint16 to uint8
        raster_data_uint8 = exposure.rescale_intensity(raster_data_uint16, in_range='uint16', out_range='uint8').astype(np.uint8)

        # Create a new GeoTIFF file for the uint8 data
        driver = gdal.GetDriverByName('GTiff')
        output_dataset = driver.Create(output_tiff_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)

        # Copy the spatial information from the original dataset
        output_dataset.SetGeoTransform(dataset.GetGeoTransform())
        output_dataset.SetProjection(dataset.GetProjection())

        # Write the uint8 data to the new GeoTIFF file
        output_dataset.GetRasterBand(1).WriteArray(raster_data_uint8)
        output_image = Image.fromarray(raster_data_uint8)
        output_image.save(output_tiff_path)
        loading.stop()
        self.log.info(f"Find the converted raster file here: {output_tiff_path}")

@click.command()
@click.option("--input_tiff_path", type = str, help = "A Geotiff file with data type unit16")
@click.option("--output_tiff_path", type = str, help = "An output tiff path")
def main(input_tiff_path, output_tiff_path):
    """Run the pipeline"""
    raster = raster_convert(log = logging)
    raster.dtype_to_uint8(
        input_tiff_path = input_tiff_path,
        output_tiff_path = output_tiff_path)

if __name__ == "__main__":
    main()