"""
    Google Cloud Authentication
"""

import click
from google.cloud import storage
from google.api_core.exceptions import BadRequest

import logging
from logging import config
config.fileConfig("logger.ini")

class Google_Cloud_Authentication:
    """Functions related to authentication"""
    def __init__(
            self, 
            log: isinstance = logging,
            project_id:str = None) -> None:
        """Initiating the variables

        Args:
            log: Custom logger file
        """
        self.log = log
        self.project_id = project_id

    def authenticate(self):
        """Authenticate Google Cloud"""
        try:
            self.storage_client = storage.Client(project = self.project_id)
            self.buckets = self.storage_client.list_buckets()
            self.bucket_names = [bucket.name for bucket in self.buckets]
            self.log.info(f"List of buckets: {self.bucket_names}")
            self.log.info("Authentication successful")
        except BadRequest as b:
            self.log.debug("There was a problem with authentication")
            self.log.debug(f"{b}")

@click.command()
@click.option("--project_id", help = "Enter the project ID")
def main(project_id:str = None):
    gcloud = Google_Cloud_Authentication(project_id = project_id)
    gcloud.authenticate()

if __name__==  "__main__":
    main()