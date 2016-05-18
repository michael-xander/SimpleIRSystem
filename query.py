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
            f = open(collection+"_index/"+word, "r", encoding='utf-8')
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
def stem_term(term, p):
    if term != '':
        term = p.stem(term, 0, len(term)-1)
    return term

# stems the list of provided terms
def stem_terms(terms):
    stemmmed_terms = []
    p = porter.PorterStemmer()
    for i in range(len(terms)):
        stemmmed_terms.append(stem_term(terms[i],p))

    return stemmmed_terms

# read in the stop words
def readin_stop_words():
    stop_words = []
    f = open("stop-word-list.txt", "r", encoding='utf-8')
    lines = f.readlines()
    f.close()
    for line in lines:
        stop_words.append(line.rstrip())
    return stop_words

# carries out the required query search
def do_query_search(query_words, collection_name, collection_size, collection_files_data):
    # create accumulator
    accum = search_index(query_words, collection_name, collection_size)

    # get document lengths and titles
    titles = {}
    lengths = {}
    for file_data in collection_files_data:
        mo = re.match(r'([0-9]+)\:([0-9\.]+)\:(.+)', file_data)
        if mo:
            document_id = mo.group(1)
            length = eval(mo.group(2))
            title = mo.group(3)
            if document_id in accum:
                titles[document_id] = title
                lengths[document_id] = length

    # normalise if option is true
    if parameters.normalization:
        for document_id in accum:
            accum[document_id] = accum[document_id] / lengths[document_id]

    return accum, titles, lengths

def query(collection_name, given_query):

    collection = collection_name
    query = given_query
    # clean query
    if parameters.case_folding:
        query = query.lower()
    query = re.sub(r'[^ a-zA-Z0-9]', ' ', query)
    query = re.sub(r'\s+', ' ', query)
    query_words = query.split(' ')

    # get list of stop words
    stop_words = readin_stop_words()

    if parameters.remove_stop_words:
        temp_arr = []
        for word in query_words:
            if not word in stop_words:
                temp_arr.append(word)
        query_words = temp_arr

    if parameters.stemming:
        query_words = stem_terms(query_words)

    # get N
    f = open(collection + "_index_N", "r", encoding='utf-8')
    N = eval(f.read())
    f.close()

    f = open(collection + "_index_len", "r", encoding='utf-8')
    file_data_list = f.readlines()
    f.close()

    accum, titles, lengths = do_query_search(query_words, collection, N, file_data_list)

    # rank the results
    result = sorted(accum, key=accum.__getitem__, reverse=True)

    if parameters.use_blind_relevance_feedback:
        # obtain the IDs of the current top k documents
        k = parameters.number_top_k_documents
        num_relevant_docs = min(len(result), k)
        relevant_document_ids = []
        for i in range(num_relevant_docs):
            relevant_document_ids.append(result[i])

        # data structure to keep track of stemmed words in the relevant documents and the No. of documents they appear in
        accumulator = {}
        word_idfs = {}
        for document_id in relevant_document_ids:
            f = open(collection + "_index_stem_count/"+ document_id, "r", encoding='utf-8')
            lines = f.readlines()
            f.close()
            for line in lines:
                mo = re.match(r'([a-z0-9]+)\:([0-9\.]+)', line)
                if mo:
                    word = mo.group(1)
                    if parameters.remove_stop_words:
                        if word in stop_words:
                            continue
                    tf = float(mo.group(2))
                    if not word in accumulator:
                        accumulator[word] = 0
                        word_idfs[word] = 1
                        if parameters.use_idf:
                            f = open(collection+'_index/'+word, 'r', encoding='utf-8')
                            other_lines = f.readlines()
                            f.close()
                            df = len(other_lines)
                            word_idfs[word] = 1/df
                            if parameters.log_idf:
                                word_idfs[word] = math.log(1 + N/df)
                    if parameters.log_tf:
                        tf = (1 + math.log(tf))
                    stat = (tf * word_idfs[word])
                    #if parameters.normalization:
                    stat = stat/lengths[document_id]
                    accumulator[word] += stat

        # rank the words found in the documents
        ranked_words = sorted(accumulator, key=accumulator.__getitem__, reverse=True)
        #print("Old query words:")
        #print(query_words)
        indicative_number = min(len(ranked_words), parameters.number_indicative_terms)
        counter = 0
        for i in range(len(ranked_words)):
            if counter >= indicative_number:
                break
            if not ranked_words[i] in query_words:
                query_words.append(ranked_words[i])
                counter += 1

        # do search again with new query words
        #print("New query words:")
        #print(query_words)
        accum, titles, lengths = do_query_search(query_words, collection, N, file_data_list)

        # rank the results
        result = sorted(accum, key=accum.__getitem__, reverse=True)

    return result, accum, titles


def main():
    # check parameter for collection name
    if len(sys.argv) < 3:
        print("Syntax: query.py <collection> <query>")
        exit(0)

    # construct collection and query
    collection = sys.argv[1]
    query_words = ''
    arg_index = 2
    while arg_index < len(sys.argv):
        query_words += sys.argv[arg_index] + ' '
        arg_index += 1

    result, accum, titles = query(collection, query_words)
    # print the ranked results
    for i in range(min(len(result), 10)):
        print("{0:10.8f} {1:5} {2}".format(accum[result[i]], result[i], titles[result[i]]))



if __name__ == "__main__":
    main()