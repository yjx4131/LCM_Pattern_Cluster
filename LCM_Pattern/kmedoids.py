'''
Another clusting method , k-medoids.
See more : http://en.wikipedia.org/wiki/K-medoids
The most common realisation of k-medoid clustering is the Partitioning Around Medoids (PAM) algorithm and is as follows:[2]
1. Initialize: randomly select k of the n data points as the medoids
2. Associate each data point to the closest medoid. ("closest" here is defined using any valid distance metric, most commonly Euclidean distance, Manhattan distance or Minkowski distance)
3. For each medoid m
     For each non-medoid data point o
         Swap m and o and compute the total cost of the configuration
4. Select the configuration with the lowest cost.
5. repeat steps 2 to 4 until there is no change in the medoid.
'''
import random
import numpy as np
import pandas as pd 


def similarity(idx1,idx2,w):
    NormDis = disArray[idx1,idx2]/np.max(disArray)
    NormKp = kpArray[idx1,idx2]
    cost = w * NormDis - (1-w) * NormKp
    return cost

distances_cache = {}

def totalcost(ZoneID, costf, medoids_idx,w):   # ZoneID is the ID number of each zone
    size = len(ZoneID)
    total_cost = 0.0
    medoids = {}
    for idx in medoids_idx :
        medoids[idx] = []
    for i in range(size) :
        choice = None
        min_cost = 2.1
        for m in medoids :
            tmp = distances_cache.get((m,i),None)
            if tmp == None :
                tmp = costf(ZoneID[m],ZoneID[i],w)
                distances_cache[(m,i)] = tmp
            if tmp < min_cost :
                choice = m
                min_cost = tmp
        medoids[choice].append(i)
        total_cost += min_cost
    return total_cost, medoids
    

def kmedoids(ZoneID, k,w):
    size = len(ZoneID)
    medoids_idx = random.sample([i for i in range(size)], k)
    pre_cost, medoids = totalcost(ZoneID,similarity,medoids_idx,w)
    current_cost = 2.1 * size # maxmum of pearson_distances is 2.    
    best_choice = []
    best_res = {}
    iter_count = 0
    while 1 :
        for m in medoids :
            for item in medoids[m] :
                if item != m :
                    idx = medoids_idx.index(m)
                    swap_temp = medoids_idx[idx]
                    medoids_idx[idx] = item
                    tmp,medoids_ = totalcost(ZoneID,similarity,medoids_idx,w)
                    #print tmp,'-------->',medoids_.keys()
                    if tmp < current_cost :
                        best_choice = list(medoids_idx)
                        best_res = dict(medoids_)
                        current_cost = tmp
                    medoids_idx[idx] = swap_temp
        iter_count += 1
        #print(current_cost,iter_count)
        if best_choice == medoids_idx : break
        if current_cost <= pre_cost :
            pre_cost = current_cost
            medoids = best_res
            medoids_idx = best_choice
        
    
    return current_cost, best_choice, best_res


if __name__ == '__main__' :
    # read the distanse array and kappa array to use
    disArray = pd.read_csv(r'C:\Users\jyang71\Desktop\LCM_Pattern_Cluster\distance.csv')
    disArray = np.array(disArray)[:,1:]
    kpArray = pd.read_csv(r'C:\Users\jyang71\Desktop\LCM_Pattern_Cluster\kappa.csv')
    kpArray = np.array(kpArray)[:,1:]
    
    #generate a ID list, the IDs in this list should be consistent with the index of the zones that are store in the geoDataFrame
    ZoneID = list(range(110))

    current_cost, best_choice, best_res = kmedoids(ZoneID,5,0)
    print("----"*30)
    print(current_cost)
    print(best_choice)
    print(best_res)
    

    elbowData = []
    for k in range(1,20,1):
        
        for w in np.arange(0,1.1,0.1):
            i = 1
            cost = []
            
            while i < 20:
                print(k,w,i)
                cur_cost, be_choice, be_res = kmedoids(ZoneID,k,w)
                cost.append(cur_cost)
                i = i + 1
            meanCost = np.mean(cost)
            elbowData.append((w,k,meanCost))

    elbow_df = pd.DataFrame(elbowData,columns = ['weight for spatial distance','num of clusters','Cost'])
    elbow_df.to_csv(r'C:\Users\jyang71\Desktop\LCM_Pattern_Cluster\Elbow.csv')
