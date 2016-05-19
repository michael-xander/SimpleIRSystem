# Calculates NDCG
# Charles Du
# 14th May, 2016

import math
def NDCG(result, query_num, testBedName, num_docs_to_consider):
    f = open(testBedName+'/relevance.'+str(query_num), 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    relevance_str = ''
    for line in lines:
        relevance_str += (line.strip())
    dcg = []
    relevance_score = int(relevance_str[int(result[0])-1])
    dcg.append(relevance_score)
    docs_num = min(len(result), num_docs_to_consider)
    for i in range (1,docs_num):
        relevance_score = int(relevance_str[int(result[i])-1])
        dcg.append(dcg[i-1] +relevance_score/(math.log2(2+i)))
    final_dcg = dcg[docs_num-1]

    idcg = 0
    
    #basically this count array keeps track of the number 0s, 1s and 2s relevance score for the query, makes sorting so much 
    #easier since you can only have 3 different values.
    count = [0,0,0]
    
    for i in range(docs_num):
        relevance_score = int(relevance_str[int(result[i])-1])
        count[relevance_score] = count[relevance_score]+1
        
    rank = 0 
    for j in range(2, -1, -1) :
        for i in range(count[j]):
            idcg = idcg + j/(math.log2(2+rank))
            rank = rank + 1
    # assumption is that if dcg == 0 == idcg, ndcg = 1 but MAP will be 0 showing that results were irrelevant
    if(final_dcg == idcg):
        return 1

    return final_dcg/idcg