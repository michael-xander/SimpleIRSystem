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
    fileNum = 1
    for query_sentence in queries:
        print()
        print('='*100)
        print('Carrying out analyse for query : ' + query_sentence)
        print()
        print('*'*100)
        print('Analysing with unmodified engine')
        print()
        result, accum, titles = submit_query(testbed_name, query_sentence, False)
        apScore = ap.AP(accum,result,titles, fileNum, testbed_name)
        NDCGScore = ndcg.NDCG(accum, result, titles, fileNum, testbed_name)
        print("\nAP:"+str(apScore)+"\nNDCG:"+str(NDCGScore))
        print('*'*100)
        print('Analysing with modified engine')
        print()
        result, accum, titles = submit_query(testbed_name, query_sentence, True)
        apScore  =ap.AP(accum,result,titles, fileNum, testbed_name)
        NDCGScore = ndcg.NDCG(accum, result, titles, fileNum, testbed_name)
        print("\nAP:"+str(apScore)+"\nNDCG:"+str(NDCGScore))

        fileNum = fileNum + 1
if __name__ == '__main__':
    main()