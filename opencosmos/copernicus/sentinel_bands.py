"""
Copernicus Sentinel visual bands
"""
import os
import click
from typing import Dict
import rasterio as rio
from opencosmos.utils import Loader
import logging
from logging import config
config.fileConfig("logger.ini")

class sentinel_bands:
    """Read Sentinel 2 bands"""

    band_types = {
        "visual" : ["B02", "B03", "B04"]
    }

    def __init__(
            self,
            log: isinstance = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log

    @staticmethod
    def find_files(root_dir, extension):
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(extension):
                    yield os.path.join(dirpath, filename)  

    @staticmethod
    def contains_any(string_list, larger_string):
        for substring in string_list:
            if substring in larger_string:
                return True
        return False  
      
    def sentinel_file_paths(
            self, 
            safe_file_path:str = None,
            band_type: str = "visual")-> None:
        r"""Get band file paths
        
        Args:\n
            safe_file: Path to the .SAFE sentinel file.
            band_type: Type of the band as defined above.
        """
        self.band_files = dict()
        file_list = sentinel_bands.find_files(safe_file_path, ".jp2")
        for file in file_list:
            file_name = os.path.basename(file).split('.')[0]
            status = sentinel_bands.contains_any(sentinel_bands.band_types[band_type], file_name)
            if status == True:
                band = file_name.split('_')[-1]
                self.band_files[band] = file
        return self.band_files
    
    def visual_bands(self, band_dict: Dict = None)-> None:
        """Read visual bands into a single file"""
        blue = rio.open(band_dict["B02"])
        green = rio.open(band_dict["B03"])
        red = rio.open(band_dict["B04"])

        # Output folder
        output_folder = os.path.join("data", "processed")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        file_path = os.path.join(output_folder, "Sentinel2_visual_process.tiff")
        loading = Loader("Reading RDB bands into a single file....", "Well, that was fast", 0.05).start()
        with rio.open(
            file_path,'w',driver='Gtiff', 
            width=blue.width, height=blue.height, count=3, 
            crs=blue.crs,transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
            rgb.write(blue.read(1),3) 
            rgb.write(green.read(1),2) 
            rgb.write(red.read(1),1) 
            rgb.close()        
        loading.stop()
        self.log.info(f"Find the RGB processed image here: {file_path}")
        
@click.command()
@click.option("--safe_file_path", type = str, help = "Path to the Sentinel 2 SAFE product file")
def main(safe_file_path):
    """Run the pipeline"""
    bands = sentinel_bands(log = logging)
    paths = bands.sentinel_file_paths(safe_file_path = safe_file_path)
    bands.visual_bands(band_dict = paths)

if __name__ == "__main__":
    main()
