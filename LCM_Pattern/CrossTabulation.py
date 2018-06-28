# Author: Jianxin
# Data: 2018/06/27
# Function: generate cross table between two numpy array
# Reference Link: https://stackoverflow.com/questions/48456145/generate-transition-matrix 


import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score


def f_pp(A, B, m):
	#A[np.isnan(A)] = 0
	#B[np.isnan(B)] = 0
	out = np.bincount(np.ravel_multi_index((A, B), (m+1, m+1)).ravel(), minlength=np.square(m+1)).reshape(m+1, m+1)
	out = out[1:,1:]
	row_sum = out.sum(1)
	row_sum = row_sum.reshape((m,1))
	out = np.concatenate((out,row_sum),axis = 1)
	row_sum = out.sum(0)
	row_sum = row_sum.reshape((1,m+1))
	out = np.concatenate((out,row_sum),axis = 0)
	#indices = ['cls_'+ str(i) for i in range(1,m+1)]
	#indices = indices.append('col_tot')
	#print(indices)
	#column = ['cls_'+ str(i) for i in range(1,m+1)]
	#column = column.append('row_tot')
	#print(column)
	#out = pd.DataFrame(out[1:,1:],index = indices,columns=column)
	#out = out.set_index("cls_" + out.index.astype(str))
	return out

def kappa(A_arr,B_arr):
	np.ravel(A_arr)
	np.ravel(B_arr)
	cohen_kappa_score(np.ravel(A_arr), np.ravel(B_arr))



if __name__ == '__main__':
	a = np.array([[3,2,1],[1,2,2],[2,2,1],[1,2,2],[2,2,1]])
	b = np.array([[3,2,1],[1,2,3],[3,2,1],[1,3,3],[3,3,1]])
	result = f_pp(a,b,3)
	print(result)

