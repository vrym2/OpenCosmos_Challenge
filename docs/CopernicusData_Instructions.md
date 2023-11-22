## [Copernicus Data Service Ecosystem](../opencosmos/copernicus/)

### Instructions of Usage

1. Before using the download and processing scripts, please provide [CDSE](https://dataspace.copernicus.eu/) username and password in `.env` variables. Please register if you do not have an account.

```
$ export COPERNICUS_USERNAME=xxxxxx
$ export COPERNICUS_PASSWORD=xxxxxx
$ python opencosmos/copernicus/access_token.py
```

2. Search with script arguments to get Sentinel 2 product IDs. Default arguments are already loaded if you prefer to see the functionality of the workflow.

```
$ python opencosmos/copernicus/open_search.py # Default input arguments
$ python opencosmos/copernicus/open_search.py --help
```

3. Download Sentinel 2 data product with a given product ID. Default product ID is already loaded.

```
$ python opencosmos/copernicus/product_download.py # Default
$ python opencosmos/copernicus/product_download.py --help
```

4. Process Sentinel 2 data to get Visual RGB bands.

```
$ python opencosmos/copernicus/sentinel_bands.py # Default
$ python opencosmos/copernicus/sentinel_bands.py --help
```

5. Convert GeoTIFF to Cloud Optimised GeoTIFF (COG), and store the metadata.

```
$ python opencosmos/copernicus/cog.py # Default
$ python opencosmos/copernicus/cog.py -- help
```
