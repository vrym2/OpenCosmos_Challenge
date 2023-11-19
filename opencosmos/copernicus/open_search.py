"""
    Copernicus data space open search
"""
import numpy as np
import requests
import pandas as pd
from datetime import date, datetime

class copernicus_api_search:
    """Copernicus data space search"""

    json = requests.get("https://catalogue.dataspace.copernicus.eu/resto/api/collections/Sentinel2/search.json?productType=S2MSI1C&cloudCover=[0,10]&startDate=2022-06-11T00:00:00Z&completionDate=2022-06-22T23:59:59Z&maxRecords=10&box=4,51,4.5,52").json()


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

    @staticmethod
    def cloud_cover(max_cloud_percentage: np.int16 = 10)-> str:
        r"""Set the cloud cover percentage
        
        Args:\n
            max_cloud_percentage: Maximum cloud percentage

        """
        return f"cloudCover=[0,{str(max_cloud_percentage)}]"
    
    @staticmethod
    def search_time_range(
            start_date:str = "2022-06-11", 
            end_date:str = "2022-06-22")-> str:
        r"""Set search time range
        
        Args:\n
            start_date: Search start date.
            end_date: search end date.
        """
        search_start_date, _ = copernicus_api_search.date_object(date_str = start_date)
        _, search_end_date = copernicus_api_search.date_object(date_str = end_date) 
        # TODO, needs the date time to end with Z UTC coordinates
        return search_start_date, search_end_date 

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
        return f"bbox={bbox_str}"

    def construct_url(
            self,
            max_cloud_percentage: np.int16 = 10,
            search_start_date: str = "2022-06-11",
            search_end_date: str = "2022-06-22",
            max_records: np.int16 = 10,
            bbox_str:str = "4,51,4.5,52"):
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
        start_date, end_date = copernicus_api_search.search_time_range(start_date = search_start_date, end_date = search_end_date)
        max_records = copernicus_api_search.max_records(max_records = max_records)
        bbox = copernicus_api_search.bbox(bbox_str = bbox_str)
        elements = [base_url, cloud_cover, start_date, end_date, max_records, bbox]
        url = "&".join(elements) 
        return url

if __name__ == "__main__":
    import logging
    from logging import config
    config.fileConfig("logger.ini")

    api = copernicus_api_search(log = logging)
    api.cloud_cover()
    api.search_time_range()
    api.max_records()
    api.bbox()
    url = api.construct_url()
    print(url)
# import requests
# import logging
# from logging import config
# from opencosmos.copernicus import copernicus_api
# from opencosmos.utils import Loader
# from dotenv import load_dotenv

# load_dotenv()
# config.fileConfig("logger.ini")

# url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products(a5ab498a-7b2f-4043-ae2a-f95f457e7b3b)/$value"

# api = copernicus_api(log = logging)
# access_token = api.get_access_token()
# headers = {"Authorization": f"Bearer {access_token}"}

# session = requests.Session()
# session.headers.update(headers)
# response = session.get(url, headers=headers, stream=True)

# loading = Loader("Downloading", "That was fast", 0.05).start()
# with open("product.zip", "wb") as file:
#     for chunk in response.iter_content(chunk_size=8192):
#         if chunk:
#             file.write(chunk)
# loading.stop()                                                                                                                                                                                                                            