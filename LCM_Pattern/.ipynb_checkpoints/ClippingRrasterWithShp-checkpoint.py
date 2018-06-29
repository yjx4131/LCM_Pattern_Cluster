import rasterio
from rasterio.mask import mask
from rasterio.plot import show
from rasterio.plot import show_hist
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import numpy as np 


# the input shapefile and raster shoul project to the same crs

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def maskRaster(rasterFile,GeoDf):
	GeoDf = GeoDf.to_crs(crs=rasterFile.crs.data)
	coords = getFeatures(GeoDf)
	out_img, out_transform = mask(raster=rasterFile, shapes=coords, crop=True)
	out_meta = rasterFile.meta.copy()
	epsg_code = int(rasterFile.crs.data['init'][5:])
	#out_meta.update({"driver": "GTiff","height": out_img.shape[1],"width": out_img.shape[2],"transform": out_transform,"crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()})
	return out_img


def getLuccArr(luccMap,clipFc):
	rasterFile = rasterio.open(luccMap)
	gpdFc = gpd.read_file(clipFc)
	length = gpdFc.shape[0]
	clipArrLst = []
	for i in range(length):
		clipShape = gpd.GeoDataFrame({'geometry': gpdFc.iloc[i].geometry}, index=[i], crs=rasterFile.crs.data)
		clipedImgArr = maskRaster(rasterFile,clipShape)
		TM_arr = clipedImgArr.data
		np.place(TM_arr,TM_arr==255,0)
		#print(np.unique(TM_arr))
		clipArrLst.append(list(TM_arr))
	gpdFc['LuccMtx'] = clipArrLst
	return 	gpdFc



if __name__ == '__main__':
	lucc1996 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB1996_WH_Erase_Merge_UGB_Dis.tif"
	lucc2002 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2002_WH_Erase_Merge_UGB_Dis.tif"
	lucc2005 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2005_WH_Erase_Merge_UGB_Dis.tif"
	lucc2010 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2010_WH_Erase_Merge_UGB_Dis.tif"
	lucc2015 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2015_WH_Erase_Merge_UGB_Dis.tif"
	clipFc = r"C:\Users\jyang71\Desktop\Datasets\WH_XZQ_Project_Eliminate.shp"
	gpdFc1996 = getLuccArr(lucc1996,clipFc)
	gpdFc2002 = getLuccArr(lucc1996,clipFc)
	gpdFc2005 = getLuccArr(lucc1996,clipFc)
	gpdFc2010 = getLuccArr(lucc1996,clipFc)
	gpdFc2015 = getLuccArr(lucc1996,clipFc)

	
#get the cliped array with sytax: 		gpdFc.TransMtx[i][0]


