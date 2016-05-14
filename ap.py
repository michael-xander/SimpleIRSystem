import math
def AP(accum, result, titles, fileNum, testBedName):
    queryNum = fileNum
    relevanceStr = open(testBedName+'/relevance.'+str(queryNum), 'r').read().replace("\n", "")
    relevantTotalScore = 0
    totalPrecision = 0
    for i in range(len(result)):

        relevanceScore = int(relevanceStr[int(result[i])-1]) /2

        relevantTotalScore = relevantTotalScore + relevanceScore
        precision = relevantTotalScore/ (i+1)
        totalPrecision = totalPrecision + precision
    #print("AP:"+str(totalPrecision/ len(result) ))
    return totalPrecision/ len(result)