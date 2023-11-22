"""
Convert GeoTIFFs to Cloud Optimised GeoTIFFs
"""
import os
import click
import json
from typing import Dict
import rasterio as rio
from rasterio.io import MemoryFile
from rasterio.transform import from_bounds
from rio_cogeo.cogeo import cog_translate, cog_info
from rio_cogeo.profiles import cog_profiles
from rio_cogeo.models import IFD
from opencosmos.utils import Loader
import logging
from logging import config
config.fileConfig("logger.ini")

class cloud_optimised_geotiff:

    def __init__(self, log: isinstance = None) -> None:
        r"""Defining variables
        
        Args:\n
            log: custom logger ini file.
        """
        self.log = log
    
    @staticmethod
    def COG_IFD(ifd: IFD = None)-> Dict:
        r"""Get the IFD from COG
        
        Args:\n
            ifd: cog_info.IFD
        """
        return {
            "Level" : ifd.Level,
            "Width" : ifd.Width,
            "Height" : ifd.Height,
            "BlockSize" : ifd.Blocksize,
            "Decimation" : ifd.Decimation
        }
    
    @staticmethod
    def metadata(cog_file_path: str = None) -> Dict:
        r"""Store COG meta data in a JSON Dictionary"""
        cog = cog_info(cog_file_path)
        cog_ifd = dict()
        for i in range(len(cog.IFD)):
            cog_ifd[f"Level_{i}"] = cloud_optimised_geotiff.COG_IFD(cog.IFD[i])
        return {
            "Driver" : cog.Driver,
            "COG" : cog.COG,
            "Compression" : cog.Compression,
            "ColorSpace" : cog.ColorSpace,
            "COG_errors" : cog.COG_errors,
            "COG_warnings" : cog.COG_warnings,
            "Profile" : {
                "Bands" : cog.Profile.Bands,
                "Width" : cog.Profile.Width,
                "Height" : cog.Profile.Height,
                "Tiled" : cog.Profile.Tiled,
                "Dtype" : cog.Profile.Dtype,
                "Interleave" : cog.Profile.Interleave,
                "AlphaBand" : cog.Profile.AlphaBand,
                "InternalMask" : cog.Profile.InternalMask,
                "Nodata" : cog.Profile.Nodata,
                "ColorInterp" : cog.Profile.ColorInterp,
                "ColorMap" : cog.Profile.ColorMap,
                "Scales" : cog.Profile.Scales,
                "Offsets" : cog.Profile.Offsets
            },
            "GEO" : {
                "CRS" : cog.GEO.CRS,
                "BoundingBox" : cog.GEO.BoundingBox,
                "Origin" : cog.GEO.Origin,
                "Resolution" : cog.GEO.Resolution,
                "MinZoom" : cog.GEO.MinZoom,
                "MaxZoom" : cog.GEO.MaxZoom
            },
            "Tags" : cog.Tags,
            "Band_Metadata" : {
                "Band 1" : {
                    "Description" : cog.Band_Metadata["Band 1"].Description,
                    "ColorInterp" : cog.Band_Metadata["Band 1"].ColorInterp,
                    "Offset" : cog.Band_Metadata["Band 1"].Offset,
                    "Metadata" : cog.Band_Metadata["Band 1"].Metadata
                    },
                "Band 2" : {
                    "Description" : cog.Band_Metadata["Band 2"].Description,
                    "ColorInterp" : cog.Band_Metadata["Band 2"].ColorInterp,
                    "Offset" : cog.Band_Metadata["Band 2"].Offset,
                    "Metadata" : cog.Band_Metadata["Band 2"].Metadata
                    },
                "Band 3" : {
                    "Description" : cog.Band_Metadata["Band 3"].Description,
                    "ColorInterp" : cog.Band_Metadata["Band 3"].ColorInterp,
                    "Offset" : cog.Band_Metadata["Band 3"].Offset,
                    "Metadata" : cog.Band_Metadata["Band 3"].Metadata
                    }                                        
            },
            "IFD" : cog_ifd
        }
        
    def cog_convert(self, input_tiff_path: str = None):
        r"""Convert Geotiff to COG
        
        Args:\n
            input_tiff_path: Path to the untilled Geotiff image.
        """
        # File paths
        output_cog_tiff = os.path.basename(input_tiff_path).split('.')[0]
        output_folder = os.path.dirname(os.path.realpath(input_tiff_path))
        output_cog_tiff = os.path.join(output_folder, f"{output_cog_tiff}_cog.tiff")
        
        # Read Geotiff data
        tiff = rio.open(input_tiff_path)
        bounds = tiff.bounds
        width = tiff.width
        height = tiff.height
        nbands = 3
        img_array = tiff.read(1)
        src_transform = from_bounds(*bounds, width=width, height=height)
        src_profile = dict(
            driver="GTiff",
            dtype=tiff.dtypes[0],
            count=nbands,
            height=height,
            width=width,
            crs="epsg:4326",
            transform=src_transform)
        
        # Convert to COG
        loading = Loader("Converting GeoTIFF to Cloud Optimised GeoTIFF...", "That was fast", 0.05).start()
        with MemoryFile() as memfile:
            with memfile.open(**src_profile) as mem:
                mem.write(img_array, indexes=3)
                dst_profile = cog_profiles.get("deflate")
                cog_translate(
                    mem,
                    output_cog_tiff,
                    dst_profile,
                    in_memory=True,
                    quiet=True,)
        loading.stop() 
        self.log.info(f"Find the converted COG file here: {output_cog_tiff}")
        return output_cog_tiff

    def cog_metadata(self, cog_tiff_path:str = None):
        """Write the COG meta data into a JSON file"""
        # COG metadata
        cog_metadata = cloud_optimised_geotiff.metadata(cog_file_path = cog_tiff_path)
        metadata_file = os.path.basename(cog_tiff_path).split('.')[0]
        folder = os.path.dirname(os.path.realpath(cog_tiff_path))
        metadata_filepath = os.path.join(folder, f"{metadata_file}_metadata.json")
        with open(metadata_filepath, "w") as outfile:
            json.dump(cog_metadata, outfile)
            outfile.close()
   
        self.log.info(f"Find the COG meta data here: {metadata_filepath}")

@click.command()
@click.option("--input_tiff_path", type = str, help = "Path to the untilled GeoTiff file")
def main(input_tiff_path):
    if input_tiff_path is None:
        input_tiff_path = "data/processed/Sentinel2_visual_processed.tiff"
    try:
        assert os.path.exists(input_tiff_path)
    except AssertionError:
        logging.debug("Please provide credible TIFF path")
    else:
        sentinel_data = cloud_optimised_geotiff(log = logging)
        cog_tiff = sentinel_data.cog_convert(input_tiff_path = input_tiff_path)
        metadata = sentinel_data.cog_metadata(cog_tiff_path=cog_tiff)

if __name__ == "__main__":
    main()