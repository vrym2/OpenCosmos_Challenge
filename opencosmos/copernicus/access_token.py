"""
Copernicus data space access token

Source: https://dataspace.copernicus.eu/
"""
import os
import requests


class copernicus_api:
    """Load the access token of Copernicus data space"""

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables

        Args:\n
            log: custom logger ini file
        """
        self.log = log
        self.username = os.environ["COPERNICUS_USERNAME"]
        self.password = os.environ["COPERNICUS_PASSWORD"]

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
                r = requests.post(
                    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                    data=data,
                )
                r.raise_for_status()
            except Exception:
                raise Exception(
                    f"Access token creation failed. Response from the server was: {r.json()}"
                )
            return r.json()["access_token"]

if __name__ == "__main__":
    import logging
    from logging import config
    config.fileConfig("logger.ini")
    from dotenv import load_dotenv
    load_dotenv()

    api = copernicus_api(log = logging)
    access_token = api.get_access_token()

    try:
        assert access_token is not None
    except AssertionError:
        logging.debug(f"Please provide authentic credentials")
    else:
        logging.info(f"Your access token: {access_token}")