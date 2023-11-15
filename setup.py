""" Usual setup file for package """
# Sourced from OCF Template
# Source: https://github.com/openclimatefix/ocf_template
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
install_requires = (this_directory / "requirements.txt").read_text().splitlines()

setup(
    name="SPL_project",
    version="0.0.1",
    description="Your repository",
    author="Your name",
    author_email="kjt7@leicester.ac.uk",
    company="Space Park Leicester",
    install_requires=install_requires,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
)
