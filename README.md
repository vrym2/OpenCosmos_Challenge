# [Open Cosmos](https://www.open-cosmos.com/) <img src="./assets/logos/open_cosmos_logo.png" width="30" height="30">
Aim High, Go Beyond! 🌍

## Data Engineering Challenge
This repository consists of the scripts developed for the data engineering challenge presented by Open Cosmos Ltd.

### Instructions

1. Make sure you have Google Cloud Storage API enabled for this Google Cloud project. Please click [here](docs/google_cloud.md) for the instructions.

2. Install the `environment.yml` or `requirements.txt` in your virtual environment.

```
$ conda env create -f environment.yml # or
$ source activate venv
$ pip install -r requirements.txt
```

3. Run the below command to crate the `SentinelHub` configuration file.

```
$ sentinelhub.config --show
```

4. If you have the [Sentinel Hub](https://apps.sentinel-hub.com/dashboard/#/) account, please create a new OAuth client in your user dash board, and add client 'ID' and client 'SECRET' to the `.env` variables below. For instructions, please click [here](https://sentinelhub-py.readthedocs.io/en/latest/configure.html).

```
$ export SH_CLIENT_ID=xxxxxxxxxx
$ export SH_CLIENT_SECRET=xxxxxxxx
``` 

### Usage

1. To download the a sentinel 2 true-color COG (Cloud Optimised GeoTIFF) data, run the following command. All the workflow scripts have CLI interface, so if you'd like to understand the input arguments, add the tag `--help` at the end of the command.

Input arguments:

  - coords_wgs84:
    - You can get required bounding box coordinates (WGS84) with [bbox finder](http://bboxfinder.com/#0.000000,0.000000,0.000000,0.000000) website. 

  - resolution:
    - Desired resolution (10m, 20m, 60m), if the given bounding box extends to multiple Kms, use lower resolutions (60m) to avoid errors.

  - time_interval:
    - Time range expressed in YYYY-MM-DD, YYYY-MM-DD format.

Returns:

  - COG and PNG formatted files, in `data/png` and  `data/tiff` folders.

```
$ python opencosmos/sh/s2_download.py --help
```

2. To get the overview of an image in `webp` format, with the size not greater than 500kb and shape 500 x 500 px, run the following command.

Input arguments:

  - png_file:
    - Relative path to the downloaded `PNG` file.

Returns:

  - `WEBP` formatted image, in `data/png` folder. 
```
$ python opencosmos/utils/img_format.py
```

3. Perform Google Cloud Authentication.

Input arguments:

  - project_id:
    - project ID that has been set.

Returns:

  - Logger message of the authentication status.

```
$ python opencosmos/gcp/gcloud_auth.py
```

4. Upload files to the Google Cloud Storage.

Input Arguments:

  - project_id:
    - project ID that has been set.
  
  - local_filepath:
    - Relative path to the file that needs uploading.

  - bucket_path:
    - Absolute path of where the file is getting uploaded.
    __Note__: The path must start with the bucket's name

```
$ python opencosmos/gcp/gcloud_upload.py
```

## ✨ Thank you Open Cosmos for the challenge ✨

Contributors of this work 👷 

<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://www.open-cosmos.com/"><img src="https://media.licdn.com/dms/image/C560BAQEyGxkRca65Wg/company-logo_200_200/0/1630649632519/opencosmos_logo?e=1707955200&v=beta&t=NEu63PndobhMvC2JedcX1uVUTz9bxThWsKQqtJioyZo" width="100px;" alt=""/><br /><sub><b>Ground segment Team</b></sub></a><br /><a href="#projectManagement-OC" title="Project Management">📆</a></td>
      <td align="center"><a href="https://github.com/vrym2"><img src="https://avatars.githubusercontent.com/u/93340339?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Raj</b></sub></a><br /><a href="https://github.com/SpaceParkLeicester/Planet/commits?author=vrym2" title="Code">💻</a></td>
    </tr>
  </tbody>
</table>     