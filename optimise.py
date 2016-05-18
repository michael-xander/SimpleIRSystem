# Finds the optimum mix of parameters for the modified engine
# Michael Kyeyune
# 16th May, 2016

import sys
import parameters
import analyse
import ap
import ndcg
import time
# get the MAP and avg NDCG for a testbed
def get_testbed_stats(testbed_name, queries):
    MAP = 0
    avg_NDCG = 0
    # get AP and NDCG score for each query
    for query in queries:
        result, accum, titles = analyse.submit_query(testbed_name, query, True)
        query_number = queries.index(query)+1
        ap_score = ap.AP(result, query_number, testbed_name, parameters.docs_to_consider)
        ndcg_score = ndcg.NDCG(result, query_number, testbed_name, parameters.docs_to_consider)
        MAP += ap_score
        avg_NDCG += ndcg_score
    MAP = MAP/len(queries)
    avg_NDCG = avg_NDCG/len(queries)
    return MAP, avg_NDCG

def all_testbeds_optimise(testbed_names):
    testbed_queries = {}
    # collect all the queries for each testbed
    for testbed_name in testbed_names:
        queries = analyse.readin_testbed_queries(testbed_name)
        testbed_queries[testbed_name] = queries

    #iterate through possible options of indicative terms and top k documents
    optimal_indicative_terms = 0
    optimal_top_k_documents = 0

    max_testbeds_MAP = 0
    max_testbeds_avg_NDCG = 0
    for i in range(20):
        parameters.number_indicative_terms = i+1
        for j in range(20):
            parameters.number_top_k_documents = j+1
            current_testbeds_MAP = 0
            current_testbeds_avg_NDCG = 0
            # cumulate the testbeds' MAP and avg NDCG scores
            for testbed_name in testbed_queries:
                localtime = time.asctime( time.localtime(time.time()))
                print("Time :", localtime)
                print('Analysing testbed : ' + testbed_name)
                testbed_MAP, testbed_avg_NDCG = get_testbed_stats(testbed_name, testbed_queries[testbed_name])
                current_testbeds_MAP += testbed_MAP
                current_testbeds_avg_NDCG += testbed_avg_NDCG
            current_testbeds_MAP = current_testbeds_MAP/len(testbed_queries)
            current_testbeds_avg_NDCG = current_testbeds_avg_NDCG/len(testbed_queries)
            # check whether a better score for MAP and NDCG over the testbeds has been obtained
            if (current_testbeds_avg_NDCG+current_testbeds_MAP) > (max_testbeds_avg_NDCG+max_testbeds_MAP):
                max_testbeds_avg_NDCG = current_testbeds_avg_NDCG
                max_testbeds_MAP = current_testbeds_MAP
                optimal_indicative_terms = parameters.number_indicative_terms
                optimal_top_k_documents = parameters.number_top_k_documents
            print('='*100)
            print('Current testbeds MAP             : ' + str(current_testbeds_MAP))
            print('Current testbeds avg NDCG        : ' + str(current_testbeds_avg_NDCG))
            print('Max testbeds MAP                 : ' + str(max_testbeds_MAP))
            print('Max testbeds avg NDCG            : ' + str(max_testbeds_avg_NDCG))
            print('*'*100)
            print('Number docs to consider          : ' + str(parameters.docs_to_consider))
            print('Current indicative terms         : ' + str(parameters.number_indicative_terms))
            print('Current top k documents          : ' + str(parameters.number_top_k_documents))
            print('Current optimal indicative terms : ' + str(optimal_indicative_terms))
            print('Current optimal top k documents  : ' + str(optimal_top_k_documents))
            print('='*100)


    return optimal_indicative_terms, optimal_top_k_documents


def main():
    if len(sys.argv)==1:
        print("Syntax: optimise.py <option -a for all or -s for single testbed> <testbed, if -s option> <num of docs to consider for MAP and NDCG analysis>")
        exit(0)
    option = sys.argv[1]
    if option == '-a':
        parameters.docs_to_consider = int(sys.argv[2])
        testbed_names = [
            'testbed1', 'testbed2', 'testbed3', 'testbed4', 'testbed5',
            'testbed6', 'testbed7', 'testbed8', 'testbed9', 'testbed11',
            'testbed12', 'testbed13', 'testbed14', 'testbed15', 'testbed16'
        ]
        indicative_terms, top_k_documents = all_testbeds_optimise(testbed_names)
        print('+'*100)
        print('Optimal indicative terms : ' + str(indicative_terms))
        print('Optimal top k documents  : ' + str(top_k_documents))
        print('+'*100)
    else:
        parameters.docs_to_consider = int(sys.argv[3])
        testbed_name = sys.argv[2]
        queries = analyse.readin_testbed_queries(testbed_name)

        max_MAP = 0
        max_avg_NDCG = 0
        optimal_indicative_terms = 0
        optimal_top_k_documents = 0
        # test 1-50 indicative terms and top k documents
        for i in range(30):
            parameters.number_indicative_terms = i+1
            for j in range(30):
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
                print('Optimal indicative terms   : ' + str(optimal_indicative_terms))
                print('Optimal top k documents    : ' + str(optimal_top_k_documents))
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
                    optimal_indicative_terms = parameters.number_indicative_terms
                    optimal_top_k_documents = parameters.number_top_k_documents
        print('#'*100)
        print('Final max MAP     : ' + str(max_MAP))
        print('Final max Average : ' + str(max_avg_NDCG))
        print('Optimal indicative terms : ' + str(optimal_indicative_terms))
        print('Optimal top k documents  : ' + str(optimal_top_k_documents))
        print('#'*100)



if __name__ == '__main__':
    main()
