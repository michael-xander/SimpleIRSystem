# Carries out comparison between the modified search engine and the old search engine
# Michael Kyeyune
# 14th May, 2016

import sys
import glob

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

def main():
    if len(sys.argv)==1:
        print("Syntax: analyse.py <testbed>")
        exit(0)
    testbed_name = sys.argv[1]
    queries = readin_testbed_queries(testbed_name)

    for query_sentence in queries:
        print(query_sentence)

if __name__ == '__main__':
    main()