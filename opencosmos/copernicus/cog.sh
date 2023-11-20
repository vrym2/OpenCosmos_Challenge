#!/bin/bash

Usage="Convert GeoTiif files to Cloud Optimised Geotiff

Inputs:
    Argument 1: Sentinel Visual RGB GeoTiff file.
    Argument 2: An output GeoTiff path
"

if [ "$1" == "-h" ]; then
    echo "$Usage"
else
    gdal_info=$(gdalinfo --version)
    if [ $? -ne 0 ]; then
        echo "Error: The coomand failed with: $gdal_info"
        echo "Install GDAL on your machine"
    else
        echo "GDAL Version: $gdal_info"
        echo "Getting the info on Raster data"
        raster_info=$(gdalinfo $1)
        echo "$raster_info"
        echo "Checking if the Geotiff is cloud optimised"
        rio_cog=$(rio cogeo validate $1)
        echo "Converting GeoTiff to Cloud Optimised GeoTiff (COG)"
        convert=$(rio cogeo create $1 $2 --blocksize 256 --forward-band-tags)
        echo "Validating $2 COG"
        rio_cog=$(rio cogeo validate $2)
        echo "Getting the info of COG file"
        cog_info=$(rio cogeo info $2)
        echo "$cog_info"
    fi
fi