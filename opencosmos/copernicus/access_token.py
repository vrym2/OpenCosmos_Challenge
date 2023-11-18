"""
    Copernicus data space access token

    Source: https://dataspace.copernicus.eu/
"""
import os
import json
import requests
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

class copernicus_api:
    """Load the access token of Copernicus data space"""

    def __init__(
            self,
            log: isinstance = None,
            username: str = None,
            password:str = None) -> None:
        """Defining variables
        
        Args:\n
            log: custom logger ini file
        """
        self.log = log

        if username and password is None:
            self.username = os.environ["COPERNICUS_USERNAME"]
            self.password = os.environ["COPERNICUS_PASSWORD"]
        else:
            self.username = username
            self.password = password

    def get_access_token(self) -> str:
        """Function to get the access token"""

        try:
            assert self.username is not None
            assert self.password is not None
        except AssertionError:
            self.log.debug("Please provide username and password in env variables")
        else:
            data = {
                "client_id": "cdse-public",
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
                }
            try:
                r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                data=data,
                )
                r.raise_for_status()
            except Exception as e:
                raise Exception(
                    f"Access token creation failed. Response from the server was: {r.json()}"
                    )
            return r.json()["access_token"]
        