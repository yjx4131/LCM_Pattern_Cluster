import numpy as np
import pandas as pd 


disArray = pd.read_csv(r'C:\Users\jyang71\Desktop\LCM_Pattern_Cluster\distance.csv')
disArray = np.array(disArray)[:,1:]
kpArray = pd.read_csv(r'C:\Users\jyang71\Desktop\LCM_Pattern_Cluster\kappa.csv')
kpArray = np.array(kpArray)[:,1:]

def similarity(idx1,idx2,w):
    NormDis = disArray[idx1,idx2]/np.max(disArray)
    NormKp = kpArray[idx1,idx2]
    cost = w * NormDis - (1-w) * NormKp
    return cost


