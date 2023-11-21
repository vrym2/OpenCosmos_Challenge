# [Open Cosmos](https://www.open-cosmos.com/) <img src="./assets/logos/open_cosmos_logo.png" width="30" height="30">
Aim High, Go Beyond! 🌍

## Data Engineering Challenge
This repository consists of the scripts developed for the data engineering challenge presented by Open Cosmos Ltd.

### Instructions

1. Make sure you have Google Cloud Storage API enabled for this Google Cloud project. Please click [here](docs/google_cloud.md) for the instructions.

2. Install `GDAL` on your machine.

```
$ sudo apt update
$ sudo apt install libpq-dev gdal-bin libgdal-dev
$ gdalinfo --version
```

3. Install the `environment.yml` or `requirements.txt` in your virtual environment.

```
$ conda env create -f environment.yml # or
$ source activate venv
$ pip install -r requirements.txt
$ pip install GDAL==$(gdalinfo --version)
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

## Usage

Please click [here](docs/usage_instructions.md) to go the usage instructions.

## Notes

* Blocking issue  - [16Bit raster image](https://help.seequent.com/Oasismontaj/2023.1/Content/gxhelp/g/geosoft_gx_gridUtils_CopyConvertMultiGrids.htm)

* [GDAL CLoud Optimised GeoTiff generator](https://gdal.org/drivers/raster/cog.html)

* [8 and 12 bit JPEG in Tiff](https://trac.osgeo.org/gdal/wiki/TIFF12BitJPEG)

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
