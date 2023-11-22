"""
    Copernicus data space open search
"""
import click
import numpy as np
import requests
import pandas as pd
from datetime import datetime
import logging
from logging import config
config.fileConfig("logger.ini")
class copernicus_api_search:
    """Copernicus data space search"""

    def __init__(
            self,
            log: isinstance = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log

        # HTTP request links                            
        self.base_link = "http://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?"  

    @staticmethod
    def date_object(date_str: str = None)-> datetime:
        """Convert date string to date time object"""
        date_object = datetime.strptime(date_str, "%Y-%m-%d").date()
        min_date_object = datetime.combine(date_object, datetime.min.time())
        min_date_str = min_date_object.strftime("%Y-%m-%dT%H:%M:%SZ")
        max_date_object = datetime.combine(date_object, datetime.max.time())
        max_date_str = max_date_object.strftime("%Y-%m-%dT%H:%M:%SZ")   
        return min_date_str, max_date_str

    @staticmethod
    def cloud_cover(max_cloud_percentage: np.int16 = 10)-> str:
        r"""Set the cloud cover percentage
        
        Args:\n
            max_cloud_percentage: Maximum cloud percentage

        """
        return f"cloudCover=[0,{str(max_cloud_percentage)}]"
    
    @staticmethod
    def search_date_range(
            start_date:str = "2022-06-11", 
            end_date:str = "2022-06-22")-> str:
        r"""Set search time range
        
        Args:\n
            start_date: Search start date.
            end_date: search end date.
        """
        search_start_date, _ = copernicus_api_search.date_object(date_str = start_date)
        _, search_end_date = copernicus_api_search.date_object(date_str = end_date) 
        search_date_range = f"startDate={search_start_date}&completionDate={search_end_date}"
        return search_date_range 

    @staticmethod
    def max_records(max_records: np.int16 = 10)-> str:
        r"""Number of maximum records
        
        Args:\n
            max_records: Number of maximum records
        """
        return f"maxRecords={str(max_records)}"
    
    @staticmethod
    def bbox(bbox_str:str = "4,51,4.5,52")-> str:
        r"""Get the Bounding box
        
        Args:\n
            bbox_str: String of bounding box coordinates.
        """
        return f"box={bbox_str}"

    @staticmethod
    def search_results(url: str = None)-> pd.DataFrame:
        r"""Request search criteria
        
        Args:\n
            url: constructed url.
        """
        json = requests.get(url).json()
        return pd.DataFrame.from_dict(json['features'])
    
    def construct_url(
            self,
            max_cloud_percentage: np.int16 = 10,
            search_start_date: str = "2022-01-01",
            search_end_date: str = "2022-03-31",
            max_records: np.int16 = 10,
            bbox_str:str = "24.5,42.5,25,43"):
        r"""Constructing the API url
        
        Args:\n
            max_cloud_percentage: Maximum cloud percentage.
            search_start_date: Start date of the search.
            search_end_date: End date of the search.
            max_records: Maximum records
            bbox_str: String format bbox coordinates
        """
        base_url = "https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?productType=S2MSI1C"
        cloud_cover = copernicus_api_search.cloud_cover(max_cloud_percentage = max_cloud_percentage)
        search_date_range = copernicus_api_search.search_date_range(start_date = search_start_date, end_date = search_end_date)
        max_records = copernicus_api_search.max_records(max_records = max_records)
        bbox = copernicus_api_search.bbox(bbox_str = bbox_str)
        elements = [base_url, cloud_cover, search_date_range, max_records, bbox]
        url = "&".join(elements) 
        return url
    
    def filter_search(self, df: pd.DataFrame = None)-> str:
        """Filter through search results"""
        # TODO
        pass

@click.command()
@click.option("--max_cloud_percentage", type = np.int16, default = 10, help = "Maximum cloud cover percentage")
@click.option("--search_start_date", type = str, default = "2022-01-01", help = "Search start date")
@click.option("--search_end_date", type = str, default = "2022-03-31", help  ="Search end date")
@click.option("--max_records", type = np.int16, default = 10, help = "Maximum records filtered")
@click.option("--bbox_str", type = str, default = "24.5,42.5,25,43", help = "BBox coordinates in a string format")
def main(max_cloud_percentage, search_start_date, search_end_date, max_records, bbox_str):
    """Script to search Sentinel 2 data"""

    # Getting the URL
    api = copernicus_api_search(log = logging)
    url = api.construct_url(
        max_cloud_percentage = max_cloud_percentage,
        search_start_date = search_start_date,
        search_end_date = search_end_date,
        max_records = max_records,
        bbox_str = bbox_str
    )
    logging.info(f"URL for the search criteria: '{url}'")

    # Getting the first product ID of the search result
    df = api.search_results(url = url)
    product_id = df["id"].iloc[0]
    logging.info(f"First Product ID of the search result: '{product_id}'")

if __name__ == "__main__":
    main()



                                                                                                                                                                                                                          