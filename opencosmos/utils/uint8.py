from osgeo import gdal
import numpy as np
from skimage import exposure
from PIL import Image

def convert(input_tiff_path, output_tiff_path):
    # Load the GeoTIFF raster
    dataset = gdal.Open(input_tiff_path)

    # Read the data into a NumPy array
    raster_data_uint16 = dataset.GetRasterBand(1).ReadAsArray()

    # Perform the conversion from uint16 to uint8
    raster_data_uint8 = exposure.rescale_intensity(raster_data_uint16, in_range='uint16', out_range='uint8').astype(np.uint8)

    # Create a new GeoTIFF file for the uint8 data
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_tiff_path, dataset.RasterXSize, dataset.RasterYSize, 1, gdal.GDT_Byte)

    # Copy the spatial information from the original dataset
    output_dataset.SetGeoTransform(dataset.GetGeoTransform())
    output_dataset.SetProjection(dataset.GetProjection())

    # Write the uint8 data to the new GeoTIFF file
    output_dataset.GetRasterBand(1).WriteArray(raster_data_uint8)

    # Close the datasets
    dataset = None
    output_dataset = None

    # Save or display the result
    output_image = Image.fromarray(raster_data_uint8)
    output_image.save(output_tiff_path)

if __name__ == "__main__":
    input_tiff = "data/processed/Sentinel2_visual_process.tiff"
    output_tiff = "data/processed/output.tiff"
    convert(input_tiff, output_tiff)
