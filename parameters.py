# simple extended boolean search engine: configurable parameters
# Hussein Suleman
# 21 April 2016

normalization = True
stemming = True
case_folding = True
log_tf = True
use_idf = True
log_idf = True

# parameters specific to blind relevance feedback
use_blind_relevance_feedback = True
remove_stop_words = True
number_indicative_terms = 20
number_top_k_documents = 10

# parameters specific to MAP and NDCG analysis
docs_to_consider = 200