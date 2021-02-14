import nltk
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize

# The follow code is inspired by 
# https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76

stop_words = nltk.corpus.stopwords.words('english')


# This function builds the tf-idf weight matrix for each
# term (column) and each document (row). This function is
# directly copied from the website listed above.
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
    # a, b, r are the constants in the final Rocchio formula
    # alpha betta gamma
    a = 1
    b = 0.75
    r = 0.25

    if query == []:
        return []

    # build a list for relevant docs and irrelevant docs respectively.
    new_relevant_docs = []
    for doc in relevant_docs:
        if doc.desc and doc.title:
            new_relevant_docs.append(doc.title + " " + doc.desc)

    relevant_docs = new_relevant_docs

    new_irrelevant_docs = []
    for doc in irrelevant_docs:
        if doc.desc and doc.title:
            new_irrelevant_docs.append(doc.title + " " + doc.desc)

    irrelevant_docs = new_irrelevant_docs


    # Put everything in one giant list. 
    concat_query = [' '.join(query)]

    all_list = relevant_docs + irrelevant_docs + concat_query

    new_all_list = []
    for text in all_list:
        new_all_list.append(clean_text(text))

    all_list = new_all_list
    
    # At this point, all_list looks like: 
    # [doc1.title + doc1.desc, doc2.title + doc2.desc, ... ]

    # For relevant docs, irrelevant docs, and query, 
    # record all their indexes in all_list.
    # This is because when we later have one giant tf-idf matrix,
    # we want to know which row correspond to which document.

    rel_range = createList(0, len(relevant_docs) - 1)
    irrel_range = createList(len(relevant_docs), len(irrelevant_docs) + len(relevant_docs) - 1)

    # tf-idf matrix. The columns are the terms and the rows are the docs.
    tf_idf = vectorize(all_list)

    # Now we calculate the three terms in the Rocchio algorithm
    # new_q = a * old_q + b * rel - r * irrel
    old_query_vec = tf_idf.iloc[tf_idf.shape[0] - 1]
    first_term = a * old_query_vec

    # For the second term in the Rocchio's algorithm, we 
    # need to add all vectors of relevant documents.
    # We initialize the rel_vector to be zero and then add all relevant 
    # vectors.
    rel_vector = np.zeros((tf_idf.shape[1]))
    for i in rel_range:
        rel_vector = rel_vector + tf_idf.iloc[i]

    second_term = b * (rel_vector / len(rel_range))

    # Same logic for irrelevant vectors (third term in the Rocchio's 
    # algorithm).
    irrel_vector = np.zeros((tf_idf.shape[1]))
    for i in irrel_range:
        irrel_vector = irrel_vector + tf_idf.iloc[i]

    third_term = r * (irrel_vector / len(irrel_range))

    # New query vector. 
    new_query_vec = first_term + second_term - third_term

    dif_vec = new_query_vec - old_query_vec

    # Sort the difference by term net change. The more a term's 
    # weight has changed, the more we want to put it in the front.
    new_dif_vec = {k: v for k, v in sorted(dif_vec.items(), key=lambda item: item[1], reverse=True)}

    # Find the first term in the difference vector that is not
    # part of the old query. That's our target term.
    for key in new_dif_vec.keys():
        if not (key in query):
            query.append(key)
            break

    return query
