# Calculates the AP for a query
# Charles Du
# 14th May, 2016

def AP(result, query_num, testbed_name, num_docs_to_consider):
    f = open(testbed_name + '/relevance.' + str(query_num), 'r', encoding='utf-8')
    lines = f.readlines()
    f.close()
    relevance_str = ''
    for line in lines:
        relevance_str += (line.strip())
    cumulative_precision = 0
    sum_precision_at_N = 0
    docs_num = min(len(result), num_docs_to_consider)
    for i in range(docs_num):
        relevanceScore = int(relevance_str[int(result[i])-1])/2
        cumulative_precision = cumulative_precision + relevanceScore
        precision = cumulative_precision/ (i+1)
        sum_precision_at_N = sum_precision_at_N + precision
    return sum_precision_at_N/docs_num