import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from pprint import pprint

stop_words = nltk.corpus.stopwords.words('english')


def vectorize(text_list):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(text_list)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    return pd.DataFrame(denselist, columns=feature_names)


def createList(r1, r2):
    return np.arange(r1, r2 + 1, 1)


def clean_text(text):
    text = text.lower()

    # split into words
    tokens = word_tokenize(text)

    # remove all tokens that are not alphabetic and are stopwords
    words = [word for word in tokens if word.isalpha() and word not in stop_words]

    return " ".join(words)


def brain_func(relevant_docs, irrelevant_docs, query, cur_precision):
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
        new_relevant_docs.append(doc.title + " " + doc.desc)

    relevant_docs = new_relevant_docs

    new_irrelevant_docs = []
    for doc in irrelevant_docs:
        new_irrelevant_docs.append(doc.title + " " + doc.desc)

    irrelevant_docs = new_irrelevant_docs

    # # ============================================================================

    # put all docs in one list, record the coords. 
    concat_query = [' '.join(query)]

    # for relevant docs, irrelevant docs, and query, 
    # record all the row indexes in the final tf_idf vector.
    all_list = relevant_docs + irrelevant_docs + concat_query

    new_all_list = []
    for text in all_list:
        new_all_list.append(clean_text(text))

    all_list = new_all_list

    rel_range = createList(0, len(relevant_docs) - 1)

    irrel_range = createList(len(relevant_docs), len(irrelevant_docs) + len(relevant_docs) - 1)

    # tf-idf vectors
    tf_idf = vectorize(all_list)

    # Now we calculate the three terms in the Rocchio algorithm
    # new_q = a * old_q + b * rel - r * irrel
    old_query_vec = tf_idf.iloc[tf_idf.shape[0] - 1]
    first_term = a * old_query_vec

    # initialize rel vector to zero and then add the rest
    rel_vector = np.zeros((tf_idf.shape[1]))
    for i in rel_range:
        rel_vector = rel_vector + tf_idf.iloc[i]

    second_term = b * (rel_vector / len(rel_range))

    # initialize irrel vector to be the first irrelevant doc vector
    # then add the rest
    irrel_vector = np.zeros((tf_idf.shape[1]))
    for i in irrel_range:
        irrel_vector = irrel_vector + tf_idf.iloc[i]

    third_term = r * (irrel_vector / len(irrel_range))

    new_query_vec = first_term + second_term - third_term

    dif_vec = new_query_vec - old_query_vec

    new_dif_vec = {k: v for k, v in sorted(dif_vec.items(), key=lambda item: item[1], reverse=True)}

    for key in new_dif_vec.keys():
        if not (key in query):
            query.append(key)
            break

    return query
