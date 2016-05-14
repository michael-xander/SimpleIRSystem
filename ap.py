# Calculates the AP for a query
# Charles Du
# 14th May, 2016

def AP(accum, result, titles, fileNum, testBedName):
    queryNum = fileNum
    relevanceStr = open(testBedName+'/relevance.'+str(queryNum), 'r').read().replace("\n", "")
    cumulativePrecision = 0
    sumPrecisionAtN = 0
    for i in range(len(result)):

        relevanceScore = int(relevanceStr[int(result[i])-1]) /2

        cumulativePrecision = cumulativePrecision + relevanceScore
        precision = cumulativePrecision/ (i+1)
        sumPrecisionAtN = sumPrecisionAtN + precision
    return sumPrecisionAtN/ len(result)