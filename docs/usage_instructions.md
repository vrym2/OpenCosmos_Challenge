### Instructions of Usage

1. To download the a sentinel 2 true-color COG (Cloud Optimised GeoTIFF) data, run the following command. All the workflow scripts have CLI interface, so if you'd like to understand the input arguments, add the tag `--help` at the end of the command.

Source: https://sentinelhub-py.readthedocs.io/en/latest/index.html

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
