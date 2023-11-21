"""
Upload COG raster data to Google Cloud
"""
import os
from rasterio.io import MemoryFile
from google.cloud import storage
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

import logging
from logging import config
config.fileConfig("logger.ini")

class cog_upload:
    """Upload COG from memory"""

    def __init__(
            self, 
            log: isinstance = None,
            project_id: str = None,
            bucket :str = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
            project_id: GCP project ID.
            bucket: Bucket in GCP storage.
        """
        self.log = log
        self.client = storage.Client(project = project_id)
        self.bucket = self.client.bucket(bucket)
    
    def memory(
            self, 
            input_tiff_path: str = None):
        """Upload to GCP from memory"""
        # Folder path
        local_folder = os.path.dirname(os.path.realpath(input_tiff_path))
        filename = os.path.basename(input_tiff_path).split('.')[0]
        bucket_file_path = os.path.join(local_folder, f"{filename}_cog.tiff")
        blob = self.bucket.blob(bucket_file_path)

        dst_profile = cog_profiles.get("deflate")
        with MemoryFile() as mem_dst:
            # Important, we pass `mem_dst.name` as output dataset path
            cog_translate(input_tiff_path, mem_dst.name, dst_profile, in_memory=True)  
            with mem_dst.open() as ds:
                blob.upload_from_file(ds)

if __name__ == "__main__":
    cog = cog_upload(log = logging)
    cog.memory(input_tiff_path = "data/processed/Sentinel2_visual_processed_cog.tiff")
