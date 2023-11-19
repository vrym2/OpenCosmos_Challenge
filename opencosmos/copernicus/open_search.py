"""
    Copernicus data space open search
"""
import numpy as np
import requests
import pandas as pd
from datetime import date, datetime

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
        min_date_str = min_date_object.strftime("%Y-%m-%dT%H:%M:%S")
        max_date_object = datetime.combine(date_object, datetime.max.time())
        max_date_str = max_date_object.strftime("%Y-%m-%dT%H:%M:%S")   
        return min_date_str, max_date_str

    def cloud_cover(self, max_cloud_percentage: np.int16 = 10)-> str:
        r"""Set the cloud cover percentage
        
        Args:\n
            max_cloud_percentage: Maximum cloud percentage

        """
        return f"cloudCover=[0,{str(max_cloud_percentage)}]"
    
    def search_time_range(
            self, 
            start_date:str = None, 
            end_date:str = None)-> str:
        r"""Set search time range
        
        Args:\n
            start_date: Search start date.
            end_date: search end date.
        """
        self.search_start_date, _ = copernicus_api_search.date_object(date_str = start_date)
        _, self.search_end_date = copernicus_api_search.date_object(date_str = end_date) 
        return self.search_start_date, self.search_end_date 

    def max_records(self, max_records: np.int16 = 10)-> str:
        r"""Number of maximum records
        
        Args:\n
            max_records: Number of maximum records
        """
        return f"maxRecords={str(max_records)}"
    
    def bbox(self, bbox_str:str = "4,51,4.5,52")-> str:
        r"""Get the Bounding box
        
        Args:\n
            bbox_str: String of bounding box coordinates.
        """
        return f"box={bbox_str}"

    def construct_url():
        # TODO
        pass

import requests
import logging
from logging import config
from opencosmos.copernicus import copernicus_api
from opencosmos.utils import Loader
from dotenv import load_dotenv

load_dotenv()
config.fileConfig("logger.ini")

url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products(a5ab498a-7b2f-4043-ae2a-f95f457e7b3b)/$value"

api = copernicus_api(log = logging)
access_token = api.get_access_token()
headers = {"Authorization": f"Bearer {access_token}"}

session = requests.Session()
session.headers.update(headers)
response = session.get(url, headers=headers, stream=True)

loading = Loader("Downloading", "That was fast", 0.05).start()
with open("product.zip", "wb") as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            file.write(chunk)
loading.stop()                                                                                                                                                                                                                            