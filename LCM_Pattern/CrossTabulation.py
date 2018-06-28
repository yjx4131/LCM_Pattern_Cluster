# Author: Jianxin
# Data: 2018/06/27
# Function: generate cross table between two numpy array
# Reference Link: https://stackoverflow.com/questions/48456145/generate-transition-matrix 


import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score


def transMatrix(A, B, m):
	#A[np.isnan(A)] = 0
	#B[np.isnan(B)] = 0
	out = np.bincount(np.ravel_multi_index((A, B), (m+1, m+1)).ravel(), minlength=np.square(m+1)).reshape(m+1, m+1)
	tranMatrix = out[1:,1:]
	row_sum = tranMatrix.sum(1)
	row_sum = row_sum.reshape((m,1))
	tranMatrix = np.concatenate((tranMatrix,row_sum),axis = 1)
	row_sum = tranMatrix.sum(0)
	row_sum = row_sum.reshape((1,m+1))
	tranMatrix = np.concatenate((tranMatrix,row_sum),axis = 0)
	indices = ['cls_'+ str(i) for i in range(1,m+1)]
	indices.append('col_tot')
	#print(indices)
	cols = ['cls_'+ str(i) for i in range(1,m+1)]
	cols.append('row_tot')
	#print(cols)
	outTranMatrix = pd.DataFrame(tranMatrix,index = indices,columns=cols)
	#out = out.set_index("cls_" + out.index.astype(str))
	return outTranMatrix.astype(np.int32),tranMatrix[:m,:m].astype(np.int32)

def TransPattern(arr,duration):       #arr is a m x m numpy array
	m = arr.shape[1]
	average_gain = []
	for i in range(m):
		totalArea_start_i = np.sum(arr[i,:])
		totalArea_start_not_i = np.sum(arr) - totalArea_start_i
		grossGain_i = np.sum(arr[:,i]) - arr[i,i]
		average_gain_i = (grossGain_i/duration)/totalArea_start_not_i
		average_gain.append(average_gain_i)
	
	gainIntenMatr = np.zeros((m,m))
	for i in range(m):
		for j in range(m):
			gainIntensity_ji = (arr[j][i]/duration)/np.sum(arr[j,:])
			gainIntenMatr[j][i] = gainIntensity_ji

	gainIntenMatr[gainIntenMatr >= average_gain] = 1		# tend to
	gainIntenMatr[gainIntenMatr < average_gain] = 2			# avoid
	np.fill_diagonal(gainIntenMatr,np.nan)
	
	average_loss = []
	for i in range(m):
		totalArea_end_i = np.sum(arr[:,i])
		totalArea_end_not_i = np.sum(arr) - totalArea_end_i
		grossLoss_i = np.sum(arr[i,:]) - arr[i,i]
		average_loss_i = (grossLoss_i/duration)/totalArea_end_not_i
		average_loss.append(average_loss_i)
	
	lossIntenMatr = np.zeros((m,m))
	for i in range(m):
		for j in range(m):
			lossIntensity_ij = (arr[i][j]/duration)/np.sum(arr[:,j])
			lossIntenMatr[i][j] = lossIntensity_ij

	lossIntenMatr[lossIntenMatr >= np.array(average_loss).T] = 1    # tend to
	lossIntenMatr[lossIntenMatr < np.array(average_loss).T] = 2		# avoid
	np.fill_diagonal(lossIntenMatr,np.nan)
	return average_gain,gainIntenMatr,average_loss,lossIntenMatr

def mergeGainLoss(gainArr,lossArr):
	m = gainArr.shape[0]
	idx = ['cls_' + str(i) for i in range(1,m+1)]
	dfGain = pd.DataFrame(gainArr,columns = idx,index = idx)
	dfLoss = pd.DataFrame(lossArr,columns = idx,index = idx)
	dfGainLoss = pd.concat([dfGain,dfLoss],axis = 1,keys = ['Gain','Loss']).swaplevel(1,0,axis=1).sort_index(axis=1,level=0)
	return dfGainLoss

def mergeInterval(*args):
	m = len(args)
	idx = ['interval_' + str(i + 1) for i in range(m)]
	multiInterval = pd.concat(list(args),axis = 0,keys = idx).swaplevel(1,0,axis = 0).sort_index(axis = 0,level = 0)
	return multiInterval

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