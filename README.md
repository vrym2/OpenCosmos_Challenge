# [Open Cosmos](https://www.open-cosmos.com/) <img src="./assets/logos/open_cosmos_logo.png" width="30" height="30">
✨ Aim High, Go Beyond! ✨

## Data Engineering Challenge
This repository consists of the scripts developed for the data engineering challenge presented by Open Cosmos Ltd.

### Instructions

1. Install the `environment.yml` or `requirements.txt` in your virtual environment.
```
$ conda env create -f environment.yml # or
$ source activate venv
$ pip install -r requirements.txt
```

2. Run the below command to crate the `SentinelHub` configuration file.
```
$ sentinelhub.config --show
```

3. If you have the [Sentinel Hub](https://apps.sentinel-hub.com/dashboard/#/) account, please create a new OAuth client in your user dash board, and add client 'ID' and client 'SECRET' to the `.env` variables below. For instructions, please click [here](https://sentinelhub-py.readthedocs.io/en/latest/configure.html).

```
$ export SH_CLIENT_ID=xxxxxxxxxx
$ export SH_CLIENT_SECRET=xxxxxxxx
``` 

### Usage

1. To download the a sentinel 2 image, run the following command.
```
$ python opencosmos/sentinel/s2_download.py
```