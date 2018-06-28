# Author: Jianxin
# Data: 2018/06/27
# Function: generate cross table between two numpy array
# Reference Link: https://stackoverflow.com/questions/48456145/generate-transition-matrix 
# important notes: land use classes must be encoded form 1 to n continuously

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score

# create transition matrix from two land use array.
# m is the number of land use categories.
# A and B are land use type arrays with all background value convert to 0 or np.nan.
def transMatrix(A, B, m):
	A[np.isnan(A)] = 0
	B[np.isnan(B)] = 0
# generate transition matrix
	out = np.bincount(np.ravel_multi_index((A, B), (m+1, m+1)).ravel(), minlength=np.square(m+1)).reshape(m+1, m+1)
# drop lines and columns that indicat transition between background values, that is 0.
	tranMatrix = out[1:,1:]
# furthur polish the transition matrix. add column and row margins(sum).
	row_sum = tranMatrix.sum(1).reshape((m,1))
	tranMatrix = np.concatenate((tranMatrix,row_sum),axis = 1)
	row_sum = tranMatrix.sum(0).reshape((1,m+1))
	tranMatrix = np.concatenate((tranMatrix,row_sum),axis = 0)
# convert the transition matrix to dataframe
	indices = ['cls_'+ str(i) for i in range(1,m+1)]
	indices.append('col_tot')
	#print(indices)
	cols = ['cls_'+ str(i) for i in range(1,m+1)]
	cols.append('row_tot')
	#print(cols)
# outTranMatrix is the final transition matrix in pandas DataFrame format
	outTranMatrix = pd.DataFrame(tranMatrix,index = indices,columns=cols)
	#out = out.set_index("cls_" + out.index.astype(str))
# finally, return the transition matrix in dataframe format and in numpy array format
	return outTranMatrix.astype(np.int32),tranMatrix[:m,:m].astype(np.int32)

# Input a numpy array wihich shows the transtion matrix in a time interval.
# The TM should not have marginal summations
# duraton is the number of years (steps) in a time interval
def TransPattern(arr,duration):       #arr is a m x m numpy array
	m = arr.shape[1]
	# calculate average gian intensity for each lucc class, then put the reslut in a list
	average_gain = []
	for i in range(m):
		totalArea_start_i = np.sum(arr[i,:])
		totalArea_start_not_i = np.sum(arr) - totalArea_start_i
		grossGain_i = np.sum(arr[:,i]) - arr[i,i]
		average_gain_i = (grossGain_i/duration)/totalArea_start_not_i
		average_gain.append(average_gain_i)
	# calculate gian intensity of class i from j, then put the reslut in a numpy array
	gainIntenMatr = np.zeros((m,m))
	for i in range(m):
		for j in range(m):
			gainIntensity_ji = (arr[j][i]/duration)/np.sum(arr[j,:])
			gainIntenMatr[j][i] = gainIntensity_ji
	# convert gain intensity to gain pattern with "1" indicat tending to convert and "2" indicate avoiding
	gainIntenMatr[gainIntenMatr >= average_gain] = 1		# tend to
	gainIntenMatr[gainIntenMatr < average_gain] = 2			# avoid
	# change the diagonal element to np.nan
	np.fill_diagonal(gainIntenMatr,np.nan)
	
	# calculate average loss intensity for each lucc class, then put the reslut in a list
	average_loss = []
	for i in range(m):
		totalArea_end_i = np.sum(arr[:,i])
		totalArea_end_not_i = np.sum(arr) - totalArea_end_i
		grossLoss_i = np.sum(arr[i,:]) - arr[i,i]
		average_loss_i = (grossLoss_i/duration)/totalArea_end_not_i
		average_loss.append(average_loss_i)
	# calculate loss intensity of class i to j, then put the reslut in a numpy array
	lossIntenMatr = np.zeros((m,m))
	for i in range(m):
		for j in range(m):
			lossIntensity_ij = (arr[i][j]/duration)/np.sum(arr[:,j])
			lossIntenMatr[i][j] = lossIntensity_ij
	# convert loss intensity to loss pattern with "1" indicat tending to convert and "2" indicate avoiding
	lossIntenMatr[lossIntenMatr >= np.array(average_loss).T] = 1    # tend to
	lossIntenMatr[lossIntenMatr < np.array(average_loss).T] = 2		# avoid
	# change the diagonal element to np.nan
	np.fill_diagonal(lossIntenMatr,np.nan)
	# four returns
	return average_gain,gainIntenMatr,average_loss,lossIntenMatr

# merge the gain and loss pattern array
def mergeGainLoss(gainArr,lossArr):
	m = gainArr.shape[0]
	idx = ['cls_' + str(i) for i in range(1,m+1)]
	dfGain = pd.DataFrame(gainArr,columns = idx,index = idx)
	dfLoss = pd.DataFrame(lossArr,columns = idx,index = idx)
	dfGainLoss = pd.concat([dfGain,dfLoss],axis = 1,keys = ['Gain','Loss']).swaplevel(1,0,axis=1).sort_index(axis=1,level=0)
	return dfGainLoss
# merge gain and loss pattern array in different time intervals
def mergeInterval(*args):
	m = len(args)
	idx = ['interval_' + str(i + 1) for i in range(m)]
	multiInterval = pd.concat(list(args),axis = 0,keys = idx).swaplevel(1,0,axis = 0).sort_index(axis = 0,level = 0)
	return multiInterval

# calculate kappa index between land change pattern array
# the array should not contain none values
def kappa(A_arr,B_arr):
	np.ravel(A_arr)
	np.ravel(B_arr)
	return cohen_kappa_score(np.ravel(A_arr), np.ravel(B_arr))




if __name__ == '__main__':
	map_a = np.array([[3,2,1],[1,2,2],[2,2,1],[1,2,2],[2,2,1]])
	map_b = np.array([[3,2,1],[1,2,3],[3,2,1],[1,3,3],[3,3,1]])
	transMatrx = transMatrix(map_a,map_b,3)[1]
	ptn1 = TransPattern(transMatrx,2)
	ptn2 = TransPattern(transMatrx,3)
	print(ptn1[1])
	print('_______________')
	print(ptn2[1])

	print(kappa(ptn1[1],ptn2[1]))