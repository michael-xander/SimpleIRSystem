# Simple extended boolean search engine: query module
# Hussein Suleman
# 14 April 2016

import re
import math
import sys
import os

import porter

import parameters

# searchs index for provided search words and returns the accumulated dictionary
def search_index(search_words, collection, N):
    accumulator = {}
    for word in search_words:
        if word != '':
            if not os.path.isfile(collection+"_index/"+word):
                continue
            f = open(collection+"_index/"+word, "r")
            lines = f.readlines()
            idf = 1
            if parameters.use_idf:
                df = len(lines)
                idf = 1/df
                if parameters.log_idf:
                    idf = math.log(1 + N/df)
            for line in lines:
                mo = re.match(r'([0-9]+)\:([0-9\.]+)', line)
                if mo:
                    file_id = mo.group(1)
                    tf = float (mo.group(2))
                    if not file_id in accumulator:
                        accumulator[file_id] = 0
                    if parameters.log_tf:
                        tf = (1 + math.log(tf))
                    accumulator[file_id] += (tf * idf)
            f.close()

    return accumulator

# stems the provided term
def stem_term(term):
    p = porter.PorterStemmer()
    if term != '':
        term = p.stem(term, 0, len(term)-1)
    return term

# stems the list of provided terms
def stem_terms(terms):
    stemmmed_terms = []
    for i in range(len(terms)):
        stemmmed_terms.append(stem_term(terms[i]))

    return stemmmed_terms

def main():
    # check parameter for collection name
    if len(sys.argv) < 3:
        print("Syntax: query.py <collection> <query>")
        exit(0)

    # construct collection and query
    collection = sys.argv[1]
    query = ''
    arg_index = 2
    while arg_index < len(sys.argv):
        query += sys.argv[arg_index] + ' '
        arg_index += 1

    # clean query
    if parameters.case_folding:
        query = query.lower()
    query = re.sub(r'[^ a-zA-Z0-9]', ' ', query)
    query = re.sub(r'\s+', ' ', query)
    query_words = query.split(' ')

    # create data structures
    filenames = []

    # get N
    f = open(collection + "_index_N", "r")
    N = eval(f.read())
    f.close()

    # get document lengths/titles
    titles = {}
    f = open(collection + "_index_len", "r")
    lengths = f.readlines()
    f.close()

    if parameters.stemming:
        query_words = stem_terms(query_words)

    # create accumulator
    accum = search_index(query_words, collection, N)

    # parse lengths data and divide by |N| and get titles
    for l in lengths:
        mo = re.match(r'([0-9]+)\:([0-9\.]+)\:(.+)', l)
        if mo:
            document_id = mo.group(1)
            length = eval(mo.group(2))
            title = mo.group(3)
            if document_id in accum:
                if parameters.normalization:
                    accum[document_id] = accum[document_id] / length
                titles[document_id] = title

    # print top ten results
    result = sorted(accum, key=accum.__getitem__, reverse=True)

    if parameters.use_blind_relevance_feedback:
        print("Utilising blind relevance feedback")

        # obtain the IDs of the current top k documents
        k = 10
        num_relevant_docs = min(len(result), k)
        relevant_document_ids = []
        for i in range(num_relevant_docs):
            relevant_document_ids.append(result[i])

        # data structure to keep track of stemmed words in the relevant documents and the No. of documents they appear in
        words_df_counter = {}
        words_tf_counter = {}
        for document_id in relevant_document_ids:
            f = open(collection + "_index_stem_count/"+ document_id, "r")
            lines = f.readlines()
            for line in lines:
                mo = re.match(r'([a-z0-9]+)\:([0-9\.]+)', line)
                if mo:
                    word = mo.group(1)
                    count = eval(mo.group(2))

                    if not word in words_tf_counter:
                        words_tf_counter[word] = {}
                    words_tf_counter[word][document_id] = count

                    if not word in words_df_counter:
                        words_df_counter[word] = 0
                    words_df_counter[word] += 1

        # data structure to contain stats on words
        word_stats = {}
        for word in words_df_counter:
            df = words_df_counter[word]
            idf = 1/df
            if parameters.log_idf:
                idf = math.log(1 + k/df)
            for document_id in words_tf_counter[word]:
                tf = float(words_tf_counter[word][document_id])
                if parameters.log_tf:
                    tf = (1 + math.log(tf))
                if not word in word_stats:
                    word_stats[word] = 0
                word_stats[word] += (tf * idf)

        # rank the words found in the documents
        ranked_words = sorted(word_stats, key=word_stats.__getitem__, reverse=True)
        indicative_number = 20
        for i in range(min(len(ranked_words), indicative_number)):
            if not ranked_words[i] in query_words:
                query_words.append(ranked_words[i])

        # do search again with new query words
    else:
        for i in range(min(len(result), 10)):
            print("{0:10.8f} {1:5} {2}".format(accum[result[i]], result[i], titles[result[i]]))


# run the main method
main()
