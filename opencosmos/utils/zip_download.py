"""Function to download zip files"""
import os
import time
from typing import Dict
from zipfile import ZipFile, error

import requests
from tqdm import tqdm


class download_from_url:
    """Function to download from url

    Source: https://stackoverflow.com/questions/37573483/progress-bar-while-download-file-over-http-with-requests
    """  # noqa : E501

    def __init__(self, log: isinstance = None, url_link: str = None, headers: Dict = None) -> None:
        """Defining variables

        Args:
            log: Custom logger file
            url_link: URL link of downloadable file
            headers: Headers of the URL link
        """
        self.log = log
        self.url_link = url_link
        self.headers = headers

    def commence(self, file_path: str = None) -> None:
        """Begin downloading

        Args:
            file_path: Path of the downloaded file with extension
        """
        self.log.info("Begin downloading")
        session = requests.Session()
        session.headers.update(self.headers)
        response = session.get(self.url_link, headers=self.headers, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        with open(file_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        self.log.info("Download finished")
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            self.log.debug("ERROR, something went wrong")

    def extract_data(self, file_path: str = None, extract_path: str = None):
        """Extract downloaded data

        Args:
            file_path: Path to the downloaded file
            extract_path: Destination of extraction
        """
        self.log.info(f"Begin extracting the zip file: {file_path}")
        with ZipFile(file_path, "r") as zip_ref:
            for member in tqdm(zip_ref.infolist(), desc="Extracting"):
                try:
                    zip_ref.extract(member, extract_path)
                except error:
                    self.log.debug("e")

        self.log.info("Extraction finished")

        # Deleting the zip file
        os.remove(file_path)


class download_data_from_url(download_from_url):
    """Download zip files"""

    def __init__(self, log: isinstance = None, url_link: str = None, headers: Dict = None) -> None:
        r"""Defining variables

        Args:\n
            log: Custom "logger" file
            url_link: Link to the downloadable URL
            headers: Headers of the URL link
        """
        super().__init__(log, url_link, headers)
        self.log = log

    @staticmethod
    def is_downloadable(url_link: str = None) -> bool:
        r"""Checking if a URL link is downloadable

        Args:\n
            url_link: A URL link.
        """
        # Source: https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un # noqa: E501
        h = requests.head(url_link, allow_redirects=True)
        header = h.headers
        content_type = header.get("content-type")
        if "text" in content_type.lower():
            return False
        elif "html" in content_type.lower():
            return False
        else:
            return True

    def main(self, download_path: str = None, file_name: str = None) -> None:
        """Function to download and extract files

        Args:
            download_path: Path of the download folder
            file_name: Name of the file downloading without ext
        """
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        file_path = os.path.join(download_path, f"{file_name}.zip")

        if len(os.listdir(download_path)) == 0:
            self.log.info(f"{download_path} appears to be empty!")
            if self.is_downloadable(self.url_link):
                # Downloading
                super().commence(file_path)
                time.sleep(10)

                # Extracting
                super().extract_data(file_path, download_path)
            else:
                self.log.debug("URL link is not downloadable")
        else:
            self.log.info(f"{file_name} already exists in {download_path}")
