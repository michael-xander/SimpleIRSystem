import math
def AP(accum, result, titles):
    queryNum = "1"
    relevanceStr = open('testbed/relevance.'+queryNum, 'r').read().replace("\n", "")
    relevantDocCount = 0;
    totalPrecision = 0;
    for i in range(len(result)):
        if(relevanceStr[int(result[i])-1] != "0"):
            relevantDocCount = relevantDocCount + 1;
            precision = relevantDocCount/ (i+1);
            totalPrecision = totalPrecision + precision;
    print("AP:"+str(totalPrecision/ len(result) ))