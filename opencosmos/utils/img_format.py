"""
    Image formatting
"""
import os
import click
from PIL import Image
from pathlib import Path
import logging
from logging import config
logging.getLogger("PIL").setLevel(logging.WARNING)
config.fileConfig("logger.ini")

class sentinel_image_webp:
    """Preparing WebP formats of sentinel data"""
    def __init__(
            self,
            log: isinstance = None) -> None:
        """Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log

    @staticmethod
    def convert_to_webp(source):
        """Convert image to WebP.

        Args:
            source (pathlib.Path): Path to source image

        Returns:
            pathlib.Path: path to new image
        """
        destination = source.with_suffix(".webp")

        image = Image.open(source)  # Open image
        resized_img = image.resize((500, 500), Image.LANCZOS)
        resized_img.save(destination, format="webp", quality = 50)  # Convert image to webp

        return destination
    
    def png_to_webp(self, png_file:str = None):
        """Converting a PNG file to WEBP format"""
        try:
            png_file_path = Path(png_file)
            assert png_file_path.suffix == ".png"
        except AssertionError:
            self.log.debug(f"Please provide a .png file")
        else:
            pre_file_size = round(os.stat(png_file).st_size/(1024 * 1024), 2)
            self.log.info(f"Size of the PNG file: {pre_file_size} MB")
            pre_file = Image.open(png_file)
            self.log.info(f"PNG File shape: {pre_file.size}")

            webp_file = self.convert_to_webp(source = png_file_path)
            
            post_file_size = round(os.stat(webp_file.as_posix()).st_size/(1024 * 1024), 2)
            self.log.info(f"File size of the converted webp format: {post_file_size} MB")
            post_file = Image.open(webp_file)
            self.log.info(f"WEBP File shape: {post_file.size}")

            self.log.info(f"Find the converted file here: {webp_file}")

@click.command()
@click.option("--png_file", type = str, help = "path to a PNG file")
def main(png_file):
    """Preparing WEBP format files"""
    src = sentinel_image_webp(log = logging)
    src.png_to_webp(png_file = png_file)

if __name__ == "__main__":
    main()