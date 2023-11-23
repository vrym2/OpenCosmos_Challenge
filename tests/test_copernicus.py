"""Testing copernicus data functions"""
import os
import logging
from logging import config
from dotenv import load_dotenv
from opencosmos.copernicus import copernicus_api

# Loading environment variables
config.fileConfig("logger.ini")
load_dotenv()


def test_access_token():
    """Testing access token"""
    api = copernicus_api(log=logging)
    token = api.get_access_token()
    assert token is not None
