# Finds the optimum mix of parameters for the modified engine
# Michael Kyeyune
# 16th May, 2016

import sys
import parameters
import analyse
import ap
import ndcg

def main():
    if len(sys.argv)==1:
        print("Syntax: optimise.py <testbed> <num of docs to consider for MAP and NDCG analysis>")
        exit(0)
    testbed_name = sys.argv[1]
    parameters.docs_to_consider = int(sys.argv[2])
    queries = analyse.readin_testbed_queries(testbed_name)

    max_MAP = 0
    max_avg_NDCG = 0
    # test 1-50 indicative terms and top k documents
    for i in range(50):
        parameters.number_indicative_terms = i+1
        for j in range(50):
            parameters.number_top_k_documents = j+1
            current_MAP = 0
            current_avg_NDCG = 0
            query_number = 1
            for query_sentence in queries:
                result, accum, titles = analyse.submit_query(testbed_name, query_sentence, True)
                ap_score = ap.AP(result, query_number, testbed_name, parameters.docs_to_consider)
                ndcg_score = ndcg.NDCG(result, query_number, testbed_name, parameters.docs_to_consider)
                current_MAP += ap_score
                current_avg_NDCG += ndcg_score
                query_number += 1
            current_MAP = current_MAP/len(queries)
            current_avg_NDCG = current_avg_NDCG/len(queries)
            print('='*100)
            print('+'*100)
            print('Number of docs to consider : ' + str(parameters.docs_to_consider))
            print('Number of indicative terms : ' + str(parameters.number_indicative_terms))
            print('Number of top k documents  : ' + str(parameters.number_top_k_documents))
            print('+'*100)
            print('Calculated MAP             : ' + str(current_MAP))
            print('Calculated Average NDCG    : ' +  str(current_avg_NDCG))
            print('*'*100)
            print('Current max MAP            : ' + str(max_MAP))
            print('Current max Average NDCG   : ' + str(max_avg_NDCG))
            print('='*100)
            if (current_avg_NDCG + current_MAP) > (max_avg_NDCG + max_MAP):
                max_MAP = current_MAP
                max_avg_NDCG = current_avg_NDCG
    print('#'*100)
    print('Final max MAP     : ' + str(max_MAP))
    print('Final max Average : ' + str(max_avg_NDCG))
    print('#'*100)



if __name__ == '__main__':
    main()
