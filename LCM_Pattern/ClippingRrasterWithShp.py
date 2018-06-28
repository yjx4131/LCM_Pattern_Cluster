import rasterio
from rasterio.plot import shows
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import json



def maskRaster(rst,GeoDf):
	rasterFile = rasterio.open(rst)
	GeoDf = GeoDf.to_crs(crs=rasterFile.crs.rasterFile)
	coords = list(json.loads(GeoDf.to_json())['features'][0]['geometry'])
	out_img, out_transform = mask(raster=rasterFile, shapes=coords, crop=True)
	out_meta = rasterFile.meta.copy()
	epsg_code = int(rasterFile.crs.rasterFile['init'][5:])
	out_meta.update({"driver": "GTiff","height": out_img.shape[1],"width": out_img.shape[2],"transform": out_transform,"crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()})
	return out_img

if __name__ == '__main__':
	landmap = r"path/1995.tif"
	clipFc = r"path/xzq.shp"
	gpdFc = gpd.read_file(clipFc)
	for i in range(gpdFc.shape[0]):
		clipedImgArr = maskRaster(landmap,gpdFc.iloc[i])
