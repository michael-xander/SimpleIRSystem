# Calculates the AP for a query
# Charles Du
# 14th May, 2016

def AP(result, query_num, testbed_name):
    relevance_str = open(testbed_name + '/relevance.' + str(query_num), 'r').read().replace("\n", "")
    cumulative_precision = 0
    sum_precision_at_N = 0
    for i in range(len(result)):
        relevanceScore = int(relevance_str[int(result[i])-1])/2
        cumulative_precision = cumulative_precision + relevanceScore
        precision = cumulative_precision/ (i+1)
        sum_precision_at_N = sum_precision_at_N + precision
    return sum_precision_at_N/len(result)