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
    query_file_names = glob.glob(testbed_name + "/query*")
    queries = []

    for query_file_name in query_file_names:
        f = open(query_file_name, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.rstrip()
            queries.append(line)
    return queries

# submit query for given testbed, adjusting on whether to use the modified engine or not
def submit_query(testbed_name, query_sentence, use_modified_engine):
    if use_modified_engine:
        parameters.use_blind_relevance_feedback = True
        parameters.remove_stop_words = True
    else:
        parameters.use_blind_relevance_feedback = False
        parameters.remove_stop_words = False

    result, accum, titles = query.query((testbed_name + "_collection"), query_sentence)
    return result, accum, titles


def main():
    if len(sys.argv)==1:
        print("Syntax: analyse.py <testbed>")
        exit(0)
    testbed_name = sys.argv[1]
    queries = readin_testbed_queries(testbed_name)

    unmodified_engine_stats = {}
    modified_engine_stats = {}
    query_number = 1

    # iterate through queries applying modified and unmodified search to obtain AP and NDCG values
    for query_sentence in queries:
        unmodified_engine_stats[query_number] = []
        modified_engine_stats[query_number] = []
        print()
        print('='*100)
        print('Carrying out analysis for query : ' + query_sentence)
        # analysis using unmodified engine
        result, accum, titles = submit_query(testbed_name, query_sentence, False)
        ap_score = ap.AP(result, query_number, testbed_name)
        ndcg_score = ndcg.NDCG(result, query_number, testbed_name)
        unmodified_engine_stats[query_number].append(ap_score)
        unmodified_engine_stats[query_number].append(ndcg_score)
        print('*'*100)
        print('Unmodified engine AP score   : ' + str(ap_score))
        print('Unmodified engine NDCG score : ' + str(ndcg_score))
        # analysis using modified engine
        result, accum, titles = submit_query(testbed_name, query_sentence, True)
        ap_score  =ap.AP(result, query_number, testbed_name)
        ndcg_score = ndcg.NDCG(result, query_number, testbed_name)
        modified_engine_stats[query_number].append(ap_score)
        modified_engine_stats[query_number].append(ndcg_score)
        print('*'*100)
        print('Modified engine AP score     : ' + str(ap_score))
        print('Modified engine NDCG score   : ' + str(ndcg_score))
        query_number += 1

    query_number -= 1
    # calculate MAP and average NDCG
    unmodified_engine_cumulative_stats = [0,0]
    modified_engine_cumulative_stats = [0,0]
    for i in range(query_number):
        unmodified_engine_cumulative_stats[0] += unmodified_engine_stats[i+1][0]
        unmodified_engine_cumulative_stats[1] += unmodified_engine_stats[i+1][1]

        modified_engine_cumulative_stats[0] += modified_engine_stats[i+1][0]
        modified_engine_cumulative_stats[1] += modified_engine_stats[i+1][1]

    print()
    print("+"*100)
    print('Unmodified engine MAP          : ' + str(unmodified_engine_cumulative_stats[0]/query_number))
    print('Unmodified engine average NDCG : ' + str(unmodified_engine_cumulative_stats[1]/query_number))
    print("*"*100)
    print('Modified engine MAP            : ' + str(modified_engine_cumulative_stats[0]/query_number))
    print('Modified engine average NDCG   : ' + str(modified_engine_cumulative_stats[1]/query_number))

if __name__ == '__main__':
    main()