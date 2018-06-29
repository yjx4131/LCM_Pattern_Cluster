import CrossTabulation as ct
import ClippingRrasterWithShp as cRs
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score
import geopandas as gpd 


lucc1996 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB1996_WH_Erase_Merge_UGB_Dis.tif"
lucc2002 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2002_WH_Erase_Merge_UGB_Dis.tif"
lucc2005 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2005_WH_Erase_Merge_UGB_Dis.tif"
lucc2010 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2010_WH_Erase_Merge_UGB_Dis.tif"
lucc2015 = r"C:\Users\jyang71\Desktop\Datasets\DLTB\DLTB2015_WH_Erase_Merge_UGB_Dis.tif"
clipFc = r"C:\Users\jyang71\Desktop\Datasets\WH_XZQ_Project_Eliminate.shp"
gpdFc1996 = cRs.getLuccArr(lucc1996,clipFc)
gpdFc2002 = cRs.getLuccArr(lucc2002,clipFc)
gpdFc2005 = cRs.getLuccArr(lucc2005,clipFc)
gpdFc2010 = cRs.getLuccArr(lucc2010,clipFc)
gpdFc2015 = cRs.getLuccArr(lucc2015,clipFc)

gpdFc = gpd.read_file(clipFc)

ptnLst = []
shapeLength = gpdFc1996.shape[0]

for i in range(shapeLength):
	mapArr_96 = gpdFc1996.LuccMtx[i][0]
	mapArr_05 = gpdFc2005.LuccMtx[i][0]
	mapArr_10 = gpdFc2010.LuccMtx[i][0]
	mapArr_15 = gpdFc2015.LuccMtx[i][0]
	TM_9605 = ct.transMatrix(mapArr_96,mapArr_05,7)[1]
	gainIntenPtn_9605,lossIntenPtn_9605 = ct.TransPattern(TM_9605,9)
	GainLossPtn_9605 = ct.mergeGainLoss(gainIntenPtn_9605,lossIntenPtn_9605)

	TM_0510 = ct.transMatrix(mapArr_05,mapArr_10,7)[1]
	gainIntenPtn_0510,lossIntenPtn_0510 = ct.TransPattern(TM_0510,5)
	GainLossPtn_0510 = ct.mergeGainLoss(gainIntenPtn_0510,lossIntenPtn_0510)

	TM_1015 = ct.transMatrix(mapArr_10,mapArr_15,7)[1]
	gainIntenPtn_1015,lossIntenPtn_1015 = ct.TransPattern(TM_1015,5)
	GainLossPtn_1015 = ct.mergeGainLoss(gainIntenPtn_1015,lossIntenPtn_1015)

	Ptn = ct.mergeInterval(GainLossPtn_9605,GainLossPtn_0510,GainLossPtn_1015)
	ptnLst.append(list(np.array(Ptn)))

gpdFc['TransPtn'] = ptnLst
#get the transition pattern array with syntax: 		np.array(gpdFc.TransPtn[0])
