from typing import List

from config import Config
from document import Document

from googleapiclient.discovery import build

import json


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
  # First, create a set of all terms that appear in the query 
  # and the documents. 

  # For now, read relevant_docs and irrelevant_docs from data.txt
  with open('data.json') as f:
    data = json.load(f)

  relevant_docs = {}
  relevant_docs[0] = data["6"]

  print(relevant_docs)

  # Create a dictionary of word: index. The index will represent
  # the location of the word in a vector. 
  word_count = 0
  word_index_dict = {}

  for word in query:
    if not (word in word_index_dict.keys()):
      word_index_dict[word] = word_count
      word_count = word_count + 1
  return query



if __name__ == '__main__':
    config = Config(
        dev_key="AIzaSyAXqKtB1mQUHZmrFmMW_EhNK3JAyWRAK9o",
        engine_key="2c6600e3a2ae8bcd0"
    )

    # ret = get_results(["Linear"], config)

    brain_func([], [], [])


    # new_ret = {}

    # i = 0
    # for doc in ret:
    #   new_ret[i] = doc.desc
    #   i += 1

    # print(new_ret)
    # with open('data.txt', 'w') as outfile:
    #   json.dump(new_ret, outfile, indent = 4)

    
