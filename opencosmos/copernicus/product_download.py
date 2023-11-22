"""
Copernicus API download

"""
import click
import os
import logging
from logging import config
from opencosmos.copernicus import copernicus_api
from opencosmos.utils import download_data_from_url
from dotenv import load_dotenv

load_dotenv()
config.fileConfig("logger.ini")

class copernicus_data_download(copernicus_api):
    """Copernicus API download"""

    def __init__(self, log: isinstance = None, product_id: str = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
            product_id: Sentinel product ID.
        """
        self.log = log
        self.product_id = product_id

        # Copernicus Access token
        super().__init__(log)
        access_token = super().get_access_token()

        # Product URL
        self.url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"

        self.headers = {"Authorization": f"Bearer {access_token}"}        

    def commence(self)-> None:
        """Begin downloading"""

        # Creating the download folder
        download_folder = os.path.join("data", "downloads")
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        download = download_data_from_url(log = self.log, url_link = self.url, headers = self.headers)
        download.main(download_path = download_folder, file_name = f"{self.product_id}")

@click.command()
@click.option("--product_id", type = str, default = "42f56c90-9613-5271-9e28-44a968e11c7d", help = "Sentinel2 product ID")
def main(product_id):
    """Function to download Sentinel 2 product"""
    download = copernicus_data_download(log = logging, product_id = product_id)
    download.commence()

if __name__ == "__main__":
    main()