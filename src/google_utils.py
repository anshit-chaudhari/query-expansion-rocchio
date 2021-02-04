
# Resource: https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76

from typing import List

from config import Config
from document import Document

from googleapiclient.discovery import build

import json
import string
import re
import pandas as pd

def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def computeIDF(documents):
    import math
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict


def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def get_results(query: List[str], config: Config) -> List[Document]:
    """
    Search the query using Google Engine and return list of document objects
    """
    ret = []

    if len(query) == 0:
        return []

    concat_query = ' '.join(query)

    service = build("customsearch", "v1",
                    developerKey=config.dev_key)

    res = service.cse().list(
        q=concat_query,
        cx=config.engine_key,
    ).execute()

    list_of_results = res['items']

    list_of_results = list_of_results[0:10]

    for item in list_of_results:
        title = item["title"]
        url = item["link"]
        desc = item["snippet"]

        doc = Document(title, url, desc)

        ret.append(doc)

    return ret


def brain_func(relevant_docs, irrelevant_docs, query):
  # a, b, r are the constants in the final formula 
  # alpha betta gamma
  a = 1
  b = 0.75
  r = 0.25
  # First, create a set of all terms that appear in the query 
  # and the documents. 

  # ID of file is preserved throughout


  # ============================================================================
  # For now, read relevant_docs and irrelevant_docs from data.txt
  with open('temp.json') as f:
    data = json.load(f)

  relevant_docs = {}
  relevant_docs[0] = data["6"]

  irrelevant_docs = {}
  for i in range(0, 10):
    if not i == 6:
      irrelevant_docs[i] = data[str(i)]

  # print(irrelevant_docs)
  # print(relevant_docs)
  # ============================================================================


  # For all words in irrelevant_docs and relevant_docs, we need 
  # to strip stop words and split the string.
  for key in relevant_docs.keys():
    s = relevant_docs[key].lower()
    s = ''.join(e for e in s if e.isalnum() or e == ' ')
    # s = s.replace('\n','')
    # s = s.translate(str.maketrans('', '', string.punctuation))
    l = s.split(' ')
    relevant_docs[key] = l

  for key in irrelevant_docs.keys():
    s = irrelevant_docs[key].lower()
    s = ''.join(e for e in s if e.isalnum() or e == ' ')
    # s = s.replace('\n','')
    # s = s.translate(str.maketrans('', '', string.punctuation))
    l = s.split(' ')
    irrelevant_docs[key] = l

  # Create a list of unique words of all docs including the query
  unique_words = set(query)
  for key in relevant_docs.keys():
    unique_words = unique_words.union(set(relevant_docs[key]))
  for key in irrelevant_docs.keys():
    unique_words = unique_words.union(set(irrelevant_docs[key]))

  words_count_q = dict.fromkeys(unique_words, 0)
  for word in query:
    words_count_q[word] += 1

  words_count_rel = {}

  for key in relevant_docs.keys():
    bag_of_words = relevant_docs[key]
    words_vec = dict.fromkeys(unique_words, 0)
    for word in bag_of_words:
      words_vec[word] += 1
    words_count_rel[key] = words_vec

  words_count_irrel = {}

  for key in irrelevant_docs.keys():
    bag_of_words = irrelevant_docs[key]
    words_vec = dict.fromkeys(unique_words, 0)
    for word in bag_of_words:
      words_vec[word] += 1
    words_count_irrel[key] = words_vec

  
  # Compute tf-idf vector for all:
  tf_q = computeTF(words_count_q, query)

  tf_vec_rel = {}
  for key in relevant_docs.keys():
    tf = computeTF(words_count_rel[key], relevant_docs[key])
    tf_vec_rel[key] = tf

  tf_vec_irrel = {}
  for key in irrelevant_docs.keys():
    tf = computeTF(words_count_irrel[key], irrelevant_docs[key])
    tf_vec_irrel[key] = tf

  # now compute idf
  list_of_all_words_count = [words_count_q]
  for key in words_count_rel.keys():
    list_of_all_words_count.append(words_count_rel[key])
  for key in words_count_irrel.keys():
    list_of_all_words_count.append(words_count_irrel[key])

  idfs = computeIDF(list_of_all_words_count)

  # Now computer vector for each
  q_vec = computeTFIDF(tf_q, idfs)
  rel_vecs = {}
  for key in tf_vec_rel.keys():
    rel_vecs[key] = computeTFIDF(tf_vec_rel[key], idfs)

  irrel_vecs = {}
  for key in tf_vec_irrel.keys():
    irrel_vecs[key] = computeTFIDF(tf_vec_irrel[key], idfs)

  # Now that we have all the vectors we need, compute the new vector for the new query.
  # new_q_vec = alpha * old q_vector + beta * __ - gamma * ___

  alpha_q_vec = {}
  for key in q_vec.keys():
    alpha_q_vec[key] = q_vec[key] * a

  # second term in the update formula
  beta_rel = {}

  sum_of_rel = {}
  for key in rel_vecs.keys():
    cur_vec = rel_vecs[key]

    # cur_vec is the vector for current rel doc
    for key_cur in cur_vec:
      if key_cur in sum_of_rel.keys():
        sum_of_rel[key_cur] = sum_of_rel[key_cur] + cur_vec[key_cur]
      else:
        sum_of_rel[key_cur] = cur_vec[key_cur]

  for key in sum_of_rel.keys():
    beta_rel[key] = (sum_of_rel[key] * b) / len(relevant_docs)

  # third term in the update formula
  gamma_irrel = {}

  sum_of_irrel = {}
  for key in irrel_vecs.keys():
    cur_vec = irrel_vecs[key]

    # cur_vec is the vector for current irrel doc
    for key_cur in cur_vec:
      if key_cur in sum_of_irrel.keys():
        sum_of_irrel[key_cur] = sum_of_irrel[key_cur] + cur_vec[key_cur]
      else:
        sum_of_irrel[key_cur] = cur_vec[key_cur]

  for key in sum_of_irrel.keys():
    gamma_irrel[key] = (sum_of_irrel[key] * b) / len(irrelevant_docs)
  
  # print(beta_rel)
  # print(gamma_irrel)

  new_vec_q = {}
  for key in alpha_q_vec.keys():
    new_vec_q[key] = alpha_q_vec[key] + beta_rel[key] - gamma_irrel[key]
  
  # print(new_vec_q)

  dif_vec = {}
  for key in alpha_q_vec.keys():
    dif_vec[key] = new_vec_q[key] - q_vec[key]

  # sort dif_vec by value
  new_dif_vec = {k: v for k, v in sorted(dif_vec.items(), key=lambda item: item[1], reverse=True)}

  # print(new_dif_vec)

  for key in new_dif_vec.keys():
    if not (key in query):
      query.append(key)
      break

  print(query)

  return query



if __name__ == '__main__':
    config = Config(
        dev_key="AIzaSyAXqKtB1mQUHZmrFmMW_EhNK3JAyWRAK9o",
        engine_key="2c6600e3a2ae8bcd0"
    )

    # ret = get_results(["Linear"], config)

    brain_func([], [], ["linear"])


    # new_ret = {}

    # i = 0
    # for doc in ret:
    #   new_ret[i] = doc.desc
    #   i += 1

    # print(new_ret)
    # with open('data.txt', 'w') as outfile:
    #   json.dump(new_ret, outfile, indent = 4)

