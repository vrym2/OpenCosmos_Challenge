"""
    Upload data to Google Cloud Storage 
"""

import os
import click
import logging
from logging import config
import shutil
import subprocess as sp
from google.cloud import storage
from google.api_core.exceptions import NotFound
from opencosmos.utils import Loader

config.fileConfig("logger.ini")

class Google_Cloud_Storage:
    """Class function related to Google Buckets"""
    def __init__(
            self,
            project_id: str = None,
            local_filepath: str = None,
            bucket_path:str = None,
            log: isinstance = None) -> None:
        """Initiating Google Client
        
        Args:
            local_filepath: Relative path of the file needs to be uploaded
            bucket_path: bucket path of the file uploading
            log: instance of custom logger function
        """
        self.log = log
        self.local_filepath = local_filepath
        self.bucket_path = bucket_path
        self.client = storage.Client(project = project_id)
    
    def upload(self)-> None:
        """Uploading to the GCP buckets"""
        # Getting the filename
        self.filename = os.path.basename(self.local_filepath)
        self.abs_filepath = os.path.join(os.getcwd(), self.local_filepath)

        if os.path.exists(self.abs_filepath):
            # Listing files in the bucket
            self.bucket_name = self.bucket_path.split('/')[0]
            self.blobs = self.client.list_blobs(self.bucket_name)
            try:
                self.bucket_files = [blob.name.split('/')[-1] for blob in self.blobs]
            except NotFound:
                self.log(f"bucket{self.bucket_name} is not found in GCP")
            else:
                if self.filename not in self.bucket_files:
                    self.log.info(f"file {self.filename} not found in GCP")
                    loading = Loader("Commencing upload.....", "Well, That was fast!", 0.05).start()
                    # Uploading file
                    sp.check_call(f'gsutil cp -r {self.abs_filepath} gs://{self.bucket_path}', 
                                shell = True, stdout = sp.PIPE)
                    loading.stop()
                    self.log.info("Upload finished")
                else:
                    self.log.debug(f"{self.filename} exists in GCP")
        else:
            self.log.debug(f"file {self.local_filepath} does not exist")

    def remove_uploaded_files(self)-> None:
        """Removing files from local system"""
        # Removing file
        if os.path.exists(self.abs_filepath):
            shutil.rmtree(self.abs_filepath, ignore_errors = True)
        else:
            self.log.debug(f"file {self.abs_filepath} does not exist")

@click.command()
@click.option("--project_id", type = str, help = "Google Cloud project ID")
@click.option("--local_filepath", type = str, help = "path to the upload file")
@click.option("--bucket_path", type = str, help = "Set a Google Cloud Storage bucket path")
def main(project_id, local_filepath, bucket_path):
    """Uploading a file to the storage"""
    gcloud = Google_Cloud_Storage(
        log = logging,
        project_id = project_id,
        local_filepath = local_filepath,
        bucket_path = bucket_path)
    gcloud.upload()

if __name__ == "__main__":
    main()