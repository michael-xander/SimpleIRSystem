# Carries out comparison between the modified search engine and the old search engine
# Michael Kyeyune
# 14th May, 2016

import sys
import glob
import parameters
import query
import ap
import ndcg

# reads in the queries for a specific testbed
def readin_testbed_queries(testbed_name):
    query_file_numbers = [1,2,3,4,5]
    queries = {}

    for query_file_number in query_file_numbers:
        query_file_name = testbed_name + '/query.' + str(query_file_number)
        f = open(query_file_name, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.rstrip()
            queries[query_file_name] = line

    return queries

# submit query for given testbed, adjusting on whether to use the modified engine or not
def submit_query(testbed_name, query_sentence, use_modified_engine):
    if use_modified_engine:
        parameters.use_blind_relevance_feedback = True
        parameters.remove_stop_words = True
        parameters.normalization = False
    else:
        parameters.use_blind_relevance_feedback = False
        parameters.remove_stop_words = False
        parameters.normalization = True

    result, accum, titles = query.query((testbed_name + "_collection"), query_sentence)
    return result, accum, titles


def main():
    if len(sys.argv)==1:
        print("Syntax: analyse.py <testbed>")
        exit(0)
    testbed_name = sys.argv[1]
    queries = readin_testbed_queries(testbed_name)

    stats = {}
    stats['unmodified'] = {'map': 0, 'avg_ndcg' : 0}
    stats['modified']   = {'map': 0, 'avg_ndcg' : 0}
    # iterate through queries applying modified and unmodified search to obtain AP and NDCG values
    for query_file_name in queries:
        query_sentence = queries[query_file_name]
        temp_arr = query_file_name.split('.')
        query_number = temp_arr[1]
        print()
        print('='*100)
        print('Carrying out analysis for query : ' + query_sentence)
        # analysis using unmodified engine
        result, accum, titles = submit_query(testbed_name, query_sentence, False)
        ap_score = ap.AP(result, query_number, testbed_name, parameters.docs_to_consider)
        ndcg_score = ndcg.NDCG(result, query_number, testbed_name, parameters.docs_to_consider)
        stats['unmodified']['map'] += ap_score
        stats['unmodified']['avg_ndcg'] += ndcg_score
        print('*'*100)
        print('Unmodified engine AP score   : ' + str(ap_score))
        print('Unmodified engine NDCG score : ' + str(ndcg_score))
        # analysis using modified engine
        result, accum, titles = submit_query(testbed_name, query_sentence, True)
        ap_score  =ap.AP(result, query_number, testbed_name, parameters.docs_to_consider)
        ndcg_score = ndcg.NDCG(result, query_number, testbed_name, parameters.docs_to_consider)
        stats['modified']['map'] += ap_score
        stats['modified']['avg_ndcg'] += ndcg_score
        print('*'*100)
        print('Modified engine AP score     : ' + str(ap_score))
        print('Modified engine NDCG score   : ' + str(ndcg_score))

    # calculate MAP and average NDCG
    num_queries = len(queries)
    stats['unmodified']['map'] = stats['unmodified']['map']/num_queries
    stats['unmodified']['avg_ndcg'] = stats['unmodified']['avg_ndcg']/num_queries
    stats['modified']['map'] = stats['modified']['map']/num_queries
    stats['modified']['avg_ndcg'] = stats['modified']['avg_ndcg']/num_queries

    print()
    print("+"*100)
    print('Unmodified engine MAP          : ' + str(stats['unmodified']['map']))
    print('Unmodified engine average NDCG : ' + str(stats['unmodified']['avg_ndcg']))
    print("*"*100)
    print('Modified engine MAP            : ' + str(stats['modified']['map']))
    print('Modified engine average NDCG   : ' + str(stats['modified']['avg_ndcg']))

if __name__ == '__main__':
    main()