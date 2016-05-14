import math
def NDCG(accum, result, titles, fileNum, testBedName):
    queryNum = fileNum
    #print("NDCP Results:")
    relevanceStr = open(testBedName+'/relevance.'+str(queryNum), 'r').read().replace("\n", "");
    #print(relevanceStr)
    dcg = []
    relevanceScore = int(relevanceStr[int(result[0])])
    dcg.append(relevanceScore)
    for i in range (1,len (result)):
        
        relevanceScore = int(relevanceStr[int(result[i])-1])
        dcg.append(dcg[i-1] +relevanceScore/(math.log2(2+i)))
    #    print ("{0:10.8f} {1:5} {2}".format (dcg[i], int(result[i]), titles[result[i]]))
    #print(dcg[len(result)-1])
    finalDCG = dcg[len(result)-1]
    idcg = 0;
    
    #basically this count array keeps track of the number 0s, 1s and 2s relevance score for the query, makes sorting so much 
    #easier since you can only have 3 different values.
    count = [0,0,0];
    
    for i in range(len(result)):
        relevanceScore = int(relevanceStr[i])
        count[relevanceScore] = count[relevanceScore]+1   
        
    rank = 0 
    for j in range(2, -1, -1) :
        #print (j)
        
        for i in range(count[j]):
            idcg = idcg + j/(math.log2(2+rank))
            rank = rank + 1
            
    #print('NDCG:' + str(finalDCG/idcg))
    return finalDCG/idcg