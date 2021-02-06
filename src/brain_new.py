

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
import json
import numpy as np

def vectorize(text_list):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(text_list)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    return pd.DataFrame(denselist, columns=feature_names)

def createList(r1, r2): 
    return np.arange(r1, r2+1, 1)

def brain_func(relevant_docs, irrelevant_docs, query):
    # a, b, r are the constants in the final formula
    # alpha betta gamma
    a = 1
    b = 0.75
    r = 0.15

    if query == []:
        return []
    # First, create a set of all terms that appear in the query
    # and the documents.

    # ID of file is preserved throughout
    # new_relevant_docs = {}
    # index = 0
    # for doc in relevant_docs:
    #     new_relevant_docs[index] = doc.title
    #     index += 1

    # relevant_docs = new_relevant_docs

    # new_irrelevant_docs = {}
    # for doc in irrelevant_docs:
    #     new_irrelevant_docs[index] = doc.title
    #     index += 1

    # irrelevant_docs = new_irrelevant_docs

    #
    # # ============================================================================
    # For now, read relevant_docs and irrelevant_docs from data.txt
    with open('temp.json') as f:
        data = json.load(f)
    
    relevant_docs = []
    relevant_docs.append(data["6"])
    
    irrelevant_docs = []
    for i in range(0, 10):
        if not i == 6:
            irrelevant_docs.append(data[str(i)])
    
    # print(irrelevant_docs)
    # print(relevant_docs)
    # # ============================================================================
    

    # put all docs in one list, record the coords. 
    concat_query = [' '.join(query)]

    # for relevant docs, irrelevant docs, and query, 
    # record all the row indexes in the final tf_idf vector.
    all_list = relevant_docs + irrelevant_docs + concat_query
    rel_range = createList(0, len(relevant_docs)-1)
    irrel_range = createList(len(relevant_docs), len(irrelevant_docs) + len(relevant_docs) - 1)

    # tf-idf vectors
    tf_idf = vectorize(all_list)

    # Now we calculate the three terms in the Rocchio algorithm
    # new_q = a * old_q + b * rel - r * irrel
    #(tf_idf.shape[0]-1)
    old_query_vec = tf_idf.iloc[tf_idf.shape[0]-1]
    first_term = a * old_query_vec

    # initialize rel vector to be the first relevant doc vector
    # then add the rest
    rel_vector = tf_idf.iloc[rel_range[0]]
    for i in rel_range[1:]:
        rel_vector = rel_vector + tf_idf.iloc[i]

    second_term = b * (rel_vector / len(rel_range))

    # initialize irrel vector to be the first irrelevant doc vector
    # then add the rest
    irrel_vector = tf_idf.iloc[irrel_range[0]]
    for i in irrel_range[1:]:
        irrel_vector = irrel_vector + tf_idf.iloc[i]

    third_term = r * (irrel_vector / len(irrel_range))

    new_query_vec = first_term + second_term - third_term

    dif_vec = new_query_vec - old_query_vec

    for key in dif_vec.keys():
        if dif_vec[key] > 0:
            pprint(key + " " + str(dif_vec[key]))

    # REMOVE STOP WORDS








def main():
    brain_func([], [], ["what", "the", "fuck"])

if __name__ == "__main__":
    main()