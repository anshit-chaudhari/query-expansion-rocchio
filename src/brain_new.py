

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from pprint import pprint
import json
import numpy as np
import nltk


def vectorize(text_list):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(text_list)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    return pd.DataFrame(denselist, columns=feature_names)

def createList(r1, r2): 
    return np.arange(r1, r2+1, 1)

# print(len(rellll))

def brain_func(relevant_docs, irrelevant_docs, query):
    # a, b, r are the constants in the final formula
    # alpha betta gamma
    a = 1
    b = 0.75
    r = 0.25

    if query == []:
        return []
    # First, create a set of all terms that appear in the query
    # and the documents.

    # ID of file is preserved throughout
    # =============================================================================
    new_relevant_docs = []
    for doc in relevant_docs:
        new_relevant_docs.append(doc.title )

    relevant_docs = new_relevant_docs

    new_irrelevant_docs = []
    for doc in irrelevant_docs:
        new_irrelevant_docs.append(doc.title )

    irrelevant_docs = new_irrelevant_docs
    # =============================================================================

    # data = {}

    # data["rel"] = relevant_docs
    # data["irrel"] = irrelevant_docs

    # with open('data.json', 'w') as outfile:
    #     # print("herereeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    #     json.dump(data, outfile)

    # pprint(relevant_docs)
    # pprint(irrelevant_docs)

    #
    # # ============================================================================
    # For now, read relevant_docs and irrelevant_docs from data.txt
    # with open('data.json') as f:
    #     data = json.load(f)
    
    # relevant_docs = data["rel"]
    
    # irrelevant_docs = data["irrel"]
    
    # print(irrelevant_docs)
    # print(relevant_docs)
    # # ============================================================================
    

    # put all docs in one list, record the coords. 
    concat_query = [' '.join(query)]

    stop_words = nltk.corpus.stopwords.words('english')

    # for relevant docs, irrelevant docs, and query, 
    # record all the row indexes in the final tf_idf vector.
    # print(relevant_docs[0])
    all_list = relevant_docs + irrelevant_docs + concat_query
    # print(all_list[0])

    # remove stop words from each element in the list (a long text)
    # then make the list again.

    new_all_list = []
    for text in all_list:
        text = text.lower()
        text = ''.join(e for e in text if e.isalnum() or e == ' ')
        words_list = text.split(" ")
        new_words_list = []
        for word in words_list:
            if not (word in stop_words):
                new_words_list.append(word)

        new_all_list.append(" ".join(new_words_list))
    
    all_list = new_all_list




    rel_range = createList(0, len(relevant_docs)-1)
    print(all_list[0])
    # print(all_list[1])
    # print(all_list[2])
    # print(rel_range)
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


    new_dif_vec = {k: v for k, v in sorted(dif_vec.items(), key=lambda item: item[1], reverse=True)}

    for key in new_dif_vec.keys():
        if new_dif_vec[key] > 0:
            pprint(key + " " + str(dif_vec[key]))

    for key in new_dif_vec.keys():
        if not (key in query):
            query.append(key)
            break

    print(query)
    return query


# def main():
#     brain_func([], [], ["per", "se"])

# if __name__ == "__main__":
#     main()



# NOTE: the algorithm only uses title. Works well. Idea: decide if you want to use title or whole based
# on accuracy score